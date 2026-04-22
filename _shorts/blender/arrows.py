"""Flow arrows between lanes with an animated pulse.

Each beat of kind `call` / `return` gets a cylinder + arrowhead running from
(world_x, y_front, z_from) → (world_x, y_front, z_to). The material scrolls a
bright band along the tube during the beat's window to convey direction.
"""
import math
from typing import Tuple

import bpy
from mathutils import Vector

from . import materials as M


ARROW_RADIUS = 0.09
ARROW_HEAD_RADIUS = 0.22
ARROW_HEAD_LENGTH = 0.30
Y_FRONT = -0.9  # slightly in front of lane plane so arrows pop visually


def _cylinder_between(name: str,
                       p_from: Vector,
                       p_to: Vector,
                       radius: float) -> bpy.types.Object:
    mid = (p_from + p_to) / 2.0
    direction = p_to - p_from
    length = direction.length
    if length < 1e-6:
        length = 1e-4  # degenerate; keep it drawable
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=length,
        vertices=24,
        location=mid)
    obj = bpy.context.active_object
    obj.name = name

    # Orient +Z of cylinder along direction.
    z = Vector((0, 0, 1))
    quat = z.rotation_difference(direction.normalized() if length > 0 else z)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat
    obj.rotation_mode = 'XYZ'

    bpy.ops.object.shade_smooth()
    return obj


def _cone_at(name: str,
              tip: Vector,
              direction: Vector,
              radius: float,
              length: float) -> bpy.types.Object:
    """Cone with base at tip - direction*length, tip at tip."""
    direction = direction.normalized()
    base_center = tip - direction * (length / 2.0)
    bpy.ops.mesh.primitive_cone_add(
        vertices=24,
        radius1=radius,
        radius2=0.0,
        depth=length,
        location=base_center)
    obj = bpy.context.active_object
    obj.name = name
    z = Vector((0, 0, 1))
    quat = z.rotation_difference(direction)
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = quat
    obj.rotation_mode = 'XYZ'
    bpy.ops.object.shade_smooth()
    return obj


def build_arrow(name: str,
                 from_pos: Tuple[float, float, float],
                 to_pos: Tuple[float, float, float],
                 material: bpy.types.Material) -> dict:
    """Build shaft + head as two meshes parented to an empty — returns {
    'root', 'shaft', 'head', 'material'}."""
    p_from = Vector(from_pos)
    p_to = Vector(to_pos)

    direction = p_to - p_from
    length = direction.length
    # Shorten shaft so the head caps the visual end cleanly.
    if length > ARROW_HEAD_LENGTH * 1.2:
        shaft_to = p_to - direction.normalized() * ARROW_HEAD_LENGTH
    else:
        shaft_to = p_to

    shaft = _cylinder_between(f"{name}_shaft", p_from, shaft_to, ARROW_RADIUS)
    shaft.data.materials.append(material)

    head = _cone_at(f"{name}_head", p_to, direction,
                    ARROW_HEAD_RADIUS, ARROW_HEAD_LENGTH)
    head.data.materials.append(material)

    # Group under an empty for bulk operations.
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = f"{name}_root"
    shaft.parent = root
    head.parent = root

    return {"root": root, "shaft": shaft, "head": head, "material": material,
            "from": p_from, "to": p_to}


def keyframe_pulse(arrow: dict, start_frame: int, end_frame: int) -> None:
    """Scroll the pulse along the arrow between start_frame and end_frame.

    Writes keyframes on the material's PulseMapping.Location Z from 0 → 1.
    """
    mat: bpy.types.Material = arrow["material"]
    mapping = mat.node_tree.nodes.get("PulseMapping")
    if mapping is None:
        return
    # Z offset 0 at beat start → 1.6 at beat end (1.6 so it fully traverses and
    # goes slightly beyond before the next beat).
    mapping.inputs["Location"].default_value[2] = -0.3
    mapping.inputs["Location"].keyframe_insert(
        "default_value", index=2, frame=max(1, start_frame))
    mapping.inputs["Location"].default_value[2] = 1.6
    mapping.inputs["Location"].keyframe_insert(
        "default_value", index=2, frame=end_frame)


def keyframe_reveal(arrow: dict, reveal_frame: int) -> None:
    """Hide arrow before reveal_frame, then reveal permanently."""
    for obj in (arrow["shaft"], arrow["head"]):
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
        ad = obj.animation_data
        if ad and ad.action:
            try:
                for fc in ad.action.fcurves:
                    if fc.data_path in ("hide_viewport", "hide_render"):
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'CONSTANT'
            except (AttributeError, TypeError):
                pass
