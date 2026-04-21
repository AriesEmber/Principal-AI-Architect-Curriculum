"""Pixel sprite generation.

Placeholder sprites live here until the mascot pick is locked. When a mascot
is chosen, its sprite sheet will go under _shorts/character/ as PNGs, and
load_robot() / load_user() will be updated to read those files. The interface
(return a PIL RGBA image at native sprite resolution) does not change.
"""
from PIL import Image, ImageDraw
from .config import (
    COLOR_PRIMARY, COLOR_OUTLINE, COLOR_ACCENT, COLOR_SHADOW,
    COLOR_USER_SKIN, COLOR_USER_SHIRT,
)

SPRITE_SIZE = 48


def _px(d: ImageDraw.ImageDraw, x: int, y: int, color, w: int = 1, h: int = 1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def placeholder_robot(frame: str = "idle_0") -> Image.Image:
    """48x48 boxy robot courier, palette B. Subtle frame variation for walk/idle."""
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head_y = 8
    body_y = 24
    leg_offset = 0
    arm_offset = 0

    if frame.startswith("walk"):
        step = int(frame.split("_")[1]) if "_" in frame else 0
        if step % 2 == 0:
            leg_offset = 1
            arm_offset = -1
        else:
            leg_offset = -1
            arm_offset = 1
    elif frame == "idle_1":
        head_y = 9  # slight breathing motion

    # Crate on back (shadow behind body)
    _px(d, 34, body_y - 2, COLOR_SHADOW, 8, 14)
    _px(d, 35, body_y - 1, COLOR_PRIMARY, 6, 12)
    _px(d, 37, body_y + 2, COLOR_OUTLINE, 2, 2)
    _px(d, 37, body_y + 8, COLOR_OUTLINE, 2, 2)

    # Head (cube)
    _px(d, 14, head_y, COLOR_OUTLINE, 20, 16)
    _px(d, 15, head_y + 1, COLOR_PRIMARY, 18, 14)
    # Visor (horizontal slit)
    _px(d, 18, head_y + 6, COLOR_OUTLINE, 12, 3)
    _px(d, 19, head_y + 7, COLOR_ACCENT, 3, 1)
    _px(d, 27, head_y + 7, COLOR_ACCENT, 2, 1)
    # Antenna
    _px(d, 23, head_y - 3, COLOR_OUTLINE, 2, 3)
    _px(d, 22, head_y - 5, COLOR_ACCENT, 4, 2)

    # Body (cube)
    _px(d, 13, body_y, COLOR_OUTLINE, 22, 16)
    _px(d, 14, body_y + 1, COLOR_PRIMARY, 20, 14)
    # Chest badge
    _px(d, 22, body_y + 5, COLOR_ACCENT, 4, 4)
    _px(d, 23, body_y + 6, COLOR_OUTLINE, 2, 2)

    # Arms (sides of body)
    _px(d, 10, body_y + 3 + arm_offset, COLOR_OUTLINE, 3, 9)
    _px(d, 10, body_y + 3 + arm_offset + 1, COLOR_PRIMARY, 3, 7)
    _px(d, 35, body_y + 3 - arm_offset, COLOR_OUTLINE, 3, 9)
    _px(d, 35, body_y + 3 - arm_offset + 1, COLOR_PRIMARY, 3, 7)

    # Legs
    _px(d, 16, 40, COLOR_OUTLINE, 5, 6 + leg_offset)
    _px(d, 27, 40, COLOR_OUTLINE, 5, 6 - leg_offset)
    _px(d, 17, 41, COLOR_PRIMARY, 3, 4 + leg_offset)
    _px(d, 28, 41, COLOR_PRIMARY, 3, 4 - leg_offset)

    return img


def placeholder_user(frame: str = "idle_0") -> Image.Image:
    """48x48 user standing figure."""
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Head
    _px(d, 18, 8, COLOR_OUTLINE, 12, 12)
    _px(d, 19, 9, COLOR_USER_SKIN, 10, 10)
    # Eyes
    _px(d, 21, 13, COLOR_OUTLINE, 2, 2)
    _px(d, 25, 13, COLOR_OUTLINE, 2, 2)
    # Smile
    _px(d, 22, 16, COLOR_OUTLINE, 4, 1)

    # Hair
    _px(d, 18, 8, COLOR_OUTLINE, 12, 3)

    # Neck
    _px(d, 22, 20, COLOR_USER_SKIN, 4, 2)

    # Shirt / body
    _px(d, 14, 22, COLOR_OUTLINE, 20, 14)
    _px(d, 15, 23, COLOR_USER_SHIRT, 18, 12)
    # Shirt collar accent
    _px(d, 22, 23, (220, 220, 220), 4, 2)

    # Arms
    _px(d, 10, 23, COLOR_OUTLINE, 4, 10)
    _px(d, 11, 24, COLOR_USER_SKIN, 3, 8)
    _px(d, 34, 23, COLOR_OUTLINE, 4, 10)
    _px(d, 35, 24, COLOR_USER_SKIN, 3, 8)

    # Legs
    _px(d, 16, 36, COLOR_OUTLINE, 6, 10)
    _px(d, 26, 36, COLOR_OUTLINE, 6, 10)
    _px(d, 17, 37, (60, 70, 100), 4, 8)
    _px(d, 27, 37, (60, 70, 100), 4, 8)

    return img


def upscale_pixel(img: Image.Image, factor: int) -> Image.Image:
    """Nearest-neighbor upscale to keep crisp pixel edges."""
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


