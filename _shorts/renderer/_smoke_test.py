"""Smoke test: render 3 sample frames from the L-001 storyboard without TTS.

Verifies scene composition, sprite drawing, lane layout, and scrolling geometry.
"""
from pathlib import Path
import sys

from . import config as C
from .storyboard import Storyboard
from .scene import compose_frame, compose_finale_frame, build_scroll_plan


def main():
    yaml_path = C.TEMPLATES_DIR / "L-001_storyboard.yaml"
    sb = Storyboard.from_yaml(yaml_path)
    # Assign placeholder timings (no TTS in smoke test)
    t = 0.0
    for beat in sb.beats:
        beat.duration = beat.min_duration
        beat.start_time = t
        t += beat.duration
    total = t
    build_scroll_plan(sb)
    print(f"smoke: {len(sb.beats)} beats, total {total:.2f}s")

    out_dir = C.WORK_DIR / "smoke"
    out_dir.mkdir(parents=True, exist_ok=True)

    sample_times = [0.5, total * 0.25, total * 0.55, total * 0.85]
    for i, t in enumerate(sample_times):
        img = compose_frame(sb, t)
        p = out_dir / f"smoke_t{int(t*10):03d}.png"
        img.save(p)
        print(f"  saved {p} (t={t:.2f})")

    # Finale frame
    img = compose_finale_frame(sb, 0.5)
    p = out_dir / "smoke_finale.png"
    img.save(p)
    print(f"  saved {p}")


if __name__ == "__main__":
    main()
