"""Pixel sprite generation.

The robot is Crate-Bot the Courier (locked from mascot research). Drawn
procedurally here rather than loaded from a PNG sheet so animation frames stay
under version control as code, not as binary diffs.
"""
from PIL import Image, ImageDraw
from .config import (
    COLOR_PRIMARY, COLOR_OUTLINE, COLOR_ACCENT, COLOR_SHADOW,
    COLOR_USER_SKIN, COLOR_USER_SHIRT,
)

SPRITE_SIZE = 48

# Crate wood tone (not used elsewhere in UI)
CRATE_WOOD = (170, 110, 60)


def _px(d: ImageDraw.ImageDraw, x: int, y: int, color, w: int = 1, h: int = 1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def _crate_bot_base(d: ImageDraw.ImageDraw, head_y: int, body_y: int,
                    left_leg_y_off: int, right_leg_y_off: int,
                    left_arm_y_off: int, right_arm_y_off: int,
                    left_leg_x_off: int = 0, right_leg_x_off: int = 0):
    """Draw Crate-Bot at the given per-part offsets. Matches the locked
    mascot-candidate design (candidate-1-crate-bot.png)."""
    # Crate on back — a wooden courier box peeking from behind the right shoulder
    _px(d, 32, body_y - 4, COLOR_SHADOW, 10, 16)
    _px(d, 33, body_y - 3, CRATE_WOOD, 8, 14)
    _px(d, 34, body_y - 1, COLOR_OUTLINE, 6, 1)   # top plank seam
    _px(d, 34, body_y + 6, COLOR_OUTLINE, 6, 1)   # bottom plank seam
    _px(d, 37, body_y - 2, COLOR_OUTLINE, 1, 14)  # vertical plank seam

    # Head (cube, large — 20 wide x 18 tall, reads as "whole top half of the body")
    _px(d, 12, head_y, COLOR_OUTLINE, 22, 18)
    _px(d, 13, head_y + 1, COLOR_PRIMARY, 20, 16)
    # Head rivet corners (amber dots)
    _px(d, 14, head_y + 2, COLOR_ACCENT, 1, 1)
    _px(d, 31, head_y + 2, COLOR_ACCENT, 1, 1)
    # Visor slit — wide, single cyclopean eye
    _px(d, 15, head_y + 7, COLOR_OUTLINE, 16, 5)
    _px(d, 17, head_y + 8, COLOR_SHADOW, 12, 3)
    # Amber pupil (the "hook feature" — appears in every frame)
    _px(d, 22, head_y + 9, COLOR_ACCENT, 4, 1)
    # Top bolt / short antenna
    _px(d, 22, head_y - 3, COLOR_OUTLINE, 4, 3)
    _px(d, 23, head_y - 2, COLOR_ACCENT, 2, 1)

    # Body (cube, slightly wider than head)
    _px(d, 10, body_y, COLOR_OUTLINE, 26, 16)
    _px(d, 11, body_y + 1, COLOR_PRIMARY, 24, 14)
    # Body divider (center seam)
    _px(d, 22, body_y + 1, COLOR_SHADOW, 2, 14)
    # Chest badge (amber "courier" emblem)
    _px(d, 16, body_y + 5, COLOR_ACCENT, 4, 4)
    _px(d, 17, body_y + 6, COLOR_OUTLINE, 2, 2)

    # Arms (thick, at sides, with dark gloves)
    la_y = body_y + 2 + left_arm_y_off
    _px(d, 7, la_y, COLOR_OUTLINE, 4, 11)
    _px(d, 8, la_y + 1, COLOR_PRIMARY, 3, 9)
    _px(d, 7, la_y + 10, COLOR_SHADOW, 4, 2)  # left glove

    ra_y = body_y + 2 + right_arm_y_off
    _px(d, 35, ra_y, COLOR_OUTLINE, 4, 11)
    _px(d, 36, ra_y + 1, COLOR_PRIMARY, 3, 9)
    _px(d, 35, ra_y + 10, COLOR_SHADOW, 4, 2)  # right glove

    # Stubby legs — separate left/right so they can step independently in walk frames
    ll_x0 = 14 + left_leg_x_off
    ll_y0 = 40 + left_leg_y_off
    _px(d, ll_x0, ll_y0, COLOR_OUTLINE, 7, 48 - ll_y0)
    _px(d, ll_x0 + 1, ll_y0 + 1, COLOR_SHADOW, 5, 48 - ll_y0 - 2)
    # Boot toe highlight
    if ll_y0 < 46:
        _px(d, ll_x0 + 1, 46, COLOR_ACCENT, 1, 1)

    rl_x0 = 25 + right_leg_x_off
    rl_y0 = 40 + right_leg_y_off
    _px(d, rl_x0, rl_y0, COLOR_OUTLINE, 7, 48 - rl_y0)
    _px(d, rl_x0 + 1, rl_y0 + 1, COLOR_SHADOW, 5, 48 - rl_y0 - 2)
    if rl_y0 < 46:
        _px(d, rl_x0 + 1, 46, COLOR_ACCENT, 1, 1)


def placeholder_robot(frame: str = "idle_0") -> Image.Image:
    """Crate-Bot sprite. `frame` is one of:
        idle_0, idle_1 — subtle breathing (±1px head bob)
        walk_0, walk_1 — alternating step with arm swing
    Other frame strings fall back to idle_0.
    """
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head_y = 6
    body_y = 24
    left_leg_y_off = 0
    right_leg_y_off = 0
    left_arm_y_off = 0
    right_arm_y_off = 0

    if frame == "idle_1":
        head_y = 7  # slight breathing motion
    elif frame == "walk_0":
        # left leg forward (lifts up), right leg planted; arms swing opposite
        left_leg_y_off = -2
        right_leg_y_off = 0
        left_arm_y_off = 1
        right_arm_y_off = -1
        head_y = 6
    elif frame == "walk_1":
        # right leg forward, left planted; arms reverse
        left_leg_y_off = 0
        right_leg_y_off = -2
        left_arm_y_off = -1
        right_arm_y_off = 1
        head_y = 6

    _crate_bot_base(
        d, head_y, body_y,
        left_leg_y_off, right_leg_y_off,
        left_arm_y_off, right_arm_y_off,
    )
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


