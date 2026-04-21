"""Per-frame scene composition — v3 liquid glass redesign.

Canvas is 1080x1920 (9:16). Two distinct frame types:

- Scroll frame (compose_frame): the timeline scrolls right-to-left while the
  mascot stays horizontally near the center. Panels use the liquid_glass
  helpers for translucency + highlights + soft shadows. The robot can drift
  horizontally during transitions to feel like it "drives" between lanes
  rather than sliding on a rail.

- Finale frame (compose_finale_frame): a static recap with two sections:
    1. A "COMMANDS ENTERED" glass panel at the top listing each input_display.
    2. A clean UML sequence diagram below with 3 swim lanes and numbered
       message arrows — no overlapping labels.
"""
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
import math

from . import config as C
from . import sprite as SPR
from .storyboard import Storyboard, Beat
from .input_display import draw_input_display, current_input_display
from .liquid_glass import (
    radial_gradient, compose_panel, accent_glow, drop_shadow,
)


# -------------------- Scroll geometry (unchanged from v2) --------------------

SELF_SCROLL = 140
OPEN_SCROLL = 80


def lane_y_positions(n_lanes: int) -> list[int]:
    y_start, y_end = C.TIMELINE_Y
    top_margin = 60
    bot_margin = 60
    usable = (y_end - bot_margin) - (y_start + top_margin)
    if n_lanes == 1:
        return [y_start + (y_end - y_start) // 2]
    step = usable / (n_lanes - 1)
    return [int(y_start + top_margin + i * step) for i in range(n_lanes)]


def beat_scroll_distance(beat: Beat) -> float:
    if beat.kind in ("call", "return"):
        return beat.duration * C.PIXELS_PER_SECOND
    if beat.kind == "self":
        return SELF_SCROLL
    if beat.kind == "open":
        return OPEN_SCROLL
    return 0.0


def build_scroll_plan(sb: Storyboard) -> None:
    x = 0.0
    for beat in sb.beats:
        d = beat_scroll_distance(beat)
        beat.event_world_x = x + d / 2
        x += d
    sb._total_scroll_world = x  # type: ignore


def _ease_in_out(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return 3 * u * u - 2 * u * u * u


def camera_x_at(sb: Storyboard, t: float) -> float:
    x = 0.0
    for beat in sb.beats:
        beat_end = beat.start_time + beat.duration
        d = beat_scroll_distance(beat)
        if t >= beat_end:
            x += d
            continue
        if t >= beat.start_time:
            u = (t - beat.start_time) / max(beat.duration, 0.01)
            u = _ease_in_out(u)
            return x + d * u
        return x
    return x


# -------------------- Robot position + animation selection --------------------

def current_beat_and_u(sb: Storyboard, t: float):
    for i, beat in enumerate(sb.beats):
        if beat.start_time <= t < beat.start_time + beat.duration:
            u = (t - beat.start_time) / max(beat.duration, 0.01)
            return i, beat, u
    if sb.beats:
        return len(sb.beats) - 1, sb.beats[-1], 1.0
    return -1, None, 0.0


def robot_xy_at(sb: Storyboard, t: float) -> tuple[float, float]:
    """(screen_x, screen_y) of the robot at time t. The sprite can drift
    horizontally during transitions and self-beats so it "drives" rather than
    slides on a rail.
    """
    ys = lane_y_positions(len(sb.lanes))
    lane_to_y = dict(zip(sb.lanes, ys))
    home_y = ys[0]

    # Walk through beats to find the current one + compute base y.
    cur_y = home_y
    cur_x = C.ROBOT_SCREEN_X
    for beat in sb.beats:
        beat_end = beat.start_time + beat.duration
        if t < beat.start_time:
            break
        if beat.kind == "open":
            cur_y = home_y
        elif beat.kind in ("call", "return"):
            from_y = lane_to_y.get(beat.from_lane, cur_y)
            to_y = lane_to_y.get(beat.to_lane, cur_y)
            if t >= beat_end:
                cur_y = to_y
            else:
                u = _ease_in_out((t - beat.start_time) / max(beat.duration, 0.01))
                cur_y = from_y + (to_y - from_y) * u
                # Horizontal arc: sweep out and back (like a car taking a gentle
                # curve between floors)
                arc = math.sin(u * math.pi) * 42  # up to 42px sideways
                sign = 1 if beat.kind == "call" else -1
                cur_x = C.ROBOT_SCREEN_X + sign * arc
                return cur_x, cur_y
        elif beat.kind == "self":
            y = lane_to_y.get(beat.from_lane, cur_y)
            if t >= beat_end:
                cur_y = y
            else:
                u = (t - beat.start_time) / max(beat.duration, 0.01)
                # Left-right dance around the lane
                cur_x = C.ROBOT_SCREEN_X + math.sin(u * math.pi * 2) * 28
                cur_y = y
                return cur_x, cur_y
    return cur_x, cur_y


def robot_animation_for(sb: Storyboard, t: float) -> tuple[str, float]:
    """Return (animation_name, local_time). `local_time` is seconds-since-beat-
    start so the animation cycles properly."""
    i, beat, _u = current_beat_and_u(sb, t)
    if beat is None:
        return "idle_bob", t
    local_t = t - beat.start_time
    if beat.kind in ("call", "return"):
        return "drive", local_t
    if beat.kind == "self":
        # Deterministic self-animation pick based on beat index
        return SPR.pick_self(i), local_t
    # open or idle-ish
    return SPR.pick_idle(i), local_t


# -------------------- Drawing helpers --------------------

def word_wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int,
              draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
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


def _draw_arrow(draw: ImageDraw.ImageDraw, x: float, y1: int, y2: int, color,
                label: str = "", label_font=None):
    draw.line([x, y1, x, y2], fill=color, width=5)
    head = 14
    if y2 > y1:
        draw.polygon([(x - head, y2 - head), (x + head, y2 - head), (x, y2)], fill=color)
    else:
        draw.polygon([(x - head, y2 + head), (x + head, y2 + head), (x, y2)], fill=color)
    if label and label_font:
        mid_y = (y1 + y2) // 2
        pad = 10
        bbox = draw.textbbox((0, 0), label, font=label_font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        bx0 = x + 18
        bx1 = bx0 + lw + pad * 2
        by0 = mid_y - lh // 2 - pad // 2
        by1 = by0 + lh + pad
        draw.rounded_rectangle([bx0, by0, bx1, by1], radius=8,
                               fill=(20, 24, 34, 220), outline=color, width=2)
        draw.text((bx0 + pad, mid_y), label, fill=C.COLOR_TEXT,
                  font=label_font, anchor="lm")


def _draw_self_bubble(draw: ImageDraw.ImageDraw, x: float, y: int, color,
                      label: str = "", label_font=None, side_gap: int = 220):
    """Small side-bubble for self-events. side_gap leaves room for the
    sprite's left-right dance-drift during the beat (~28px), plus its
    128px footprint, plus half the bubble width."""
    if not label or not label_font:
        return
    pad_x, pad_y = 18, 12
    bbox = draw.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    bubble_w = lw + pad_x * 2
    bubble_h = lh + pad_y * 2
    bcx = x + side_gap
    bcy = y - 4
    bx0 = bcx - bubble_w // 2
    bx1 = bcx + bubble_w // 2
    by0 = bcy - bubble_h // 2
    by1 = bcy + bubble_h // 2
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=12,
                           fill=(18, 22, 32, 220), outline=color, width=2)
    draw.line([(x + 14, y), (bx0 - 2, bcy)], fill=color, width=2)
    draw.text((bcx, bcy), label, fill=C.COLOR_TEXT,
              font=label_font, anchor="mm")
    draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=color,
                 outline=(14, 18, 28), width=1)


def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# -------------------- Backdrop --------------------

_BACKDROP_CACHE: dict[tuple[int, int], Image.Image] = {}


def _backdrop() -> Image.Image:
    """Radial-gradient dark indigo backdrop. Cached — it never changes."""
    key = (C.CANVAS_W, C.CANVAS_H)
    if key not in _BACKDROP_CACHE:
        inner = (30, 36, 56)
        outer = (8, 11, 18)
        _BACKDROP_CACHE[key] = radial_gradient(key, inner, outer,
                                                center=(0.5, 0.25),
                                                falloff=1.3)
    return _BACKDROP_CACHE[key].copy()


# -------------------- Scroll frame --------------------

def compose_frame(sb: Storyboard, t: float) -> Image.Image:
    # RGBA base so glass panels composite cleanly.
    img = _backdrop().convert("RGBA")
    draw = ImageDraw.Draw(img)

    header_font = _get_font(C.FONT_CAPTION_BOLD, 64)
    sub_font = _get_font(C.FONT_CAPTION, 42)
    label_font = _get_font(C.FONT_LABEL, 28)
    arrow_label_font = _get_font(C.FONT_MONO, 26)
    caption_font = _get_font(C.FONT_CAPTION_BOLD, 40)
    watermark_font = _get_font(C.FONT_ITALIC, 26)

    # 1. Header with subtle glow behind "DAY 01"
    day_line = f"DAY {sb.day_number:02d}"
    # Glow
    accent_glow(img, C.CANVAS_W // 2 - 180, 26, (360, 90),
                radius=44, color=C.COLOR_ACCENT, alpha=40, blur=18)
    draw.text((C.CANVAS_W // 2, 36), day_line, fill=C.COLOR_ACCENT,
              font=header_font, anchor="mt")
    draw.text((C.CANVAS_W // 2, 112), sb.learning_title.upper(),
              fill=C.COLOR_TEXT, font=sub_font, anchor="mt")

    # 2. Lane geometry
    ys = lane_y_positions(len(sb.lanes))
    camera_x = camera_x_at(sb, t)

    # Background lane lines (subtle)
    for y in ys:
        draw.line([C.LANE_LABEL_X[1] + 4, y, C.CANVAS_W, y],
                  fill=(60, 72, 92, 200), width=2)

    # 3. Timeline events (scrolling)
    for beat in sb.beats:
        if beat.kind in ("open", "finale"):
            continue
        if t < beat.start_time - 0.05:
            continue
        screen_x = C.ROBOT_SCREEN_X + (beat.event_world_x - camera_x)
        if screen_x < C.LANE_LABEL_X[1] - 40 or screen_x > C.CANVAS_W + 100:
            continue
        if beat.kind in ("call", "return"):
            if beat.from_lane not in sb.lanes or beat.to_lane not in sb.lanes:
                continue
            y1 = ys[sb.lanes.index(beat.from_lane)]
            y2 = ys[sb.lanes.index(beat.to_lane)]
            color = C.COLOR_ACCENT if beat.kind == "call" else C.COLOR_PRIMARY
            _draw_arrow(draw, screen_x, y1, y2, color, beat.label, arrow_label_font)
        elif beat.kind == "self":
            if beat.from_lane not in sb.lanes:
                continue
            y = ys[sb.lanes.index(beat.from_lane)]
            _draw_self_bubble(draw, screen_x, y, C.COLOR_ACCENT,
                              beat.label, arrow_label_font)

    # 4. Lane label glass panels (pinned left)
    for lane, y in zip(sb.lanes, ys):
        x0, x1 = C.LANE_LABEL_X
        w = x1 - x0
        h = 68
        compose_panel(img, x0, y - h // 2, (w, h), radius=18,
                      fill_rgba=(28, 36, 54, 200),
                      accent_edge_rgba=(*C.COLOR_ACCENT, 160),
                      shadow_blur=14, shadow_opacity=110,
                      shadow_offset=(0, 6))
        # Re-draw text on top (compose_panel draws to img as RGBA)
        dd = ImageDraw.Draw(img)
        lines = word_wrap(lane, label_font, w - 16, dd)
        line_h = 30
        total_h = len(lines) * line_h
        y_start = y - total_h // 2 + line_h // 2
        for i, line in enumerate(lines[:2]):
            dd.text(((x0 + x1) // 2, y_start + i * line_h), line,
                    fill=C.COLOR_LANE_LABEL_TEXT, font=label_font, anchor="mm")

    # 5. Input display at top
    display = current_input_display(sb, t)
    draw_input_display(img, ImageDraw.Draw(img), display, t)

    # Connector line from input zone down to top lane
    connector_top = C.USER_Y[1] - 10
    connector_bot = ys[0] - 40
    if connector_bot > connector_top:
        ImageDraw.Draw(img).line(
            [C.CANVAS_W // 2, connector_top, C.CANVAS_W // 2, connector_bot],
            fill=(90, 104, 128, 200), width=3)

    # 6. Mascot sprite (tiny, animated, with horizontal drift)
    anim, local_t = robot_animation_for(sb, t)
    frame_img = SPR.frame_at(anim, local_t)
    robot_scale = 4  # 32*4 = 128 px footprint — tiny & nimble
    robot_img = SPR.upscale_pixel(frame_img, robot_scale)
    rx_center, ry = robot_xy_at(sb, t)
    rx = int(rx_center) - robot_img.width // 2
    ry_paste = int(ry) - robot_img.height // 2
    img.alpha_composite(robot_img, (rx, ry_paste))

    # 7. Caption glass panel
    current = None
    for beat in sb.beats:
        if beat.start_time <= t < beat.start_time + beat.duration:
            current = beat
            break
    if current and current.narration:
        cap_x0 = 60
        cap_w = C.CANVAS_W - 120
        dd = ImageDraw.Draw(img)
        lines = word_wrap(current.narration, caption_font, cap_w - 40, dd)
        line_h = 52
        shown = lines[:4]
        cap_h = max(140, len(shown) * line_h + 50)
        cap_y = C.CAPTION_Y[0] + (C.CAPTION_Y[1] - C.CAPTION_Y[0] - cap_h) // 2
        compose_panel(img, cap_x0, cap_y, (cap_w, cap_h), radius=28,
                      fill_rgba=(14, 18, 30, 190),
                      accent_edge_rgba=(255, 255, 255, 40),
                      shadow_blur=22, shadow_opacity=160,
                      shadow_offset=(0, 14),
                      gradient=((40, 50, 72, 200), (12, 16, 28, 210)))
        dd = ImageDraw.Draw(img)
        text_y = cap_y + (cap_h - len(shown) * line_h) // 2 + 4
        for i, line in enumerate(shown):
            dd.text((C.CANVAS_W // 2, text_y + i * line_h), line,
                    fill=C.COLOR_TEXT, font=caption_font, anchor="mt")

    # 8. Watermark
    ImageDraw.Draw(img).text(
        (C.CANVAS_W - 24, C.CANVAS_H - 24), "by Elvis Jones",
        fill=(200, 200, 200), font=watermark_font, anchor="rb")

    return img.convert("RGB")


# -------------------- Finale frame --------------------

def _draw_mini_input(img: Image.Image, draw: ImageDraw.ImageDraw,
                     display: dict, area: tuple[int, int, int, int]):
    """Compact version of an input_display for the finale's commands panel.
    area = (x0, y0, x1, y1) — fits into one row."""
    x0, y0, x1, y1 = area
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2

    kind = display.get("type", "")
    label_font = _get_font(C.FONT_LABEL, 24)
    key_font = _get_font(C.FONT_CAPTION_BOLD, 28)
    mono_font = _get_font(C.FONT_MONO, 30)

    if kind == "keycaps":
        # One line per platform, all in the row: "Mac: [Cmd][Space]  Win: [Win]  Linux: [Super]"
        rows = display.get("rows", [])
        parts = []
        for row in rows:
            platform = row.get("platform", "")
            keys = row.get("keys", [])
            parts.append((platform, keys))
        # Render left-to-right
        x = x0 + 12
        for platform, keys in parts:
            # Platform label
            draw.text((x, cy), f"{platform}:", fill=C.COLOR_TEXT_DIM,
                      font=label_font, anchor="lm")
            pbbox = draw.textbbox((0, 0), f"{platform}:", font=label_font)
            x += (pbbox[2] - pbbox[0]) + 12
            # Keys
            first = True
            for k in keys:
                if not first:
                    draw.text((x, cy), "+", fill=C.COLOR_ACCENT,
                              font=key_font, anchor="lm")
                    x += 22
                kbbox = draw.textbbox((0, 0), k, font=key_font)
                kw = kbbox[2] - kbbox[0] + 24
                draw.rounded_rectangle([x, cy - 24, x + kw, cy + 24],
                                       radius=8, fill=(28, 36, 54, 255),
                                       outline=C.COLOR_ACCENT, width=2)
                draw.text((x + kw // 2, cy), k, fill=C.COLOR_LANE_LABEL_TEXT,
                          font=key_font, anchor="mm")
                x += kw + 14
                first = False
            x += 30
    elif kind == "key":
        label = display.get("label", "")
        # Single keycap centered
        kbbox = draw.textbbox((0, 0), label, font=key_font)
        kw = kbbox[2] - kbbox[0] + 32
        draw.rounded_rectangle([cx - kw // 2, cy - 24, cx + kw // 2, cy + 24],
                               radius=8, fill=(28, 36, 54, 255),
                               outline=C.COLOR_ACCENT, width=2)
        draw.text((cx, cy), label, fill=C.COLOR_LANE_LABEL_TEXT,
                  font=key_font, anchor="mm")
    elif kind == "text_input":
        text = display.get("text", "")
        box_w = min(x1 - x0 - 40, 460)
        box_h = 54
        bx0 = cx - box_w // 2
        bx1 = cx + box_w // 2
        draw.rounded_rectangle([bx0, cy - box_h // 2, bx1, cy + box_h // 2],
                               radius=14, fill=(28, 36, 54, 255),
                               outline=C.COLOR_ACCENT, width=2)
        # Magnifying glass
        gx = bx0 + 30
        draw.ellipse([gx - 10, cy - 10, gx + 4, cy + 4],
                     outline=C.COLOR_TEXT_DIM, width=3)
        draw.line([gx + 2, cy + 2, gx + 10, cy + 10],
                  fill=C.COLOR_TEXT_DIM, width=3)
        draw.text((bx0 + 52, cy), text, fill=C.COLOR_LANE_LABEL_TEXT,
                  font=key_font, anchor="lm")
    elif kind == "command":
        prompt = display.get("prompt", "$")
        text = display.get("text", "")
        full = f"{prompt}  {text}"
        box_w = min(x1 - x0 - 40, 460)
        box_h = 54
        bx0 = cx - box_w // 2
        bx1 = cx + box_w // 2
        draw.rounded_rectangle([bx0, cy - box_h // 2, bx1, cy + box_h // 2],
                               radius=12, fill=(8, 12, 18, 255),
                               outline=C.COLOR_ACCENT, width=2)
        draw.text((bx0 + 20, cy), prompt, fill=C.COLOR_ACCENT,
                  font=mono_font, anchor="lm")
        draw.text((bx0 + 60, cy), text, fill=C.COLOR_LANE_LABEL_TEXT,
                  font=mono_font, anchor="lm")


def compose_finale_frame(sb: Storyboard, phase_u: float) -> Image.Image:
    """Recap: 'COMMANDS ENTERED' glass panel + proper UML sequence diagram."""
    img = _backdrop().convert("RGBA")
    draw = ImageDraw.Draw(img)

    title_font = _get_font(C.FONT_CAPTION_BOLD, 64)
    sub_font = _get_font(C.FONT_CAPTION, 36)
    section_font = _get_font(C.FONT_CAPTION_BOLD, 32)
    label_font = _get_font(C.FONT_LABEL, 26)
    step_font = _get_font(C.FONT_CAPTION_BOLD, 28)
    arrow_label_font = _get_font(C.FONT_MONO, 22)
    watermark_font = _get_font(C.FONT_ITALIC, 26)

    # ---------- Header ----------
    accent_glow(img, C.CANVAS_W // 2 - 260, 26, (520, 100),
                radius=50, color=C.COLOR_ACCENT, alpha=50, blur=22)
    draw.text((C.CANVAS_W // 2, 36), "RECAP",
              fill=C.COLOR_ACCENT, font=title_font, anchor="mt")
    draw.text((C.CANVAS_W // 2, 118), sb.lesson_title.upper(),
              fill=C.COLOR_TEXT, font=sub_font, anchor="mt")

    # ---------- Commands-entered panel (top) ----------
    beats_with_input = [b for b in sb.beats if b.input_display]
    row_h = 80
    panel_top_pad = 60
    panel_bot_pad = 30
    section_header_h = 56
    panel_h = section_header_h + len(beats_with_input) * row_h + panel_top_pad + panel_bot_pad
    panel_x0 = 50
    panel_x1 = C.CANVAS_W - 50
    panel_w = panel_x1 - panel_x0
    panel_y0 = 210
    compose_panel(img, panel_x0, panel_y0, (panel_w, panel_h), radius=36,
                  fill_rgba=(18, 24, 40, 200),
                  gradient=((40, 52, 78, 210), (14, 18, 30, 220)),
                  accent_edge_rgba=(*C.COLOR_ACCENT, 120),
                  shadow_blur=24, shadow_opacity=170,
                  shadow_offset=(0, 14))
    dd = ImageDraw.Draw(img)
    dd.text((C.CANVAS_W // 2, panel_y0 + 26), "COMMANDS ENTERED",
            fill=C.COLOR_ACCENT, font=section_font, anchor="mt")
    # Row for each input
    rows_top = panel_y0 + section_header_h + panel_top_pad
    for i, beat in enumerate(beats_with_input):
        ry = rows_top + i * row_h
        area = (panel_x0 + 20, ry, panel_x1 - 20, ry + row_h)
        # Step number (left circle)
        cn = panel_x0 + 52
        dd.ellipse([cn - 22, ry + row_h // 2 - 22, cn + 22, ry + row_h // 2 + 22],
                   fill=C.COLOR_ACCENT)
        dd.text((cn, ry + row_h // 2), str(i + 1),
                fill=(18, 22, 32), font=step_font, anchor="mm")
        # Compact input rendering
        _draw_mini_input(img, dd, beat.input_display,
                         (panel_x0 + 100, ry, panel_x1 - 30, ry + row_h))

    # ---------- UML sequence diagram section ----------
    diagram_top = panel_y0 + panel_h + 50
    diagram_bot = C.CANVAS_H - 160

    # Title for diagram
    dd.text((C.CANVAS_W // 2, diagram_top - 2), "SEQUENCE FLOW",
            fill=C.COLOR_ACCENT, font=section_font, anchor="mt")
    diagram_top += 56

    # Lane labels on the LEFT, lifelines running down vertically — this is a
    # true UML sequence diagram style.
    n_lanes = len(sb.lanes)
    lane_label_w = 250
    lane_header_h = 76
    lane_x_start = 80
    lane_gap = (C.CANVAS_W - 2 * lane_x_start - lane_label_w) / max(n_lanes - 1, 1)
    lane_head_xs = [lane_x_start + lane_label_w // 2 + int(i * lane_gap) for i in range(n_lanes)]

    # Draw lane header boxes at the top of the diagram
    for x, lane in zip(lane_head_xs, sb.lanes):
        box_w = 200
        box_x = x - box_w // 2
        compose_panel(img, box_x, diagram_top, (box_w, lane_header_h),
                      radius=18, fill_rgba=(28, 36, 54, 220),
                      accent_edge_rgba=(*C.COLOR_ACCENT, 200),
                      shadow_blur=10, shadow_opacity=120,
                      shadow_offset=(0, 6))
        dd = ImageDraw.Draw(img)
        dd.text((x, diagram_top + lane_header_h // 2), lane,
                fill=C.COLOR_LANE_LABEL_TEXT, font=label_font, anchor="mm")

    # Vertical lifelines (dashed)
    lifeline_top = diagram_top + lane_header_h + 8
    lifeline_bot = diagram_bot
    for x in lane_head_xs:
        for y in range(lifeline_top, lifeline_bot, 10):
            dd.line([x, y, x, y + 5], fill=(90, 104, 130, 200), width=2)

    # Arrange events vertically. Each event occupies a horizontal "row"
    # spanning two lanes; self-events sit on a single lane.
    events = [b for b in sb.beats if b.kind in ("call", "return", "self")]
    if events:
        row_gap = (lifeline_bot - lifeline_top - 40) / len(events)
        for idx, beat in enumerate(events):
            row_y = lifeline_top + 40 + int(idx * row_gap)
            step_no = idx + 1
            if beat.kind in ("call", "return"):
                if beat.from_lane not in sb.lanes or beat.to_lane not in sb.lanes:
                    continue
                x1 = lane_head_xs[sb.lanes.index(beat.from_lane)]
                x2 = lane_head_xs[sb.lanes.index(beat.to_lane)]
                color = C.COLOR_ACCENT if beat.kind == "call" else C.COLOR_PRIMARY
                # Arrow from x1 to x2 at row_y
                dd.line([x1, row_y, x2, row_y], fill=color, width=4)
                # Arrowhead at x2
                head = 12
                if x2 > x1:
                    dd.polygon([(x2 - head, row_y - head),
                                (x2 - head, row_y + head),
                                (x2, row_y)], fill=color)
                else:
                    dd.polygon([(x2 + head, row_y - head),
                                (x2 + head, row_y + head),
                                (x2, row_y)], fill=color)
                # Step number circle at left of line
                left_x = min(x1, x2) - 28
                dd.ellipse([left_x - 20, row_y - 20, left_x + 20, row_y + 20],
                           fill=(28, 36, 54), outline=C.COLOR_ACCENT, width=2)
                dd.text((left_x, row_y), str(step_no),
                        fill=C.COLOR_ACCENT, font=step_font, anchor="mm")
                # Label above midpoint
                mid_x = (x1 + x2) // 2
                lbox = dd.textbbox((0, 0), beat.label, font=arrow_label_font)
                lw = lbox[2] - lbox[0]
                dd.rounded_rectangle(
                    [mid_x - lw // 2 - 14, row_y - 32, mid_x + lw // 2 + 14, row_y - 4],
                    radius=8, fill=(18, 22, 34, 230), outline=color, width=1)
                dd.text((mid_x, row_y - 18), beat.label,
                        fill=C.COLOR_TEXT, font=arrow_label_font, anchor="mm")
            elif beat.kind == "self":
                if beat.from_lane not in sb.lanes:
                    continue
                x = lane_head_xs[sb.lanes.index(beat.from_lane)]
                # Self-loop arrow — loop to the right of the lane
                loop_w = 60
                dd.line([x, row_y, x + loop_w, row_y], fill=C.COLOR_ACCENT, width=3)
                dd.line([x + loop_w, row_y, x + loop_w, row_y + 24],
                        fill=C.COLOR_ACCENT, width=3)
                dd.line([x + loop_w, row_y + 24, x, row_y + 24],
                        fill=C.COLOR_ACCENT, width=3)
                head = 10
                dd.polygon([(x + head, row_y + 24 - head),
                            (x + head, row_y + 24 + head),
                            (x, row_y + 24)], fill=C.COLOR_ACCENT)
                # Step number on the left
                left_x = x - 48
                dd.ellipse([left_x - 20, row_y - 20, left_x + 20, row_y + 20],
                           fill=(28, 36, 54), outline=C.COLOR_ACCENT, width=2)
                dd.text((left_x, row_y), str(step_no),
                        fill=C.COLOR_ACCENT, font=step_font, anchor="mm")
                # Label to the right
                lbox = dd.textbbox((0, 0), beat.label, font=arrow_label_font)
                lw = lbox[2] - lbox[0]
                lx = x + loop_w + 16
                dd.rounded_rectangle(
                    [lx, row_y + 12 - 14, lx + lw + 22, row_y + 12 + 14],
                    radius=8, fill=(18, 22, 34, 230),
                    outline=C.COLOR_ACCENT, width=1)
                dd.text((lx + 11, row_y + 12), beat.label,
                        fill=C.COLOR_TEXT, font=arrow_label_font, anchor="lm")

    # Watermark
    dd.text((C.CANVAS_W - 24, C.CANVAS_H - 24), "by Elvis Jones",
            fill=(200, 200, 200), font=watermark_font, anchor="rb")

    return img.convert("RGB")


# -------------------- Backward-compat exports for build.py --------------------

def is_robot_moving(sb: Storyboard, t: float) -> bool:  # no-op; new anim picks handle this
    return False


def robot_y_at(sb: Storyboard, t: float) -> int:
    _, y = robot_xy_at(sb, t)
    return int(y)


def robot_walk_frame(t: float, moving: bool) -> str:
    return "idle_bob_0"
