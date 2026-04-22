"""Per-beat input_display rendered as 3D glass tiles inside the commands panel.

Shapes (matching the YAML schema used by the PIL pipeline):

    {"type": "keycaps",
     "rows": [{"platform": "Mac", "keys": ["Cmd", "Space"]}, ...]}

    {"type": "key", "label": "Enter"}

    {"type": "command", "prompt": "$", "text": "echo hello"}

    {"type": "text_input", "placeholder": "search...", "text": "terminal"}

Each display is built as a small group of mesh objects (glass keycap bodies +
3D text) parented to an empty. The empty's visibility is keyframed per-beat.
"""
from typing import List, Optional

import bpy
from mathutils import Vector

from . import materials as M
from . import text as T


# Panel-local coordinates inside the commands pill. The commands pill is at
# (0, -0.2, COMMANDS_Z). These offsets put displays just in front of its front
# face (y = -0.25 + small offset) so they read through the glass.
PANEL_Y_FRONT = -0.95   # well in front of commands pill (pill front ≈ Y=-0.525)
KEYCAP_HEIGHT = 0.56
KEYCAP_DEPTH = 0.22


def _parent_all(children: list, parent: bpy.types.Object) -> None:
    """Set parent on each child while preserving the child's world transform.

    Without setting matrix_parent_inverse, Blender treats the child's existing
    location as LOCAL relative to the new parent — which shifts the child by
    the parent's world offset. We explicitly compute the inverse so the child
    stays exactly where it was placed.
    """
    parent_inv = parent.matrix_world.inverted()
    for c in children:
        c.parent = parent
        c.matrix_parent_inverse = parent_inv


def _glass_keycap(name: str,
                   width: float,
                   location,
                   material: bpy.types.Material) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width / 2.0, KEYCAP_DEPTH / 2.0, KEYCAP_HEIGHT / 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.segments = 8
    bev.width = min(KEYCAP_HEIGHT, KEYCAP_DEPTH) * 0.35
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


def _pill_tile(name: str,
                width: float,
                height: float,
                location,
                material: bpy.types.Material) -> bpy.types.Object:
    """Longer pill (for text_input / command backgrounds)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (width / 2.0, KEYCAP_DEPTH / 2.0, height / 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.segments = 8
    bev.width = min(height, KEYCAP_DEPTH) * 0.45
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


# -------------------- Builders --------------------

def build_keycaps_display(spec: dict, panel_center_z: float,
                           key_glass_mat: bpy.types.Material,
                           text_mat: bpy.types.Material,
                           platform_text_mat: bpy.types.Material) -> bpy.types.Object:
    """Stacked rows: platform label on left, keycaps right. Returns a parent empty."""
    rows = spec.get("rows", [])
    bpy.ops.object.empty_add(type='PLAIN_AXES',
                              location=(0, PANEL_Y_FRONT, panel_center_z))
    parent = bpy.context.active_object
    parent.name = "InputDisp_Keycaps"

    n = len(rows)
    # Vertical stack: top of stack slightly above panel center.
    row_gap = 0.82
    total_h = (n - 1) * row_gap if n > 0 else 0
    top_z = panel_center_z + total_h / 2.0

    children: list[bpy.types.Object] = []
    for i, row in enumerate(rows):
        row_z = top_z - i * row_gap
        platform = row.get("platform", "")
        keys = row.get("keys", [])

        if platform:
            plat_txt = T.make_text(
                f"KeycapPlat_{i}",
                body=platform,
                location=(-2.9, PANEL_Y_FRONT - 0.12, row_z),
                size=0.28,
                extrude=0.01,
                bevel=0.002,
                font_path=T.FONT_REGULAR,
                align_x='LEFT',
                material=platform_text_mat)
            children.append(plat_txt)

        # Keycaps right of platform label. Measure approximate width per key.
        # Simple: uniform slot width per key. Cmd/Space/Win/Super all fit.
        slot_w = 1.05
        n_keys = len(keys)
        start_x = -1.2  # first key starts here (aligned to right of platform label)
        for j, key_label in enumerate(keys):
            width = 1.4 if len(key_label) >= 5 else slot_w
            x = start_x + j * (slot_w + 0.2) + width / 2.0 - slot_w / 2.0
            loc = (x, PANEL_Y_FRONT, row_z)
            cap = _glass_keycap(f"Keycap_{i}_{j}", width=width,
                                location=loc, material=key_glass_mat)
            children.append(cap)
            # Text on the cap front face
            txt = T.make_text(
                f"KeycapTxt_{i}_{j}",
                body=key_label,
                location=(x, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02, row_z),
                size=0.25,
                extrude=0.008,
                bevel=0.002,
                font_path=T.FONT_SEMIBOLD,
                material=text_mat)
            children.append(txt)

    _parent_all(children, parent)
    return parent


def build_single_key_display(spec: dict, panel_center_z: float,
                              key_glass_mat: bpy.types.Material,
                              text_mat: bpy.types.Material) -> bpy.types.Object:
    label = spec.get("label", "")
    bpy.ops.object.empty_add(type='PLAIN_AXES',
                              location=(0, PANEL_Y_FRONT, panel_center_z))
    parent = bpy.context.active_object
    parent.name = "InputDisp_Key"

    width = max(1.4, 0.45 + 0.28 * len(label))
    cap = _glass_keycap("KeyCap_Single", width=width,
                        location=(0, PANEL_Y_FRONT, panel_center_z),
                        material=key_glass_mat)
    txt = T.make_text(
        "KeyCapTxt_Single",
        body=label,
        location=(0, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02, panel_center_z),
        size=0.34,
        extrude=0.008,
        bevel=0.002,
        font_path=T.FONT_SEMIBOLD,
        material=text_mat)
    _parent_all([cap, txt], parent)
    return parent


def build_command_display(spec: dict, panel_center_z: float,
                           pill_mat: bpy.types.Material,
                           text_mat: bpy.types.Material,
                           prompt_mat: bpy.types.Material) -> bpy.types.Object:
    prompt = spec.get("prompt", "$")
    text = spec.get("text", "")

    bpy.ops.object.empty_add(type='PLAIN_AXES',
                              location=(0, PANEL_Y_FRONT, panel_center_z))
    parent = bpy.context.active_object
    parent.name = "InputDisp_Command"

    # Long pill, narrow.
    pill = _pill_tile("CmdPill", width=5.4, height=0.9,
                       location=(0, PANEL_Y_FRONT, panel_center_z),
                       material=pill_mat)

    prompt_txt = T.make_text(
        "CmdPrompt", body=prompt,
        location=(-2.35, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02,
                  panel_center_z),
        size=0.36, extrude=0.008, bevel=0.002,
        font_path=T.FONT_SEMIBOLD, align_x='LEFT',
        material=prompt_mat)

    body_txt = T.make_text(
        "CmdBody", body=text,
        location=(-1.8, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02,
                  panel_center_z),
        size=0.36, extrude=0.008, bevel=0.002,
        font_path=T.FONT_REGULAR, align_x='LEFT',
        material=text_mat)

    _parent_all([pill, prompt_txt, body_txt], parent)
    return parent


def build_text_input_display(spec: dict, panel_center_z: float,
                              pill_mat: bpy.types.Material,
                              text_mat: bpy.types.Material,
                              placeholder_mat: bpy.types.Material) -> bpy.types.Object:
    placeholder = spec.get("placeholder", "")
    text = spec.get("text", "")

    bpy.ops.object.empty_add(type='PLAIN_AXES',
                              location=(0, PANEL_Y_FRONT, panel_center_z))
    parent = bpy.context.active_object
    parent.name = "InputDisp_TextInput"

    pill = _pill_tile("TxtPill", width=5.4, height=0.9,
                       location=(0, PANEL_Y_FRONT, panel_center_z),
                       material=pill_mat)

    # If text has content, show it primary; otherwise show the placeholder faint.
    if text:
        main_txt = T.make_text(
            "TxtBody", body=text,
            location=(-2.35, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02,
                      panel_center_z),
            size=0.38, extrude=0.008, bevel=0.002,
            font_path=T.FONT_REGULAR, align_x='LEFT',
            material=text_mat)
        children = [pill, main_txt]
    else:
        ph = T.make_text(
            "TxtPlaceholder", body=placeholder,
            location=(-2.35, PANEL_Y_FRONT - KEYCAP_DEPTH / 2.0 - 0.02,
                      panel_center_z),
            size=0.36, extrude=0.008, bevel=0.002,
            font_path=T.FONT_REGULAR, align_x='LEFT',
            material=placeholder_mat)
        children = [pill, ph]

    _parent_all(children, parent)
    return parent


# -------------------- Dispatcher --------------------

def build_for_beat(spec: Optional[dict], panel_center_z: float,
                    mats: dict) -> Optional[bpy.types.Object]:
    """Return the parent empty for the beat's input display, or None if the
    beat has no display.
    """
    if not spec:
        return None
    kind = spec.get("type")
    if kind == "keycaps":
        return build_keycaps_display(
            spec, panel_center_z,
            key_glass_mat=mats["key_glass"],
            text_mat=mats["text_dark"],
            platform_text_mat=mats["text_platform"])
    if kind == "key":
        return build_single_key_display(
            spec, panel_center_z,
            key_glass_mat=mats["key_glass"],
            text_mat=mats["text_dark"])
    if kind == "command":
        return build_command_display(
            spec, panel_center_z,
            pill_mat=mats["pill_dark"],
            text_mat=mats["text_white"],
            prompt_mat=mats["text_accent"])
    if kind == "text_input":
        return build_text_input_display(
            spec, panel_center_z,
            pill_mat=mats["pill_glass"],
            text_mat=mats["text_dark"],
            placeholder_mat=mats["text_platform"])
    return None


def keyframe_display_visibility(parent: bpy.types.Object,
                                  reveal_frame: int,
                                  hide_frame: int) -> None:
    """Show the whole subtree between [reveal_frame, hide_frame].

    Keyframes the parent empty + every descendant mesh/text object. Blender
    does NOT cascade hide_render from an empty to its children, so we have to
    keyframe each child explicitly.
    """
    objs = [parent] + _descendants(parent)
    for obj in objs:
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport",
                             frame=max(1, reveal_frame - 1))
        obj.keyframe_insert(data_path="hide_render",
                             frame=max(1, reveal_frame - 1))
        obj.hide_viewport = False
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_viewport", frame=reveal_frame)
        obj.keyframe_insert(data_path="hide_render", frame=reveal_frame)
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=hide_frame + 1)
        obj.keyframe_insert(data_path="hide_render", frame=hide_frame + 1)
        ad = obj.animation_data
        if ad and ad.action:
            try:
                for fc in ad.action.fcurves:
                    if fc.data_path in ("hide_viewport", "hide_render"):
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'CONSTANT'
            except (AttributeError, TypeError):
                pass


def _descendants(obj: bpy.types.Object) -> List[bpy.types.Object]:
    out: List[bpy.types.Object] = []
    stack = list(obj.children)
    while stack:
        n = stack.pop()
        out.append(n)
        stack.extend(n.children)
    return out
