"""Orchestrator: storyboard YAML -> TTS per beat -> frames -> MP4."""
import argparse
import sys
import time
from pathlib import Path

from . import config as C
from .storyboard import Storyboard, Beat
from .scene import compose_frame, compose_finale_frame, build_scroll_plan
from .tts import synthesize, audio_duration
from .encode import concat_audio_with_timing, frames_to_mp4


def log(msg: str):
    print(f"[shorts] {msg}", flush=True)


def generate_beat_audio(sb: Storyboard, audio_dir: Path) -> list[tuple[Beat, Path]]:
    """Synthesize TTS for each beat. Returns list of (beat, audio_path) in beat order."""
    result: list[tuple[Beat, Path]] = []
    for i, beat in enumerate(sb.beats):
        if not beat.narration.strip():
            continue
        out = audio_dir / f"beat_{i:03d}.wav"
        if not out.exists():
            log(f"  TTS beat {i}: {beat.narration[:60]}...")
            synthesize(beat.narration, out)
        beat.audio_path = out
        beat.audio_duration = audio_duration(out)
        result.append((beat, out))
    return result


def compute_timing(sb: Storyboard):
    """Set beat.start_time and beat.duration based on audio or min_duration."""
    t = 0.0
    for beat in sb.beats:
        dur = beat.audio_duration if beat.audio_duration > 0 else 0.0
        dur = max(beat.min_duration, dur + beat.hold_after)
        beat.start_time = t
        beat.duration = dur
        t += dur


def render_frames(sb: Storyboard, frames_dir: Path, finale_frames: int = 90):
    total_beat_frames = int(sb.beats[-1].start_time * C.FPS + sb.beats[-1].duration * C.FPS)
    total_frames = total_beat_frames + finale_frames
    log(f"rendering {total_frames} frames ({total_beat_frames} scroll + {finale_frames} finale)")
    t0 = time.time()
    for i in range(total_beat_frames):
        t = i / C.FPS
        img = compose_frame(sb, t)
        img.save(frames_dir / f"frame_{i:06d}.png", optimize=False)
        if (i + 1) % 30 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            log(f"  scroll frame {i+1}/{total_beat_frames} ({rate:.1f} fps render)")

    # Finale frames (hold on full-sequence view)
    for j in range(finale_frames):
        u = j / max(finale_frames - 1, 1)
        img = compose_finale_frame(sb, u)
        img.save(frames_dir / f"frame_{total_beat_frames + j:06d}.png", optimize=False)
    log(f"  finale frames done ({finale_frames})")
    return total_frames


def build(storyboard_path: Path, output_mp4: Path,
          work_dir: Path | None = None, keep_frames: bool = False):
    sb = Storyboard.from_yaml(storyboard_path)
    log(f"storyboard: {sb.lesson_id} / {len(sb.beats)} beats / {len(sb.lanes)} lanes")

    work_dir = work_dir or (C.WORK_DIR / sb.lesson_id)
    work_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = work_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    audio_dir = work_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    # Clean leftover frames from prior runs
    for old in frames_dir.glob("frame_*.png"):
        old.unlink()

    # 1. TTS
    log("synthesizing narration for each beat")
    _segs = generate_beat_audio(sb, audio_dir)

    # 2. Timing
    compute_timing(sb)
    build_scroll_plan(sb)
    total_scroll = sb.beats[-1].start_time + sb.beats[-1].duration if sb.beats else 0
    log(f"scroll duration: {total_scroll:.2f}s, finale {sb.finale_hold:.2f}s")

    # 3. Render frames
    finale_frames = int(sb.finale_hold * C.FPS)
    render_frames(sb, frames_dir, finale_frames)
    total_duration = total_scroll + sb.finale_hold

    # 4. Build master audio aligned to beat start times
    log("mixing narration audio")
    master_audio = work_dir / "master.wav"
    audio_segments = [(b.audio_path, b.start_time) for b in sb.beats if b.audio_path]
    concat_audio_with_timing(audio_segments, total_duration, master_audio)

    # 5. Encode
    log(f"encoding {output_mp4.name}")
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    frames_to_mp4(frames_dir, master_audio, output_mp4)

    if not keep_frames:
        for old in frames_dir.glob("frame_*.png"):
            old.unlink()
    log(f"done -> {output_mp4}")
    return output_mp4


def main():
    ap = argparse.ArgumentParser(description="Build a short MP4 from a storyboard YAML.")
    ap.add_argument("--storyboard", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--work", type=Path, default=None)
    ap.add_argument("--keep-frames", action="store_true")
    args = ap.parse_args()
    build(args.storyboard, args.out, args.work, args.keep_frames)


if __name__ == "__main__":
    main()
