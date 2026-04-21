"""Per-frame scene composition.

The camera travels right along the timeline at PIXELS_PER_SECOND. The robot is
pinned to ROBOT_SCREEN_X. Events (arrows, self-loops) are drawn at their
world_x = event_time * pps, which places them at screen center when the event
is happening and scrolls them left afterward. Lane labels on the far left are
pinned in screen-space on top of the scrolling content.
"""
from typing import Optional
from PIL import Image, ImageDraw, ImageFont

from . import config as C
from .sprite import (
    placeholder_robot, placeholder_user, upscale_pixel, SPRITE_SIZE,
)
from .storyboard import Storyboard, Beat
from .input_display import draw_input_display, current_input_display


def lane_y_positions(n_lanes: int) -> list[int]:
    y_start, y_end = C.TIMELINE_Y
    top_margin = 60
    bot_margin = 60
    usable = (y_end - bot_margin) - (y_start + top_margin)
    if n_lanes == 1:
        return [y_start + (y_end - y_start) // 2]
    step = usable / (n_lanes - 1)
    return [int(y_start + top_margin + i * step) for i in range(n_lanes)]


SELF_SCROLL = 140
OPEN_SCROLL = 80


def beat_scroll_distance(beat: Beat) -> float:
    if beat.kind in ("call", "return"):
        return beat.duration * C.PIXELS_PER_SECOND
    if beat.kind == "self":
        return SELF_SCROLL
    if beat.kind == "open":
        return OPEN_SCROLL
    return 0.0


def build_scroll_plan(sb: Storyboard) -> None:
    """Annotate each beat with event_world_x (at scroll midpoint)."""
    x = 0.0
    for beat in sb.beats:
        d = beat_scroll_distance(beat)
        beat.event_world_x = x + d / 2
        x += d
    sb._total_scroll_world = x  # type: ignore


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


def _ease_in_out(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return 3 * u * u - 2 * u * u * u


def robot_y_at(sb: Storyboard, t: float) -> int:
    ys = lane_y_positions(len(sb.lanes))
    lane_to_y = dict(zip(sb.lanes, ys))
    home_y = ys[0]
    current = home_y

    for beat in sb.beats:
        beat_end = beat.start_time + beat.duration
        if t < beat.start_time:
            return current
        if beat.kind == "open":
            if t >= beat.start_time:
                current = home_y
        elif beat.kind in ("call", "return"):
            from_y = lane_to_y.get(beat.from_lane, current)
            to_y = lane_to_y.get(beat.to_lane, current)
            if t >= beat_end:
                current = to_y
            elif t >= beat.start_time:
                u = (t - beat.start_time) / max(beat.duration, 0.01)
                return int(from_y + (to_y - from_y) * _ease_in_out(u))
        elif beat.kind == "self":
            y = lane_to_y.get(beat.from_lane, current)
            if t >= beat_end:
                current = y
            elif t >= beat.start_time:
                wobble = int(6 * (1 - abs(2 * ((t - beat.start_time) / max(beat.duration, 0.01)) - 1)))
                return y - wobble
        elif beat.kind == "finale":
            return current
    return current


def robot_walk_frame(t: float, moving: bool) -> str:
    if not moving:
        return "idle_0" if int(t * 2) % 2 == 0 else "idle_1"
    step = int(t * 8) % 2
    return f"walk_{step}"


def is_robot_moving(sb: Storyboard, t: float) -> bool:
    for beat in sb.beats:
        if beat.kind in ("call", "return") and beat.start_time <= t < beat.start_time + beat.duration:
            return True
    return False


def word_wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
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


def _draw_arrow(draw: ImageDraw.ImageDraw, x: float, y1: int, y2: int, color, label: str = "", label_font=None):
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
        draw.rectangle([bx0, by0, bx1, by1], fill=C.COLOR_OUTLINE)
        draw.rectangle([bx0, by0, bx1, by1], outline=C.COLOR_ACCENT, width=2)
        draw.text((bx0 + pad, mid_y), label, fill=C.COLOR_TEXT, font=label_font, anchor="lm")


def _draw_self_bubble(draw: ImageDraw.ImageDraw, x: float, y: int, color,
                      label: str = "", label_font=None, side_gap: int = 290):
    """Speech bubble sitting to the right of the robot at the lane's y. Action
    dot is placed at (x, y) on the lane line; the bubble body sits at
    (x + side_gap, y).
    """
    if not label or not label_font:
        return
    pad_x, pad_y = 18, 12
    bbox = draw.textbbox((0, 0), label, font=label_font)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    bubble_w = lw + pad_x * 2
    bubble_h = lh + pad_y * 2
    bcx = x + side_gap
    bcy = y - 8
    bx0 = bcx - bubble_w // 2
    bx1 = bcx + bubble_w // 2
    by0 = bcy - bubble_h // 2
    by1 = bcy + bubble_h // 2
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=12,
                           fill=C.COLOR_OUTLINE, outline=color, width=3)
    # Connector from the bubble to the action dot (short line left of bubble)
    draw.line([(x + 30, y), (bx0 - 4, bcy)], fill=color, width=3)
    # Label
    draw.text((bcx, bcy), label, fill=C.COLOR_TEXT,
              font=label_font, anchor="mm")
    # Action dot on the lane line at the event point
    draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=color,
                 outline=C.COLOR_OUTLINE, width=2)


def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def compose_frame(sb: Storyboard, t: float) -> Image.Image:
    img = Image.new("RGB", (C.CANVAS_W, C.CANVAS_H), C.COLOR_BG)
    draw = ImageDraw.Draw(img)

    header_font = _get_font(C.FONT_CAPTION_BOLD, 64)
    sub_font = _get_font(C.FONT_CAPTION, 42)
    label_font = _get_font(C.FONT_LABEL, 28)
    arrow_label_font = _get_font(C.FONT_MONO, 26)
    caption_font = _get_font(C.FONT_CAPTION_BOLD, 44)
    watermark_font = _get_font(C.FONT_ITALIC, 26)

    # 1. Header
    day_line = f"DAY {sb.day_number:02d}"
    draw.text((C.CANVAS_W // 2, 36), day_line, fill=C.COLOR_ACCENT, font=header_font, anchor="mt")
    draw.text((C.CANVAS_W // 2, 112), sb.learning_title.upper(),
              fill=C.COLOR_TEXT, font=sub_font, anchor="mt")

    # 2. Timeline: draw background lane lines
    ys = lane_y_positions(len(sb.lanes))
    camera_x = camera_x_at(sb, t)

    for y in ys:
        draw.line([C.LANE_LABEL_X[1] + 4, y, C.CANVAS_W, y],
                  fill=C.COLOR_LANE_LINE, width=2)

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
            _draw_self_bubble(draw, screen_x, y, C.COLOR_ACCENT, beat.label, arrow_label_font)

    # 4. Lane label boxes (pinned, drawn on top of scroll)
    for lane, y in zip(sb.lanes, ys):
        x0, x1 = C.LANE_LABEL_X
        draw.rectangle([x0, y - 34, x1, y + 34], fill=C.COLOR_LANE_LABEL_BG,
                       outline=C.COLOR_ACCENT, width=2)
        lines = word_wrap(lane, label_font, x1 - x0 - 16, draw)
        line_h = 30
        total_h = len(lines) * line_h
        y_start = y - total_h // 2 + line_h // 2
        for i, line in enumerate(lines[:2]):
            draw.text(((x0 + x1) // 2, y_start + i * line_h), line,
                      fill=C.COLOR_LANE_LABEL_TEXT, font=label_font, anchor="mm")

    # 5. Top area: dynamic input display for the current beat (keycaps, command,
    # text input, etc.) replacing the old user sprite.
    display = current_input_display(sb, t)
    draw_input_display(img, draw, display, t)

    # Connector line from the input-display zone down to the top lane
    connector_top = C.USER_Y[1] - 10
    connector_bot = ys[0] - 42
    if connector_bot > connector_top:
        draw.line([C.CANVAS_W // 2, connector_top, C.CANVAS_W // 2, connector_bot],
                  fill=C.COLOR_LANE_LINE, width=3)

    # 6. Robot sprite (centered, y follows state)
    moving = is_robot_moving(sb, t)
    robot_frame = robot_walk_frame(t, moving)
    robot_scale = 5
    robot_img = upscale_pixel(placeholder_robot(robot_frame), robot_scale)
    ry = robot_y_at(sb, t)
    rx = C.ROBOT_SCREEN_X - robot_img.width // 2
    img.paste(robot_img, (rx, ry - robot_img.height // 2), robot_img)

    # 7. Caption (current beat narration)
    current = None
    for beat in sb.beats:
        if beat.start_time <= t < beat.start_time + beat.duration:
            current = beat
            break
    if current and current.narration:
        cap_y_top = C.CAPTION_Y[0] + 30
        cap_w = C.CANVAS_W - 120
        lines = word_wrap(current.narration, caption_font, cap_w, draw)
        line_h = 54
        total_h = min(len(lines), 4) * line_h
        pad = 20
        box_x0 = 60
        box_x1 = C.CANVAS_W - 60
        box_y0 = cap_y_top - pad
        box_y1 = cap_y_top + total_h + pad
        # translucent box
        overlay = Image.new("RGBA", (box_x1 - box_x0, box_y1 - box_y0), (0, 0, 0, 180))
        img.paste(overlay, (box_x0, box_y0), overlay)
        for i, line in enumerate(lines[:4]):
            draw.text((C.CANVAS_W // 2, cap_y_top + i * line_h), line,
                      fill=C.COLOR_TEXT, font=caption_font, anchor="mt")

    # 8. Watermark
    draw.text((C.CANVAS_W - 24, C.CANVAS_H - 24), "by Elvis Jones",
              fill=(200, 200, 200), font=watermark_font, anchor="rb")

    return img


def compose_finale_frame(sb: Storyboard, phase_u: float) -> Image.Image:
    """Static summary view: whole sequence diagram visible at once.
    phase_u ranges 0..1 and controls a subtle fade-in effect.
    """
    img = Image.new("RGB", (C.CANVAS_W, C.CANVAS_H), C.COLOR_BG)
    draw = ImageDraw.Draw(img)

    header_font = _get_font(C.FONT_CAPTION_BOLD, 64)
    sub_font = _get_font(C.FONT_CAPTION, 42)
    label_font = _get_font(C.FONT_LABEL, 26)
    arrow_label_font = _get_font(C.FONT_MONO, 22)
    caption_font = _get_font(C.FONT_CAPTION_BOLD, 46)
    watermark_font = _get_font(C.FONT_ITALIC, 26)

    # Header
    draw.text((C.CANVAS_W // 2, 36), "FULL SEQUENCE",
              fill=C.COLOR_ACCENT, font=header_font, anchor="mt")
    draw.text((C.CANVAS_W // 2, 112), sb.lesson_title.upper(),
              fill=C.COLOR_TEXT, font=sub_font, anchor="mt")

    # Lane positions
    ys = lane_y_positions(len(sb.lanes))

    # Compress time: fit all events into viewport
    events = [b for b in sb.beats if b.kind in ("call", "return", "self")]
    view_x0 = C.LANE_LABEL_X[1] + 60
    view_x1 = C.CANVAS_W - 60
    if not events:
        xs_world = []
    else:
        step = (view_x1 - view_x0) / max(len(events), 1)
        xs_world = [view_x0 + i * step + step / 2 for i in range(len(events))]

    # Background lane lines
    for y in ys:
        draw.line([C.LANE_LABEL_X[1] + 4, y, C.CANVAS_W - 20, y],
                  fill=C.COLOR_LANE_LINE, width=2)

    # Events
    for beat, ex in zip(events, xs_world):
        if beat.kind in ("call", "return"):
            if beat.from_lane not in sb.lanes or beat.to_lane not in sb.lanes:
                continue
            y1 = ys[sb.lanes.index(beat.from_lane)]
            y2 = ys[sb.lanes.index(beat.to_lane)]
            color = C.COLOR_ACCENT if beat.kind == "call" else C.COLOR_PRIMARY
            _draw_arrow(draw, ex, y1, y2, color, beat.label, arrow_label_font)
        elif beat.kind == "self":
            if beat.from_lane not in sb.lanes:
                continue
            y = ys[sb.lanes.index(beat.from_lane)]
            _draw_self_bubble(draw, ex, y, C.COLOR_ACCENT, beat.label, arrow_label_font)

    # Lane labels
    for lane, y in zip(sb.lanes, ys):
        x0, x1 = C.LANE_LABEL_X
        draw.rectangle([x0, y - 34, x1, y + 34], fill=C.COLOR_LANE_LABEL_BG,
                       outline=C.COLOR_ACCENT, width=2)
        lines = word_wrap(lane, label_font, x1 - x0 - 16, draw)
        line_h = 28
        total_h = len(lines) * line_h
        y_start = y - total_h // 2 + line_h // 2
        for i, line in enumerate(lines[:2]):
            draw.text(((x0 + x1) // 2, y_start + i * line_h), line,
                      fill=C.COLOR_LANE_LABEL_TEXT, font=label_font, anchor="mm")

    # Top area: "ALL STEPS" badge instead of the old user sprite.
    badge_y = C.USER_Y[0] + (C.USER_Y[1] - C.USER_Y[0]) // 2
    badge_w = 340
    bx0 = C.CANVAS_W // 2 - badge_w // 2
    bx1 = C.CANVAS_W // 2 + badge_w // 2
    draw.rounded_rectangle([bx0, badge_y - 44, bx1, badge_y + 44], radius=14,
                           fill=C.COLOR_OUTLINE, outline=C.COLOR_ACCENT, width=3)
    check_font = _get_font(C.FONT_CAPTION_BOLD, 44)
    draw.text((C.CANVAS_W // 2, badge_y), "ALL STEPS \u2713",
              fill=C.COLOR_ACCENT, font=check_font, anchor="mm")

    # Final caption
    final_text = sb.lesson_title.rstrip(".") + "."
    cap_y_top = C.CAPTION_Y[0] + 30
    box_x0 = 60
    box_x1 = C.CANVAS_W - 60
    lines = word_wrap(final_text, caption_font, C.CANVAS_W - 120, draw)
    line_h = 56
    total_h = min(len(lines), 3) * line_h
    overlay = Image.new("RGBA", (box_x1 - box_x0, total_h + 40), (0, 0, 0, 200))
    img.paste(overlay, (box_x0, cap_y_top - 20), overlay)
    for i, line in enumerate(lines[:3]):
        draw.text((C.CANVAS_W // 2, cap_y_top + i * line_h), line,
                  fill=C.COLOR_ACCENT, font=caption_font, anchor="mt")

    # Watermark
    draw.text((C.CANVAS_W - 24, C.CANVAS_H - 24), "by Elvis Jones",
              fill=(200, 200, 200), font=watermark_font, anchor="rb")

    return img
