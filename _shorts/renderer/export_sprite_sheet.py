"""One-off: render Crate-Bot's animation frames as PNGs for the repo.

These files under _shorts/character/robot/ are archival — the running renderer
draws the robot procedurally from sprite.py, so these PNGs are for reference
(reviewing frames individually, using them as brand assets elsewhere).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from . import config as C
from .sprite import placeholder_robot, upscale_pixel


FRAMES = ["idle_0", "idle_1", "walk_0", "walk_1"]


def main():
    out_dir = C.CHARACTER_DIR / "robot"
    out_dir.mkdir(parents=True, exist_ok=True)

    prefix = "johnny5-32bit"
    # Individual native-resolution PNGs
    for name in FRAMES:
        img = placeholder_robot(name)
        img.save(out_dir / f"{prefix}-{name}.png")

    # Upscaled individual sheets (4x = 384 px)
    for name in FRAMES:
        img = upscale_pixel(placeholder_robot(name), 4)
        img.save(out_dir / f"{prefix}-{name}-x4.png")

    # Contact sheet (all 4 frames, upscaled, with labels)
    from .sprite import SPRITE_SIZE
    scale = 4
    tile = SPRITE_SIZE * scale
    pad = 40
    w = len(FRAMES) * tile + (len(FRAMES) + 1) * pad
    h = tile + pad * 3
    sheet = Image.new("RGB", (w, h), (234, 222, 205))
    d = ImageDraw.Draw(sheet)
    try:
        label_font = ImageFont.truetype(C.FONT_LABEL, 28)
    except OSError:
        label_font = ImageFont.load_default()
    for i, name in enumerate(FRAMES):
        x = pad + i * (tile + pad)
        y = pad
        tile_img = upscale_pixel(placeholder_robot(name), scale)
        sheet.paste(tile_img, (x, y), tile_img)
        d.rectangle([x - 2, y - 2, x + tile + 1, y + tile + 1],
                    outline=(80, 80, 90), width=2)
        d.text((x + tile // 2, y + tile + 8), name,
               fill=(40, 40, 55), font=label_font, anchor="mt")
    sheet.save(out_dir / f"{prefix}-sheet.png")

    print(f"wrote {len(FRAMES) * 2 + 1} files to {out_dir}")


if __name__ == "__main__":
    main()
