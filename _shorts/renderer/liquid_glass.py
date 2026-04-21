"""Liquid-glass panel rendering — Apple Liquid Glass approximation in pure PIL.

Implements the 9-layer recipe from the research pass:

    1. Crop backdrop under panel -> GaussianBlur(18) -> refraction base
    2. ImageEnhance.Color(1.7) on the blurred crop -> saturation punch
    3. Fake lensing: np.roll inward weighted by rim mask -> edge distortion
    4. Body tint (translucent white, cool variant)
    5. Vertical body gradient (top lighter)
    6. Inset rim highlight (bright 1.5px border, slightly blurred)
    7. Corner specular (TL + TR radial gradients)
    8. Outer drop shadow (y+6, blur 24)
    9. Ripple noise (optional tiled overlay for surface imperfection)

Budget ~25-40ms per panel at ~600x100. For a frame with 3 panels: ~100ms.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


# -------------------- Public radial / linear gradient helpers --------------------

def radial_gradient(size: tuple[int, int], inner: tuple[int, int, int],
                    outer: tuple[int, int, int],
                    center: tuple[float, float] | None = None,
                    falloff: float = 1.1) -> Image.Image:
    """Quick radial gradient (numpy-backed for speed)."""
    w, h = size
    if center is None:
        center = (0.5, 0.3)
    cx = center[0] * w
    cy = center[1] * h
    ys = np.arange(h, dtype=np.float32)[:, None]
    xs = np.arange(w, dtype=np.float32)[None, :]
    d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2)
    max_d = max(max(cx, w - cx), max(cy, h - cy)) * falloff
    t = np.clip(d / max_d, 0, 1)
    t = t * t * (3 - 2 * t)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for i, (a, b) in enumerate(zip(inner, outer)):
        arr[..., i] = a + (b - a) * t
    return Image.fromarray(arr.astype(np.uint8), mode="RGB")


def linear_gradient(size: tuple[int, int], c1: tuple[int, int, int],
                    c2: tuple[int, int, int], vertical: bool = True) -> Image.Image:
    w, h = size
    steps = h if vertical else w
    t = np.linspace(0, 1, steps, dtype=np.float32)
    arr = np.zeros((steps, 3), dtype=np.float32)
    for i, (a, b) in enumerate(zip(c1, c2)):
        arr[:, i] = a + (b - a) * t
    if vertical:
        arr = np.broadcast_to(arr[:, None, :], (h, w, 3))
    else:
        arr = np.broadcast_to(arr[None, :, :], (h, w, 3))
    return Image.fromarray(arr.astype(np.uint8), mode="RGB")


# -------------------- Ripple-noise tile --------------------

@lru_cache(maxsize=2)
def _ripple_tile(seed: int = 42) -> Image.Image:
    """Low-contrast 256x256 noise tile for the 'surface imperfection' layer."""
    rng = np.random.default_rng(seed)
    # Start small then upsample so we get blob-ish detail, not static TV snow.
    base = rng.random((32, 32)).astype(np.float32)
    img = Image.fromarray((base * 255).astype(np.uint8), mode="L")
    img = img.resize((256, 256), Image.BICUBIC)
    return img.filter(ImageFilter.GaussianBlur(1.5))


def _ripple_overlay(size: tuple[int, int], alpha: int = 10) -> Image.Image:
    """Tile the ripple texture over `size` at low alpha."""
    w, h = size
    tile = _ripple_tile()
    out = Image.new("L", (w, h), 0)
    tw, th = tile.size
    for y in range(0, h, th):
        for x in range(0, w, tw):
            out.paste(tile, (x, y))
    # Convert to RGBA with subtle tint.
    arr = np.asarray(out, dtype=np.float32) / 255.0
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., :3] = 255  # white
    rgba[..., 3] = (arr * alpha).astype(np.uint8)
    return Image.fromarray(rgba, mode="RGBA")


# -------------------- Rim / corner masks --------------------

def _rim_mask(size: tuple[int, int], radius: int, rim_px: int = 12) -> np.ndarray:
    """Float32 mask 0..1 where 1 is close to the rim of a rounded-rect, 0 is
    deep interior. Used to weight the fake-lensing displacement."""
    w, h = size
    # Distance-from-edge approximation for a rounded rect: min(x, w-1-x, y, h-1-y),
    # plus corner correction.
    ys = np.arange(h, dtype=np.float32)[:, None]
    xs = np.arange(w, dtype=np.float32)[None, :]
    dist_l = xs
    dist_r = w - 1 - xs
    dist_t = ys
    dist_b = h - 1 - ys
    dist_edge = np.minimum(np.minimum(dist_l, dist_r), np.minimum(dist_t, dist_b))
    # Corner correction: subtract the arc overshoot.
    # Near each corner, real distance to rounded edge is sqrt((r-x)^2+(r-y)^2) - r(?) — we
    # skip this and rely on the straight-edge distance, which slightly overestimates
    # interior-ness near corners. Good enough.
    # Convert to 0..1 where 1=on rim, 0=deep.
    falloff = np.clip(1.0 - dist_edge / max(rim_px, 1), 0, 1)
    falloff = falloff ** 2.2  # sharpen toward edge
    return falloff.astype(np.float32)


# -------------------- Drop shadow --------------------

def drop_shadow(mask_size: tuple[int, int], radius: int = 24,
                blur: int = 20, opacity: int = 120,
                offset: tuple[int, int] = (0, 12)) -> tuple[Image.Image, tuple[int, int]]:
    w, h = mask_size
    pad = blur * 2 + 4
    shadow = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle([pad, pad, pad + w - 1, pad + h - 1],
                        radius=radius, fill=(0, 0, 0, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, (-pad + offset[0], -pad + offset[1])


def accent_glow(base: Image.Image, x: int, y: int, size: tuple[int, int],
                radius: int = 28, color: tuple[int, int, int] = (244, 211, 94),
                alpha: int = 70, blur: int = 18):
    w, h = size
    pad = blur * 2
    glow = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.rounded_rectangle([pad - 2, pad - 2, pad + w + 1, pad + h + 1],
                        radius=radius + 2, outline=(*color, alpha), width=4)
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(glow, (x - pad, y - pad))


# -------------------- The main act: liquid glass panel --------------------

def render_liquid_glass(
    backdrop: Image.Image, x: int, y: int, size: tuple[int, int], *,
    radius: int = 28,
    blur_radius: int = 18,
    saturation: float = 1.65,
    tint_rgba: tuple[int, int, int, int] = (255, 255, 255, 30),
    rim_alpha: int = 200,
    corner_specular_alpha: int = 90,
    lensing_shift_px: int = 6,
    chromatic_aberration_px: int = 2,
    ripple_alpha: int = 9,
) -> Image.Image:
    """Produce a single liquid-glass panel tile (RGBA, size w x h) ready to
    composite at (x, y) on top of `backdrop`. Does NOT include the outer drop
    shadow — call `drop_shadow` separately for that."""
    w, h = size

    # ---- Extract the backdrop region under the panel ----
    bx0 = max(0, x)
    by0 = max(0, y)
    bx1 = min(backdrop.width, x + w)
    by1 = min(backdrop.height, y + h)
    region = backdrop.crop((bx0, by0, bx1, by1)).convert("RGBA")
    # Align into a full panel-sized canvas (padded with black if the panel
    # hangs off an edge).
    full_region = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    full_region.paste(region, (bx0 - x, by0 - y))

    # ---- Layer 1: blur (refraction base) ----
    blurred = full_region.filter(ImageFilter.GaussianBlur(blur_radius))

    # ---- Layer 2: saturation punch ----
    rgb = blurred.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(saturation)
    # Also nudge brightness down a hair so the glass has a slight base darken.
    rgb = ImageEnhance.Brightness(rgb).enhance(0.92)
    punch = rgb.convert("RGBA")

    # ---- Layer 3: fake lensing — displace rim pixels inward ----
    # Stronger shift + per-channel split for chromatic aberration ("rainbow
    # fringe" at the edge that gives glass its physical feel).
    if lensing_shift_px > 0:
        punch_arr = np.asarray(punch, dtype=np.uint8).copy()
        # Base vertical shift for top/bottom halves.
        shifted_down = np.roll(punch_arr, shift=(-lensing_shift_px, 0), axis=(0, 1))
        shifted_up = np.roll(punch_arr, shift=(lensing_shift_px, 0), axis=(0, 1))
        rim = _rim_mask((w, h), radius, rim_px=20)[..., None]
        half_mask = np.zeros((h, w, 1), dtype=np.float32)
        half_mask[:h // 2] = 1.0
        blended = punch_arr.astype(np.float32) * (1 - rim)
        pick_top = shifted_down.astype(np.float32) * rim * half_mask
        pick_bot = shifted_up.astype(np.float32) * rim * (1 - half_mask)
        lensed = (blended + pick_top + pick_bot).clip(0, 255)

        # Chromatic aberration: shift R one way and B the other, weighted by
        # rim. This is the "rainbow fringe" real glass produces.
        if chromatic_aberration_px > 0:
            ca = chromatic_aberration_px
            # Red channel: pull toward rim
            red_shift = np.roll(lensed[..., 0], shift=(ca, 0), axis=(0, 1))
            blue_shift = np.roll(lensed[..., 2], shift=(-ca, 0), axis=(0, 1))
            rim_flat = rim[..., 0]
            lensed[..., 0] = lensed[..., 0] * (1 - rim_flat) + red_shift * rim_flat
            lensed[..., 2] = lensed[..., 2] * (1 - rim_flat) + blue_shift * rim_flat

        punch = Image.fromarray(lensed.astype(np.uint8), mode="RGBA")

    # Rounded-rect mask (all subsequent layers clip to this).
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)

    # Start the panel canvas with the refracted/saturated/lensed region.
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    panel.paste(punch, (0, 0), mask)

    # ---- Layer 4: body tint ----
    tint = Image.new("RGBA", (w, h), tint_rgba)
    panel.paste(tint, (0, 0), mask)

    # ---- Layer 5: vertical illumination gradient ----
    # Bright near top, transparent by mid-panel.
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    peak = 28
    mid = h // 2
    for yy in range(h):
        if yy >= mid:
            a = 0
        else:
            t = yy / max(mid - 1, 1)
            a = int(peak * (1 - t))
        gd.line([(0, yy), (w, yy)], fill=(255, 255, 255, a))
    panel.paste(grad, (0, 0), mask)

    # ---- Layer 6: inset rim highlight ----
    rim_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim_layer)
    rd.rounded_rectangle([1, 1, w - 2, h - 2], radius=max(1, radius - 1),
                         outline=(255, 255, 255, rim_alpha), width=2)
    rim_layer = rim_layer.filter(ImageFilter.GaussianBlur(0.8))
    panel.paste(rim_layer, (0, 0), mask)

    # ---- Layer 7: corner specular (top-left + top-right) ----
    if corner_specular_alpha > 0:
        for (cx_frac, cy_frac) in [(0.18, 0.25), (0.82, 0.25)]:
            cx = int(w * cx_frac)
            cy = int(h * cy_frac)
            spec = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            sd = ImageDraw.Draw(spec)
            r = min(80, w // 4, h)
            sd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(255, 255, 255, corner_specular_alpha))
            spec = spec.filter(ImageFilter.GaussianBlur(r // 2))
            panel.paste(spec, (0, 0), mask)

    # ---- Layer 9: ripple noise ----
    if ripple_alpha > 0:
        ripple = _ripple_overlay((w, h), alpha=ripple_alpha)
        panel.paste(ripple, (0, 0), mask)

    # Hairline outer stroke for definition on very dark backdrops.
    od = ImageDraw.Draw(panel)
    od.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius,
                         outline=(255, 255, 255, 55), width=1)

    return panel


def compose_liquid_glass(
    base: Image.Image, x: int, y: int, size: tuple[int, int], *,
    radius: int = 28,
    shadow_blur: int = 22, shadow_opacity: int = 150,
    shadow_offset: tuple[int, int] = (0, 10),
    **glass_kwargs,
):
    """Drop shadow + liquid-glass panel — all in one call. `base` is the full
    1080x1920 RGBA canvas (which is also the backdrop sampler for layer 1).
    """
    if shadow_opacity > 0:
        sh, off = drop_shadow(size, radius=radius, blur=shadow_blur,
                              opacity=shadow_opacity, offset=shadow_offset)
        base.alpha_composite(sh, (x + off[0], y + off[1]))
    panel = render_liquid_glass(base, x, y, size, radius=radius, **glass_kwargs)
    base.alpha_composite(panel, (x, y))


# Back-compat: older scene.py calls into these names. Keep as aliases.
compose_panel = compose_liquid_glass
compose_apple_tile = compose_liquid_glass
