# Render phase

Produce the MP4 by running the orchestrator.

## Command

From the repo root:

```bash
python -m _shorts.renderer.build \
  --storyboard _shorts/templates/L-###_storyboard.yaml \
  --out _deliverables/shorts/L-###-short.mp4
```

This will:

1. Load the storyboard YAML
2. Synthesize TTS audio for each beat via F5-TTS on GPU (model loads once, reused across beats)
3. Compute timing: `beat.duration = max(beat.min_duration, audio_duration + 0.25s)`
4. Compute scroll plan (assigns each beat an `event_world_x` anchor)
5. Render PNG frames at 30 fps into `_shorts/_work/L-###/frames/`
6. Render the finale frames (static summary view)
7. Mix beat audio into a master track with per-beat start offsets
8. Encode H.264 + AAC MP4 to the output path
9. Delete frames (unless `--keep-frames` is passed)

## Gate checks after render

- `ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height -of default <out.mp4>` returns:
  - `codec_name=h264`
  - `width=1080` / `height=1920`
  - `codec_name=aac` (second stream)
  - `duration` between 20 and 90 seconds
- File size < 50 MB (should be 1–10 MB for a 30-45 s short)
- No frames marked `_work/L-###/frames/` left behind (unless `--keep-frames` was used intentionally)

If any gate fails, halt and write to `_state/pending_review.md`.

## Iteration

If the MP4 is wrong (wrong pacing, wrong labels, off-mic audio), do NOT hand-edit frames. Edit the **storyboard YAML** and re-run the build. The renderer is the source of truth.
