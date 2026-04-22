"""Material library for the production Blender pipeline.

Produces:
    glass_material            — Thin-film iridescent refractive glass
    frosted_glass_material    — Same but rougher, for backdrop blobs
    liquid_blob_material      — Soft translucent pastel blob for backdrop
    emission_material         — Generic emissive (electron, trail, accents)
    matte_lane_material       — Thin lane slab
    text_material             — Near-white with subtle emission so text reads
    text_material_dark        — Dark gray text for on-glass labels
    step_number_material      — Amber emissive glass for step badges
    arrow_pulse_material      — Cylinder emission with animated scrolling pulse
    white_shell_material      — Opaque white + subtle emission (fallback)

All Blender 5 / Eevee Next compatible.
"""
import math
import bpy


# -------------------- internals --------------------

def _new_mat(name: str) -> bpy.types.Material:
    if name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[name])
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    return m


def _set_input(node, name: str, value) -> bool:
    if name in node.inputs:
        node.inputs[name].default_value = value
        return True
    return False


def _mark_glass(mat: bpy.types.Material, blended: bool = True) -> None:
    """Flag a material for refractive glass rendering in Eevee Next.

    Note: `BLENDED` mode is required for true refraction but breaks depth-
    sorting against opaque objects behind it — when you have opaque tiles
    stacked with glass, pass blended=False to use `DITHERED` which preserves
    z-ordering at the cost of a slight grainy look on refractive edges.
    """
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = 'BLENDED' if blended else 'DITHERED'
    if hasattr(mat, "use_screen_refraction"):
        mat.use_screen_refraction = True
    if hasattr(mat, "use_raytrace_refraction"):
        mat.use_raytrace_refraction = True
    if hasattr(mat, "blend_method"):
        # Blender 4.x fallback
        try:
            mat.blend_method = 'HASHED' if not blended else 'BLEND'
        except TypeError:
            pass


# -------------------- Glass (thin-film iridescent) --------------------

def glass_material(name: str,
                   tint=(0.97, 0.98, 1.0, 1.0),
                   roughness: float = 0.03,
                   ior: float = 1.45,
                   coat: float = 0.45,
                   thin_film_nm: float = 520.0,
                   thin_film_ior: float = 1.33,
                   blended: bool = True) -> bpy.types.Material:
    """Clear refractive glass with a thin-film layer → subtle Apple iridescence.

    thin_film_nm in nanometers controls which wavelength interferes — 400-700 is
    the visible range. 520 gives a neutral rainbow sheen shifted slightly green.
    """
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    _set_input(bsdf, "Base Color", tint)
    _set_input(bsdf, "Roughness", roughness)
    _set_input(bsdf, "IOR", ior)
    # Blender 5 renamed transmission input; try both.
    if not _set_input(bsdf, "Transmission Weight", 1.0):
        _set_input(bsdf, "Transmission", 1.0)
    _set_input(bsdf, "Coat Weight", coat)
    _set_input(bsdf, "Coat Roughness", 0.05)
    _set_input(bsdf, "Coat IOR", 1.6)
    # Thin-film (Blender 4.0+ / 5.x). Silently skipped on earlier builds.
    _set_input(bsdf, "Thin Film Thickness", thin_film_nm)
    _set_input(bsdf, "Thin Film IOR", thin_film_ior)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    _mark_glass(mat, blended=blended)
    return mat


def frosted_glass_material(name: str,
                            tint=(0.96, 0.97, 1.0, 1.0),
                            roughness: float = 0.22) -> bpy.types.Material:
    return glass_material(name, tint=tint, roughness=roughness,
                          coat=0.25, thin_film_nm=480.0)


# -------------------- Liquid-glass backdrop blobs --------------------

def liquid_blob_material(name: str, color=(1.0, 0.85, 0.78)) -> bpy.types.Material:
    """Soft pastel blob for layered moving background — opaque enough to
    read as a distinct colored shape against the white world, with a mild
    emission so it self-illuminates.
    """
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (600, 0)

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", (*color, 1.0))
    _set_input(bsdf, "Roughness", 0.22)
    _set_input(bsdf, "Metallic", 0.0)
    _set_input(bsdf, "IOR", 1.3)
    # Emission gives the blob its glow — strong so the pastel reads against
    # the white world + bloom pass.
    _set_input(bsdf, "Emission Color", (*color, 1.0))
    _set_input(bsdf, "Emission Strength", 6.5)
    _set_input(bsdf, "Coat Weight", 0.35)
    _set_input(bsdf, "Coat Roughness", 0.1)
    _set_input(bsdf, "Coat IOR", 1.55)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


# -------------------- Emission (electron, trail, accents) --------------------

def emission_material(name: str,
                      color=(0.45, 0.80, 1.0),
                      strength: float = 80.0) -> bpy.types.Material:
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    em = nt.nodes.new("ShaderNodeEmission")
    em.location = (50, 0)
    em.inputs["Color"].default_value = (*color, 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return mat


# -------------------- Text --------------------

def text_material(name: str,
                  color=(0.08, 0.09, 0.12, 1.0),
                  emission_strength: float = 0.0) -> bpy.types.Material:
    """Default text material — dark, near-black, slight sheen. Used for text on
    light backgrounds (lane labels, caption, commands title).
    """
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", color)
    _set_input(bsdf, "Roughness", 0.42)
    _set_input(bsdf, "Metallic", 0.0)
    if emission_strength > 0:
        _set_input(bsdf, "Emission Color", (color[0], color[1], color[2], 1.0))
        _set_input(bsdf, "Emission Strength", emission_strength)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def text_material_white(name: str,
                         emission_strength: float = 2.0) -> bpy.types.Material:
    """Bright white text used on darker pills (commands panel row tiles)."""
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    em = nt.nodes.new("ShaderNodeEmission")
    em.location = (50, 0)
    em.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    em.inputs["Strength"].default_value = emission_strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return mat


def text_material_accent(name: str,
                          color=(0.12, 0.45, 0.95)) -> bpy.types.Material:
    """Accent blue text (e.g., SF accent blue for the commands title)."""
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", (*color, 1.0))
    _set_input(bsdf, "Roughness", 0.35)
    _set_input(bsdf, "Metallic", 0.1)
    _set_input(bsdf, "Emission Color", (*color, 1.0))
    _set_input(bsdf, "Emission Strength", 1.2)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


# -------------------- Matte lane slab --------------------

def matte_lane_material(name: str) -> bpy.types.Material:
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (50, 0)
    _set_input(bsdf, "Base Color", (0.12, 0.14, 0.18, 1.0))
    _set_input(bsdf, "Roughness", 0.48)
    _set_input(bsdf, "Metallic", 0.15)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def lane_line_material(name: str) -> bpy.types.Material:
    """Apple-style hairline: subtle dark gray translucent line."""
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    _set_input(bsdf, "Base Color", (0.22, 0.24, 0.28, 1.0))
    _set_input(bsdf, "Roughness", 0.55)
    _set_input(bsdf, "Metallic", 0.05)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


# -------------------- Step number amber badge --------------------

def step_number_material(name: str,
                          color=(1.0, 0.62, 0.18)) -> bpy.types.Material:
    """Amber emissive badge background — like an iOS notification dot."""
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", (*color, 1.0))
    _set_input(bsdf, "Roughness", 0.18)
    _set_input(bsdf, "Metallic", 0.1)
    _set_input(bsdf, "Emission Color", (*color, 1.0))
    _set_input(bsdf, "Emission Strength", 6.0)
    _set_input(bsdf, "Coat Weight", 0.3)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


# -------------------- Flow-arrow pulse shader --------------------

def arrow_pulse_material(name: str,
                          color=(0.4, 0.78, 1.0),
                          strength: float = 14.0) -> bpy.types.Material:
    """Emissive material with a wave-texture pulse that scrolls along the arrow.

    The arrow cylinder is assumed to have its Z axis along the flow direction
    (created by aligning a cylinder between two points). The wave reads
    generated coordinates to produce a scrolling bright band.

    Animation hook: keyframe node_tree.nodes['PulseMapping'].inputs['Location']
    default_value[2] from 0 → 1 over the beat duration to slide the pulse.
    """
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (800, 0)

    tc = nt.nodes.new("ShaderNodeTexCoord")
    tc.location = (-800, 0)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.name = "PulseMapping"
    mapping.location = (-550, 0)
    # Initial offset — animation will keyframe this to scroll.
    mapping.inputs["Location"].default_value[2] = 0.0

    wave = nt.nodes.new("ShaderNodeTexWave")
    wave.location = (-300, 0)
    wave.wave_type = "BANDS"
    wave.bands_direction = "Z"
    wave.inputs["Scale"].default_value = 1.0
    wave.inputs["Distortion"].default_value = 0.0
    wave.inputs["Detail"].default_value = 0.0

    # Map the wave through a ramp for a narrow bright band.
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-50, 0)
    cr = ramp.color_ramp
    cr.elements[0].position = 0.35
    cr.elements[0].color = (0.05, 0.12, 0.22, 1.0)
    cr.elements[1].position = 0.52
    cr.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    e2 = cr.elements.new(0.68)
    e2.color = (0.05, 0.12, 0.22, 1.0)

    em = nt.nodes.new("ShaderNodeEmission")
    em.location = (300, 0)
    em.inputs["Color"].default_value = (*color, 1.0)
    em.inputs["Strength"].default_value = strength

    mult = nt.nodes.new("ShaderNodeMath")
    mult.operation = "MULTIPLY"
    mult.location = (500, 0)

    # Base emission always on at low level, pulse boosts it.
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], wave.inputs["Vector"])
    nt.links.new(wave.outputs["Color"], ramp.inputs["Fac"])
    # Drive emission strength by (base + pulse*ramp) — keep background faint.
    ramp_to_val = nt.nodes.new("ShaderNodeRGBToBW")
    ramp_to_val.location = (150, -150)
    nt.links.new(ramp.outputs["Color"], ramp_to_val.inputs["Color"])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    add.location = (350, -150)
    add.inputs[1].default_value = 0.20  # base baseline glow
    nt.links.new(ramp_to_val.outputs["Val"], add.inputs[0])
    nt.links.new(add.outputs[0], mult.inputs[0])
    mult.inputs[1].default_value = strength
    # Final emission:
    em2 = nt.nodes.new("ShaderNodeEmission")
    em2.location = (650, 0)
    em2.inputs["Color"].default_value = (*color, 1.0)
    nt.links.new(mult.outputs[0], em2.inputs["Strength"])
    nt.links.new(em2.outputs[0], out.inputs[0])
    return mat


# -------------------- Commands-panel UI tiles --------------------

def ui_tile_material(name: str,
                      tint=(0.88, 0.91, 0.96, 1.0),
                      roughness: float = 0.22,
                      coat: float = 0.45) -> bpy.types.Material:
    """Opaque UI tile for keycaps / text_input / command backgrounds.

    Opaque so the tile is distinct against the white world + glass commands
    pill. A cool-gray tint + coat gives it the Apple keycap/text-field feel
    without the read-through of real glass.
    """
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", tint)
    _set_input(bsdf, "Roughness", roughness)
    _set_input(bsdf, "Metallic", 0.05)
    _set_input(bsdf, "Coat Weight", coat)
    _set_input(bsdf, "Coat Roughness", 0.1)
    _set_input(bsdf, "Coat IOR", 1.5)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def ui_tile_dark_material(name: str) -> bpy.types.Material:
    """Dark variant for terminal-style command pills."""
    return ui_tile_material(name, tint=(0.10, 0.12, 0.16, 1.0),
                             roughness=0.3, coat=0.3)


# -------------------- White opaque (accent shells) --------------------

def white_shell_material(name: str,
                          emission_strength: float = 0.6) -> bpy.types.Material:
    mat = _new_mat(name)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    _set_input(bsdf, "Base Color", (0.99, 0.99, 1.0, 1.0))
    _set_input(bsdf, "Roughness", 0.25)
    _set_input(bsdf, "Metallic", 0.0)
    _set_input(bsdf, "Emission Color", (1.0, 1.0, 1.0, 1.0))
    _set_input(bsdf, "Emission Strength", emission_strength)
    _set_input(bsdf, "Coat Weight", 0.4)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat
