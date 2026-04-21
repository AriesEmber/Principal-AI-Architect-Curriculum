"""Glowing electron — replaces the mascot sprite.

A bright cyan core with a soft blue bloom, optionally a trailing particle
stream. Used as the "pen" that draws the sequence diagram: the electron
orbits during self-beats, travels vertically along arrows during call/return
beats, and hops horizontally between beat x-positions in between.

Arrow and marker persistence is handled in scene.py — this module only renders
the electron itself at a given (x, y) on a given canvas.
"""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter


# Electron color stack — layered radial glows from biggest/softest to core.
CORE_RGB = (230, 248, 255)
INNER_GLOW_RGB = (90, 190, 255)
OUTER_GLOW_RGB = (40, 120, 220)
SPARK_RGB = (255, 240, 180)


@lru_cache(maxsize=4)
def _glow_sprite(size: int, core_r: int) -> Image.Image:
    """Circular glow sprite of diameter `size`. Drawn once, cached."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = size // 2

    # Build up radial falloff by drawing concentric circles with decreasing alpha
    layers = [
        (size // 2,      OUTER_GLOW_RGB, 36),
        (int(size * 0.35), INNER_GLOW_RGB, 80),
        (int(size * 0.22), INNER_GLOW_RGB, 160),
        (core_r + 2,     CORE_RGB,      220),
        (core_r,         CORE_RGB,      255),
    ]
    for r, color, alpha in layers:
        bbox = [cx - r, cy - r, cx + r, cy + r]
        d.ellipse(bbox, fill=(*color, alpha))
    img = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    # Draw sharper core on top after blur
    d2 = ImageDraw.Draw(img)
    d2.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r],
               fill=(*CORE_RGB, 255))
    # Tiny inner highlight
    d2.ellipse([cx - core_r // 2 - 1, cy - core_r // 2 - 1,
                cx - core_r // 2 + 1, cy - core_r // 2 + 1],
               fill=(255, 255, 255, 255))
    return img


def paste_electron(base: Image.Image, x: float, y: float, size: int = 56,
                   core_r: int = 5, intensity: float = 1.0):
    """Stamp the electron glow onto base (RGBA) centered at (x, y)."""
    sprite = _glow_sprite(size, core_r)
    if intensity < 0.99:
        a = sprite.split()[3]
        a = a.point(lambda v: int(v * intensity))
        sprite = sprite.copy()
        sprite.putalpha(a)
    base.alpha_composite(sprite, (int(x) - size // 2, int(y) - size // 2))


def paste_trail(base: Image.Image, positions: list[tuple[float, float]],
                size: int = 46, core_r: int = 3):
    """Render a fading trail of past electron positions.
    `positions` is oldest→newest.
    """
    n = len(positions)
    if n == 0:
        return
    sprite = _glow_sprite(size, core_r)
    for i, (x, y) in enumerate(positions):
        # Older positions fade out.
        u = (i + 1) / n
        alpha_scale = (u * u) * 0.55
        s = sprite.copy()
        a = s.split()[3].point(lambda v: int(v * alpha_scale))
        s.putalpha(a)
        base.alpha_composite(s, (int(x) - size // 2, int(y) - size // 2))


# -------------------- Path helpers --------------------

def orbit_xy(center_x: float, center_y: float, radius: float,
             angular_speed: float, t: float,
             phase: float = 0.0) -> tuple[float, float]:
    """Electron orbiting a center at t seconds. angular_speed in rotations/sec."""
    theta = phase + 2 * math.pi * angular_speed * t
    return (center_x + radius * math.cos(theta),
            center_y + radius * math.sin(theta))


def lerp(a: float, b: float, u: float) -> float:
    return a + (b - a) * u


def ease_in_out(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return 3 * u * u - 2 * u * u * u
