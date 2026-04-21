"""Three mascot candidate sprites (single showcase frame each).

Each concept is drawn pixel-by-pixel on a 48x48 grid, then presented on a
showcase card with its name, palette swatches, and tagline. Elvis picks one,
and that sprite becomes the locked character under _shorts/character/.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from . import config as C


SPRITE_W = 48
SPRITE_H = 48


def _px(d, x, y, color, w=1, h=1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


# ---------- Concept 1: Crate-Bot the Courier ----------
# Palette A: Industrial Workshop
C1_PRIMARY = (210, 105, 59)      # #D2693B terracotta
C1_SECONDARY = (62, 76, 94)      # #3E4C5E slate
C1_ACCENT = (244, 211, 94)       # #F4D35E safety amber
C1_OUTLINE = (31, 36, 48)        # #1F2430
C1_SHADOW = (138, 79, 46)        # #8A4F2E
C1_BG = (234, 222, 205)


def concept_1_sprite():
    """Crate-Bot: boxy, monocular visor, wooden crate on back."""
    img = Image.new("RGBA", (SPRITE_W, SPRITE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Crate on back (peek from behind shoulders)
    _px(d, 32, 20, C1_SHADOW, 10, 16)
    _px(d, 33, 21, (170, 110, 60), 8, 14)  # wood brown
    _px(d, 34, 23, C1_OUTLINE, 6, 1)
    _px(d, 34, 30, C1_OUTLINE, 6, 1)
    _px(d, 37, 22, C1_OUTLINE, 1, 12)  # vertical plank line
    # Head (cube, larger)
    _px(d, 12, 6, C1_OUTLINE, 22, 18)
    _px(d, 13, 7, C1_PRIMARY, 20, 16)
    # Visor slit (wide, central, single eye)
    _px(d, 15, 13, C1_OUTLINE, 16, 5)
    _px(d, 17, 14, C1_SECONDARY, 12, 3)
    _px(d, 22, 15, C1_ACCENT, 4, 1)  # glowing pupil
    # Head rivet corners
    _px(d, 14, 8, C1_ACCENT, 1, 1)
    _px(d, 31, 8, C1_ACCENT, 1, 1)
    # Bolt / antenna on top
    _px(d, 22, 3, C1_OUTLINE, 4, 3)
    _px(d, 23, 4, C1_ACCENT, 2, 1)
    # Body (cube, slightly wider than head)
    _px(d, 10, 24, C1_OUTLINE, 26, 16)
    _px(d, 11, 25, C1_PRIMARY, 24, 14)
    # Chest plate divider
    _px(d, 22, 25, C1_SECONDARY, 2, 14)
    # Badge / delivery emblem
    _px(d, 16, 29, C1_ACCENT, 4, 4)
    _px(d, 17, 30, C1_OUTLINE, 2, 2)
    # Arms (thick, at sides)
    _px(d, 7, 26, C1_OUTLINE, 4, 11)
    _px(d, 8, 27, C1_PRIMARY, 3, 9)
    _px(d, 35, 26, C1_OUTLINE, 4, 11)
    _px(d, 36, 27, C1_PRIMARY, 3, 9)
    # Gloves
    _px(d, 7, 36, C1_SECONDARY, 4, 3)
    _px(d, 35, 36, C1_SECONDARY, 4, 3)
    # Stubby legs
    _px(d, 14, 40, C1_OUTLINE, 7, 8)
    _px(d, 25, 40, C1_OUTLINE, 7, 8)
    _px(d, 15, 41, C1_SECONDARY, 5, 6)
    _px(d, 26, 41, C1_SECONDARY, 5, 6)
    # Boot toe highlight
    _px(d, 15, 45, C1_ACCENT, 1, 1)
    _px(d, 26, 45, C1_ACCENT, 1, 1)
    return img


# ---------- Concept 2: Clip the Stock-Clerk ----------
# Palette B: Warm Chrome
C2_PRIMARY = (232, 168, 124)     # #E8A87C peach
C2_SECONDARY = (44, 62, 77)      # #2C3E4D graphite
C2_ACCENT = (133, 220, 176)      # #85DCB0 mint
C2_OUTLINE = (26, 31, 43)        # #1A1F2B
C2_SHADOW = (184, 116, 80)       # #B87450
C2_BG = (232, 222, 204)


def concept_2_sprite():
    """Clip: large rounded-rect head, two oval eyes, clipboard on chest,
    wheeled base."""
    img = Image.new("RGBA", (SPRITE_W, SPRITE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Head (rounded rect, big)
    _px(d, 10, 4, C2_OUTLINE, 28, 22)
    _px(d, 11, 5, C2_PRIMARY, 26, 20)
    # Round the corners
    _px(d, 10, 4, (0, 0, 0, 0), 1, 1)
    _px(d, 37, 4, (0, 0, 0, 0), 1, 1)
    _px(d, 10, 25, (0, 0, 0, 0), 1, 1)
    _px(d, 37, 25, (0, 0, 0, 0), 1, 1)
    # Eyes (two big ovals)
    _px(d, 16, 12, C2_OUTLINE, 5, 6)
    _px(d, 27, 12, C2_OUTLINE, 5, 6)
    _px(d, 17, 13, (255, 255, 255), 3, 4)
    _px(d, 28, 13, (255, 255, 255), 3, 4)
    _px(d, 18, 15, C2_SECONDARY, 2, 2)  # pupil
    _px(d, 29, 15, C2_SECONDARY, 2, 2)
    # Eyebrow highlight (cute)
    _px(d, 16, 10, C2_SECONDARY, 5, 1)
    _px(d, 27, 10, C2_SECONDARY, 5, 1)
    # Smile
    _px(d, 20, 21, C2_SECONDARY, 8, 1)
    _px(d, 19, 20, C2_SECONDARY, 1, 1)
    _px(d, 28, 20, C2_SECONDARY, 1, 1)
    # Cheeks (mint blush)
    _px(d, 14, 18, C2_ACCENT, 2, 2)
    _px(d, 32, 18, C2_ACCENT, 2, 2)
    # Neck
    _px(d, 20, 26, C2_SECONDARY, 8, 2)
    # Body (smaller than head)
    _px(d, 13, 28, C2_OUTLINE, 22, 12)
    _px(d, 14, 29, C2_PRIMARY, 20, 10)
    # Clipboard on chest
    _px(d, 18, 30, C2_OUTLINE, 12, 9)
    _px(d, 19, 31, (245, 240, 225), 10, 7)  # paper
    _px(d, 20, 32, C2_SECONDARY, 8, 1)  # line 1
    _px(d, 20, 34, C2_SECONDARY, 6, 1)  # line 2
    _px(d, 20, 36, C2_ACCENT, 4, 1)  # check mark (green)
    _px(d, 23, 29, C2_ACCENT, 2, 2)  # clip on top
    # Arms (short, rounded)
    _px(d, 10, 29, C2_OUTLINE, 3, 9)
    _px(d, 35, 29, C2_OUTLINE, 3, 9)
    _px(d, 11, 30, C2_PRIMARY, 2, 7)
    _px(d, 36, 30, C2_PRIMARY, 2, 7)
    # Wheeled base (single wheel)
    _px(d, 18, 40, C2_OUTLINE, 12, 7)
    _px(d, 19, 41, C2_SECONDARY, 10, 5)
    _px(d, 20, 43, C2_PRIMARY, 8, 2)  # hubcap shine
    _px(d, 23, 43, C2_ACCENT, 2, 1)  # spark
    return img


# ---------- Concept 3: Nyx the Night-Shift Librarian-Bot ----------
# Palette C: Midnight Courier
C3_PRIMARY = (107, 91, 149)      # #6B5B95 muted violet
C3_SECONDARY = (240, 228, 211)   # #F0E4D3 cream
C3_ACCENT = (255, 182, 39)       # #FFB627 mustard gold
C3_OUTLINE = (27, 26, 46)        # #1B1A2E
C3_SHADOW = (74, 63, 107)        # #4A3F6B
C3_BG = (230, 226, 242)


def concept_3_sprite():
    """Nyx: taller hooded silhouette, gold eye-slots, floating parcel."""
    img = Image.new("RGBA", (SPRITE_W, SPRITE_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Hood outer silhouette (tall, pointed-ish)
    _px(d, 16, 2, C3_OUTLINE, 16, 4)
    _px(d, 14, 4, C3_OUTLINE, 20, 6)
    _px(d, 12, 8, C3_OUTLINE, 24, 14)
    # Hood inner fill
    _px(d, 17, 3, C3_PRIMARY, 14, 3)
    _px(d, 15, 5, C3_PRIMARY, 18, 5)
    _px(d, 13, 9, C3_PRIMARY, 22, 12)
    # Hood shadow inside (dark under hood)
    _px(d, 18, 10, C3_OUTLINE, 12, 8)
    # Glowing eye slots (gold)
    _px(d, 20, 13, C3_ACCENT, 2, 3)
    _px(d, 26, 13, C3_ACCENT, 2, 3)
    # Tiny glow dot (lighter)
    _px(d, 20, 13, (255, 240, 200), 1, 1)
    _px(d, 26, 13, (255, 240, 200), 1, 1)
    # Cloak body (flowing)
    _px(d, 11, 22, C3_OUTLINE, 26, 20)
    _px(d, 12, 23, C3_PRIMARY, 24, 18)
    # Cloak seam / clasp
    _px(d, 23, 22, C3_ACCENT, 2, 3)
    _px(d, 24, 23, C3_OUTLINE, 1, 1)
    # Cloak vertical folds (shadow)
    _px(d, 16, 24, C3_SHADOW, 1, 14)
    _px(d, 24, 24, C3_SHADOW, 1, 14)
    _px(d, 31, 24, C3_SHADOW, 1, 14)
    # Cloak bottom ragged edge
    _px(d, 11, 41, C3_OUTLINE, 26, 2)
    _px(d, 13, 42, C3_PRIMARY, 2, 1)
    _px(d, 17, 42, C3_PRIMARY, 3, 1)
    _px(d, 22, 42, C3_PRIMARY, 2, 1)
    _px(d, 26, 42, C3_PRIMARY, 3, 1)
    _px(d, 31, 42, C3_PRIMARY, 2, 1)
    # Arms (inside cloak, emerging at front)
    _px(d, 17, 26, C3_OUTLINE, 3, 10)
    _px(d, 28, 26, C3_OUTLINE, 3, 10)
    _px(d, 18, 27, C3_SHADOW, 2, 8)
    _px(d, 29, 27, C3_SHADOW, 2, 8)
    # Floating parcel in front (hovers at chest)
    _px(d, 21, 28, C3_ACCENT, 6, 6)
    _px(d, 22, 29, C3_SECONDARY, 4, 4)
    _px(d, 23, 31, C3_ACCENT, 2, 1)  # parcel band
    _px(d, 21, 30, C3_ACCENT, 6, 1)  # parcel band horizontal
    # Parcel glow sparkles
    _px(d, 20, 27, C3_ACCENT, 1, 1)
    _px(d, 27, 27, C3_ACCENT, 1, 1)
    _px(d, 20, 34, C3_ACCENT, 1, 1)
    _px(d, 27, 34, C3_ACCENT, 1, 1)
    # Feet (barely visible)
    _px(d, 18, 43, C3_OUTLINE, 4, 4)
    _px(d, 26, 43, C3_OUTLINE, 4, 4)
    return img


# ---------- Showcase card layout ----------

CARD_W = 1080
CARD_H = 1920


def _fit_font(text, font_path, start_size, max_width, draw):
    """Return the largest FreeTypeFont size that fits `text` within max_width."""
    size = start_size
    while size > 18:
        font = ImageFont.truetype(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(font_path, 18)


def _wrap(text, font, max_width, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_showcase(sprite, name, tagline, palette_hex, card_bg, out_path):
    img = Image.new("RGB", (CARD_W, CARD_H), card_bg)
    draw = ImageDraw.Draw(img)

    title_font = _fit_font(name.upper(), C.FONT_CAPTION_BOLD, 72, CARD_W - 80, draw)
    sub_font = ImageFont.truetype(C.FONT_CAPTION, 36)
    label_font = ImageFont.truetype(C.FONT_LABEL, 28)
    mono_font = ImageFont.truetype(C.FONT_MONO, 30)

    # Title strip
    draw.text((CARD_W // 2, 80), name.upper(),
              fill=(20, 20, 30), font=title_font, anchor="mt")

    # Native 48x48 reference panel (small)
    draw.text((CARD_W // 2, 200), "NATIVE 48 x 48",
              fill=(90, 90, 105), font=label_font, anchor="mt")
    native = sprite.resize((48 * 4, 48 * 4), Image.NEAREST)
    native_x = CARD_W // 2 - native.width // 2
    native_y = 250
    img.paste(native, (native_x, native_y), native)
    # Bounding frame on native
    draw.rectangle([native_x - 4, native_y - 4,
                    native_x + native.width + 4, native_y + native.height + 4],
                   outline=(120, 120, 130), width=2)

    # Large showcase (12x scale)
    scaled = sprite.resize((48 * 14, 48 * 14), Image.NEAREST)
    sc_x = CARD_W // 2 - scaled.width // 2
    sc_y = native_y + native.height + 80
    # Platform shadow
    draw.ellipse([sc_x + scaled.width // 2 - 200, sc_y + scaled.height + 20,
                  sc_x + scaled.width // 2 + 200, sc_y + scaled.height + 55],
                 fill=(180, 170, 155))
    img.paste(scaled, (sc_x, sc_y), scaled)

    # Tagline below large sprite (wrap each "|"-separated chunk to card width)
    tag_y = sc_y + scaled.height + 70
    max_tag_w = CARD_W - 100
    y_cursor = tag_y
    for chunk in tagline.split("|"):
        chunk = chunk.strip()
        lines = _wrap(chunk, sub_font, max_tag_w, draw)
        for line in lines:
            draw.text((CARD_W // 2, y_cursor), line,
                      fill=(30, 30, 45), font=sub_font, anchor="mt")
            y_cursor += 46
        y_cursor += 10

    # Palette swatches near bottom
    pal_y = CARD_H - 320
    draw.text((CARD_W // 2, pal_y - 50), "PALETTE",
              fill=(90, 90, 105), font=label_font, anchor="mt")
    swatch_w = 140
    swatch_h = 140
    gap = 24
    total_w = len(palette_hex) * swatch_w + (len(palette_hex) - 1) * gap
    start_x = (CARD_W - total_w) // 2
    for i, (name_s, hex_s, rgb) in enumerate(palette_hex):
        x = start_x + i * (swatch_w + gap)
        draw.rectangle([x, pal_y, x + swatch_w, pal_y + swatch_h],
                       fill=rgb, outline=(40, 40, 50), width=2)
        draw.text((x + swatch_w // 2, pal_y + swatch_h + 12),
                  name_s, fill=(30, 30, 45), font=label_font, anchor="mt")
        draw.text((x + swatch_w // 2, pal_y + swatch_h + 46),
                  hex_s, fill=(90, 90, 105), font=mono_font, anchor="mt")

    # Footer
    draw.text((CARD_W // 2, CARD_H - 50),
              "Candidate preview - pick one to lock", fill=(120, 120, 135),
              font=label_font, anchor="mb")

    img.save(out_path)
    return out_path


def main():
    out_dir = C.CHARACTER_DIR / "candidates"
    out_dir.mkdir(parents=True, exist_ok=True)

    render_showcase(
        concept_1_sprite(),
        "Crate-Bot the Courier",
        "Industrial Workshop palette | A Stardew-meets-Wall-E courier with a wooden crate on its back",
        [
            ("PRIMARY", "#D2693B", C1_PRIMARY),
            ("SECONDARY", "#3E4C5E", C1_SECONDARY),
            ("ACCENT", "#F4D35E", C1_ACCENT),
            ("OUTLINE", "#1F2430", C1_OUTLINE),
        ],
        C1_BG,
        out_dir / "candidate-1-crate-bot.png",
    )

    render_showcase(
        concept_2_sprite(),
        "Clip the Stock-Clerk",
        "Warm Chrome palette | Rounded head, clipboard on chest, wheeled base - the friendly retail associate archetype",
        [
            ("PRIMARY", "#E8A87C", C2_PRIMARY),
            ("SECONDARY", "#2C3E4D", C2_SECONDARY),
            ("ACCENT", "#85DCB0", C2_ACCENT),
            ("OUTLINE", "#1A1F2B", C2_OUTLINE),
        ],
        C2_BG,
        out_dir / "candidate-2-clip.png",
    )

    render_showcase(
        concept_3_sprite(),
        "Nyx the Night-Shift Archivist",
        "Midnight Courier palette | Tall hooded silhouette with glowing gold eye-slots and a floating parcel - premium archivist vibe",
        [
            ("PRIMARY", "#6B5B95", C3_PRIMARY),
            ("SECONDARY", "#F0E4D3", C3_SECONDARY),
            ("ACCENT", "#FFB627", C3_ACCENT),
            ("OUTLINE", "#1B1A2E", C3_OUTLINE),
        ],
        C3_BG,
        out_dir / "candidate-3-nyx.png",
    )

    # Also save raw sprites for later use
    concept_1_sprite().save(out_dir / "sprite-1-crate-bot.png")
    concept_2_sprite().save(out_dir / "sprite-2-clip.png")
    concept_3_sprite().save(out_dir / "sprite-3-nyx.png")

    print(f"3 candidates rendered in {out_dir}")


if __name__ == "__main__":
    main()
