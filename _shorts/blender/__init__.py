"""Blender-based shorts renderer (v2 pipeline).

This package is a net-new solution running in parallel with the
_shorts/renderer PIL pipeline. When the Blender pipeline reaches the quality
bar, shorts generation will migrate off PIL. Until then, both live here and
can produce MP4s independently.

Architecture:
    build.py          orchestrator — runs in a normal Python env.
                      Reuses _shorts.renderer.tts (Kokoro) and
                      _shorts.renderer.encode (ffmpeg mux). Launches Blender
                      as a subprocess to render frames.

    render_runner.py  Blender entry-point (imports bpy). Reads a JSON scene
                      descriptor written by build.py, constructs the 3D
                      scene via materials/scene/animation modules, renders
                      the PNG frame sequence.

    materials.py      Glass / emission / iridescent-backdrop / lane-slab
                      shader node graphs. Blender-only.

    scene.py          Geometry: lane slabs, glass pills, electron sphere,
                      lights, camera. Blender-only.

    animation.py      Keyframes electron path + camera from beat list.
                      Blender-only.

Run:
    python -m _shorts.blender.build \
        --storyboard _shorts/templates/L-001_storyboard.yaml \
        --out _deliverables/shorts/blender/L-001-short.mp4
"""
