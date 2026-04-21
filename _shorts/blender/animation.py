"""Keyframe generation for the electron + camera from the beat list.

The orchestrator (build.py) runs TTS first and writes each beat's start_time
and duration into the descriptor. This module reads those and sets Blender
keyframes so the electron follows the sequence-diagram path and the camera
slightly tracks it. At the finale, the camera pulls back to a dead-on view.
"""
import math
import bpy
from mathutils import Vector

from .scene import BEAT_X_MIN, BEAT_X_MAX, FPS, CANVAS_H


# -------------------- Beat x/z layout --------------------

def assign_beat_positions(descriptor: dict, lane_z: dict[str, float]) -> None:
    """Annotate each beat with (world_x, world_z_from, world_z_to) used by the
    electron path. Skips 'open' beats when distributing x — they share the x
    of the next visible beat."""
    beats = descriptor["beats"]
    visible = [b for b in beats if b["kind"] != "open"]
    nv = len(visible)
    step = (BEAT_X_MAX - BEAT_X_MIN) / max(nv, 1)
    for i, b in enumerate(visible):
        b["world_x"] = BEAT_X_MIN + step * (i + 0.5)

    # Open beats: x = next visible beat's x.
    next_x = visible[0]["world_x"] if visible else 0.0
    for i, b in enumerate(beats):
        if b["kind"] == "open":
            # Scan forward for next visible.
            for j in range(i + 1, len(beats)):
                if beats[j]["kind"] != "open":
                    next_x = beats[j]["world_x"]
                    break
            b["world_x"] = next_x

    # World Z for each beat (from/to lane positions).
    for b in beats:
        if b["kind"] == "open":
            b["z_from"] = lane_z[b["to_lane"]]
            b["z_to"] = b["z_from"]
        elif b["kind"] == "self":
            b["z_from"] = lane_z[b["from_lane"]]
            b["z_to"] = b["z_from"]
        elif b["kind"] in ("call", "return"):
            b["z_from"] = lane_z[b["from_lane"]]
            b["z_to"] = lane_z[b["to_lane"]]


# -------------------- Timing helpers --------------------

def sec_to_frame(t: float) -> int:
    return max(1, int(round(t * FPS)) + 1)


def _iter_fcurves(action):
    """Blender 5 Actions use layered slots; Blender 4.x exposes fcurves directly.
    Yield fcurves from whichever API exists."""
    if hasattr(action, "fcurves") and action.fcurves is not None:
        try:
            for fc in action.fcurves:
                yield fc
            return
        except (AttributeError, TypeError):
            pass
    # Blender 5 layered action path
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for ch in getattr(strip, "channelbag", lambda *a: [])(layer.slots[0]) if hasattr(strip, "channelbag") else []:
                for fc in getattr(ch, "fcurves", []):
                    yield fc


def _set_bezier_interpolation(obj):
    """Best-effort: set bezier interpolation on all keyframes for obj. Silently
    no-ops on Blender 5's newer layered Actions where fcurve access changed."""
    ad = getattr(obj, "animation_data", None)
    if not ad or not ad.action:
        return
    try:
        for fc in _iter_fcurves(ad.action):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'
                kp.handle_left_type = 'AUTO_CLAMPED'
                kp.handle_right_type = 'AUTO_CLAMPED'
    except Exception:
        pass  # Non-fatal — Blender defaults to Bezier anyway.


# -------------------- Electron keyframing --------------------

def keyframe_electron(electron: bpy.types.Object, descriptor: dict) -> None:
    """Drive the electron's location through all beats.

    For each beat:
        - open:   sit at (world_x, -0.9, z_from) for the beat's duration.
        - self:   same position (small orbit could be added with a driver).
        - call:   lerp from (world_x, *, z_from) -> (world_x, *, z_to).
        - return: same as call but z direction reversed.

    Between beats: the location simply keyframes to the next beat's start.
    Blender's default interpolation (Bezier) gives smooth motion.
    """
    beats = descriptor["beats"]
    if not beats:
        return

    # Always keep the electron slightly in front of the lane plane (at Y=-0.9)
    # so it reads against the dark lane.
    y_front = -0.9

    first = beats[0]
    electron.location = (first["world_x"], y_front, first["z_from"])
    electron.keyframe_insert(data_path="location", frame=1)

    for i, b in enumerate(beats):
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])

        # Start of beat: electron must be at (world_x, _, z_from).
        electron.location = (b["world_x"], y_front, b["z_from"])
        electron.keyframe_insert(data_path="location", frame=start_f)

        # End of beat: electron at (world_x, _, z_to). For self/open this is
        # the same as start, which is fine — no motion for that beat.
        electron.location = (b["world_x"], y_front, b["z_to"])
        electron.keyframe_insert(data_path="location", frame=end_f)

    _set_bezier_interpolation(electron)


# -------------------- Camera keyframing --------------------

def keyframe_camera(camera: bpy.types.Object, descriptor: dict) -> None:
    """Subtle camera push toward electron during beats, then pull back and
    straighten for the finale hold."""
    total_duration = descriptor["total_duration"]
    finale_hold = descriptor.get("finale_hold", 3.0)

    base_loc = Vector((1.5, -15.0, 0.8))
    finale_loc = Vector((0.0, -18.0, 0.0))

    # Start
    camera.location = base_loc
    camera.keyframe_insert(data_path="location", frame=1)

    # Mid (hold the 3/4 view during the bulk of the diagram build).
    mid_f = sec_to_frame(total_duration - finale_hold - 0.2)
    camera.location = base_loc + Vector((-0.5, 0.3, 0.0))
    camera.keyframe_insert(data_path="location", frame=mid_f)

    # Finale: pull back + center.
    finale_start_f = sec_to_frame(total_duration - finale_hold)
    camera.location = finale_loc
    camera.keyframe_insert(data_path="location", frame=finale_start_f)

    # End: hold the finale position.
    end_f = sec_to_frame(total_duration)
    camera.location = finale_loc + Vector((0.0, -1.0, 0.0))
    camera.keyframe_insert(data_path="location", frame=end_f)

    # Also animate the camera rotation: start at 3/4 angle, end dead-on.
    base_rot = camera.rotation_euler.copy()
    # Dead-on finale rotation: point camera straight down +Y at origin.
    camera.rotation_euler = (math.radians(90), 0.0, 0.0)
    # Reset to base at frame 1
    camera.rotation_euler = base_rot
    camera.keyframe_insert(data_path="rotation_euler", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=mid_f)
    camera.rotation_euler = (math.radians(90), 0.0, 0.0)
    camera.keyframe_insert(data_path="rotation_euler", frame=finale_start_f)
    camera.keyframe_insert(data_path="rotation_euler", frame=end_f)

    _set_bezier_interpolation(camera)


# -------------------- Backdrop rotation driver --------------------

def animate_backdrop(backdrop_mat: bpy.types.Material,
                     total_duration: float) -> None:
    """Slowly rotate the backdrop gradient so the iridescent sheen shifts
    over time. Uses a linear keyframe on the Mapping node's Z rotation.
    """
    mapping = backdrop_mat.node_tree.nodes.get("BackdropMapping")
    if mapping is None:
        return
    # Rotate 60 degrees over the whole short — subtle.
    mapping.inputs["Rotation"].default_value[2] = math.radians(20)
    mapping.inputs["Rotation"].keyframe_insert("default_value", index=2,
                                                 frame=1)
    mapping.inputs["Rotation"].default_value[2] = math.radians(80)
    mapping.inputs["Rotation"].keyframe_insert("default_value", index=2,
                                                 frame=sec_to_frame(total_duration))
    # Linear interpolation (constant rate) — best-effort, works on 4.x, safe
    # no-op on Blender 5 layered actions.
    ad = getattr(backdrop_mat.node_tree, "animation_data", None)
    if ad and ad.action:
        try:
            for fc in _iter_fcurves(ad.action):
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
        except Exception:
            pass


# -------------------- Main entrypoint --------------------

def apply_animation(objs: dict, descriptor: dict) -> None:
    scene = bpy.context.scene
    # Set playback range based on total duration.
    total_duration = descriptor["total_duration"]
    scene.frame_start = 1
    scene.frame_end = sec_to_frame(total_duration)

    # Assign beat positions on the descriptor.
    assign_beat_positions(descriptor, objs["lane_z"])

    # Keyframe objects.
    keyframe_electron(objs["electron"], descriptor)
    keyframe_camera(objs["camera"], descriptor)
    animate_backdrop(objs["backdrop_mat"], total_duration)
