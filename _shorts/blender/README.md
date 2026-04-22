# Blender shorts pipeline — production build

Net-new solution running in parallel with the PIL-based `_shorts/renderer` pipeline. Produces fully-rendered 3D liquid-glass UML sequence flow MP4s with thin-film iridescent glass, emissive electron path + trail, animated flow arrows, and Apple-style 3D typography — no placeholders, no human recording, no post-production required.

## Why this exists

The PIL pipeline hit a ceiling on "looks like Apple liquid glass." Pure 2D compositing can approximate the look but can't deliver:
- True refraction + thin-film iridescence through glass
- Real reflections / soft area-light interaction
- Camera that follows the electron through the sequence flow and pulls back for a dead-on finale
- Layered translucent glass blobs drifting in the background

Blender 5.0.1 (Eevee Next) on the RTX 4070 SUPER delivers all of the above.

## How it runs

```bash
python -m _shorts.blender.build \
  --storyboard _shorts/templates/L-001_storyboard.yaml \
  --out _deliverables/shorts/blender/L-001-short.mp4
```

This command:
1. Loads the storyboard YAML (same schema as the PIL pipeline).
2. Generates per-beat narration audio via Kokoro on GPU, reusing `_shorts.renderer.tts`.
3. Computes beat start times + durations from audio length.
4. Writes a JSON descriptor to `_shorts/_work/blender/<lesson_id>/descriptor.json`.
5. Launches Blender 5 headless with `render_runner.py`, which builds the 3D scene, keyframes every animated element, and renders the PNG frame sequence.
6. Mixes narration audio via `_shorts.renderer.encode.concat_audio_with_timing`.
7. Encodes frames + audio → MP4 via ffmpeg.

Both pipelines use the same YAML storyboard format, the same TTS, the same audio mix. Only the frame generator differs.

## Visual system

**Backdrop.** Pure white world plane. Four large translucent pastel liquid-glass blobs (peach / mint / lilac / sky) drift slowly in the deep background over the duration of the short — the "layered liquid glass slowly moving" look.

**Commands panel.** Large iridescent glass pill at the top. Contains:
- Lesson title in Segoe UI Semibold (SF Pro analogue).
- "Day N · <learning_title>" subtitle in accent blue.
- Per-beat input display — keycaps, text_input, command, or single key — realized as 3D glass tiles with front-facing Segoe UI text. Visibility is keyframed per beat.

**Lanes.** Thin hairline slabs running horizontally with lane-label glass pills on the left edge. Lane label text is 3D extruded, sits on the front face of each pill.

**Flow arrows.** For each `call` / `return` beat, a cylinder + cone arrow runs from (world_x, z_from) to (world_x, z_to) with an animated `Wave Texture`-based pulse scrolling along its length during the beat's time window. Arrows reveal at beat start and persist.

**Step badges.** Amber emissive circular badges with 3D-extruded Segoe UI Bold step numbers, positioned above the top lane at each visible beat's world_x. Reveal at beat start and persist.

**Electron.** Emissive blue sphere with a halo and an 8-orb delayed trail. Drives the entire flow. Keyframed per beat from (world_x, z_from) to (world_x, z_to).

**Caption.** Glass pill at the bottom with per-beat 3D text (beat label). Visibility keyframed per beat.

**Camera.** Starts 3/4 angle, loosely follows the electron horizontally through each beat (camera_x = electron_x × 0.45), then pulls back and straightens to a dead-on wide shot for the finale hold.

**Post.** Compositor Glare (Bloom) node — makes the electron, step badges, and arrow pulses glow against the white world.

## File layout

| File | Runs in | Purpose |
|---|---|---|
| `__init__.py` | regular | package marker + top-level doc |
| `build.py` | regular Python | orchestrator; CLI entry |
| `render_runner.py` | Blender subprocess | reads descriptor JSON, builds scene, animates, renders |
| `scene.py` | Blender | 3D geometry (lanes, pills, liquid-glass backdrop, electron, trail, step badges, arrows, input displays, lights, camera) |
| `animation.py` | Blender | keyframes electron + trail + camera + backdrop drift + arrows + badges + captions + input-display visibility |
| `materials.py` | Blender | thin-film iridescent glass, frosted glass, liquid-blob pastel, emission, amber badge, arrow-pulse shader graph, text materials |
| `text.py` | Blender | 3D text helpers (Segoe UI) + visibility keyframing |
| `arrows.py` | Blender | cylinder + cone arrow construction + pulse + reveal keyframing |
| `input_display.py` | Blender | per-beat commands-panel tiles: keycaps / text_input / command / single key |

## Requirements

- **Blender 5.0.1** at `C:\Program Files\Blender Foundation\Blender 5.0\`. Update `BLENDER_EXE` in `build.py` if you install elsewhere. Compatible with Blender 5's new compositor node group API (`scene.compositing_node_group`) with automatic fallback to 4.x `scene.node_tree`.
- **Python 3.12** with the PIL pipeline's deps (Kokoro, PyYAML, ffmpeg on PATH).
- **Windows 11** font set (Segoe UI Regular / Semibold / Bold) at `C:\Windows\Fonts\`.
- **CUDA GPU** for Eevee Next raytracing.

## Migration plan

1. Ship this PR — production visuals on `main`.
2. Iterate on remaining polish (per-lesson storyboard tweaks, richer finale, per-beat camera choreography hand-tuning) in follow-up PRs. PIL pipeline keeps running in production the whole time.
3. When the short-author skill's operators agree the Blender output beats PIL subjectively, flip `render_phase.md` to invoke `_shorts.blender.build`. That's the migration.
4. `_shorts/renderer/` then retires or stays as a fallback.
