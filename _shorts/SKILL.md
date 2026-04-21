---
name: short-author
description: Turn a published lesson into a vertical (9:16) narrated MP4 short for TikTok/Reels/Shorts/LinkedIn. Uses the warehouse-worker-fetches analogy with a fixed visual system (scrolling UML sequence flow, centered robot sprite, left-pinned lane labels, user at top, captions + TTS narration). Produces one MP4 per lesson and commits it on branch `shorts/L-###`.
---

# `short-author` skill — vertical shorts from lessons

**Invoke this skill when Elvis says `create short on lesson N` / `create short L-###` / `create next short`.** Nothing else triggers this — regular `do Lesson N` still goes to the `lesson-author` skill.

## What this skill produces

Every run produces, for one lesson:

1. An MP4 at `_deliverables/shorts/L-###-short.mp4` — 1080×1920, H.264 + AAC, 30 fps, 25–60 s
2. A storyboard at `_shorts/templates/L-###_storyboard.yaml` (committed for reuse / editing)
3. A new line in `_state/shorts_index.md` recording the render
4. A draft branch `shorts/L-###` pushed to the remote, with a PR opened against `main`
5. The MP4 is **not** merged — Elvis reviews it and merges, same pattern as lesson-author

## The visual contract (fixed — do not improvise per lesson)

Every short uses the same analogy and the same layout:

- **User** is an 8-bit character at the top center of the frame (pinned in screen-space)
- **Robot** is an 8-bit mascot (locked sprite under `_shorts/character/`) always centered horizontally
- **Swim lanes** are horizontal lifelines running across the canvas, labeled by **boxes pinned to the left edge** (lane names: apps, directories, systems)
- **Timeline scrolls right→left** as time advances — the robot's x position is fixed, the world moves
- **Call/return arrows** are vertical between lanes, drawn at their event x-position (appears at screen center when it happens, scrolls left afterward)
- **Self-actions** (the robot acting on its own lane, e.g. "type: terminal") are drawn as a speech bubble to the right of the robot, with a dot on the lane
- **Finale**: after the last beat, a static frame shows the full sequence diagram (all lanes, all arrows) for ~3.5 seconds
- **Watermark**: `by Elvis Jones` in italic Segoe UI, 26pt, bottom-right, ~80% opacity

## The TTS voice

F5-TTS v1 Base on GPU. By default, the wrapper in `_shorts/renderer/tts.py` uses the bundled English reference clip. When Elvis records a voice sample, replace `DEFAULT_REF_AUDIO` and `DEFAULT_REF_TEXT` in that file — nothing else in the pipeline changes.

## The phases

Run them in order. Each phase file has its own detailed instructions — read the one you're about to run, don't try to hold everything in head.

1. [Research phase](assets/research_phase.md) — read the lesson, map commands to warehouse beats
2. [Script phase](assets/script_phase.md) — draft narration following the "Day X of Learning Y" template
3. [Storyboard phase](assets/storyboard_phase.md) — convert the script into a storyboard YAML
4. [Render phase](assets/render_phase.md) — invoke `_shorts.renderer.build` to produce the MP4
5. [Assembly phase](assets/assembly_phase.md) — commit, push, PR, update `shorts_index.md`, append to production log

## Command dispatch

| Command | Action |
|---|---|
| `create short on lesson 7` / `create short L-007` | Author the short for that lesson. Requires it to be published (in `_state/published_index.md`). |
| `create next short` | Read `_state/shorts_index.md`, pick the lowest-numbered published lesson that does NOT yet have a short. Author that one. |

## Hard rules

- **One lesson per run.** Never batch. If Elvis says "create next short", you pick exactly one.
- **Lesson must be published on `main`.** If the lesson is only on a draft branch, halt and tell Elvis.
- **Never edit the existing `lesson-author` skill.** The shorts module is strictly parallel — same repo, separate directories, separate branch prefix.
- **Never merge the PR yourself.** Elvis reviews and merges.
- **If a quality gate fails** (TTS missing, ffmpeg fails, frame count wrong), halt and write the failure to `_state/pending_review.md` with enough detail for Elvis to decide.
- **Never re-render a published short** unless Elvis explicitly asks.

## Sanity checks before rendering

- `ffmpeg -version` returns 0
- `python -c "from f5_tts.api import F5TTS"` returns 0
- GPU is available (`python -c "import torch; print(torch.cuda.is_available())"` → `True`)
- `_shorts/character/robot.png` exists (the locked mascot sprite sheet)

If any of these fail, halt before burning GPU time on frames.
