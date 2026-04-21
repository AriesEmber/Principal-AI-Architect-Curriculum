"""Animated smoke/nebula backdrop.

Per-frame cost: ~10-15ms on a 1080x1920 canvas. The expensive work (tile
generation) is done offline via gen_backdrop.py and cached as a PNG.

Per frame we:
  1. Pan a pre-baked seamless noise tile (x=t*12, y=t*7 px/sec — non-integer
     ratio means no visible repeat).
  2. Add two drifting soft color blobs on Lissajous paths, screen-blended.
  3. Darken to 0.75 and apply a vertical vignette so the foreground content
     sits on the brightest band.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from . import config as C


_TILE_CACHE: Image.Image | None = None
_VIGNETTE_CACHE: Image.Image | None = None


def _tile() -> Image.Image:
    global _TILE_CACHE
    if _TILE_CACHE is None:
        path = C.SHORTS_DIR / "assets" / "backgrounds" / "smoke_tile.png"
        _TILE_CACHE = Image.open(path).convert("RGB")
    return _TILE_CACHE


def _pan_viewport(t: float) -> Image.Image:
    """Crop a 1080x1920 window out of the pre-baked tile at time t."""
    tile = _tile()
    tw, th = tile.size
    dx = int((t * 12) % tw)
    dy = int((t * 7) % th)
    x0 = dx
    y0 = dy
    x1 = x0 + C.CANVAS_W
    y1 = y0 + C.CANVAS_H
    # If the window spills past the tile edge, we wrap — but since our tile
    # (2160) is bigger than the canvas (1080x1920), only y-wrap needs care.
    if x1 <= tw and y1 <= th:
        return tile.crop((x0, y0, x1, y1))
    # Rare case: wrap with mirroring.
    canvas = Image.new("RGB", (C.CANVAS_W, C.CANVAS_H))
    for ox in (0, -tw):
        for oy in (0, -th):
            canvas.paste(tile, (ox - x0, oy - y0))
    return canvas


def _radial_blob(size: tuple[int, int], cx: float, cy: float, radius: float,
                 color: tuple[int, int, int], alpha: int) -> Image.Image:
    """A soft circular color blob (translucent) for compositing."""
    w, h = size
    # We render at a reduced resolution then upscale — very fast and the
    # blob is soft anyway.
    sf = 6
    sw, sh = w // sf, h // sf
    scx, scy, sr = cx / sf, cy / sf, radius / sf
    # Use numpy to compute Gaussian falloff on the small canvas.
    ys = np.arange(sh, dtype=np.float32)[:, None]
    xs = np.arange(sw, dtype=np.float32)[None, :]
    d2 = (xs - scx) ** 2 + (ys - scy) ** 2
    g = np.exp(-d2 / (2 * sr * sr))
    a = (g * alpha).clip(0, 255).astype(np.uint8)
    rgba = np.zeros((sh, sw, 4), dtype=np.uint8)
    rgba[..., 0] = color[0]
    rgba[..., 1] = color[1]
    rgba[..., 2] = color[2]
    rgba[..., 3] = a
    img = Image.fromarray(rgba, mode="RGBA")
    return img.resize((w, h), Image.BILINEAR)


def _screen_blend(base_rgb: np.ndarray, overlay_rgba: np.ndarray) -> np.ndarray:
    """Screen-blend overlay onto base. Both float32 in [0,1]."""
    a = overlay_rgba[..., 3:4]
    out = 1.0 - (1.0 - base_rgb) * (1.0 - overlay_rgba[..., :3] * a)
    return out


def _vignette() -> Image.Image:
    """Vertical vignette — top/bottom darker, middle clear. Cached."""
    global _VIGNETTE_CACHE
    if _VIGNETTE_CACHE is not None:
        return _VIGNETTE_CACHE
    w, h = C.CANVAS_W, C.CANVAS_H
    ys = np.arange(h, dtype=np.float32)
    # Dark at top/bottom, bright in middle. Peak at y=0.5, falloff to edges.
    center = h / 2
    falloff = (abs(ys - center) / center) ** 1.6  # 0 at center, 1 at edges
    # Max darken 25% at edges.
    dim = 1.0 - 0.25 * falloff
    grad = np.broadcast_to(dim[:, None, None], (h, w, 1)).astype(np.float32)
    # Store as an alpha-multiplier image: convert to 0..255.
    arr = np.broadcast_to(grad, (h, w, 3)) * 255
    _VIGNETTE_CACHE = Image.fromarray(arr.astype(np.uint8), mode="RGB")
    return _VIGNETTE_CACHE


def render_backdrop(t: float) -> Image.Image:
    """Return a 1080x1920 RGB backdrop for time t."""
    # 1. Panned noise tile
    frame = _pan_viewport(t)
    # 2. Two drifting blobs (Lissajous paths).
    cx, cy = C.CANVAS_W / 2, C.CANVAS_H / 2
    blob_a_x = cx + 180 * math.sin(0.08 * t)
    blob_a_y = cy - 200 + 120 * math.cos(0.05 * t)
    blob_b_x = cx - 160 + 140 * math.cos(0.06 * t + 1.2)
    blob_b_y = cy + 250 + 180 * math.sin(0.04 * t + 0.7)
    blob_a = _radial_blob(frame.size, blob_a_x, blob_a_y, 420, (58, 30, 110), 55)
    blob_b = _radial_blob(frame.size, blob_b_x, blob_b_y, 520, (16, 74, 122), 45)
    # 3. Compose via screen blend (using numpy for speed).
    base = np.asarray(frame, dtype=np.float32) / 255.0
    for blob in (blob_a, blob_b):
        ov = np.asarray(blob, dtype=np.float32) / 255.0
        base = _screen_blend(base, ov)
    out = (base * 255).clip(0, 255).astype(np.uint8)
    # 4. Darken slightly + vignette (multiply).
    vign = np.asarray(_vignette(), dtype=np.float32) / 255.0
    final = (out.astype(np.float32) * 0.78 * vign).clip(0, 255).astype(np.uint8)
    return Image.fromarray(final, mode="RGB")
