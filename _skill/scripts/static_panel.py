"""Static-panel Pillow renderer for L-001 / L-002 mockups.

Every mockup is a single-image panel with four building blocks:

  1. A title strip at the top
  2. A "hero" region in the middle (a Spotlight panel, a Start menu, a
     Terminal window, or a prompt line)
  3. One or more annotation callouts with dashed-line pointers to specific
     anchors inside the hero
  4. An optional caption strip at the bottom

The canvas is sized to the content so there is no trailing whitespace - the
same rule that Gate 12 enforces on shell GIFs applies here too.

This is a small drawing library, not a full SVG engine. It intentionally
does not ship every mockup primitive; each lesson calls into it with its
own compose() function.
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont


# ---------- colour tokens ----------

PAGE_BG = (11, 13, 18)
CAPTION_BAR = (20, 25, 35)
CAPTION_FG = (154, 163, 178)
TITLE_FG = (236, 241, 250)
SUBTITLE_FG = (174, 188, 208)

CALLOUT_BODY = (15, 10, 24)
CALLOUT_LABEL_DIM = (205, 213, 224)
CALLOUT_TEXT = (255, 255, 255)
CALLOUT_TEXT_DIM = (214, 226, 240)

# Accent palette (for callouts)
MINT = (80, 232, 179)
CORAL = (249, 158, 158)
AZURE = (95, 163, 209)
GOLD = (255, 214, 102)
ORCHID = (201, 147, 234)

# Terminal palette (Bash)
BASH_WIN = (27, 27, 31)
BASH_TITLE = (46, 46, 51)
BASH_TITLE_FG = (208, 208, 216)
BASH_BODY = (30, 30, 34)

# Terminal palette (PowerShell)
PS_WIN = (12, 36, 86)
PS_TITLE = (23, 23, 23)
PS_TITLE_FG = (208, 208, 216)

# Prompt segment colours
BASH_USER = (80, 232, 179)
BASH_AT = (208, 208, 216)
BASH_HOST = (249, 158, 158)
BASH_COLON = (208, 208, 216)
BASH_PATH = (95, 163, 209)
BASH_DOLLAR = (255, 214, 102)

ZSH_USER = (80, 232, 179)
ZSH_AT = (208, 208, 216)
ZSH_HOST = (249, 158, 158)
ZSH_SPACE = (208, 208, 216)
ZSH_PATH = (95, 163, 209)
ZSH_PCT = (255, 214, 102)

PS_INTRO = (201, 147, 234)
PS_PATH = (95, 163, 209)
PS_GT = (255, 214, 102)


# ---------- font loading ----------


def _font_candidates_mono() -> list[str]:
    return [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]


def _font_candidates_ui() -> list[str]:
    return [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]


def _font_candidates_ui_bold() -> list[str]:
    return [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]


def _load(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def font_mono(size: int) -> ImageFont.FreeTypeFont:
    return _load(_font_candidates_mono(), size)


def font_ui(size: int) -> ImageFont.FreeTypeFont:
    return _load(_font_candidates_ui(), size)


def font_ui_bold(size: int) -> ImageFont.FreeTypeFont:
    return _load(_font_candidates_ui_bold(), size)


# ---------- building blocks ----------


def draw_page(im: Image.Image, *, fill: tuple[int, int, int] = PAGE_BG) -> None:
    ImageDraw.Draw(im).rectangle([0, 0, im.width, im.height], fill=fill)


def draw_title(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    canvas_w: int,
    y: int,
    size: int = 22,
    fill: tuple[int, int, int] = TITLE_FG,
) -> int:
    f = font_ui_bold(size)
    tw = draw.textlength(text, font=f)
    draw.text(((canvas_w - tw) / 2, y), text, font=f, fill=fill)
    return y + size + 4


def draw_subtitle(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    canvas_w: int,
    y: int,
    size: int = 14,
    fill: tuple[int, int, int] = SUBTITLE_FG,
) -> int:
    f = font_ui(size)
    tw = draw.textlength(text, font=f)
    draw.text(((canvas_w - tw) / 2, y), text, font=f, fill=fill)
    return y + size + 8


def draw_caption(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    canvas_w: int,
    canvas_h: int,
    bar_h: int = 44,
    fill: tuple[int, int, int] = CAPTION_FG,
    bar: tuple[int, int, int] = CAPTION_BAR,
) -> None:
    f = font_ui(13)
    y = canvas_h - bar_h
    draw.rectangle([20, y, canvas_w - 20, canvas_h - 8], fill=bar)
    tw = draw.textlength(text, font=f)
    draw.text(((canvas_w - tw) / 2, y + (bar_h - 22) // 2), text, font=f, fill=fill)


def draw_window(
    im: Image.Image,
    x: int,
    y: int,
    w: int,
    h: int,
    *,
    title: str,
    body_fill: tuple[int, int, int] = BASH_WIN,
    title_fill: tuple[int, int, int] = BASH_TITLE,
    title_fg: tuple[int, int, int] = BASH_TITLE_FG,
    border: tuple[int, int, int] = (70, 70, 76),
    radius: int = 10,
    title_h: int = 36,
    traffic_lights: bool = True,
) -> None:
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=radius, fill=body_fill, outline=border, width=1
    )
    draw.rounded_rectangle(
        [x, y, x + w, y + title_h], radius=radius, fill=title_fill
    )
    draw.rectangle(
        [x, y + title_h - 10, x + w, y + title_h], fill=title_fill
    )
    if traffic_lights:
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            cx = x + 18 + i * 18
            cy = y + title_h // 2
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=c)
    f = font_ui(12)
    tw = draw.textlength(title, font=f)
    draw.text(
        (x + (w - tw) / 2, y + (title_h - 16) // 2), title, font=f, fill=title_fg
    )


def draw_terminal_window_windows(
    im: Image.Image, x: int, y: int, w: int, h: int, *, profile: str, user_host: str
) -> None:
    """Windows Terminal-style chrome: dark tab strip with a tab, no traffic
    lights, a PowerShell > cursor in the tab, and min/max/close at the right."""
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=6, fill=(20, 20, 20), outline=(60, 60, 60), width=1
    )
    # Tab bar
    tab_h = 32
    draw.rectangle([x, y, x + w, y + tab_h], fill=(30, 30, 30))
    # Tab
    draw.rounded_rectangle(
        [x + 8, y + 4, x + 280, y + tab_h], radius=6, fill=(46, 46, 46)
    )
    # Tab icon (tiny >_ ) - draw a small green-tinted square
    draw.rounded_rectangle(
        [x + 16, y + 10, x + 32, y + 24], radius=3, fill=(40, 80, 50)
    )
    f = font_mono(11)
    draw.text((x + 18, y + 11), ">_", font=f, fill=(160, 230, 170))
    f = font_ui(12)
    draw.text((x + 40, y + 10), profile, font=f, fill=(220, 220, 220))
    draw.text((x + 120, y + 10), user_host, font=f, fill=(160, 170, 185))
    # + and v (new tab)
    draw.text((x + 290, y + 10), "+", font=font_ui(14), fill=(200, 200, 200))
    draw.text((x + 310, y + 10), "v", font=font_ui(10), fill=(160, 170, 185))
    # Window controls at far right
    for i, sym in enumerate([("\u2014", 12), ("\u25A1", 12), ("\u2715", 14)]):
        cx = x + w - 74 + i * 24
        draw.text((cx, y + 10), sym[0], font=font_ui(sym[1]), fill=(220, 220, 220))


def draw_gnome_window(
    im: Image.Image, x: int, y: int, w: int, h: int, *, title: str
) -> None:
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=8, fill=(55, 40, 60), outline=(90, 60, 95), width=1
    )
    title_h = 34
    draw.rounded_rectangle(
        [x, y, x + w, y + title_h], radius=8, fill=(40, 30, 46)
    )
    draw.rectangle(
        [x, y + title_h - 10, x + w, y + title_h], fill=(40, 30, 46)
    )
    f = font_ui(12)
    tw = draw.textlength(title, font=f)
    draw.text((x + (w - tw) / 2, y + 9), title, font=f, fill=(220, 220, 220))
    # Minimise / max circles on the right
    for i, c in enumerate([(120, 120, 130), (120, 120, 130)]):
        cx = x + w - 24 - i * 20
        cy = y + title_h // 2
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=c)


# ---------- prompt line composer ----------


@dataclass
class PromptSegment:
    text: str
    color: tuple[int, int, int]


def measure_prompt(segs: list[PromptSegment], font: ImageFont.FreeTypeFont) -> int:
    # Measure total width without drawing.
    from PIL import Image as _I

    tmp = _I.new("RGB", (1, 1))
    d = ImageDraw.Draw(tmp)
    return sum(int(d.textlength(s.text, font=font)) for s in segs)


def draw_prompt(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    segs: list[PromptSegment],
    font: ImageFont.FreeTypeFont,
) -> list[tuple[str, int, int, int, int]]:
    """Draw segments. Return list of (text, x0, y0, x1, y1) bounds for each
    segment - callers use these to anchor callout arrows."""
    out: list[tuple[str, int, int, int, int]] = []
    ascent, descent = font.getmetrics()
    line_h = ascent + descent
    cur_x = x
    for seg in segs:
        w = int(draw.textlength(seg.text, font=font))
        draw.text((cur_x, y), seg.text, font=font, fill=seg.color)
        out.append((seg.text, cur_x, y, cur_x + w, y + line_h))
        cur_x += w
    return out


# ---------- callout ----------


@dataclass
class Callout:
    label: str
    lines: list[str]
    color: tuple[int, int, int]
    # Box position (top-left) and size in canvas coords
    x: int
    y: int
    w: int
    h: int
    # Arrow anchor in canvas coords
    anchor: tuple[int, int]
    # Which edge of the box to start the arrow from: "top", "bottom", "left", "right"
    start_edge: str = "bottom"


def draw_callout(draw: ImageDraw.ImageDraw, c: Callout) -> None:
    # Box
    draw.rounded_rectangle(
        [c.x, c.y, c.x + c.w, c.y + c.h],
        radius=10,
        fill=CALLOUT_BODY,
        outline=c.color,
        width=2,
    )
    # Label (bold)
    f_label = font_ui_bold(14)
    draw.text((c.x + 12, c.y + 10), c.label, font=f_label, fill=c.color)
    # Body lines
    f_body = font_ui(12)
    for i, line in enumerate(c.lines):
        fg = CALLOUT_TEXT if i == 0 else CALLOUT_TEXT_DIM
        draw.text((c.x + 12, c.y + 32 + i * 16), line, font=f_body, fill=fg)

    # Arrow start
    if c.start_edge == "top":
        sx, sy = c.x + c.w // 2, c.y
    elif c.start_edge == "bottom":
        sx, sy = c.x + c.w // 2, c.y + c.h
    elif c.start_edge == "left":
        sx, sy = c.x, c.y + c.h // 2
    else:  # right
        sx, sy = c.x + c.w, c.y + c.h // 2

    ax, ay = c.anchor
    # Dashed curve from (sx, sy) to (ax, ay)
    draw_dashed_curve(draw, sx, sy, ax, ay, c.color)
    # Anchor dot
    draw.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=c.color)


def draw_dashed_curve(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: tuple[int, int, int],
    *,
    dash_on: int = 6,
    dash_off: int = 5,
    width: int = 2,
) -> None:
    # Approximate a quadratic Bezier from (x0,y0) to (x1,y1) with a mild bow.
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2 - 30 if y1 > y0 else (y0 + y1) // 2 + 30
    prev = (x0, y0)
    t = 0.0
    on = True
    acc = 0.0
    step = 0.01
    while t < 1.0:
        t2 = min(1.0, t + step)
        # Quadratic bezier
        def bez(t: float) -> tuple[float, float]:
            mt = 1 - t
            return (
                mt * mt * x0 + 2 * mt * t * cx + t * t * x1,
                mt * mt * y0 + 2 * mt * t * cy + t * t * y1,
            )

        px, py = bez(t2)
        dx = px - prev[0]
        dy = py - prev[1]
        seg = math.hypot(dx, dy)
        if on:
            if acc + seg >= dash_on:
                # End this dash somewhere on the segment
                frac = (dash_on - acc) / seg if seg > 0 else 0
                ex = prev[0] + dx * frac
                ey = prev[1] + dy * frac
                draw.line(
                    [int(prev[0]), int(prev[1]), int(ex), int(ey)],
                    fill=color,
                    width=width,
                )
                prev = (ex, ey)
                acc = 0.0
                on = False
                continue
            draw.line(
                [int(prev[0]), int(prev[1]), int(px), int(py)],
                fill=color,
                width=width,
            )
            acc += seg
        else:
            if acc + seg >= dash_off:
                frac = (dash_off - acc) / seg if seg > 0 else 0
                ex = prev[0] + dx * frac
                ey = prev[1] + dy * frac
                prev = (ex, ey)
                acc = 0.0
                on = True
                continue
            acc += seg
        prev = (px, py)
        t = t2


# ---------- key cap ----------


def draw_keycap(
    im: Image.Image,
    x: int,
    y: int,
    text: str,
    *,
    width: int = 64,
    height: int = 52,
    size: int = 20,
) -> None:
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(
        [x, y, x + width, y + height],
        radius=8,
        fill=(255, 255, 255),
        outline=(200, 200, 210),
        width=1,
    )
    f = font_ui_bold(size)
    tw = draw.textlength(text, font=f)
    draw.text((x + (width - tw) / 2, y + (height - size - 4) // 2), text, font=f, fill=(32, 34, 40))


def draw_plus(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 22) -> None:
    f = font_ui_bold(size)
    draw.text((x, y), "+", font=f, fill=(230, 230, 240))
