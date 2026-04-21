"""Audio concatenation + frame-to-MP4 encoding via ffmpeg."""
import subprocess
from pathlib import Path
from . import config as C


def generate_silence(duration: float, out_path: Path, sample_rate: int = 24000):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"anullsrc=r={sample_rate}:cl=mono",
         "-t", f"{duration:.3f}", "-q:a", "0", str(out_path)],
        capture_output=True, check=True,
    )
    return out_path


def concat_audio_with_timing(
    audio_segments: list[tuple[Path, float]],
    total_duration: float,
    out_path: Path,
    sample_rate: int = 24000,
) -> Path:
    """Place each audio segment at its target start time.

    audio_segments: list of (wav_path, start_time_seconds).
    A silent master track of length total_duration is produced, then each
    segment is overlaid at its start time.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    work = out_path.parent
    # Build filter graph: silent base + each input delayed by start time.
    inputs = ["-f", "lavfi", "-t", f"{total_duration:.3f}",
              "-i", f"anullsrc=r={sample_rate}:cl=mono"]
    for wav, _ in audio_segments:
        inputs += ["-i", str(wav)]
    filter_parts = []
    for i, (_wav, start_s) in enumerate(audio_segments):
        delay_ms = int(start_s * 1000)
        filter_parts.append(f"[{i+1}:a]adelay={delay_ms}|{delay_ms},apad[a{i}]")
    amix_inputs = "[0:a]" + "".join(f"[a{i}]" for i in range(len(audio_segments)))
    filter_parts.append(
        f"{amix_inputs}amix=inputs={len(audio_segments)+1}:dropout_transition=0:normalize=0,"
        f"atrim=end={total_duration:.3f}[out]"
    )
    filter_complex = ";".join(filter_parts)
    cmd = ["ffmpeg", "-y", *inputs,
           "-filter_complex", filter_complex,
           "-map", "[out]",
           "-ar", str(sample_rate), "-ac", "1",
           str(out_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"audio mux failed:\n{result.stderr[-1500:]}\nCMD: {' '.join(cmd)}"
        )
    return out_path


def frames_to_mp4(frames_dir: Path, audio_path: Path, out_path: Path,
                  fps: int = C.FPS) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%06d.png"),
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"encode failed:\n{result.stderr[-1500:]}\nCMD: {' '.join(cmd)}"
        )
    return out_path
