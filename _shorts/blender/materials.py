"""Blender material library — Blender 5 (Eevee Next). Import inside Blender only.

Provides:
    glass_material(name, tint)             — Principled BSDF transmission glass
    iridescent_backdrop_material(name)     — Cream/pastel moving gradient
    emission_material(name, color, str)    — Emissive (electron, pulses)
    matte_lane_material(name)              — Dark matte slab for lanes
    pill_label_material(name, tint)        — Slightly frosted glass pill
"""
import math
import bpy


def _new_mat(name: str) -> bpy.types.Material:
    if name in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[name])
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m


def _clear(mat: bpy.types.Material) -> None:
    mat.node_tree.nodes.clear()


def _set_input(node, name: str, value) -> bool:
    """Set an input by name if it exists. Returns True on success."""
    if name in node.inputs:
        node.inputs[name].default_value = value
        return True
    return False


# ---------- Glass ----------

def glass_material(name: str, tint=(0.96, 0.98, 1.0, 1.0),
                   roughness: float = 0.02, ior: float = 1.45,
                   coat: float = 0.25) -> bpy.types.Material:
    """Clear glass with slight tint, high transmission, thin-film coat for a
    subtle rainbow sheen. Works in Eevee Next's raytracing mode."""
    mat = _new_mat(name)
    _clear(mat)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    _set_input(bsdf, "Base Color", tint)
    _set_input(bsdf, "Roughness", roughness)
    _set_input(bsdf, "IOR", ior)
    # Blender 5 uses "Transmission Weight". 4.x had "Transmission".
    if not _set_input(bsdf, "Transmission Weight", 1.0):
        _set_input(bsdf, "Transmission", 1.0)
    _set_input(bsdf, "Coat Weight", coat)
    _set_input(bsdf, "Coat Roughness", 0.06)
    _set_input(bsdf, "Coat IOR", 1.6)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    # Eevee — mark material as refractive/blended.
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = 'BLENDED'
    if hasattr(mat, "use_screen_refraction"):
        mat.use_screen_refraction = True
    if hasattr(mat, "use_raytrace_refraction"):
        mat.use_raytrace_refraction = True
    return mat


def pill_label_material(name: str, tint=(0.94, 0.96, 1.0, 1.0)) -> bpy.types.Material:
    """Mostly-clear but slightly frosted glass used for small labels so text
    on top reads without the pill disappearing into the backdrop."""
    return glass_material(name, tint=tint, roughness=0.08, ior=1.45, coat=0.35)


# ---------- Emission ----------

def emission_material(name: str, color=(0.45, 0.85, 1.0),
                      strength: float = 40.0) -> bpy.types.Material:
    mat = _new_mat(name)
    _clear(mat)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    em = nt.nodes.new("ShaderNodeEmission")
    em.location = (50, 0)
    em.inputs["Color"].default_value = (*color, 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return mat


# ---------- Iridescent backdrop ----------

def iridescent_backdrop_material(name: str) -> bpy.types.Material:
    """Cream base with a soft rotating pastel gradient. The rotation is
    animated per-frame via a driver on the Mapping node's Z rotation."""
    mat = _new_mat(name)
    _clear(mat)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)
    em = nt.nodes.new("ShaderNodeEmission")
    em.location = (700, 0)
    em.inputs["Strength"].default_value = 1.3
    tc = nt.nodes.new("ShaderNodeTexCoord")
    tc.location = (-800, 0)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.location = (-500, 0)
    mapping.name = "BackdropMapping"  # so animation.py can find it
    mapping.inputs["Rotation"].default_value[2] = math.radians(20)
    grad = nt.nodes.new("ShaderNodeTexGradient")
    grad.gradient_type = "LINEAR"
    grad.location = (-250, 0)
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (50, 0)
    # Cream -> peach -> mint -> lilac -> cream
    cr = ramp.color_ramp
    stops = [
        (0.00, (0.97, 0.94, 0.90, 1.0)),
        (0.25, (0.99, 0.88, 0.82, 1.0)),
        (0.50, (0.88, 0.96, 0.92, 1.0)),
        (0.75, (0.90, 0.88, 0.98, 1.0)),
        (1.00, (0.97, 0.94, 0.90, 1.0)),
    ]
    cr.elements[0].position = stops[0][0]
    cr.elements[0].color = stops[0][1]
    cr.elements[1].position = stops[-1][0]
    cr.elements[1].color = stops[-1][1]
    for p, c in stops[1:-1]:
        e = cr.elements.new(p)
        e.color = c
    nt.links.new(tc.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], grad.inputs["Vector"])
    nt.links.new(grad.outputs["Color"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs[0], out.inputs[0])
    return mat


# ---------- Matte lane slab ----------

def matte_lane_material(name: str) -> bpy.types.Material:
    mat = _new_mat(name)
    _clear(mat)
    nt = mat.node_tree
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    _set_input(bsdf, "Base Color", (0.08, 0.09, 0.12, 1.0))
    _set_input(bsdf, "Roughness", 0.55)
    _set_input(bsdf, "Metallic", 0.0)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return mat


def flow_arrow_material(name: str, color=(0.35, 0.78, 1.0),
                        strength: float = 20.0) -> bpy.types.Material:
    """Glowing tube for UML call/return arrows."""
    return emission_material(name, color=color, strength=strength)
