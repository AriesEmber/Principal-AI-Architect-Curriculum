"""Pixel sprite generation.

Locked mascot: **Johnny 5 — 32-bit** (96x96, PS1-2D era palette). Drawn
procedurally so animation frames live in code, not binary diffs.
Frames: idle_0, idle_1, walk_0, walk_1.
"""
from PIL import Image, ImageDraw
from .config import (
    COLOR_PRIMARY, COLOR_OUTLINE, COLOR_ACCENT, COLOR_SHADOW,
    COLOR_USER_SKIN, COLOR_USER_SHIRT,
)

SPRITE_SIZE = 96

# Johnny 5 (32-bit) palette — kept self-contained so the UI palette can change
# independently of the robot's colors.
J5 = {
    "chassis_hi":  (224, 230, 244),
    "chassis_hi2": (196, 204, 220),
    "chassis":     (162, 170, 184),
    "chassis_m":   (122, 130, 146),
    "chassis_d":   (82, 90, 108),
    "chassis_d2":  (46, 54, 72),
    "eye_white":   (250, 252, 255),
    "eye_iris_hi": (132, 196, 232),
    "eye_iris":    (58, 148, 204),
    "eye_iris_d":  (36, 92, 142),
    "pupil":       (14, 18, 30),
    "glint":       (255, 255, 255),
    "accent":      (216, 56, 54),
    "accent_hi":   (248, 128, 124),
    "accent_d":    (146, 32, 34),
    "amber":       (244, 200, 72),
    "amber_hi":    (252, 228, 148),
    "solar_dark":  (28, 32, 50),
    "outline":     (14, 16, 26),
}


def _px(d: ImageDraw.ImageDraw, x: int, y: int, color, w: int = 1, h: int = 1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def _j5_head_torso(d: ImageDraw.ImageDraw, head_y_off: int = 0):
    """Draw head, torso, chest, neck, antennas. `head_y_off` shifts the head a
    pixel or two for idle breathing / walk bob."""
    p = J5
    hy = 8 + head_y_off
    # Head
    _px(d, 20, hy, p["outline"], 56, 24)
    _px(d, 21, hy + 1, p["chassis"], 54, 22)
    _px(d, 21, hy + 1, p["chassis_hi"], 54, 3)
    # Visor recess
    _px(d, 26, hy + 6, p["outline"], 44, 14)
    _px(d, 27, hy + 7, p["chassis_d2"], 42, 12)
    # Eyes
    for eye_x in [30, 54]:
        _px(d, eye_x, hy + 5, p["outline"], 14, 14)
        _px(d, eye_x + 1, hy + 6, p["chassis_d2"], 12, 12)
        _px(d, eye_x + 2, hy + 7, p["eye_white"], 10, 10)
        _px(d, eye_x + 3, hy + 8, p["eye_iris_d"], 8, 8)
        _px(d, eye_x + 4, hy + 9, p["eye_iris"], 6, 6)
        _px(d, eye_x + 5, hy + 10, p["eye_iris_hi"], 4, 4)
        _px(d, eye_x + 6, hy + 11, p["pupil"], 2, 2)
        _px(d, eye_x + 6, hy + 9, p["glint"], 2, 1)
        _px(d, eye_x + 5, hy + 8, p["glint"], 1, 1)
    # Eyebrow panel
    _px(d, 28, hy + 2, p["outline"], 40, 3)
    _px(d, 29, hy + 3, p["chassis_d"], 38, 2)
    # Top solar panel + antennas
    _px(d, 44, hy - 6, p["outline"], 8, 7)
    _px(d, 45, hy - 5, p["amber"], 6, 5)
    _px(d, 45, hy - 5, p["amber_hi"], 6, 1)
    _px(d, 30, hy - 4, p["outline"], 3, 6)
    _px(d, 63, hy - 4, p["outline"], 3, 6)
    _px(d, 30, hy - 4, p["accent"], 3, 2)
    _px(d, 63, hy - 4, p["accent"], 3, 2)
    _px(d, 31, hy - 3, p["accent_hi"], 1, 1)
    _px(d, 64, hy - 3, p["accent_hi"], 1, 1)

    # Neck (telescoping)
    _px(d, 42, 26, p["outline"], 12, 14)
    _px(d, 43, 27, p["chassis_d"], 10, 12)
    for seg_y in [28, 31, 34, 37]:
        _px(d, 43, seg_y, p["chassis_m"], 10, 1)
        _px(d, 43, seg_y + 1, p["chassis_hi2"], 10, 1)

    # Torso
    _px(d, 36, 40, p["outline"], 24, 32)
    _px(d, 37, 41, p["chassis_m"], 22, 30)
    _px(d, 37, 41, p["chassis_hi"], 22, 3)
    _px(d, 37, 41, p["chassis_hi2"], 3, 30)
    _px(d, 56, 41, p["chassis_d"], 3, 30)
    # Chest instrument panel
    _px(d, 40, 48, p["outline"], 16, 14)
    _px(d, 41, 49, p["solar_dark"], 14, 12)
    _px(d, 43, 52, p["amber"], 3, 3)
    _px(d, 43, 52, p["amber_hi"], 1, 1)
    _px(d, 50, 52, p["accent"], 3, 3)
    _px(d, 50, 52, p["accent_hi"], 1, 1)
    _px(d, 42, 58, p["amber"], 12, 2)
    _px(d, 42, 58, p["amber_hi"], 8, 1)
    # Side vent grilles
    _px(d, 38, 64, p["outline"], 2, 6)
    _px(d, 41, 64, p["outline"], 2, 6)
    _px(d, 53, 64, p["outline"], 2, 6)
    _px(d, 56, 64, p["outline"], 2, 6)


def _j5_arms(d: ImageDraw.ImageDraw, left_y_off: int = 0, right_y_off: int = 0):
    """Draw the two shoulder + arm assemblies. Per-side vertical offset gives
    a subtle swing for walk frames."""
    p = J5
    for side_x, y_off in ((20, left_y_off), (62, right_y_off)):
        # Shoulder
        _px(d, side_x, 36 + y_off, p["outline"], 16, 14)
        _px(d, side_x + 1, 37 + y_off, p["chassis"], 14, 12)
        _px(d, side_x + 1, 37 + y_off, p["chassis_hi"], 14, 2)
        _px(d, side_x + 2, 40 + y_off, p["chassis_d"], 12, 1)
        _px(d, side_x + 2, 44 + y_off, p["chassis_d"], 12, 1)
        _px(d, side_x + 6, 42 + y_off, p["amber"], 4, 4)
        _px(d, side_x + 6, 42 + y_off, p["amber_hi"], 2, 2)

    # Upper arm
    for ax, y_off in ((18, left_y_off), (74, right_y_off)):
        _px(d, ax, 46 + y_off, p["outline"], 6, 14)
        _px(d, ax + 1, 47 + y_off, p["chassis_m"], 4, 12)
        _px(d, ax + 1, 47 + y_off, p["chassis_hi2"], 1, 12)
    # Elbow
    for ex, y_off in ((16, left_y_off), (72, right_y_off)):
        _px(d, ex, 60 + y_off, p["outline"], 10, 6)
        _px(d, ex + 1, 61 + y_off, p["chassis_d"], 8, 4)
        _px(d, ex + 4, 62 + y_off, p["amber"], 2, 2)
    # Forearm
    for fx, y_off in ((15, left_y_off), (75, right_y_off)):
        _px(d, fx, 66 + y_off, p["outline"], 6, 10)
        _px(d, fx + 1, 67 + y_off, p["chassis_m"], 4, 8)
    # Grippers
    for gx, y_off in ((12, left_y_off), (76, right_y_off)):
        _px(d, gx, 76 + y_off, p["outline"], 6, 6)
        _px(d, gx + 6, 76 + y_off, p["outline"], 6, 6)
        _px(d, gx + 1, 77 + y_off, p["chassis_d"], 4, 4)
        _px(d, gx + 7, 77 + y_off, p["chassis_d"], 4, 4)


def _j5_treads(d: ImageDraw.ImageDraw, link_shift: int = 0):
    """Draw tank treads. `link_shift` cycles the tread-link positions left/right
    so walking reads as motion even though the sprite stays centered."""
    p = J5
    # Main tread belt
    _px(d, 10, 76, p["outline"], 76, 20)
    _px(d, 11, 77, p["chassis_d2"], 74, 18)
    _px(d, 11, 77, p["chassis_d"], 74, 3)
    _px(d, 11, 93, p["outline"], 74, 3)

    # Tread links — slide based on link_shift
    start = 14 + (link_shift % 5)
    for x in range(start, 84, 5):
        if 10 <= x <= 82:
            _px(d, x, 79, p["outline"], 3, 14)
            _px(d, x + 1, 80, p["chassis_m"], 1, 12)
            _px(d, x, 92, p["chassis_d2"], 3, 1)

    # Visible wheels (3)
    for wx in [15, 45, 74]:
        _px(d, wx, 83, p["outline"], 10, 10)
        _px(d, wx + 1, 84, p["chassis_m"], 8, 8)
        _px(d, wx + 2, 85, p["chassis_d"], 6, 6)
        _px(d, wx + 4, 87, p["chassis_hi"], 2, 2)

    # Tread mudguard / top cover
    _px(d, 14, 70, p["outline"], 68, 6)
    _px(d, 15, 71, p["chassis_hi"], 66, 2)
    _px(d, 15, 73, p["chassis"], 66, 2)
    _px(d, 15, 75, p["chassis_d"], 66, 1)


def placeholder_robot(frame: str = "idle_0") -> Image.Image:
    """Johnny 5 32-bit sprite. `frame`:
        idle_0, idle_1 — subtle head bob (±1px)
        walk_0, walk_1 — tread links shift + arms swing opposite
    """
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head_y_off = 0
    left_arm_off = 0
    right_arm_off = 0
    link_shift = 0

    if frame == "idle_1":
        head_y_off = 1
    elif frame == "walk_0":
        head_y_off = 1
        left_arm_off = -1
        right_arm_off = 1
        link_shift = 2
    elif frame == "walk_1":
        head_y_off = 0
        left_arm_off = 1
        right_arm_off = -1
        link_shift = 4

    _j5_treads(d, link_shift)
    _j5_arms(d, left_arm_off, right_arm_off)
    _j5_head_torso(d, head_y_off)
    return img


def placeholder_user(frame: str = "idle_0") -> Image.Image:
    """Kept for backward compatibility. The top area now uses input_display
    instead of this sprite, but the function stays in case we ever want a user
    avatar elsewhere."""
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _px(d, 18, 8, COLOR_OUTLINE, 12, 12)
    _px(d, 19, 9, COLOR_USER_SKIN, 10, 10)
    _px(d, 21, 13, COLOR_OUTLINE, 2, 2)
    _px(d, 25, 13, COLOR_OUTLINE, 2, 2)
    _px(d, 22, 16, COLOR_OUTLINE, 4, 1)
    _px(d, 14, 22, COLOR_OUTLINE, 20, 14)
    _px(d, 15, 23, COLOR_USER_SHIRT, 18, 12)
    _px(d, 10, 23, COLOR_OUTLINE, 4, 10)
    _px(d, 11, 24, COLOR_USER_SKIN, 3, 8)
    _px(d, 34, 23, COLOR_OUTLINE, 4, 10)
    _px(d, 35, 24, COLOR_USER_SKIN, 3, 8)
    _px(d, 16, 36, COLOR_OUTLINE, 6, 10)
    _px(d, 26, 36, COLOR_OUTLINE, 6, 10)
    return img


def upscale_pixel(img: Image.Image, factor: int) -> Image.Image:
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)
