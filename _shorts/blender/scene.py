"""3D scene builder — production-quality UML sequence flow.

World convention:
    +X right, +Z up, +Y into scene (away from camera)
    Camera sits at -Y looking toward +Y

Aesthetic targets:
    - Pure white world base
    - Layered translucent "liquid glass" blobs drifting in the deep background
    - Thin-film iridescent glass panels (commands + caption + lane labels)
    - Hairline lanes with clear lane-label pills on the left
    - Amber step-number badges on each beat
    - Emissive electron w/ trail
    - Emissive flow arrows with scrolling pulse per beat
    - Commands panel with 3D keycap / text / command tiles per beat
"""
import math

import bpy
from mathutils import Vector

from . import materials as M
from . import text as T
from . import arrows as A
from . import input_display as IDisp


# -------------------- Render / canvas --------------------

CANVAS_W = 1080
CANVAS_H = 1920
FPS = 30

# -------------------- Layout --------------------

# Lane z-spread — farther apart reads more clearly as a UML sequence.
LANE_SPREAD = 2.2
# Beat x range tightened so all beats + lane labels fit in the camera FOV
# with zero horizontal follow. Nothing should EVER clip out of frame.
BEAT_X_MIN = -3.1
BEAT_X_MAX = 3.1

COMMANDS_Z = 5.8
COMMANDS_TITLE_Z = COMMANDS_Z + 1.10
COMMANDS_SUBTITLE_Z = COMMANDS_Z + 0.55
# Input display sits below the subtitle — lower half of the commands pill.
COMMANDS_INPUT_Z = COMMANDS_Z - 0.95
CAPTION_Z = -5.3

Y_FRONT = -0.9       # electron + arrows pop just in front of lane plane
Y_LANE = 0.0
Y_BACKDROP = 22.0    # deep background for blobs


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
    scene.render.film_transparent = False

    ev = scene.eevee
    # Env var override for fast smoke tests: BLENDER_TAA_SAMPLES=16 runs quick.
    import os as _os
    _samples = int(_os.environ.get("BLENDER_TAA_SAMPLES", "128"))
    if hasattr(ev, "taa_render_samples"):
        ev.taa_render_samples = _samples
    if hasattr(ev, "use_raytracing"):
        ev.use_raytracing = True
    # Bloom is replaced in Eevee Next by compositor glare; set up below.
    if hasattr(ev, "use_bloom"):
        ev.use_bloom = True
    if hasattr(ev, "bloom_intensity"):
        ev.bloom_intensity = 0.08

    # Color management — AgX with Base Contrast look. Keeps pastels visible
    # while tone-mapping HDR emission (step badges, electron, arrow pulses)
    # so they bloom instead of clipping to white. Standard view clipped all
    # the amber/blue emissive accents to pure white.
    try:
        scene.view_settings.view_transform = 'AgX'
    except TypeError:
        pass
    for look in ("AgX - Base Contrast", "AgX - Medium High Contrast",
                 "Base Contrast", "None"):
        try:
            scene.view_settings.look = look
            break
        except TypeError:
            continue
    try:
        scene.view_settings.exposure = 0.3   # slight lift so pastels pop
        scene.view_settings.gamma = 1.0
    except (AttributeError, TypeError):
        pass

    _setup_compositor_bloom()


def _setup_compositor_bloom():
    """Enable compositor → Render Layers → Glare → Composite for a soft bloom.

    Works on Blender 4.x (scene.node_tree) and Blender 5.x (scene.compositing_node_group).
    Silent no-op if the compositor API isn't available.
    """
    scene = bpy.context.scene
    try:
        scene.use_nodes = True
    except AttributeError:
        pass

    nt = None
    # Blender 4.x path
    nt = getattr(scene, "node_tree", None)
    if nt is None:
        # Blender 5.x path — new compositing system.
        nt = getattr(scene, "compositing_node_group", None)
    if nt is None:
        # Try to create a fresh compositing node group on Blender 5.
        try:
            ng = bpy.data.node_groups.new("SceneComposite", "CompositorNodeTree")
            scene.compositing_node_group = ng
            nt = ng
        except Exception:
            return  # no compositor available; skip bloom entirely

    try:
        nt.nodes.clear()
        rl = nt.nodes.new("CompositorNodeRLayers")
        rl.location = (-400, 0)
        glare = nt.nodes.new("CompositorNodeGlare")
        glare.location = (0, 0)
        # Discover which enum attribute Blender exposes — 'glare_type' on 4.x,
        # renamed to 'type' or similar on 5.x. Walk properties.
        type_attr = None
        for candidate in ("glare_type", "type"):
            if candidate in glare.bl_rna.properties:
                type_attr = candidate
                break
        if type_attr is not None:
            prop = glare.bl_rna.properties[type_attr]
            # enum_items only on EnumProperty. StringProperty on Blender 5+.
            enum_items = set()
            try:
                enum_items = {item.identifier for item in prop.enum_items}
            except AttributeError:
                pass
            if enum_items:
                value = 'BLOOM' if 'BLOOM' in enum_items else (
                    'FOG_GLOW' if 'FOG_GLOW' in enum_items
                    else next(iter(enum_items), None))
            else:
                value = 'BLOOM'  # string-typed: try a sensible default
            if value is not None:
                try:
                    setattr(glare, type_attr, value)
                except (TypeError, AttributeError):
                    pass
        for attr, val in (("quality", 'HIGH'), ("mix", -0.75),
                          ("threshold", 0.85), ("size", 7)):
            try:
                setattr(glare, attr, val)
            except (AttributeError, TypeError):
                pass
        comp = nt.nodes.new("CompositorNodeComposite")
        comp.location = (400, 0)
        nt.links.new(rl.outputs["Image"], glare.inputs["Image"])
        nt.links.new(glare.outputs["Image"], comp.inputs["Image"])
    except Exception as e:
        print(f"[scene] compositor bloom skipped: {e}")


# -------------------- Primitives --------------------

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


def _add_glass_pill(name, sx, sy, sz, location, material, pill_factor=0.48,
                     segments=10):
    obj = _add_cube_slab(name, sx, sy, sz, location,
                         bevel=min(sy, sz) * pill_factor,
                         bevel_segs=segments)
    obj.data.materials.append(material)
    return obj


def _add_sphere(name, radius, location, material, segments=48, rings=24):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location,
                                          segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


def _add_plane(name, size, location, rotation=(0, 0, 0), material=None):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    if material:
        obj.data.materials.append(material)
    return obj


# -------------------- Lane layout --------------------

def lane_z_positions(n_lanes: int) -> list[float]:
    if n_lanes <= 1:
        return [0.0]
    half = (n_lanes - 1) / 2.0
    return [half * LANE_SPREAD - i * LANE_SPREAD for i in range(n_lanes)]


def beat_x_position(idx: int, total: int) -> float:
    if total <= 0:
        return 0.0
    step = (BEAT_X_MAX - BEAT_X_MIN) / total
    return BEAT_X_MIN + step * (idx + 0.5)


# -------------------- World + backdrop --------------------

def _build_world(scene):
    world = bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs[0], out.inputs[0])


def _build_flowing_backdrop():
    """Large plane with a shader-driven aurora of layered pastel color waves.

    This IS the "layered liquid glass slowly moving background" — four
    slow-moving noise fields (peach / mint / lilac / sky) blended through
    color ramps produce soft flowing colored regions against a white base.
    Animation.py drives the Mapping nodes so the whole field flows over the
    duration of the short.

    Returns (plane_obj, material) so animation.py can drive the mapping.
    """
    plane = _add_plane("Backdrop", size=120,
                        location=(0, Y_BACKDROP, 0),
                        rotation=(math.radians(90), 0, 0))
    mat = M.flowing_aurora_backdrop_material("BackdropAuroraMat")
    plane.data.materials.append(mat)
    return plane, mat


# -------------------- Scene build --------------------

def build_scene(descriptor: dict) -> dict:
    """Build the whole 3D scene. Returns a dict of references animation.py
    needs to keyframe."""
    reset_scene()
    configure_render()

    lanes = descriptor["lanes"]
    beats = descriptor["beats"]
    lesson_title = descriptor.get("lesson_title", "")
    day_number = descriptor.get("day_number", 0)
    learning_title = descriptor.get("learning_title", "")

    lane_z = {lane: z for lane, z in zip(lanes, lane_z_positions(len(lanes)))}

    scene = bpy.context.scene
    _build_world(scene)

    backdrop, backdrop_mat = _build_flowing_backdrop()

    # -------- Lanes — thin slabs, legible from camera distance --------
    lane_line_mat = M.lane_line_material("LaneLineMat")
    lane_objects = {}
    for lane, z in lane_z.items():
        line = _add_cube_slab(
            f"Lane_{lane}", sx=7.2, sy=0.12, sz=0.09,
            location=(0.3, Y_LANE, z), bevel=0.03, bevel_segs=3)
        line.data.materials.append(lane_line_mat)
        lane_objects[lane] = line

    # -------- Commands panel --------
    # DITHERED instead of BLENDED so opaque keycap tiles in front of the pill
    # sort correctly against the glass (BLENDED breaks z-ordering in Eevee Next).
    commands_mat = M.glass_material(
        "CommandsMat",
        tint=(0.98, 0.99, 1.0, 1.0),
        roughness=0.06,
        thin_film_nm=540.0,
        blended=False)
    commands = _add_glass_pill(
        "Commands", sx=8.4, sy=0.55, sz=2.8,
        location=(0, -0.25, COMMANDS_Z), material=commands_mat,
        pill_factor=0.42)

    # -------- Commands title + subtitle --------
    text_dark = M.text_material("TextDark", color=(0.08, 0.10, 0.14, 1.0))
    text_accent = M.text_material_accent("TextAccent",
                                          color=(0.12, 0.45, 0.95))
    text_subtle = M.text_material("TextSubtle",
                                    color=(0.35, 0.38, 0.44, 1.0))

    title_body = lesson_title if lesson_title else "Lesson"
    title = T.make_text(
        "CommandsTitle",
        body=title_body,
        location=(0, -0.55, COMMANDS_TITLE_Z),
        size=0.75,
        extrude=0.02,
        bevel=0.005,
        font_path=T.FONT_SEMIBOLD,
        material=text_dark)

    subtitle_body = f"Day {day_number} · {learning_title}" if learning_title \
        else f"Day {day_number}"
    subtitle = T.make_text(
        "CommandsSubtitle",
        body=subtitle_body,
        location=(0, -0.55, COMMANDS_SUBTITLE_Z),
        size=0.40,
        extrude=0.014,
        bevel=0.003,
        font_path=T.FONT_SEMIBOLD,
        material=text_accent)

    # -------- Lane labels --------
    label_glass_mat = M.glass_material(
        "LabelGlassMat",
        tint=(0.96, 0.98, 1.0, 1.0),
        roughness=0.10,
        coat=0.4,
        thin_film_nm=500.0,
        blended=False)
    label_objs = {}
    label_texts = {}
    LABEL_X = -3.55  # moved inward so the label never clips at frame edge
    for lane, z in lane_z.items():
        pill = _add_glass_pill(
            f"Label_{lane}", sx=1.9, sy=0.4, sz=0.6,
            location=(LABEL_X, -0.3, z), material=label_glass_mat,
            pill_factor=0.48)
        label_objs[lane] = pill
        # Text on front face of pill.
        txt = T.make_text(
            f"LabelTxt_{lane}",
            body=lane,
            location=(LABEL_X, -0.52, z),
            size=0.36,
            extrude=0.014,
            bevel=0.003,
            font_path=T.FONT_SEMIBOLD,
            material=text_dark)
        label_texts[lane] = txt

    # -------- Caption panel --------
    caption_mat = M.glass_material(
        "CaptionMat",
        tint=(0.97, 0.99, 1.0, 1.0),
        roughness=0.09,
        thin_film_nm=560.0,
        blended=False)
    caption = _add_glass_pill(
        "Caption", sx=7.4, sy=0.45, sz=1.4,
        location=(0, -0.25, CAPTION_Z), material=caption_mat,
        pill_factor=0.48)

    # Per-beat caption texts — all in the same screen position, visibility
    # keyframed per-beat.
    caption_texts: list[bpy.types.Object] = []
    for i, b in enumerate(beats):
        label = b.get("label") or ""
        if not label and b.get("kind") == "open":
            # Intro beat: caption shows the to_lane as the starting point.
            label = f"start at {b.get('to_lane', '')}"
        ct = T.make_text(
            f"Caption_{i}",
            body=label,
            location=(0, -0.5, CAPTION_Z),
            size=0.58,
            extrude=0.015,
            bevel=0.003,
            font_path=T.FONT_SEMIBOLD,
            material=text_dark)
        # Start hidden — animation.py toggles visibility.
        ct.hide_viewport = True
        ct.hide_render = True
        caption_texts.append(ct)

    # -------- Electron --------
    electron_mat = M.emission_material(
        "ElectronMat", color=(0.42, 0.78, 1.0), strength=120.0)
    electron_start_x = BEAT_X_MIN
    electron_start_z = lane_z[lanes[0]]
    electron = _add_sphere(
        "Electron", radius=0.26,
        location=(electron_start_x, Y_FRONT, electron_start_z),
        material=electron_mat)

    # Electron halo — larger, softer emission for bloom.
    halo_mat = M.emission_material(
        "ElectronHalo", color=(0.48, 0.82, 1.0), strength=22.0)
    halo = _add_sphere(
        "ElectronHalo", radius=0.52,
        location=(electron_start_x, Y_FRONT, electron_start_z),
        material=halo_mat, segments=24, rings=12)

    # -------- Electron trail (small spheres, fade via hide keyframes) --------
    trail_mat = M.emission_material(
        "ElectronTrail", color=(0.42, 0.78, 1.0), strength=35.0)
    trail_orbs: list[bpy.types.Object] = []
    TRAIL_COUNT = 8
    for k in range(TRAIL_COUNT):
        r = 0.14 - k * 0.011
        ob = _add_sphere(
            f"Trail_{k}", radius=max(0.03, r),
            location=(electron_start_x, Y_FRONT, electron_start_z),
            material=trail_mat, segments=16, rings=8)
        ob.hide_viewport = True
        ob.hide_render = True
        trail_orbs.append(ob)

    # -------- Step number badges --------
    step_mat = M.step_number_material(
        "StepMat", color=(1.0, 0.64, 0.2))
    # Step numbers: pure white with subtle emission so they pop on the amber
    # badge even with bloom.
    text_amber = M.text_material_white("StepNumTxtMat", emission_strength=3.2)
    step_badges: list[bpy.types.Object] = []
    visible_beats = [b for b in beats if b.get("kind") != "open"]
    n_visible = len(visible_beats)
    for i, b in enumerate(beats):
        if b.get("kind") == "open":
            step_badges.append(None)
            continue
        # Choose Z slightly above the top lane to keep badges out of the flow.
        top_lane_z = max(lane_z.values())
        badge_z = top_lane_z + 1.15
        # world_x assigned later in assign_beat_positions, but we need it now.
        # Replicate that math:
        vi = visible_beats.index(b)
        bx = beat_x_position(vi, n_visible)
        b["world_x_preview"] = bx

        # Flat circle-ish badge (cylinder flipped thin).
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.42, depth=0.16,
            vertices=32, location=(bx, Y_FRONT + 0.1, badge_z))
        badge = bpy.context.active_object
        badge.name = f"StepBadge_{i}"
        badge.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.shade_smooth()
        badge.data.materials.append(step_mat)

        num_txt = T.make_text(
            f"StepNum_{i}",
            body=str(vi + 1),
            location=(bx, Y_FRONT - 0.04, badge_z),
            size=0.34, extrude=0.008, bevel=0.002,
            font_path=T.FONT_BOLD,
            material=text_amber)

        # Parent text to badge for easy handling — preserve world transform.
        num_txt.parent = badge
        num_txt.matrix_parent_inverse = badge.matrix_world.inverted()
        # Start hidden.
        badge.hide_viewport = True
        badge.hide_render = True
        num_txt.hide_viewport = True
        num_txt.hide_render = True
        step_badges.append({"badge": badge, "num": num_txt})

    # -------- Arrows (call/return beats) --------
    arrow_objects: list = []  # parallel to beats; None for open/self
    for i, b in enumerate(beats):
        kind = b.get("kind")
        if kind not in ("call", "return"):
            arrow_objects.append(None)
            continue
        vi = visible_beats.index(b)
        bx = beat_x_position(vi, n_visible)
        z_from = lane_z[b["from_lane"]]
        z_to = lane_z[b["to_lane"]]
        arrow_mat = M.arrow_pulse_material(
            f"ArrowMat_{i}", color=(0.4, 0.78, 1.0), strength=24.0)
        arrow = A.build_arrow(
            f"Arrow_{i}",
            from_pos=(bx, Y_FRONT + 0.05, z_from),
            to_pos=(bx, Y_FRONT + 0.05, z_to),
            material=arrow_mat)
        # Start hidden — animation.py reveals per beat.
        arrow["shaft"].hide_viewport = True
        arrow["shaft"].hide_render = True
        arrow["head"].hide_viewport = True
        arrow["head"].hide_render = True
        arrow_objects.append(arrow)

    # -------- Input-display materials (shared) --------
    # Opaque tile (not glass) so the small UI pills read clearly against the
    # big glass commands pill + white world.
    key_glass_mat = M.ui_tile_material(
        "KeyTileMat", tint=(0.93, 0.95, 1.0, 1.0))
    pill_glass_mat = M.ui_tile_material(
        "PillTileMat", tint=(0.91, 0.94, 0.99, 1.0))
    pill_dark_mat = M.ui_tile_dark_material("PillDarkMat")
    text_white_mat = M.text_material_white("TextWhite", emission_strength=2.4)

    disp_mats = {
        "key_glass": key_glass_mat,
        "pill_glass": pill_glass_mat,
        "pill_dark": pill_dark_mat,
        "text_dark": text_dark,
        "text_white": text_white_mat,
        "text_accent": text_accent,
        "text_platform": text_subtle,
    }

    # Commands-panel inputs — one per beat (empty if no spec).
    display_objects: list = []
    for i, b in enumerate(beats):
        spec = b.get("input_display")
        disp = IDisp.build_for_beat(spec, panel_center_z=COMMANDS_INPUT_Z,
                                     mats=disp_mats)
        display_objects.append(disp)
        if disp is not None:
            disp.hide_viewport = True
            disp.hide_render = True
            for child in IDisp._descendants(disp):
                child.hide_viewport = True
                child.hide_render = True

    # -------- Lighting --------
    _build_lighting()

    # -------- Camera --------
    cam = _build_camera()

    return {
        "backdrop": backdrop,
        "backdrop_mat": backdrop_mat,
        "lanes": lane_objects,
        "lane_z": lane_z,
        "commands": commands,
        "commands_title": title,
        "commands_subtitle": subtitle,
        "caption": caption,
        "caption_texts": caption_texts,
        "labels": label_objs,
        "label_texts": label_texts,
        "electron": electron,
        "electron_halo": halo,
        "trail_orbs": trail_orbs,
        "step_badges": step_badges,
        "arrow_objects": arrow_objects,
        "display_objects": display_objects,
        "camera": cam,
    }


# -------------------- Lighting --------------------

def _build_lighting():
    # Soft Apple-ish key from upper-left.
    bpy.ops.object.light_add(type='AREA', location=(3.5, -6.5, 5.5))
    key = bpy.context.active_object
    key.name = "KeyLight"
    key.data.size = 7
    key.data.energy = 2100
    key.data.color = (1.0, 0.96, 0.92)
    key.rotation_euler = (math.radians(55), 0, math.radians(25))

    # Cool fill from lower-right behind lane.
    bpy.ops.object.light_add(type='AREA', location=(-4.5, -4.5, -1.5))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.size = 6
    fill.data.energy = 700
    fill.data.color = (0.82, 0.90, 1.0)
    fill.rotation_euler = (math.radians(75), 0, math.radians(-30))

    # Warm rim from behind to pop glass edges.
    bpy.ops.object.light_add(type='AREA', location=(0, 11, 3))
    rim = bpy.context.active_object
    rim.name = "RimLight"
    rim.data.size = 10
    rim.data.energy = 900
    rim.data.color = (1.0, 0.92, 0.82)
    rim.rotation_euler = (math.radians(-65), 0, 0)

    # Soft top from directly above for the commands panel surface highlight.
    bpy.ops.object.light_add(type='AREA', location=(0, -2, 9))
    top = bpy.context.active_object
    top.name = "TopLight"
    top.data.size = 6
    top.data.energy = 600
    top.data.color = (1.0, 1.0, 1.0)
    top.rotation_euler = (math.radians(0), 0, 0)


# -------------------- Camera --------------------

def _build_camera():
    bpy.ops.object.camera_add(location=(1.6, -14.5, 0.7))
    cam = bpy.context.active_object
    cam.name = "MainCam"
    target = Vector((0.0, 0.0, 0.4))
    direction = target - cam.location
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = direction.to_track_quat('-Z', 'Y')
    cam.rotation_mode = 'XYZ'
    cam.data.lens = 40
    cam.data.sensor_width = 36
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 14.8
    cam.data.dof.aperture_fstop = 4.0
    bpy.context.scene.camera = cam
    return cam
