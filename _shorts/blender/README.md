# Blender shorts pipeline (v2)

Net-new solution running in parallel with the PIL-based `_shorts/renderer` pipeline. Built so shorts generation can migrate to true 3D rendering once this reaches the quality bar. Until then, the PIL pipeline stays the production path and this one is the work-in-progress alternative.

## Why this exists

The PIL pipeline hit a ceiling on "looks like Apple liquid glass." Pure 2D compositing can approximate the look but can't deliver:
- True refraction + chromatic dispersion through glass
- Real reflections / HDRI lighting
- Camera moves through a 3D scene (follow-cam, zoom-out finale)
- Iridescent material with physically-based sheen

Blender 5 (Eevee Next) on the local RTX 4070 SUPER can do all of this at ~2 s/frame — faster than the PIL v5 pipeline AND with higher fidelity.

## How it runs

```bash
python -m _shorts.blender.build \
  --storyboard _shorts/templates/L-001_storyboard.yaml \
  --out _deliverables/shorts/blender/L-001-short.mp4
```

This command:
1. Loads the storyboard YAML (same schema the PIL pipeline uses).
2. Generates per-beat narration audio via Kokoro on GPU, reusing `_shorts.renderer.tts` so voice is identical between pipelines.
3. Computes beat start times + durations from audio length.
4. Writes a JSON descriptor to `_shorts/_work/blender/<lesson_id>/descriptor.json`.
5. Launches Blender headless, pointed at `render_runner.py`. Blender builds the 3D scene, keyframes the electron path + camera, renders frame_0001.png..frame_NNNN.png.
6. Mixes audio via `_shorts.renderer.encode.concat_audio_with_timing`.
7. Encodes frames + audio → MP4 via ffmpeg.

Both pipelines use the same YAML storyboard format, the same TTS, the same audio mix. Only the frame generator differs.

## File layout

| File | Runs in | Purpose |
|---|---|---|
| `__init__.py` | regular | package marker + top-level doc |
| `build.py` | regular Python | orchestrator; CLI entry |
| `render_runner.py` | Blender subprocess | reads descriptor JSON, builds scene, animates, renders |
| `scene.py` | Blender | 3D geometry (lanes, glass panels, electron, lights, camera) |
| `animation.py` | Blender | keyframes electron + camera + backdrop from beat list |
| `materials.py` | Blender | glass / emission / iridescent backdrop shaders |

## Known gaps (the migration checklist)

The pipeline currently renders a working MP4, but the visual isn't production-ready yet. Remaining work before this can replace the PIL pipeline:

- [ ] **Text on panels.** Commands panel / lane labels / caption need actual text — currently the panels are glass shells with nothing written on them. Options: (a) Blender `Text` objects extruded in 3D, (b) pre-rendered text as image textures on a plane floating above each pill.
- [ ] **Flow-pulse arrows.** PIL v5 has animated pulses flowing along arrows. Blender version currently has no arrow geometry at all — need to add cylinder arrows between lane Z positions at each beat's world_x, with an emissive pulse shader that scrolls along the arrow (shader node `Wave Texture` or keyframed gradient UV offset).
- [ ] **Commands panel rows (keycap/search/command tiles).** The PIL version accumulates input displays inside the commands panel. In 3D we need smaller pills/plates inside the big commands glass.
- [ ] **Step numbers.** Amber circle-with-number on each beat — 3D extruded numbers or baked text textures.
- [ ] **Electron trail.** Currently just a point emitter; could use Geometry Nodes particle trail or a screen-space post effect.
- [ ] **Finale: all-events-visible overview.** Camera zoom-out hits a dead-on view but doesn't do anything beyond that. Could trigger all input_display tiles to light up, or animate a camera orbit.
- [ ] **Materials tuning.** Iridescent backdrop is a gradient placeholder. Real Apple-style glass needs thin-film with view-dependent color shift; should iterate on the shader graph in Blender's UI and export.
- [ ] **Bloom / post.** Eevee's bloom pass would make the emissive electron read much more brightly; needs enabling + tuning.
- [ ] **Render speed.** Currently ~2 s/frame in Eevee. 38 s video → ~40 min. Acceptable but can be dropped further by reducing samples on static frames.

## Migration plan

1. Ship this PR as-is — pipeline scaffolding, running end-to-end, producing a baseline MP4 at `_deliverables/shorts/blender/L-001-short.mp4`.
2. Iterate on the gaps above in follow-up PRs. Each iteration keeps the PIL pipeline untouched so production isn't blocked.
3. When Blender output beats PIL output by subjective quality on the test lesson, update the `short-author` skill's `render_phase.md` to invoke `_shorts.blender.build` instead of `_shorts.renderer.build`. That's the migration.
4. At that point, `_shorts/renderer/` can be retired (or kept as a fallback).

## Requirements

- **Blender 5.0.1** installed at `C:\Program Files\Blender Foundation\Blender 5.0\`. If you install a newer Blender, update `BLENDER_EXE` in `build.py`.
- **Python 3.12** env with the same deps as the PIL pipeline (Kokoro, PyYAML, ffmpeg on PATH).
- **CUDA GPU** for Eevee Next's raytracing (currently assumes RTX 4070 SUPER).
