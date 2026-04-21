"""Dynamic top-area input display.

Replaces the old static user sprite with a context-aware panel that shows what
the user is actually doing during the current beat: a keyboard shortcut,
a typed search query, a shell command, or a single keycap like Enter.

Shape of `input_display` on a beat (all optional — None means show nothing):

    # Keyboard shortcut, one row per platform
    {"type": "keycaps",
     "rows": [{"platform": "Mac",   "keys": ["⌘", "Space"]},
              {"platform": "Win",   "keys": ["⊞"]},
              {"platform": "Linux", "keys": ["Super"]}]}

    # Single keycap, no platform label
    {"type": "key", "label": "Enter"}

    # Shell command in a terminal prompt
    {"type": "command", "prompt": "$", "text": "echo hello"}

    # Text typed into a search/input field
    {"type": "text_input", "placeholder": "search...", "text": "terminal"}
"""
from typing import Optional
from PIL import Image, ImageDraw, ImageFont

from . import config as C
from .storyboard import Storyboard


def current_input_display(sb: Storyboard, t: float) -> Optional[dict]:
    """Return the input_display dict active at time t, or None."""
    for beat in sb.beats:
        if beat.start_time <= t < beat.start_time + beat.duration:
            return beat.input_display
    return None


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def _draw_keycap(draw: ImageDraw.ImageDraw, cx: int, cy: int, label: str,
                 font: ImageFont.FreeTypeFont, min_w: int = 72, h: int = 78):
    """Draw a single keycap centered on (cx, cy). Returns (w, h) drawn."""
    pad_x = 22
    bbox = draw.textbbox((0, 0), label, font=font)
    text_w = bbox[2] - bbox[0]
    w = max(min_w, text_w + pad_x * 2)
    x0 = cx - w // 2
    x1 = cx + w // 2
    y0 = cy - h // 2
    y1 = cy + h // 2
    # Drop shadow
    draw.rounded_rectangle([x0 + 3, y0 + 4, x1 + 3, y1 + 4], radius=10,
                           fill=C.COLOR_OUTLINE)
    # Body
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                           fill=C.COLOR_LANE_LABEL_BG, outline=C.COLOR_ACCENT, width=3)
    # Highlight pip on top edge
    draw.rectangle([x0 + 8, y0 + 6, x1 - 8, y0 + 10], fill=(70, 88, 108))
    # Label
    draw.text((cx, cy - 2), label, fill=C.COLOR_LANE_LABEL_TEXT,
              font=font, anchor="mm")
    return w, h


def _draw_plus(draw: ImageDraw.ImageDraw, cx: int, cy: int, color, size: int = 22):
    """Small '+' glyph between keycaps."""
    t = 5
    draw.rectangle([cx - size // 2, cy - t // 2, cx + size // 2, cy + t // 2], fill=color)
    draw.rectangle([cx - t // 2, cy - size // 2, cx + t // 2, cy + size // 2], fill=color)


def _render_keycaps(draw: ImageDraw.ImageDraw, area: tuple[int, int, int, int],
                    data: dict):
    """area: (x0, y0, x1, y1) — the USER_Y zone below the header."""
    x0, y0, x1, y1 = area
    rows = data.get("rows", [])
    if not rows:
        return

    key_font = _font(C.FONT_CAPTION_BOLD, 34)
    platform_font = _font(C.FONT_LABEL, 26)

    # Measure row heights; place evenly in the area.
    row_h = 92
    total_h = len(rows) * row_h
    start_y = y0 + ((y1 - y0) - total_h) // 2 + row_h // 2

    platform_col_w = 170  # left-side platform label column
    plus_gap = 40
    key_gap = 16

    cx_keys_start = x0 + platform_col_w + 40

    for i, row in enumerate(rows):
        cy = start_y + i * row_h
        platform = row.get("platform", "")
        keys = row.get("keys", [])

        # Platform label (left)
        if platform:
            plat_x = x0 + 30
            draw.rounded_rectangle([plat_x, cy - 26, plat_x + platform_col_w - 30, cy + 26],
                                   radius=6, fill=C.COLOR_OUTLINE,
                                   outline=C.COLOR_TEXT_DIM, width=1)
            draw.text((plat_x + (platform_col_w - 30) // 2, cy), platform,
                      fill=C.COLOR_TEXT_DIM, font=platform_font, anchor="mm")

        # Keys + pluses
        x = cx_keys_start
        first = True
        for k in keys:
            if not first:
                _draw_plus(draw, x + plus_gap // 2, cy, C.COLOR_ACCENT)
                x += plus_gap
            # Measure cap width
            bbox = draw.textbbox((0, 0), k, font=key_font)
            text_w = bbox[2] - bbox[0]
            w = max(72, text_w + 44)
            w, _h = _draw_keycap(draw, x + w // 2, cy, k, key_font, min_w=w)
            x += w + key_gap
            first = False


def _render_key(draw: ImageDraw.ImageDraw, area: tuple[int, int, int, int], data: dict):
    x0, y0, x1, y1 = area
    label = data.get("label", "")
    key_font = _font(C.FONT_CAPTION_BOLD, 48)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    _draw_keycap(draw, cx, cy, label, key_font, min_w=160, h=110)


def _render_command(draw: ImageDraw.ImageDraw, img: Image.Image,
                    area: tuple[int, int, int, int], data: dict):
    x0, y0, x1, y1 = area
    prompt = data.get("prompt", "$")
    text = data.get("text", "")
    full = f"{prompt}  {text}"

    mono_font = _font(C.FONT_MONO, 46)
    # Terminal-style box
    pad_x, pad_y = 34, 28
    bbox = draw.textbbox((0, 0), full, font=mono_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    box_w = min(text_w + pad_x * 2, (x1 - x0) - 60)
    box_h = text_h + pad_y * 2
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    bx0 = cx - box_w // 2
    bx1 = cx + box_w // 2
    by0 = cy - box_h // 2
    by1 = cy + box_h // 2
    # Background
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=14,
                           fill=(8, 12, 18), outline=C.COLOR_ACCENT, width=3)
    # Mac-style window dots (decorative)
    dot_y = by0 + 18
    for i, dot_color in enumerate([(232, 96, 84), (244, 196, 72), (120, 200, 110)]):
        draw.ellipse([bx0 + 18 + i * 24, dot_y, bx0 + 30 + i * 24, dot_y + 12],
                     fill=dot_color)
    # Prompt colored separately
    prompt_font = _font(C.FONT_MONO, 46)
    prompt_w = draw.textbbox((0, 0), prompt, font=prompt_font)[2]
    full_w = draw.textbbox((0, 0), full, font=mono_font)[2]
    text_start_x = cx - full_w // 2
    text_y = cy + 8
    draw.text((text_start_x, text_y), prompt, fill=C.COLOR_ACCENT,
              font=prompt_font, anchor="lm")
    gap_after_prompt = draw.textbbox((0, 0), f"{prompt}  ", font=mono_font)[2]
    draw.text((text_start_x + gap_after_prompt, text_y), text,
              fill=C.COLOR_LANE_LABEL_TEXT, font=mono_font, anchor="lm")


def _render_text_input(draw: ImageDraw.ImageDraw,
                       area: tuple[int, int, int, int], data: dict, t: float):
    x0, y0, x1, y1 = area
    placeholder = data.get("placeholder", "")
    text = data.get("text", "")

    input_font = _font(C.FONT_CAPTION_BOLD, 46)
    pad_x, pad_y = 34, 28
    box_w = min((x1 - x0) - 60, 860)
    box_h = 100
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    bx0 = cx - box_w // 2
    bx1 = cx + box_w // 2
    by0 = cy - box_h // 2
    by1 = cy + box_h // 2

    # Search-input look
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=18,
                           fill=C.COLOR_LANE_LABEL_BG,
                           outline=C.COLOR_ACCENT, width=3)
    # Magnifying glass glyph (left)
    glass_cx = bx0 + 46
    glass_cy = cy
    draw.ellipse([glass_cx - 16, glass_cy - 16, glass_cx + 10, glass_cy + 10],
                 outline=C.COLOR_TEXT_DIM, width=4)
    draw.line([glass_cx + 6, glass_cy + 6, glass_cx + 20, glass_cy + 20],
              fill=C.COLOR_TEXT_DIM, width=4)
    # Text
    text_x = bx0 + 90
    if text:
        draw.text((text_x, cy), text, fill=C.COLOR_LANE_LABEL_TEXT,
                  font=input_font, anchor="lm")
        # Blinking cursor
        if int(t * 2) % 2 == 0:
            bbox = draw.textbbox((0, 0), text, font=input_font)
            cur_x = text_x + (bbox[2] - bbox[0]) + 6
            draw.rectangle([cur_x, cy - 22, cur_x + 4, cy + 22],
                           fill=C.COLOR_ACCENT)
    elif placeholder:
        draw.text((text_x, cy), placeholder, fill=C.COLOR_TEXT_DIM,
                  font=input_font, anchor="lm")


def draw_input_display(img: Image.Image, draw: ImageDraw.ImageDraw,
                       display: Optional[dict], t: float):
    """Render the given input_display into the USER_Y region of the canvas."""
    if not display:
        return
    area = (40, C.USER_Y[0], C.CANVAS_W - 40, C.USER_Y[1])
    kind = display.get("type", "")
    if kind == "keycaps":
        _render_keycaps(draw, area, display)
    elif kind == "key":
        _render_key(draw, area, display)
    elif kind == "command":
        _render_command(draw, img, area, display)
    elif kind == "text_input":
        _render_text_input(draw, area, display, t)
