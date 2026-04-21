"""Three Johnny-5-inspired mascot candidates at different pixel-art fidelities.

All three share the Johnny 5 silhouette: tank treads at the base, tall thin
body, segmented neck, large expressive eyes, articulated arms. The difference
is resolution + palette depth:

- candidate-8bit  (48x48, 6 colors)   — NES/Pico-8 era vibe
- candidate-16bit (64x64, 14 colors)  — SNES / Genesis era, subtle shading
- candidate-32bit (96x96, 28 colors)  — PS1-2D / Symphony-of-the-Night era

Each is drawn procedurally (no external asset files). Run this module to
write showcase cards into _shorts/character/candidates/johnny5/.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from . import config as C


# ---------- Shared palette families (Johnny 5 reads as chrome + warning lights) ----------

# 8-bit (limited, high-contrast)
P8 = {
    "bg":        (240, 230, 210),
    "chassis":   (178, 182, 192),  # light steel
    "chassis_d": (90, 96, 110),    # dark steel / outline
    "eye":       (255, 255, 255),
    "pupil":     (24, 28, 40),
    "accent":    (220, 62, 60),    # warning red
    "outline":   (18, 20, 28),
}

# 16-bit (more tonal range — adds mids)
P16 = {
    "bg":         (232, 226, 210),
    "chassis_hi": (210, 216, 228),
    "chassis":    (168, 174, 186),
    "chassis_m":  (120, 126, 140),
    "chassis_d":  (70, 78, 94),
    "eye_white":  (250, 250, 255),
    "eye_iris":   (68, 158, 210),   # blue iris (Johnny 5's are distinctive)
    "pupil":      (18, 22, 34),
    "accent":     (220, 62, 60),
    "accent_hi":  (248, 128, 124),
    "amber":      (244, 200, 72),
    "outline":    (16, 18, 28),
}

# 32-bit (rich shading; adds more mids + highlights)
P32 = {
    "bg":         (226, 220, 204),
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


# ---------- 8-bit, 48x48 ----------

def johnny5_8bit() -> Image.Image:
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = P8
    # Treads (base, 2 tracks side by side)
    _px(d, 8, 40, p["outline"], 32, 7)
    _px(d, 9, 41, p["chassis_d"], 30, 5)
    # Tread links
    for x in range(10, 40, 4):
        _px(d, x, 42, p["outline"], 2, 3)
    # Wheel dots
    _px(d, 11, 43, p["chassis"], 1, 1)
    _px(d, 36, 43, p["chassis"], 1, 1)

    # Torso (narrow rectangle)
    _px(d, 19, 26, p["outline"], 10, 14)
    _px(d, 20, 27, p["chassis"], 8, 12)
    # Chest warning panel
    _px(d, 21, 31, p["outline"], 6, 3)
    _px(d, 22, 32, p["accent"], 4, 1)

    # Shoulders (flared)
    _px(d, 15, 22, p["outline"], 5, 6)
    _px(d, 28, 22, p["outline"], 5, 6)
    _px(d, 16, 23, p["chassis"], 3, 4)
    _px(d, 29, 23, p["chassis"], 3, 4)

    # Arms (hanging forward)
    _px(d, 13, 26, p["outline"], 3, 10)
    _px(d, 32, 26, p["outline"], 3, 10)
    _px(d, 14, 27, p["chassis_d"], 1, 8)
    _px(d, 33, 27, p["chassis_d"], 1, 8)
    # Claws
    _px(d, 12, 35, p["outline"], 5, 3)
    _px(d, 31, 35, p["outline"], 5, 3)

    # Neck (segmented)
    _px(d, 22, 20, p["outline"], 4, 6)
    _px(d, 23, 21, p["chassis_d"], 2, 4)

    # Head (Johnny 5 is wider than tall)
    _px(d, 14, 8, p["outline"], 20, 14)
    _px(d, 15, 9, p["chassis"], 18, 12)

    # Eyes (huge — the iconic feature)
    _px(d, 17, 12, p["outline"], 6, 6)
    _px(d, 25, 12, p["outline"], 6, 6)
    _px(d, 18, 13, p["eye"], 4, 4)
    _px(d, 26, 13, p["eye"], 4, 4)
    _px(d, 19, 14, p["pupil"], 2, 2)
    _px(d, 27, 14, p["pupil"], 2, 2)

    # Antenna
    _px(d, 23, 4, p["outline"], 2, 5)
    _px(d, 22, 2, p["accent"], 4, 3)
    return img


# ---------- 16-bit, 64x64 ----------

def johnny5_16bit() -> Image.Image:
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = P16

    # Treads (2 tread belts, more defined)
    _px(d, 8, 50, p["outline"], 48, 12)
    _px(d, 9, 51, p["chassis_d"], 46, 10)
    # Tread link shadow
    for x in range(10, 55, 4):
        _px(d, x, 52, p["outline"], 2, 8)
        _px(d, x + 1, 53, p["chassis_m"], 1, 6)
    # Wheels (front/back bigger, visible through tread)
    _px(d, 11, 55, p["outline"], 6, 6)
    _px(d, 12, 56, p["chassis"], 4, 4)
    _px(d, 13, 57, p["chassis_d"], 2, 2)
    _px(d, 47, 55, p["outline"], 6, 6)
    _px(d, 48, 56, p["chassis"], 4, 4)
    _px(d, 49, 57, p["chassis_d"], 2, 2)
    # Middle wheel
    _px(d, 29, 56, p["outline"], 6, 5)
    _px(d, 30, 57, p["chassis"], 4, 3)

    # Treads top hat cover
    _px(d, 12, 46, p["outline"], 40, 4)
    _px(d, 13, 47, p["chassis_hi"], 38, 2)

    # Main torso / chassis
    _px(d, 24, 30, p["outline"], 16, 18)
    _px(d, 25, 31, p["chassis"], 14, 16)
    _px(d, 25, 31, p["chassis_hi"], 14, 2)  # top highlight
    # Chest sensor panel
    _px(d, 28, 35, p["outline"], 8, 6)
    _px(d, 29, 36, p["chassis_d"], 6, 4)
    _px(d, 30, 37, p["amber"], 2, 1)
    _px(d, 33, 37, p["accent"], 2, 1)
    # Side vents
    _px(d, 26, 40, p["outline"], 1, 5)
    _px(d, 37, 40, p["outline"], 1, 5)

    # Shoulders (big, ribbed — classic Johnny 5)
    _px(d, 16, 26, p["outline"], 10, 8)
    _px(d, 38, 26, p["outline"], 10, 8)
    _px(d, 17, 27, p["chassis"], 8, 6)
    _px(d, 39, 27, p["chassis"], 8, 6)
    _px(d, 17, 27, p["chassis_hi"], 8, 1)
    _px(d, 39, 27, p["chassis_hi"], 8, 1)
    # Shoulder joint dots (amber)
    _px(d, 21, 29, p["amber"], 2, 2)
    _px(d, 41, 29, p["amber"], 2, 2)

    # Arms (upper arm, forearm, gripper — classic lanky)
    # Upper (from shoulder down)
    _px(d, 14, 32, p["outline"], 4, 10)
    _px(d, 46, 32, p["outline"], 4, 10)
    _px(d, 15, 33, p["chassis_m"], 2, 8)
    _px(d, 47, 33, p["chassis_m"], 2, 8)
    # Elbow joint
    _px(d, 13, 42, p["outline"], 6, 4)
    _px(d, 45, 42, p["outline"], 6, 4)
    _px(d, 14, 43, p["chassis_d"], 4, 2)
    _px(d, 46, 43, p["chassis_d"], 4, 2)
    # Forearm
    _px(d, 12, 46, p["outline"], 4, 6)
    _px(d, 48, 46, p["outline"], 4, 6)
    _px(d, 13, 47, p["chassis_m"], 2, 4)
    _px(d, 49, 47, p["chassis_m"], 2, 4)
    # Pincer claws
    _px(d, 10, 51, p["outline"], 4, 4)
    _px(d, 14, 51, p["outline"], 4, 4)
    _px(d, 46, 51, p["outline"], 4, 4)
    _px(d, 50, 51, p["outline"], 4, 4)

    # Neck (telescoping segments)
    _px(d, 29, 22, p["outline"], 6, 8)
    _px(d, 30, 23, p["chassis_d"], 4, 6)
    _px(d, 30, 24, p["chassis_m"], 4, 1)  # segment line
    _px(d, 30, 27, p["chassis_m"], 4, 1)  # segment line

    # Head — wide and low, with distinctive shape (visor-like face)
    _px(d, 16, 6, p["outline"], 32, 18)
    _px(d, 17, 7, p["chassis"], 30, 16)
    _px(d, 17, 7, p["chassis_hi"], 30, 2)
    # Face recess (darker area behind eyes)
    _px(d, 19, 12, p["outline"], 26, 8)
    _px(d, 20, 13, p["chassis_d"], 24, 6)

    # Eyes (BIG round eyes)
    # Left eye
    _px(d, 22, 12, p["outline"], 8, 8)
    _px(d, 23, 13, p["eye_white"], 6, 6)
    _px(d, 24, 14, p["eye_iris"], 4, 4)
    _px(d, 25, 15, p["pupil"], 2, 2)
    _px(d, 25, 14, (255, 255, 255), 1, 1)  # glint
    # Right eye
    _px(d, 34, 12, p["outline"], 8, 8)
    _px(d, 35, 13, p["eye_white"], 6, 6)
    _px(d, 36, 14, p["eye_iris"], 4, 4)
    _px(d, 37, 15, p["pupil"], 2, 2)
    _px(d, 37, 14, (255, 255, 255), 1, 1)

    # Eyebrow panels above eyes (mechanical "expression")
    _px(d, 22, 10, p["outline"], 8, 2)
    _px(d, 34, 10, p["outline"], 8, 2)
    _px(d, 22, 10, p["chassis_d"], 8, 1)
    _px(d, 34, 10, p["chassis_d"], 8, 1)

    # Solar panels / antenna cluster on top of head
    _px(d, 30, 2, p["outline"], 4, 5)
    _px(d, 31, 3, p["amber"], 2, 3)
    _px(d, 26, 4, p["outline"], 4, 3)
    _px(d, 38, 4, p["outline"], 4, 3)
    _px(d, 27, 5, p["accent_hi"], 2, 1)
    _px(d, 39, 5, p["accent_hi"], 2, 1)

    return img


# ---------- 32-bit, 96x96 ----------

def johnny5_32bit() -> Image.Image:
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = P32

    # Treads — layered highlights/shadows for volume
    _px(d, 10, 76, p["outline"], 76, 20)
    _px(d, 11, 77, p["chassis_d2"], 74, 18)
    _px(d, 11, 77, p["chassis_d"], 74, 3)      # top highlight
    _px(d, 11, 93, p["outline"], 74, 3)        # ground shadow

    # Individual tread links
    for x in range(14, 84, 5):
        _px(d, x, 79, p["outline"], 3, 14)
        _px(d, x + 1, 80, p["chassis_m"], 1, 12)
        _px(d, x, 92, p["chassis_d2"], 3, 1)

    # Wheels visible through tread cutouts (3 wheels)
    for wx in [15, 45, 74]:
        _px(d, wx, 83, p["outline"], 10, 10)
        _px(d, wx + 1, 84, p["chassis_m"], 8, 8)
        _px(d, wx + 2, 85, p["chassis_d"], 6, 6)
        _px(d, wx + 4, 87, p["chassis_hi"], 2, 2)   # inner highlight

    # Tread mudguard / top cover
    _px(d, 14, 70, p["outline"], 68, 6)
    _px(d, 15, 71, p["chassis_hi"], 66, 2)
    _px(d, 15, 73, p["chassis"], 66, 2)
    _px(d, 15, 75, p["chassis_d"], 66, 1)

    # Torso (taller, more detailed chassis)
    _px(d, 36, 40, p["outline"], 24, 32)
    _px(d, 37, 41, p["chassis_m"], 22, 30)
    _px(d, 37, 41, p["chassis_hi"], 22, 3)     # top highlight
    _px(d, 37, 41, p["chassis_hi2"], 3, 30)    # left edge highlight
    _px(d, 56, 41, p["chassis_d"], 3, 30)      # right edge shadow

    # Chest instrument panel
    _px(d, 40, 48, p["outline"], 16, 14)
    _px(d, 41, 49, p["solar_dark"], 14, 12)
    # Panel dials/lights
    _px(d, 43, 52, p["amber"], 3, 3)
    _px(d, 43, 52, p["amber_hi"], 1, 1)
    _px(d, 50, 52, p["accent"], 3, 3)
    _px(d, 50, 52, p["accent_hi"], 1, 1)
    # Readout bar
    _px(d, 42, 58, p["amber"], 12, 2)
    _px(d, 42, 58, p["amber_hi"], 8, 1)

    # Side vent grilles
    _px(d, 38, 64, p["outline"], 2, 6)
    _px(d, 41, 64, p["outline"], 2, 6)
    _px(d, 53, 64, p["outline"], 2, 6)
    _px(d, 56, 64, p["outline"], 2, 6)

    # Shoulders (ribbed, more cylindrical)
    for side_x in [20, 62]:
        _px(d, side_x, 36, p["outline"], 16, 14)
        _px(d, side_x + 1, 37, p["chassis"], 14, 12)
        _px(d, side_x + 1, 37, p["chassis_hi"], 14, 2)
        # Rib detail
        _px(d, side_x + 2, 40, p["chassis_d"], 12, 1)
        _px(d, side_x + 2, 44, p["chassis_d"], 12, 1)
        # Joint dot
        _px(d, side_x + 6, 42, p["amber"], 4, 4)
        _px(d, side_x + 6, 42, p["amber_hi"], 2, 2)

    # Arms (lankier, 3 segments: upper, elbow, forearm)
    # Upper arm
    for ax in [18, 74]:
        _px(d, ax, 46, p["outline"], 6, 14)
        _px(d, ax + 1, 47, p["chassis_m"], 4, 12)
        _px(d, ax + 1, 47, p["chassis_hi2"], 1, 12)
    # Elbow joint
    for ex in [16, 72]:
        _px(d, ex, 60, p["outline"], 10, 6)
        _px(d, ex + 1, 61, p["chassis_d"], 8, 4)
        _px(d, ex + 4, 62, p["amber"], 2, 2)
    # Forearm
    for fx in [15, 75]:
        _px(d, fx, 66, p["outline"], 6, 10)
        _px(d, fx + 1, 67, p["chassis_m"], 4, 8)
    # Gripper claws (2-prong)
    for gx in [12, 76]:
        _px(d, gx, 76, p["outline"], 6, 6)
        _px(d, gx + 6, 76, p["outline"], 6, 6)
        _px(d, gx + 1, 77, p["chassis_d"], 4, 4)
        _px(d, gx + 7, 77, p["chassis_d"], 4, 4)

    # Neck (telescoping accordion, highly detailed)
    _px(d, 42, 26, p["outline"], 12, 14)
    _px(d, 43, 27, p["chassis_d"], 10, 12)
    for seg_y in [28, 31, 34, 37]:
        _px(d, 43, seg_y, p["chassis_m"], 10, 1)
        _px(d, 43, seg_y + 1, p["chassis_hi2"], 10, 1)

    # Head — wide with pronounced visor
    _px(d, 20, 8, p["outline"], 56, 24)
    _px(d, 21, 9, p["chassis"], 54, 22)
    _px(d, 21, 9, p["chassis_hi"], 54, 3)

    # Face/visor recess
    _px(d, 26, 14, p["outline"], 44, 14)
    _px(d, 27, 15, p["chassis_d2"], 42, 12)

    # Eyes (BIG, expressive — the iconic Johnny 5 feature)
    for eye_x in [30, 54]:
        # Socket
        _px(d, eye_x, 13, p["outline"], 14, 14)
        _px(d, eye_x + 1, 14, p["chassis_d2"], 12, 12)
        # White sclera
        _px(d, eye_x + 2, 15, p["eye_white"], 10, 10)
        # Iris (ringed with dark outline)
        _px(d, eye_x + 3, 16, p["eye_iris_d"], 8, 8)
        _px(d, eye_x + 4, 17, p["eye_iris"], 6, 6)
        _px(d, eye_x + 5, 18, p["eye_iris_hi"], 4, 4)
        # Pupil
        _px(d, eye_x + 6, 19, p["pupil"], 2, 2)
        # Catchlight glint
        _px(d, eye_x + 6, 17, p["glint"], 2, 1)
        _px(d, eye_x + 5, 16, p["glint"], 1, 1)

    # "Eyebrow" panel above the eyes (gives expression)
    _px(d, 28, 10, p["outline"], 40, 3)
    _px(d, 29, 11, p["chassis_d"], 38, 2)

    # Solar antenna cluster on top
    _px(d, 44, 2, p["outline"], 8, 7)
    _px(d, 45, 3, p["amber"], 6, 5)
    _px(d, 45, 3, p["amber_hi"], 6, 1)
    # Side tuning antennas
    _px(d, 30, 4, p["outline"], 3, 6)
    _px(d, 63, 4, p["outline"], 3, 6)
    _px(d, 30, 4, p["accent"], 3, 2)
    _px(d, 63, 4, p["accent"], 3, 2)
    _px(d, 31, 5, p["accent_hi"], 1, 1)
    _px(d, 64, 5, p["accent_hi"], 1, 1)

    return img


# ---------- Showcase rendering (reuses the earlier layout, fixed for wide sprites) ----------

CARD_W = 1080
CARD_H = 1920


def _wrap(text, font, max_width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit_font(text, font_path, start_size, max_width, draw):
    size = start_size
    while size > 18:
        f = ImageFont.truetype(font_path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
        size -= 4
    return ImageFont.truetype(font_path, 18)


def render_showcase(sprite, name, tagline, palette_hex, card_bg, out_path):
    img = Image.new("RGB", (CARD_W, CARD_H), card_bg)
    draw = ImageDraw.Draw(img)

    title_font = _fit_font(name.upper(), C.FONT_CAPTION_BOLD, 72, CARD_W - 80, draw)
    sub_font = ImageFont.truetype(C.FONT_CAPTION, 36)
    label_font = ImageFont.truetype(C.FONT_LABEL, 28)
    mono_font = ImageFont.truetype(C.FONT_MONO, 30)

    # Title
    draw.text((CARD_W // 2, 80), name.upper(),
              fill=(20, 20, 30), font=title_font, anchor="mt")

    # Native reference (shown at 4x)
    ref_scale = 4
    ref_img = sprite.resize((sprite.width * ref_scale, sprite.height * ref_scale),
                            Image.NEAREST)
    ref_x = CARD_W // 2 - ref_img.width // 2
    ref_y = 220
    draw.text((CARD_W // 2, 180), f"NATIVE {sprite.width} x {sprite.height}",
              fill=(90, 90, 105), font=label_font, anchor="mt")
    img.paste(ref_img, (ref_x, ref_y), ref_img)
    draw.rectangle([ref_x - 4, ref_y - 4, ref_x + ref_img.width + 4,
                    ref_y + ref_img.height + 4], outline=(120, 120, 130), width=2)

    # Large showcase — size so the tallest dimension is ~700 px
    target = 700
    hero_scale = max(1, target // max(sprite.width, sprite.height))
    hero = sprite.resize((sprite.width * hero_scale, sprite.height * hero_scale),
                         Image.NEAREST)
    hx = CARD_W // 2 - hero.width // 2
    hy = ref_y + ref_img.height + 70
    # Platform shadow ellipse
    draw.ellipse([hx + hero.width // 2 - 200, hy + hero.height + 10,
                  hx + hero.width // 2 + 200, hy + hero.height + 45],
                 fill=(180, 170, 155))
    img.paste(hero, (hx, hy), hero)

    # Tagline
    tag_y = hy + hero.height + 70
    max_tag_w = CARD_W - 100
    for chunk in tagline.split("|"):
        lines = _wrap(chunk.strip(), sub_font, max_tag_w, draw)
        for line in lines:
            draw.text((CARD_W // 2, tag_y), line,
                      fill=(30, 30, 45), font=sub_font, anchor="mt")
            tag_y += 46
        tag_y += 10

    # Palette swatches
    pal_y = CARD_H - 320
    draw.text((CARD_W // 2, pal_y - 50), "PALETTE",
              fill=(90, 90, 105), font=label_font, anchor="mt")
    sw = 140
    sh = 140
    gap = 24
    total_w = len(palette_hex) * sw + (len(palette_hex) - 1) * gap
    sx = (CARD_W - total_w) // 2
    for i, (pname, phex, prgb) in enumerate(palette_hex):
        x = sx + i * (sw + gap)
        draw.rectangle([x, pal_y, x + sw, pal_y + sh],
                       fill=prgb, outline=(40, 40, 50), width=2)
        draw.text((x + sw // 2, pal_y + sh + 12), pname,
                  fill=(30, 30, 45), font=label_font, anchor="mt")
        draw.text((x + sw // 2, pal_y + sh + 46), phex,
                  fill=(90, 90, 105), font=mono_font, anchor="mt")

    draw.text((CARD_W // 2, CARD_H - 50),
              "Candidate preview - pick one to lock", fill=(120, 120, 135),
              font=label_font, anchor="mb")

    img.save(out_path)
    return out_path


def _hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def main():
    out_dir = C.CHARACTER_DIR / "candidates" / "johnny5"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 8-bit card
    s8 = johnny5_8bit()
    render_showcase(
        s8,
        "Johnny 5 - 8-bit",
        "48x48 sprite, 6-color palette | NES/Pico-8 era vibe, "
        "chunky silhouette, maximum readability at phone thumbnail size",
        [("CHASSIS", _hex(P8["chassis"]), P8["chassis"]),
         ("DARK",    _hex(P8["chassis_d"]), P8["chassis_d"]),
         ("ACCENT",  _hex(P8["accent"]), P8["accent"]),
         ("OUTLINE", _hex(P8["outline"]), P8["outline"])],
        P8["bg"],
        out_dir / "candidate-johnny5-8bit.png",
    )
    s8.save(out_dir / "sprite-johnny5-8bit.png")

    # 16-bit card
    s16 = johnny5_16bit()
    render_showcase(
        s16,
        "Johnny 5 - 16-bit",
        "64x64 sprite, 14-color palette | SNES / Genesis era, "
        "subtle shading, visible tread links, blue iris",
        [("CHASSIS", _hex(P16["chassis"]), P16["chassis"]),
         ("IRIS",    _hex(P16["eye_iris"]), P16["eye_iris"]),
         ("ACCENT",  _hex(P16["accent"]), P16["accent"]),
         ("AMBER",   _hex(P16["amber"]), P16["amber"]),
         ("OUTLINE", _hex(P16["outline"]), P16["outline"])],
        P16["bg"],
        out_dir / "candidate-johnny5-16bit.png",
    )
    s16.save(out_dir / "sprite-johnny5-16bit.png")

    # 32-bit card
    s32 = johnny5_32bit()
    render_showcase(
        s32,
        "Johnny 5 - 32-bit",
        "96x96 sprite, 28-color palette | PS1-2D era, "
        "rich shading and panel detail, catchlight glints, telescoping neck",
        [("CHASSIS HI", _hex(P32["chassis_hi"]), P32["chassis_hi"]),
         ("CHASSIS",    _hex(P32["chassis"]), P32["chassis"]),
         ("IRIS",       _hex(P32["eye_iris"]), P32["eye_iris"]),
         ("ACCENT",     _hex(P32["accent"]), P32["accent"]),
         ("AMBER",      _hex(P32["amber"]), P32["amber"]),
         ("OUTLINE",    _hex(P32["outline"]), P32["outline"])],
        P32["bg"],
        out_dir / "candidate-johnny5-32bit.png",
    )
    s32.save(out_dir / "sprite-johnny5-32bit.png")

    print(f"3 Johnny 5 candidates rendered in {out_dir}")


if __name__ == "__main__":
    main()
