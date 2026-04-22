"""Keyframing for electron path, camera follow, arrows, badges, captions,
input displays, and liquid-glass backdrop drift.

Timing model:
    descriptor.total_duration = sum(beat.duration) + finale_hold
    frame(t) = round(t * FPS) + 1

Each beat has start_time (sec) and duration (sec). The finale begins at
total_duration - finale_hold and lasts finale_hold seconds.
"""
import math

import bpy
from mathutils import Vector

from . import text as T
from . import arrows as A
from . import input_display as IDisp
from .scene import (BEAT_X_MIN, BEAT_X_MAX, FPS, Y_FRONT, beat_x_position)


# -------------------- Helpers --------------------

def sec_to_frame(t: float) -> int:
    return max(1, int(round(t * FPS)) + 1)


def _iter_fcurves(action):
    """Yield fcurves across Blender 4.x / 5.x Action APIs."""
    if hasattr(action, "fcurves") and action.fcurves is not None:
        try:
            for fc in action.fcurves:
                yield fc
            return
        except (AttributeError, TypeError):
            pass
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            cb = getattr(strip, "channelbag", None)
            if cb:
                try:
                    bag = cb(layer.slots[0])
                    for fc in getattr(bag, "fcurves", []):
                        yield fc
                except Exception:
                    continue


def _set_bezier(obj):
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
        pass


# -------------------- Beat geometry --------------------

def assign_beat_positions(descriptor: dict, lane_z: dict) -> None:
    beats = descriptor["beats"]
    visible = [b for b in beats if b["kind"] != "open"]
    nv = len(visible)
    for i, b in enumerate(visible):
        b["world_x"] = beat_x_position(i, nv)

    # Open beats adopt next visible beat's x.
    last_x = visible[0]["world_x"] if visible else 0.0
    for i, b in enumerate(beats):
        if b["kind"] == "open":
            next_x = last_x
            for j in range(i + 1, len(beats)):
                if beats[j]["kind"] != "open":
                    next_x = beats[j]["world_x"]
                    break
            b["world_x"] = next_x

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


# -------------------- Electron --------------------

def keyframe_electron(electron: bpy.types.Object,
                       halo: bpy.types.Object,
                       descriptor: dict) -> None:
    beats = descriptor["beats"]
    if not beats:
        return

    first = beats[0]
    for obj in (electron, halo):
        obj.location = (first["world_x"], Y_FRONT, first["z_from"])
        obj.keyframe_insert(data_path="location", frame=1)

    for i, b in enumerate(beats):
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])
        for obj in (electron, halo):
            obj.location = (b["world_x"], Y_FRONT, b["z_from"])
            obj.keyframe_insert(data_path="location", frame=start_f)
            obj.location = (b["world_x"], Y_FRONT, b["z_to"])
            obj.keyframe_insert(data_path="location", frame=end_f)

    _set_bezier(electron)
    _set_bezier(halo)


def keyframe_trail(trail_orbs: list, electron: bpy.types.Object,
                    descriptor: dict) -> None:
    """Trail orbs follow the electron with per-orb delay.

    Approach: offset each orb's location keyframes by k frames behind the
    electron's path, and fade them in after the electron starts moving.
    """
    if not trail_orbs:
        return
    beats = descriptor["beats"]
    if not beats:
        return

    FPS_LOCAL = FPS
    delay_per_orb = 2  # frames

    # Reveal each orb after its delay frame, then keep it visible.
    for k, orb in enumerate(trail_orbs):
        reveal_f = 1 + (k + 1) * delay_per_orb
        orb.hide_viewport = True
        orb.hide_render = True
        orb.keyframe_insert(data_path="hide_viewport", frame=max(1, reveal_f - 1))
        orb.keyframe_insert(data_path="hide_render", frame=max(1, reveal_f - 1))
        orb.hide_viewport = False
        orb.hide_render = False
        orb.keyframe_insert(data_path="hide_viewport", frame=reveal_f)
        orb.keyframe_insert(data_path="hide_render", frame=reveal_f)
        ad = orb.animation_data
        if ad and ad.action:
            try:
                for fc in _iter_fcurves(ad.action):
                    if fc.data_path in ("hide_viewport", "hide_render"):
                        for kp in fc.keyframe_points:
                            kp.interpolation = 'CONSTANT'
            except Exception:
                pass

    # Keyframe positions: orb_k position = electron position at (t - k*delay/FPS).
    first = beats[0]
    start_loc = Vector((first["world_x"], Y_FRONT, first["z_from"]))
    for k, orb in enumerate(trail_orbs):
        orb.location = start_loc
        orb.keyframe_insert(data_path="location", frame=1)

    for i, b in enumerate(beats):
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])
        for k, orb in enumerate(trail_orbs):
            lag = (k + 1) * delay_per_orb
            f1 = max(1, start_f + lag)
            f2 = max(1, end_f + lag)
            orb.location = (b["world_x"], Y_FRONT, b["z_from"])
            orb.keyframe_insert(data_path="location", frame=f1)
            orb.location = (b["world_x"], Y_FRONT, b["z_to"])
            orb.keyframe_insert(data_path="location", frame=f2)

    for orb in trail_orbs:
        _set_bezier(orb)


# -------------------- Camera --------------------

def keyframe_camera(camera: bpy.types.Object, descriptor: dict) -> None:
    """Camera smoothly follows electron through beats, then pulls back and
    straightens for the finale overview.
    """
    total_duration = descriptor["total_duration"]
    finale_hold = descriptor.get("finale_hold", 3.0)
    beats = descriptor["beats"]

    # Offsets from the electron position — the camera stays back in -Y and up
    # in +Z, giving a 3/4 view that tracks horizontally with the electron.
    CAM_Y = -14.5
    CAM_Z_BASE = 0.7

    # Initial — at the first beat, slightly offset for lead-in.
    if beats:
        first = beats[0]
        cam_x0 = first["world_x"] * 0.20
    else:
        cam_x0 = 0.0
    camera.location = (cam_x0, CAM_Y, CAM_Z_BASE)
    camera.rotation_euler = _lookat_euler(camera.location,
                                           target=(0.0, 0.0, 0.4))
    camera.keyframe_insert(data_path="location", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=1)

    # Per-beat: track electron X lightly, stay centered in Z.
    # Gentle follow (0.25x) so lane labels on the far left edge stay in frame.
    for i, b in enumerate(beats):
        mid_t = b["start_time"] + b["duration"] / 2.0
        mid_f = sec_to_frame(mid_t)
        mid_x = b["world_x"]
        mid_z = (b["z_from"] + b["z_to"]) / 2.0
        cam_x = mid_x * 0.25
        cam_z = CAM_Z_BASE + mid_z * 0.12
        cam_y = CAM_Y
        camera.location = (cam_x, cam_y, cam_z)
        target = (mid_x * 0.2, 0.0, mid_z * 0.35 + 0.4)
        camera.rotation_euler = _lookat_euler(camera.location, target=target)
        camera.keyframe_insert(data_path="location", frame=mid_f)
        camera.keyframe_insert(data_path="rotation_euler", frame=mid_f)

    # Pre-finale: align to center before pull-back.
    finale_start_t = max(0.0, total_duration - finale_hold)
    approach_f = sec_to_frame(max(0.0, finale_start_t - 0.4))
    camera.location = (0.0, -16.0, 0.6)
    camera.rotation_euler = _lookat_euler(camera.location,
                                           target=(0.0, 0.0, 0.4))
    camera.keyframe_insert(data_path="location", frame=approach_f)
    camera.keyframe_insert(data_path="rotation_euler", frame=approach_f)

    # Finale start: pull back, straighten (dead-on).
    finale_f = sec_to_frame(finale_start_t)
    camera.location = (0.0, -20.5, 0.0)
    camera.rotation_euler = _lookat_euler(camera.location,
                                           target=(0.0, 0.0, 0.0))
    camera.keyframe_insert(data_path="location", frame=finale_f)
    camera.keyframe_insert(data_path="rotation_euler", frame=finale_f)

    # Hold slight drift during finale.
    end_f = sec_to_frame(total_duration)
    camera.location = (0.0, -21.2, 0.05)
    camera.rotation_euler = _lookat_euler(camera.location,
                                           target=(0.0, 0.0, 0.0))
    camera.keyframe_insert(data_path="location", frame=end_f)
    camera.keyframe_insert(data_path="rotation_euler", frame=end_f)

    # DOF focus follows subject distance (approximate — camera Y distance to target).
    _keyframe_camera_focus(camera, descriptor)

    _set_bezier(camera)


def _keyframe_camera_focus(camera: bpy.types.Object, descriptor: dict) -> None:
    beats = descriptor["beats"]
    total_duration = descriptor["total_duration"]
    finale_hold = descriptor.get("finale_hold", 3.0)

    camera.data.dof.focus_distance = 15.0
    camera.data.dof.keyframe_insert(data_path="focus_distance", frame=1)

    for b in beats:
        mid_f = sec_to_frame(b["start_time"] + b["duration"] / 2.0)
        camera.data.dof.focus_distance = 15.0
        camera.data.dof.keyframe_insert(data_path="focus_distance", frame=mid_f)

    finale_f = sec_to_frame(max(0.0, total_duration - finale_hold))
    camera.data.dof.focus_distance = 21.0
    camera.data.dof.keyframe_insert(data_path="focus_distance", frame=finale_f)

    end_f = sec_to_frame(total_duration)
    camera.data.dof.focus_distance = 21.5
    camera.data.dof.keyframe_insert(data_path="focus_distance", frame=end_f)


def _lookat_euler(cam_loc, target) -> tuple[float, float, float]:
    """Compute XYZ euler rotation for a camera at `cam_loc` pointed at
    `target`, with up = +Z."""
    v = Vector(target) - Vector(cam_loc)
    quat = v.to_track_quat('-Z', 'Y')
    e = quat.to_euler('XYZ')
    return (e.x, e.y, e.z)


# -------------------- Step badges --------------------

def keyframe_step_badges(step_badges: list, descriptor: dict) -> None:
    beats = descriptor["beats"]
    for i, b in enumerate(beats):
        entry = step_badges[i] if i < len(step_badges) else None
        if entry is None:
            continue
        reveal_f = sec_to_frame(b["start_time"] + 0.05)
        for obj in (entry["badge"], entry["num"]):
            T.keyframe_persistent_reveal(obj, reveal_f)


# -------------------- Arrows --------------------

def keyframe_arrows(arrow_objects: list, descriptor: dict) -> None:
    beats = descriptor["beats"]
    for i, b in enumerate(beats):
        arr = arrow_objects[i] if i < len(arrow_objects) else None
        if arr is None:
            continue
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])
        A.keyframe_reveal(arr, reveal_frame=start_f)
        A.keyframe_pulse(arr, start_frame=start_f, end_frame=end_f)


# -------------------- Captions --------------------

def keyframe_captions(caption_texts: list, descriptor: dict) -> None:
    beats = descriptor["beats"]
    for i, b in enumerate(beats):
        if i >= len(caption_texts):
            break
        ct = caption_texts[i]
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])
        T.keyframe_visibility(ct, visible_from=start_f, visible_to=end_f)


# -------------------- Input displays --------------------

def keyframe_displays(display_objects: list, descriptor: dict) -> None:
    beats = descriptor["beats"]
    for i, b in enumerate(beats):
        if i >= len(display_objects):
            break
        disp = display_objects[i]
        if disp is None:
            continue
        start_f = sec_to_frame(b["start_time"])
        end_f = sec_to_frame(b["start_time"] + b["duration"])
        IDisp.keyframe_display_visibility(disp, reveal_frame=start_f,
                                            hide_frame=end_f)


# -------------------- Liquid-glass backdrop drift --------------------

def keyframe_liquid_layers(layers: list, total_duration: float) -> None:
    """Slow horizontal + slight vertical drift of each layer across the run.
    Gives the "layered liquid glass slowly moving" effect.
    """
    if not layers:
        return
    end_f = sec_to_frame(total_duration)
    for i, layer in enumerate(layers):
        start_loc = layer.location.copy()
        # Each layer drifts in a different direction at different speed.
        dx = 1.8 * (1 if i % 2 == 0 else -1) * (0.7 + 0.3 * (i % 3))
        dz = 0.9 * ((i + 1) % 2 - 0.5) * 2.0
        layer.location = start_loc
        layer.keyframe_insert(data_path="location", frame=1)
        layer.location = (start_loc.x + dx, start_loc.y, start_loc.z + dz)
        layer.keyframe_insert(data_path="location", frame=end_f)
        # Linear-ish: set bezier with soft handles.
        _set_bezier(layer)


# -------------------- Entrypoint --------------------

def apply_animation(objs: dict, descriptor: dict) -> None:
    scene = bpy.context.scene
    total_duration = descriptor["total_duration"]
    scene.frame_start = 1
    scene.frame_end = sec_to_frame(total_duration)

    assign_beat_positions(descriptor, objs["lane_z"])

    keyframe_electron(objs["electron"], objs["electron_halo"], descriptor)
    keyframe_trail(objs["trail_orbs"], objs["electron"], descriptor)
    keyframe_camera(objs["camera"], descriptor)
    keyframe_step_badges(objs["step_badges"], descriptor)
    keyframe_arrows(objs["arrow_objects"], descriptor)
    keyframe_captions(objs["caption_texts"], descriptor)
    keyframe_displays(objs["display_objects"], descriptor)
    keyframe_liquid_layers(objs["liquid_layers"], total_duration)
