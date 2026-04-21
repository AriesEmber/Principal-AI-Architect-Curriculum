"""Liquid-glass-style rendering helpers.

Produces the "modern 3D-ish" look via pure PIL compositing:
- Radial/linear gradients for backdrops
- Soft multi-layer drop shadows
- Translucent rounded panels with gradient fills + highlight edges
- Inner glows / halos for accent emphasis

All functions operate on RGBA PIL images so panels layer cleanly.
"""
from typing import Sequence
from PIL import Image, ImageDraw, ImageFilter


# -------------------------- Backdrops --------------------------

def radial_gradient(size: tuple[int, int], inner: tuple[int, int, int],
                    outer: tuple[int, int, int],
                    center: tuple[float, float] | None = None,
                    falloff: float = 1.1) -> Image.Image:
    """RGB image, radial gradient from inner (center) to outer (corners).
    `center` is in 0..1 normalized coords; default (0.5, 0.3) biases slightly up.
    `falloff` > 1 stretches the gradient softer; < 1 tightens.
    """
    w, h = size
    if center is None:
        center = (0.5, 0.3)
    cx = center[0] * w
    cy = center[1] * h
    max_d = ((max(cx, w - cx)) ** 2 + (max(cy, h - cy)) ** 2) ** 0.5
    max_d *= falloff

    img = Image.new("RGB", (w, h), outer)
    px = img.load()
    # Two-pass: rows, then per-pixel for speed-reasonable quality.
    for y in range(h):
        dy = (y - cy) ** 2
        for x in range(w):
            d = (dy + (x - cx) ** 2) ** 0.5
            t = min(1.0, d / max_d)
            # Smooth step
            t = t * t * (3 - 2 * t)
            r = int(inner[0] + (outer[0] - inner[0]) * t)
            g = int(inner[1] + (outer[1] - inner[1]) * t)
            b = int(inner[2] + (outer[2] - inner[2]) * t)
            px[x, y] = (r, g, b)
    return img


def linear_gradient(size: tuple[int, int], c1: tuple[int, int, int],
                    c2: tuple[int, int, int], vertical: bool = True) -> Image.Image:
    w, h = size
    img = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(img)
    steps = h if vertical else w
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        if vertical:
            d.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            d.line([(i, 0), (i, h)], fill=(r, g, b))
    return img


# -------------------------- Shadow --------------------------

def drop_shadow(mask_size: tuple[int, int], radius: int = 24,
                blur: int = 20, opacity: int = 120,
                offset: tuple[int, int] = (0, 12)) -> tuple[Image.Image, tuple[int, int]]:
    """Return (RGBA shadow image, paste_offset) for a rounded-rect of mask_size.
    Caller pastes onto the canvas at (panel_x + paste_off[0], panel_y + paste_off[1]).
    """
    w, h = mask_size
    pad = blur * 2 + 4
    shadow = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(shadow)
    d.rounded_rectangle([pad, pad, pad + w - 1, pad + h - 1],
                        radius=radius, fill=(0, 0, 0, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    paste_off = (-pad + offset[0], -pad + offset[1])
    return shadow, paste_off


# -------------------------- Glass panel --------------------------

def glass_panel(size: tuple[int, int], radius: int = 28,
                fill_rgba: tuple[int, int, int, int] = (255, 255, 255, 22),
                top_highlight_alpha: int = 60,
                gradient: tuple[tuple[int, int, int, int],
                                tuple[int, int, int, int]] | None = None,
                edge_rgba: tuple[int, int, int, int] = (255, 255, 255, 34),
                edge_width: int = 1) -> Image.Image:
    """Rounded rectangular translucent panel with a subtle top-edge highlight
    and a hairline edge. No shadow baked in — composite with `drop_shadow`.
    """
    w, h = size
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)

    if gradient is None:
        # Flat translucent fill.
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=fill_rgba)
    else:
        # Vertical gradient fill inside rounded-rect mask.
        top_c, bot_c = gradient
        grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(grad)
        for y in range(h):
            t = y / max(h - 1, 1)
            r = int(top_c[0] + (bot_c[0] - top_c[0]) * t)
            g = int(top_c[1] + (bot_c[1] - top_c[1]) * t)
            b = int(top_c[2] + (bot_c[2] - top_c[2]) * t)
            a = int(top_c[3] + (bot_c[3] - top_c[3]) * t)
            gd.line([(0, y), (w, y)], fill=(r, g, b, a))
        # Mask to rounded-rect
        mask = Image.new("L", (w, h), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
        panel.paste(grad, (0, 0), mask)

    # Top-edge highlight — a 2px-thick bright arc on the top half
    hl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.rounded_rectangle([1, 1, w - 2, h - 2], radius=radius - 1,
                         outline=(255, 255, 255, top_highlight_alpha), width=2)
    # Mask: only keep the top half of the highlight
    top_mask = Image.new("L", (w, h), 0)
    tmd = ImageDraw.Draw(top_mask)
    tmd.rectangle([0, 0, w, h // 2], fill=255)
    # Blend only the top part
    panel.alpha_composite(Image.composite(hl, Image.new("RGBA", (w, h), (0, 0, 0, 0)), top_mask))

    # Hairline edge (full perimeter, very subtle)
    if edge_width > 0:
        ed = ImageDraw.Draw(panel)
        ed.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius,
                             outline=edge_rgba, width=edge_width)

    return panel


def compose_panel(base: Image.Image, x: int, y: int, size: tuple[int, int],
                  *, radius: int = 28, fill_rgba=(255, 255, 255, 22),
                  accent_edge_rgba: tuple[int, int, int, int] | None = None,
                  shadow_blur: int = 20, shadow_opacity: int = 130,
                  shadow_offset: tuple[int, int] = (0, 10),
                  gradient: tuple | None = None):
    """Paste a shadow + glass panel at (x, y) on `base` (RGBA)."""
    w, h = size
    if shadow_opacity > 0:
        sh, off = drop_shadow(size, radius=radius, blur=shadow_blur,
                              opacity=shadow_opacity, offset=shadow_offset)
        base.alpha_composite(sh, (x + off[0], y + off[1]))
    panel = glass_panel(size, radius=radius, fill_rgba=fill_rgba,
                        gradient=gradient,
                        edge_rgba=accent_edge_rgba or (255, 255, 255, 34))
    base.alpha_composite(panel, (x, y))
    # Second accent stroke (brighter) if provided
    if accent_edge_rgba is not None:
        d = ImageDraw.Draw(base)
        d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=radius,
                            outline=accent_edge_rgba, width=2)


def accent_glow(base: Image.Image, x: int, y: int, size: tuple[int, int],
                radius: int = 28, color: tuple[int, int, int] = (244, 211, 94),
                alpha: int = 70, blur: int = 18):
    """Soft outer glow around a rounded rect — for accent emphasis."""
    w, h = size
    pad = blur * 2
    glow = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.rounded_rectangle([pad - 2, pad - 2, pad + w + 1, pad + h + 1],
                        radius=radius + 2, outline=(*color, alpha), width=4)
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(glow, (x - pad, y - pad))


# -------------------- Apple-style liquid glass tile --------------------

def apple_glass_tile(size: tuple[int, int], *, radius: int = 28,
                     tint: tuple[int, int, int] = (200, 220, 240),
                     tint_alpha_top: int = 48,
                     tint_alpha_bot: int = 90,
                     rim_alpha: int = 180,
                     inner_glow_alpha: int = 70,
                     specular: bool = True) -> Image.Image:
    """Return an RGBA tile (size w x h) styled like iOS 26 / macOS Tahoe liquid
    glass — translucent top-light gradient + bright rim + subtle inner glow +
    a soft specular highlight in the upper-left quadrant.

    Compose this ON TOP of a blurred background patch to complete the
    frosted/refractive feel (see `frosted_under`).
    """
    w, h = size
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    # ---- Rounded-rect mask for clipping ----
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)

    # ---- Vertical tint gradient (top lighter, bottom slightly deeper) ----
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(h):
        t = y / max(h - 1, 1)
        a = int(tint_alpha_top + (tint_alpha_bot - tint_alpha_top) * t)
        gd.line([(0, y), (w, y)], fill=(*tint, a))
    img.paste(grad, (0, 0), mask)

    # ---- Inner glow (bright ring just inside the edge) ----
    if inner_glow_alpha > 0:
        glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        glow_draw.rounded_rectangle(
            [2, 2, w - 3, h - 3], radius=max(1, radius - 2),
            outline=(255, 255, 255, inner_glow_alpha), width=3)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(2.5))
        # Clip glow to the rounded rect
        img.paste(glow_layer, (0, 0), mask)

    # ---- Rim highlight (sharp, bright top/left edge) ----
    rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rim)
    rd.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius,
                         outline=(255, 255, 255, rim_alpha), width=2)
    # Keep only top-left ~50% of the rim (emphasizes light direction)
    rim_mask = Image.new("L", (w, h), 0)
    rmd = ImageDraw.Draw(rim_mask)
    # Gradient mask that fades from full on top-left to nothing on bottom-right.
    for y in range(h):
        for x in range(w):
            d = 1.0 - ((x / w) + (y / h)) / 2
            rmd.point((x, y), fill=max(0, int(d * 255 * 0.9)))
    # Too slow per-pixel; replace with a simpler alpha mask.
    rim_mask = Image.new("L", (w, h), 0)
    rmd = ImageDraw.Draw(rim_mask)
    # Top edge: full bright. Fades down to 40% by bottom.
    for y in range(h):
        fade = int(255 - (255 - 80) * (y / max(h - 1, 1)))
        rmd.line([(0, y), (w, y)], fill=fade)
    rim_clipped = Image.composite(rim,
                                   Image.new("RGBA", (w, h), (0, 0, 0, 0)),
                                   rim_mask)
    img.alpha_composite(rim_clipped)

    # ---- Specular highlight (elongated soft gleam on upper-left) ----
    if specular:
        spec = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sd = ImageDraw.Draw(spec)
        sx = int(w * 0.28)
        sy = int(h * 0.30)
        sw = int(w * 0.38)
        sh = int(h * 0.14)
        sd.ellipse([sx - sw // 2, sy - sh // 2, sx + sw // 2, sy + sh // 2],
                   fill=(255, 255, 255, 80))
        spec = spec.filter(ImageFilter.GaussianBlur(18))
        # Clip to the panel
        img.paste(spec, (0, 0), mask)

    # ---- Final outer stroke (very faint, for definition on dark bg) ----
    od = ImageDraw.Draw(img)
    od.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius,
                         outline=(255, 255, 255, 50), width=1)

    return img


def frosted_under(backdrop: Image.Image, x: int, y: int,
                  size: tuple[int, int], *, radius: int = 28,
                  blur: float = 14.0) -> Image.Image:
    """Create a frosted backdrop patch for an Apple-glass tile. Extract the
    region of `backdrop` under where the tile will sit, blur it, and mask it
    with the rounded-rect shape.
    """
    w, h = size
    # Clamp to canvas
    bx0 = max(0, x)
    by0 = max(0, y)
    bx1 = min(backdrop.width, x + w)
    by1 = min(backdrop.height, y + h)
    region = backdrop.crop((bx0, by0, bx1, by1))
    if region.mode != "RGBA":
        region = region.convert("RGBA")
    region = region.filter(ImageFilter.GaussianBlur(blur))
    # Enhance: bump brightness slightly so the frosted area feels lit
    region = Image.blend(region,
                         Image.new("RGBA", region.size, (255, 255, 255, 255)),
                         0.12)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    # Align region inside a full-size transparent tile
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(region, (bx0 - x, by0 - y))
    out.putalpha(mask)
    return out


def compose_apple_tile(base: Image.Image, x: int, y: int,
                       size: tuple[int, int], *, radius: int = 28,
                       tint: tuple[int, int, int] = (200, 220, 240),
                       shadow_blur: int = 24, shadow_opacity: int = 150,
                       shadow_offset: tuple[int, int] = (0, 12),
                       backdrop: Image.Image | None = None):
    """Drop shadow + frosted backdrop + Apple-glass tile — all in one call."""
    w, h = size
    if shadow_opacity > 0:
        sh, off = drop_shadow(size, radius=radius, blur=shadow_blur,
                              opacity=shadow_opacity, offset=shadow_offset)
        base.alpha_composite(sh, (x + off[0], y + off[1]))
    if backdrop is not None:
        frosted = frosted_under(backdrop, x, y, size, radius=radius, blur=14.0)
        base.alpha_composite(frosted, (x, y))
    tile = apple_glass_tile(size, radius=radius, tint=tint)
    base.alpha_composite(tile, (x, y))

