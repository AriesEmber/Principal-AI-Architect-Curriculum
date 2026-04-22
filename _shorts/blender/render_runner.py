"""Blender subprocess entry-point. Runs inside Blender's Python env.

Called by build.py as:
    blender.exe --background --python render_runner.py -- \
        --descriptor <path.json> --frames-dir <path>

Reads the JSON descriptor, builds the 3D scene, keyframes the animation, and
renders every frame (frame_000001.png ... frame_NNNNNN.png) into frames-dir.
"""
import argparse
import json
import os
import sys

# Add repo root to path so we can import _shorts.blender.*
# __file__ = .../_shorts/blender/render_runner.py
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import bpy  # noqa: E402
from _shorts.blender import scene as _scene  # noqa: E402
from _shorts.blender import animation as _anim  # noqa: E402


def parse_args() -> argparse.Namespace:
    # Blender eats its own args before `--`, pass the rest to us.
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    ap = argparse.ArgumentParser()
    ap.add_argument("--descriptor", required=True)
    ap.add_argument("--frames-dir", required=True)
    return ap.parse_args(argv)


def main() -> None:
    args = parse_args()
    with open(args.descriptor, "r", encoding="utf-8") as f:
        descriptor = json.load(f)

    print(f"[blender] descriptor loaded: {len(descriptor['beats'])} beats, "
          f"total {descriptor['total_duration']:.2f}s")

    objs = _scene.build_scene(descriptor)
    _anim.apply_animation(objs, descriptor)

    # Debug: scene inventory
    print(f"[blender] scene objects: {len(bpy.data.objects)}")
    keycap_n = sum(1 for o in bpy.data.objects if o.name.startswith("Keycap"))
    txt_n = sum(1 for o in bpy.data.objects if o.name.startswith("KeycapTxt") or o.name.startswith("KeycapPlat"))
    disp_n = sum(1 for o in bpy.data.objects if o.name.startswith("InputDisp"))
    print(f"[blender] keycaps={keycap_n} keycap_text={txt_n} input_display_empties={disp_n}")

    scene = bpy.context.scene
    os.makedirs(args.frames_dir, exist_ok=True)
    # Blender writes to <filepath><frame_number>.png. Use frame_ prefix.
    scene.render.filepath = os.path.join(args.frames_dir, "frame_")
    # Default filename is frame_XXXX.png where XXXX is frame number.

    print(f"[blender] rendering {scene.frame_start}..{scene.frame_end} to "
          f"{args.frames_dir}")
    bpy.ops.render.render(animation=True)
    print("[blender] done")


if __name__ == "__main__":
    main()
