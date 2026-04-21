"""Orchestrator for the Blender-based shorts pipeline.

Runs in a regular Python env (not Blender). Flow:

  1. Load the storyboard YAML (same schema as the PIL pipeline uses).
  2. Generate TTS per beat via _shorts.renderer.tts (Kokoro on GPU) — this
     reuses the PIL pipeline's proven voice code, no duplication.
  3. Compute timing (beat.start_time, beat.duration) from audio lengths.
  4. Serialize the descriptor to JSON.
  5. Launch Blender as a subprocess pointed at render_runner.py, which
     builds the 3D scene, applies animation, and renders the PNG frame
     sequence.
  6. Mix beat audio via _shorts.renderer.encode (ffmpeg) into a master.wav.
  7. Encode frames + audio -> MP4.

Usage:
    python -m _shorts.blender.build \
        --storyboard _shorts/templates/L-001_storyboard.yaml \
        --out _deliverables/shorts/blender/L-001-short.mp4
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Reuse the PIL pipeline's TTS, encode, storyboard loader — same audio
# pipeline, just swapping the visual renderer.
from _shorts.renderer.storyboard import Storyboard
from _shorts.renderer.tts import synthesize, audio_duration
from _shorts.renderer.encode import concat_audio_with_timing, frames_to_mp4


REPO_ROOT = Path(__file__).resolve().parents[2]
BLENDER_EXE = Path(r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe")
RUNNER_SCRIPT = Path(__file__).parent / "render_runner.py"

FPS = 30


def log(msg: str) -> None:
    print(f"[blender-build] {msg}", flush=True)


def generate_tts(sb: Storyboard, audio_dir: Path) -> None:
    """Fill beat.audio_path + beat.audio_duration for every beat with
    narration."""
    audio_dir.mkdir(parents=True, exist_ok=True)
    for i, beat in enumerate(sb.beats):
        if not beat.narration.strip():
            continue
        out = audio_dir / f"beat_{i:03d}.wav"
        if not out.exists():
            log(f"TTS beat {i}: {beat.narration[:60]}...")
            synthesize(beat.narration, out)
        beat.audio_path = out
        beat.audio_duration = audio_duration(out)


def compute_timing(sb: Storyboard) -> float:
    """Set start_time + duration on every beat. Returns total_duration
    (scroll + finale_hold)."""
    t = 0.0
    for beat in sb.beats:
        dur = beat.audio_duration if beat.audio_duration > 0 else 0.0
        dur = max(beat.min_duration, dur + beat.hold_after)
        beat.start_time = t
        beat.duration = dur
        t += dur
    return t + sb.finale_hold


def build_descriptor(sb: Storyboard, total_duration: float) -> dict:
    """Convert the Storyboard into a JSON-safe descriptor for Blender."""
    return {
        "lesson_id": sb.lesson_id,
        "day_number": sb.day_number,
        "lesson_title": sb.lesson_title,
        "learning_title": sb.learning_title,
        "lanes": list(sb.lanes),
        "total_duration": total_duration,
        "finale_hold": sb.finale_hold,
        "beats": [
            {
                "kind": beat.kind,
                "from_lane": beat.from_lane,
                "to_lane": beat.to_lane,
                "label": beat.label,
                "narration": beat.narration,
                "input_display": beat.input_display,
                "start_time": beat.start_time,
                "duration": beat.duration,
                "audio_duration": beat.audio_duration,
                "audio_path": str(beat.audio_path) if beat.audio_path else None,
            }
            for beat in sb.beats
        ],
    }


def launch_blender(descriptor_path: Path, frames_dir: Path) -> None:
    if not BLENDER_EXE.exists():
        raise RuntimeError(f"Blender not found at {BLENDER_EXE}")
    cmd = [
        str(BLENDER_EXE),
        "--background",
        "--python", str(RUNNER_SCRIPT),
        "--",
        "--descriptor", str(descriptor_path),
        "--frames-dir", str(frames_dir),
    ]
    log(f"launching Blender: {' '.join(cmd[:3])} ...")
    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0
    log(f"Blender finished in {elapsed:.1f}s (exit {result.returncode})")
    # Always surface Blender's own output — its exit code is unreliable for
    # errors inside the embedded Python.
    if result.stdout:
        sys.stdout.write(result.stdout[-3000:])
        sys.stdout.write("\n")
    if result.stderr:
        sys.stderr.write(result.stderr[-3000:])
        sys.stderr.write("\n")
    if result.returncode != 0:
        raise RuntimeError("Blender render failed")


def frames_to_mp4_blender(frames_dir: Path, audio_path: Path, out_path: Path,
                           fps: int = FPS) -> Path:
    """Blender writes frame_XXXX.png — our encode.frames_to_mp4 expects
    frame_XXXXXX.png (6-digit). Write a matching pattern directly."""
    import subprocess as sp
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(out_path),
    ]
    result = sp.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg encode failed:\n{result.stderr[-1500:]}")
    return out_path


def build(storyboard_path: Path, output_mp4: Path,
          work_dir: Path | None = None, keep_frames: bool = False) -> Path:
    sb = Storyboard.from_yaml(storyboard_path)
    log(f"storyboard: {sb.lesson_id} / {len(sb.beats)} beats / {len(sb.lanes)} lanes")

    work_dir = work_dir or (REPO_ROOT / "_shorts" / "_work" / "blender"
                            / sb.lesson_id)
    work_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = work_dir / "audio"
    frames_dir = work_dir / "frames"
    for old in frames_dir.glob("*.png"):
        old.unlink()
    frames_dir.mkdir(parents=True, exist_ok=True)

    # 1-3. TTS + timing.
    log("generating TTS for each beat")
    generate_tts(sb, audio_dir)
    total_duration = compute_timing(sb)
    log(f"total duration: {total_duration:.2f}s (audio + finale_hold)")

    # 4. Descriptor JSON.
    descriptor = build_descriptor(sb, total_duration)
    descriptor_path = work_dir / "descriptor.json"
    with descriptor_path.open("w", encoding="utf-8") as f:
        json.dump(descriptor, f, indent=2)

    # 5. Launch Blender render.
    launch_blender(descriptor_path, frames_dir)
    # Guard: Blender's exit code is unreliable for Python errors inside the
    # embedded interpreter — verify frames actually landed.
    rendered = sorted(frames_dir.glob("frame_*.png"))
    if not rendered:
        raise RuntimeError(
            f"Blender completed but wrote no frames to {frames_dir}. "
            "Check the Blender stdout above for the actual error.")
    log(f"rendered {len(rendered)} frames")

    # 6. Mix audio.
    log("mixing narration audio")
    master_audio = work_dir / "master.wav"
    audio_segments = [(b.audio_path, b.start_time) for b in sb.beats
                      if b.audio_path]
    concat_audio_with_timing(audio_segments, total_duration, master_audio)

    # 7. Encode MP4.
    log(f"encoding {output_mp4.name}")
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    frames_to_mp4_blender(frames_dir, master_audio, output_mp4)

    if not keep_frames:
        for old in frames_dir.glob("*.png"):
            old.unlink()

    log(f"done -> {output_mp4}")
    return output_mp4


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Build an MP4 short via the Blender pipeline.")
    ap.add_argument("--storyboard", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args()
    build(args.storyboard, args.out, args.work, args.keep_frames)


if __name__ == "__main__":
    main()
