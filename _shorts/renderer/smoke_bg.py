"""Animated backdrop: dark gradient base + panning code-cloud tile whose hue
slowly rotates + two slow-drifting color blobs for depth.

Design intent: no longer "blue/black powerpoint" — the viewer sees faint
code-colored clouds shifting through cyan, magenta, amber, etc., while the
glass foreground reads as floating on top of a living background.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from . import config as C


_CLOUDS_CACHE: Image.Image | None = None
_VIGNETTE_CACHE: Image.Image | None = None


def _clouds_tile() -> Image.Image:
    global _CLOUDS_CACHE
    if _CLOUDS_CACHE is None:
        path = C.SHORTS_DIR / "assets" / "backgrounds" / "code_clouds.png"
        _CLOUDS_CACHE = Image.open(path).convert("RGBA")
    return _CLOUDS_CACHE


def _pan_rgba(tile: Image.Image, dx: float, dy: float,
              out_size: tuple[int, int]) -> Image.Image:
    """Sample a (w, h) viewport out of a large seamless RGBA tile at (dx, dy)."""
    tw, th = tile.size
    w, h = out_size
    x0 = int(dx) % tw
    y0 = int(dy) % th
    if x0 + w <= tw and y0 + h <= th:
        return tile.crop((x0, y0, x0 + w, y0 + h))
    # Wrap — tile is seamless so this is safe.
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for oy in (0, -th):
        for ox in (0, -tw):
            canvas.paste(tile, (ox - x0, oy - y0), tile)
    return canvas


def _hue_rotate_rgba(img: Image.Image, degrees: float) -> Image.Image:
    """Rotate the hue of every pixel by `degrees`. RGBA preserved."""
    arr = np.asarray(img, dtype=np.float32) / 255.0
    rgb = arr[..., :3]
    a = arr[..., 3:4]

    # RGB -> HSV via numpy
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    maxc = np.max(rgb, axis=-1)
    minc = np.min(rgb, axis=-1)
    v = maxc
    delta = maxc - minc
    s = np.where(maxc > 1e-6, delta / (maxc + 1e-6), 0)
    rc = np.where(delta > 1e-6, (maxc - r) / (delta + 1e-6), 0)
    gc = np.where(delta > 1e-6, (maxc - g) / (delta + 1e-6), 0)
    bc = np.where(delta > 1e-6, (maxc - b) / (delta + 1e-6), 0)
    h = np.where(r == maxc, bc - gc,
         np.where(g == maxc, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0
    # Rotate
    h = (h + degrees / 360.0) % 1.0
    # HSV -> RGB
    i = np.floor(h * 6).astype(np.int32)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    i = i % 6
    r_out = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5],
                       [v, q, p, p, t, v])
    g_out = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5],
                       [t, v, v, q, p, p])
    b_out = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5],
                       [p, p, t, v, v, q])
    out = np.stack([r_out, g_out, b_out, a[..., 0]], axis=-1)
    return Image.fromarray(
        (out.clip(0, 1) * 255).astype(np.uint8), mode="RGBA")


def _gradient_base(t: float) -> Image.Image:
    """Slow-shifting dark-grey-with-color-tint gradient base.
    Never pure black, never pure blue — cycles subtly through warm and cool
    dark tones over ~40-second loop."""
    w, h = C.CANVAS_W, C.CANVAS_H
    # Cycle period ~45s so single short doesn't visibly repeat.
    phase = (t / 45.0) * 2 * math.pi
    # Pick 2 colors based on phase.
    def palette(ph):
        # Returns an RGB in a dark-tone band that shifts around the hue wheel.
        # Radius (saturation) ~0.20 so it stays subtle.
        base = 24
        amp = 16
        r = base + amp * (0.5 + 0.5 * math.sin(ph))
        g = base + amp * (0.5 + 0.5 * math.sin(ph + 2.1))
        b = base + amp * (0.5 + 0.5 * math.sin(ph + 4.2))
        return (int(r), int(g), int(b))
    top = palette(phase)
    bot = palette(phase + 1.8)

    # Vertical gradient via numpy
    ys = np.linspace(0, 1, h, dtype=np.float32)
    r_arr = top[0] + (bot[0] - top[0]) * ys
    g_arr = top[1] + (bot[1] - top[1]) * ys
    b_arr = top[2] + (bot[2] - top[2]) * ys
    col = np.stack([r_arr, g_arr, b_arr], axis=-1)[:, None, :]  # (h, 1, 3)
    col = np.broadcast_to(col, (h, w, 3)).astype(np.uint8)
    return Image.fromarray(col, mode="RGB")


def _vignette() -> Image.Image:
    global _VIGNETTE_CACHE
    if _VIGNETTE_CACHE is not None:
        return _VIGNETTE_CACHE
    w, h = C.CANVAS_W, C.CANVAS_H
    ys = np.arange(h, dtype=np.float32)
    xs = np.arange(w, dtype=np.float32)
    cy = h / 2
    cx = w / 2
    # Mild radial vignette, max 22% darken at corners.
    dy = ((ys - cy) / cy) ** 2
    dx = ((xs - cx) / cx) ** 2
    d = np.minimum(1.0, np.sqrt(dy[:, None] + dx[None, :]) ** 1.4)
    dim = 1.0 - 0.22 * d
    arr = (np.broadcast_to(dim[..., None], (h, w, 3)) * 255).astype(np.uint8)
    _VIGNETTE_CACHE = Image.fromarray(arr, mode="RGB")
    return _VIGNETTE_CACHE


def render_backdrop(t: float) -> Image.Image:
    """Return a 1080x1920 RGB backdrop for time t.
    Composition (bottom -> top):
      - Color-shifting gradient base (very dark, never pure black)
      - Code-cloud layer, panned + hue-rotated (primary visual character)
      - Code-cloud second pass, panned differently + opposite hue rotation for
        parallax/chroma-shift
      - Mild radial vignette
    """
    base = _gradient_base(t).convert("RGBA")

    tile = _clouds_tile()

    # Layer 1: slower pan, modest hue rotation.
    layer1 = _pan_rgba(tile, t * 8.0, t * 4.5, (C.CANVAS_W, C.CANVAS_H))
    layer1 = _hue_rotate_rgba(layer1, (t * 6.0) % 360)
    # Reduce alpha so it's truly faint.
    a1 = layer1.split()[3].point(lambda v: int(v * 0.75))
    layer1.putalpha(a1)
    base.alpha_composite(layer1)

    # Layer 2: faster pan, opposite direction, different hue shift — creates
    # subtle parallax + color chroma.
    layer2 = _pan_rgba(tile, -t * 13.0 + 700, -t * 7.0 + 400,
                      (C.CANVAS_W, C.CANVAS_H))
    layer2 = _hue_rotate_rgba(layer2, (t * -9.0 + 120) % 360)
    a2 = layer2.split()[3].point(lambda v: int(v * 0.6))
    layer2.putalpha(a2)
    base.alpha_composite(layer2)

    # Final vignette (multiply)
    out = np.asarray(base.convert("RGB"), dtype=np.float32)
    vign = np.asarray(_vignette(), dtype=np.float32) / 255.0
    out = (out * vign * 0.92).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
