"""3D scene builder for a short. Blender-only (imports bpy).

Reads a JSON scene descriptor (written by build.py) and produces the scene:
    - Iridescent backdrop plane
    - Three dark lane slabs at Z-heights
    - Glass commands panel above the top lane
    - Small glass lane-label pill on the left edge of each lane
    - Glass caption panel below the bottom lane
    - Emissive "electron" sphere (initial position = first beat start)
    - Key / fill / rim lighting
    - 3/4 angle camera

World convention:
    +X right, +Z up, +Y into scene (away from camera)
    Camera sits at -Y looking toward +Y
"""
import math
import bpy
from mathutils import Vector

from . import materials as M


# -------------------- Scene constants --------------------

CANVAS_W = 1080
CANVAS_H = 1920
FPS = 30

# Vertical Z positions for a 3-lane diagram. More lanes → spread them further.
DEFAULT_LANE_Z = [2.2, 0.0, -2.2]

# World X span used to lay out beats across the diagram.
BEAT_X_MIN = -4.0
BEAT_X_MAX = 4.0

# Commands / caption Z positions.
COMMANDS_Z = 5.2
CAPTION_Z = -4.8


# -------------------- Scene reset --------------------

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


# -------------------- Render settings --------------------

def configure_render():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = CANVAS_W
    scene.render.resolution_y = CANVAS_H
    scene.render.resolution_percentage = 100
    scene.render.fps = FPS
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'

    ev = scene.eevee
    if hasattr(ev, "taa_render_samples"):
        ev.taa_render_samples = 64
    if hasattr(ev, "use_raytracing"):
        ev.use_raytracing = True
    if hasattr(ev, "use_bloom"):
        ev.use_bloom = True

    scene.view_settings.view_transform = 'AgX'
    try:
        scene.view_settings.look = 'AgX - Medium High Contrast'
    except TypeError:
        # Some Blender builds expose 'Medium High Contrast' without the AgX prefix.
        try:
            scene.view_settings.look = 'Medium High Contrast'
        except TypeError:
            pass  # Leave at default; not fatal.


# -------------------- Helpers --------------------

def _add_cube_slab(name, sx, sy, sz, location, bevel=0.1, bevel_segs=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx / 2, sy / 2, sz / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.segments = bevel_segs
    bev.width = bevel
    bpy.ops.object.shade_smooth()
    return obj


def _add_glass_pill(name, sx, sy, sz, location, material, pill_factor=0.48):
    """Rounded-pill glass mesh. pill_factor controls how round."""
    obj = _add_cube_slab(name, sx, sy, sz, location,
                         bevel=min(sy, sz) * pill_factor, bevel_segs=10)
    obj.data.materials.append(material)
    return obj


def _add_sphere(name, radius, location, material):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location,
                                          segments=32, ring_count=16)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


def _add_plane(name, size, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    return obj


# -------------------- Scene build --------------------

def lane_z_positions(n_lanes: int) -> list[float]:
    if n_lanes <= 1:
        return [0.0]
    half = (n_lanes - 1) / 2.0
    spread = 2.2
    return [half * spread - i * spread for i in range(n_lanes)]


def beat_x_position(beat_index_visible: int, n_visible: int) -> float:
    """Distribute `n_visible` beats evenly across [BEAT_X_MIN, BEAT_X_MAX]."""
    if n_visible <= 0:
        return 0.0
    step = (BEAT_X_MAX - BEAT_X_MIN) / n_visible
    return BEAT_X_MIN + (beat_index_visible + 0.5) * step


def build_scene(descriptor: dict) -> dict:
    """Build the 3D scene from a descriptor. Returns references to key objects
    (the caller will keyframe these in animation.py)."""
    reset_scene()
    configure_render()

    lanes = descriptor["lanes"]
    beats = descriptor["beats"]

    lane_z = {lane: z for lane, z in zip(lanes, lane_z_positions(len(lanes)))}

    # World env — neutral warm for glass reflections.
    scene = bpy.context.scene
    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    wnt = world.node_tree
    wnt.nodes.clear()
    wout = wnt.nodes.new("ShaderNodeOutputWorld")
    wbg = wnt.nodes.new("ShaderNodeBackground")
    wbg.inputs["Color"].default_value = (0.97, 0.95, 0.92, 1.0)
    wbg.inputs["Strength"].default_value = 0.9
    wnt.links.new(wbg.outputs[0], wout.inputs[0])

    # Backdrop — large plane behind everything.
    backdrop = _add_plane("Backdrop", size=80, location=(0, 18, 0),
                          rotation=(math.radians(90), 0, 0))
    bmat = M.iridescent_backdrop_material("BackdropMat")
    backdrop.data.materials.append(bmat)

    # Lanes
    lane_mat = M.matte_lane_material("LaneMat")
    lane_objects = {}
    for lane, z in lane_z.items():
        slab = _add_cube_slab(f"Lane_{lane}", sx=9.0, sy=0.25, sz=0.35,
                              location=(0, 0, z), bevel=0.1)
        slab.data.materials.append(lane_mat)
        lane_objects[lane] = slab

    # Commands panel — big glass pill above top lane.
    commands_mat = M.glass_material("CommandsMat")
    commands = _add_glass_pill(
        "Commands", sx=7.5, sy=0.5, sz=2.4,
        location=(0, -0.2, COMMANDS_Z), material=commands_mat,
        pill_factor=0.42)

    # Lane label glass pills on the left of each lane.
    label_objs = {}
    for lane, z in lane_z.items():
        mat = M.pill_label_material(f"LabelMat_{lane}")
        p = _add_glass_pill(f"Label_{lane}", sx=2.0, sy=0.35, sz=0.55,
                            location=(-4.0, -0.3, z), material=mat,
                            pill_factor=0.48)
        label_objs[lane] = p

    # Caption panel — below bottom lane.
    caption_mat = M.glass_material("CaptionMat")
    caption = _add_glass_pill(
        "Caption", sx=7.2, sy=0.45, sz=1.6,
        location=(0, -0.2, CAPTION_Z), material=caption_mat,
        pill_factor=0.48)

    # Electron — emissive sphere. Start at first beat's location (set later
    # by animation.py via keyframes).
    electron_mat = M.emission_material("ElectronMat", color=(0.45, 0.85, 1.0),
                                        strength=80.0)
    # Initial location: top lane, leftmost x. Animation keyframes take over.
    electron_start_x = BEAT_X_MIN
    electron_start_z = lane_z[lanes[0]]
    electron = _add_sphere("Electron", radius=0.22,
                            location=(electron_start_x, -0.9, electron_start_z),
                            material=electron_mat)

    # Lighting
    bpy.ops.object.light_add(type='AREA', location=(3, -6, 6))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.size = 6
    key.data.energy = 1800
    key.data.color = (1.0, 0.95, 0.88)
    key.rotation_euler = (math.radians(55), 0, math.radians(20))

    bpy.ops.object.light_add(type='AREA', location=(-4, -5, -1))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.size = 5
    fill.data.energy = 500
    fill.data.color = (0.82, 0.9, 1.0)
    fill.rotation_euler = (math.radians(75), 0, math.radians(-35))

    bpy.ops.object.light_add(type='AREA', location=(0, 8, 4))
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.size = 8
    rim.data.energy = 700
    rim.data.color = (0.95, 0.88, 1.0)
    rim.rotation_euler = (math.radians(-60), 0, 0)

    # Camera.
    bpy.ops.object.camera_add(location=(1.5, -15.0, 0.8))
    cam = bpy.context.active_object
    cam.name = "MainCam"
    target = Vector((0.0, 0.0, 0.5))
    direction = target - cam.location
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = direction.to_track_quat('-Z', 'Y')
    cam.rotation_mode = 'XYZ'
    cam.data.lens = 42
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 15.0
    cam.data.dof.aperture_fstop = 4.5
    scene.camera = cam

    return {
        "backdrop": backdrop,
        "backdrop_mat": bmat,
        "lanes": lane_objects,
        "lane_z": lane_z,
        "commands": commands,
        "caption": caption,
        "labels": label_objs,
        "electron": electron,
        "camera": cam,
    }
