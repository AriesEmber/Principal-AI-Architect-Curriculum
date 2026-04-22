"""3D text helpers — Apple-style typography via Segoe UI on Windows.

Uses Blender's TextCurve (FONT curve) objects. Segoe UI is the SF Pro analogue
and is always available on Windows 11.

All text here is native 3D — it extrudes, reflects light, respects DOF, and
looks crisp at 1080x1920. No PNG textures required.
"""
import os
from typing import Optional

import bpy


FONT_DIR = r"C:\Windows\Fonts"
FONT_REGULAR = os.path.join(FONT_DIR, "segoeui.ttf")
FONT_SEMIBOLD = os.path.join(FONT_DIR, "seguisb.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")
FONT_LIGHT = os.path.join(FONT_DIR, "segoeuil.ttf")


_font_cache: dict[str, bpy.types.VectorFont] = {}


def load_font(path: str) -> Optional[bpy.types.VectorFont]:
    """Load a TTF via bpy.data.fonts. Returns None if missing (falls back to
    Blender's built-in Bfont)."""
    if not os.path.isfile(path):
        return None
    if path in _font_cache:
        return _font_cache[path]
    f = bpy.data.fonts.load(path, check_existing=True)
    _font_cache[path] = f
    return f


import math


def make_text(name: str,
              body: str,
              location=(0.0, 0.0, 0.0),
              rotation=None,
              size: float = 0.5,
              extrude: float = 0.02,
              bevel: float = 0.003,
              font_path: str = FONT_SEMIBOLD,
              align_x: str = 'CENTER',
              align_y: str = 'CENTER',
              material: Optional[bpy.types.Material] = None
              ) -> bpy.types.Object:
    """Create a Blender text object and return it.

    By default the text is rotated 90° around X so its readable face points
    toward the -Y camera (Blender's default text lies flat in XY — that's
    unreadable from a -Y camera). Pass an explicit rotation to override.
    """
    if rotation is None:
        rotation = (math.radians(90.0), 0.0, 0.0)
    curve = bpy.data.curves.new(f"{name}_curve", 'FONT')
    curve.body = body
    curve.size = size
    curve.extrude = extrude
    curve.bevel_depth = bevel
    curve.bevel_resolution = 2
    curve.align_x = align_x
    curve.align_y = align_y
    font = load_font(font_path)
    if font is not None:
        curve.font = font

    obj = bpy.data.objects.new(name, curve)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = rotation
    if material is not None:
        obj.data.materials.append(material)
    return obj


def hide_on_frame(obj: bpy.types.Object, frame: int) -> None:
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=frame)
    obj.keyframe_insert(data_path="hide_render", frame=frame)


def show_on_frame(obj: bpy.types.Object, frame: int) -> None:
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=frame)
    obj.keyframe_insert(data_path="hide_render", frame=frame)


def keyframe_visibility(obj: bpy.types.Object,
                         visible_from: int,
                         visible_to: int,
                         hidden_default: bool = True) -> None:
    """Keyframe an object to be visible in [visible_from, visible_to], hidden
    elsewhere. Sets constant interpolation so the flip is instant.
    """
    # Frame 1 (or earlier): hidden
    if hidden_default:
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=max(1, visible_from - 1))
        obj.keyframe_insert(data_path="hide_render", frame=max(1, visible_from - 1))

    # Show
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=visible_from)
    obj.keyframe_insert(data_path="hide_render", frame=visible_from)

    # Hide again after window (if visible_to is finite)
    if visible_to > visible_from:
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=visible_to + 1)
        obj.keyframe_insert(data_path="hide_render", frame=visible_to + 1)

    # Constant interpolation so hide flags snap cleanly.
    ad = obj.animation_data
    if ad and ad.action:
        try:
            for fc in ad.action.fcurves:
                if fc.data_path in ("hide_viewport", "hide_render"):
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'CONSTANT'
        except (AttributeError, TypeError):
            pass  # Blender 5 layered actions — defaults are fine here.


def keyframe_persistent_reveal(obj: bpy.types.Object, reveal_frame: int) -> None:
    """Keep `obj` hidden before `reveal_frame`, visible after. No auto-hide."""
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=max(1, reveal_frame - 1))
    obj.keyframe_insert(data_path="hide_render", frame=max(1, reveal_frame - 1))
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=reveal_frame)
    obj.keyframe_insert(data_path="hide_render", frame=reveal_frame)
    ad = obj.animation_data
    if ad and ad.action:
        try:
            for fc in ad.action.fcurves:
                if fc.data_path in ("hide_viewport", "hide_render"):
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'CONSTANT'
        except (AttributeError, TypeError):
            pass
