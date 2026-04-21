"""Per-frame scene composition — v4 electron redesign.

Key differences from v3:
- **No scrolling.** The layout is static. All lanes, arrows, and labels live
  in fixed screen positions the whole time.
- **No sprite mascot.** The "pen" is a glowing electron orb that travels the
  sequence diagram, drawing arrows progressively as it visits each beat.
- **Progressive build.** Arrows, self-dots, labels persist once drawn. The
  commands panel at the top fills up one row at a time.
- **Apple-style liquid glass panels** for the commands panel, lane labels,
  and caption.

Layout (all static):

    y=  0 — 140   Header strip
    y=140 — 440   COMMANDS ENTERED glass panel (accumulating)
    y=460 —1540   Sequence diagram canvas
                   ├ Lane labels (left pinned, x=40..280)
                   └ Lifelines + beat events (x=320..1040)
    y=1560—1820  Caption panel
    y=1820—1920  Watermark footer
"""
from __future__ import annotations

import math
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import config as C
from .storyboard import Storyboard, Beat
from .input_display import draw_input_display
from . import liquid_glass as LG
from . import electron as E
from . import smoke_bg


# -------------------- Layout constants (static) --------------------

HEADER_Y = (0, 140)
COMMANDS_Y = (150, 440)
DIAGRAM_Y = (480, 1540)
CAPTION_Y = (1560, 1820)
FOOTER_Y = (1820, 1920)

# Lane column geometry inside the diagram zone.
LANE_LABEL_X = (40, 300)
LIFELINE_X_START = 320
LIFELINE_X_END = 1040

# Beat x-positions are assigned evenly across the lifeline zone.
BEAT_LEFT_PAD = 60
BEAT_RIGHT_PAD = 80


# -------------------- Plan (beat -> screen coordinates) --------------------

def build_plan(sb: Storyboard) -> None:
    """Annotate each beat with:
      - `event_world_x` = its screen X (static — no camera).
      - `_e_start`, `_e_end` = electron positions for the beat.
      - `_step_no` = numbering that MATCHES the commands panel (1..N for the
         N beats with input_display, None for beats without).

    X positions are chosen so the *visible* events (non-open beats) are
    centered inside the diagram canvas, not the raw beat list — otherwise
    skipping beat 1 (open) shifts the whole diagram right.
    """
    if not sb.beats:
        return
    lane_y = _lane_y_map(sb)

    # Commands-panel step numbers: only beats with input_display count.
    input_step = 0
    for beat in sb.beats:
        if beat.input_display:
            input_step += 1
            beat._step_no = input_step
        else:
            beat._step_no = None

    # Figure out which beats actually render an event on the diagram.
    visible = [b for b in sb.beats if b.kind != "open"]
    nv = len(visible)

    usable = (LIFELINE_X_END - BEAT_RIGHT_PAD) - (LIFELINE_X_START + BEAT_LEFT_PAD)
    if nv > 0:
        step = usable / nv
        for i, beat in enumerate(visible):
            beat.event_world_x = LIFELINE_X_START + BEAT_LEFT_PAD + step * (i + 0.5)

    # Open beats take the x of the next visible beat (so the electron enters
    # the diagram at the same lane-column where the first event happens).
    next_visible_x = visible[0].event_world_x if visible else (
        LIFELINE_X_START + usable / 2)
    for i, beat in enumerate(sb.beats):
        if beat.kind == "open":
            # Find the next visible beat after this one.
            for j in range(i + 1, len(sb.beats)):
                if sb.beats[j].kind != "open":
                    next_visible_x = sb.beats[j].event_world_x
                    break
            beat.event_world_x = next_visible_x

    # Precompute start/end (x,y) for electron for each beat.
    for beat in sb.beats:
        bx = beat.event_world_x
        if beat.kind == "open":
            ly = lane_y[beat.to_lane]
            beat._e_start = (bx, ly)
            beat._e_end = (bx, ly)
        elif beat.kind == "self":
            ly = lane_y[beat.from_lane]
            beat._e_start = (bx, ly)
            beat._e_end = (bx, ly)
        elif beat.kind in ("call", "return"):
            ly1 = lane_y[beat.from_lane]
            ly2 = lane_y[beat.to_lane]
            beat._e_start = (bx, ly1)
            beat._e_end = (bx, ly2)
        else:
            beat._e_start = (bx, lane_y.get(beat.from_lane, list(lane_y.values())[0]))
            beat._e_end = beat._e_start


def _lane_y_map(sb: Storyboard) -> dict[str, int]:
    n = len(sb.lanes)
    y_start, y_end = DIAGRAM_Y
    top_margin = 80
    bot_margin = 60
    usable = (y_end - bot_margin) - (y_start + top_margin)
    if n == 1:
        return {sb.lanes[0]: y_start + usable // 2}
    step = usable / (n - 1)
    return {lane: int(y_start + top_margin + i * step)
            for i, lane in enumerate(sb.lanes)}


# Legacy shim: build.py and the smoke test call this name.
build_scroll_plan = build_plan


# -------------------- Electron path --------------------

def electron_xy_at(sb: Storyboard, t: float) -> tuple[float, float, float]:
    """Return (x, y, intensity) for the electron at time t.
    Intensity is 1.0 while active, fades to 0 during the finale hold."""
    if not sb.beats:
        return (0, 0, 0)

    # Before beat 0 starts: sit at beat 0 start.
    b0 = sb.beats[0]
    if t < b0.start_time:
        return (*b0._e_start, 1.0)

    # Find which beat we're in.
    for i, beat in enumerate(sb.beats):
        beat_end = beat.start_time + beat.duration
        if t >= beat_end:
            continue
        u = (t - beat.start_time) / max(beat.duration, 0.01)

        # At the very start of any beat after the first, hop from previous
        # beat's end to this beat's start over the first 15% of duration.
        hop_u_cap = 0.18
        if i > 0 and u < hop_u_cap:
            prev_end = sb.beats[i - 1]._e_end
            hu = u / hop_u_cap
            hu = E.ease_in_out(hu)
            x = E.lerp(prev_end[0], beat._e_start[0], hu)
            y = E.lerp(prev_end[1], beat._e_start[1], hu)
            return (x, y, 1.0)

        # Remap u to [0, 1] after the hop.
        u2 = (u - hop_u_cap) / max(1 - hop_u_cap, 0.01)
        u2 = max(0.0, min(1.0, u2))

        if beat.kind == "open":
            return (*beat._e_start, 1.0)
        if beat.kind == "self":
            # Orbit around the beat's x,y on the lane's horizontal line
            cx, cy = beat._e_start
            # 1.8 revolutions during the beat
            return (*E.orbit_xy(cx, cy, radius=32,
                                angular_speed=1.8 / max(beat.duration, 0.01),
                                t=u2 * beat.duration, phase=-math.pi / 2),
                    1.0)
        if beat.kind in ("call", "return"):
            eu = E.ease_in_out(u2)
            x = E.lerp(beat._e_start[0], beat._e_end[0], eu)
            y = E.lerp(beat._e_start[1], beat._e_end[1], eu)
            return (x, y, 1.0)

    # After all beats: sit at the final end point, fading out during finale_hold.
    last = sb.beats[-1]
    last_end = last.start_time + last.duration
    if t >= last_end:
        fade_t = t - last_end
        intensity = max(0.0, 1.0 - fade_t / max(sb.finale_hold * 0.4, 0.5))
        return (*last._e_end, intensity)
    return (*last._e_end, 1.0)


# -------------------- Trail --------------------

TRAIL_SPAN = 0.28  # seconds — how long the trail stretches behind
TRAIL_SAMPLES = 10


def electron_trail_positions(sb: Storyboard, t: float) -> list[tuple[float, float]]:
    """Sample recent electron positions for the trail effect."""
    positions = []
    for i in range(TRAIL_SAMPLES):
        dt = (i + 1) / TRAIL_SAMPLES * TRAIL_SPAN
        ts = t - dt
        if ts < 0:
            continue
        x, y, _ = electron_xy_at(sb, ts)
        positions.append((x, y))
    # oldest -> newest
    positions.reverse()
    return positions


# -------------------- Drawing helpers --------------------

def word_wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int,
              draw: ImageDraw.ImageDraw) -> list[str]:
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


def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


# -------------------- Backdrop --------------------

def _backdrop(t: float = 0.0) -> Image.Image:
    """Animated smoke/nebula backdrop at time t."""
    return smoke_bg.render_backdrop(t)


# -------------------- Event drawing --------------------

def _draw_lane_labels(img: Image.Image, sb: Storyboard, lane_y: dict[str, int],
                      label_font):
    for lane in sb.lanes:
        y = lane_y[lane]
        x0, x1 = LANE_LABEL_X
        w = x1 - x0
        h = 76
        LG.compose_liquid_glass(img, x0, y - h // 2, (w, h), radius=20,
                                blur_radius=14,
                                saturation=1.7,
                                tint_rgba=(220, 228, 242, 30),
                                rim_alpha=210,
                                corner_specular_alpha=90,
                                lensing_shift_px=5,
                                chromatic_aberration_px=1,
                                ripple_alpha=0,
                                shadow_blur=18, shadow_opacity=150,
                                shadow_offset=(0, 8))
        dd = ImageDraw.Draw(img)
        dd.text(((x0 + x1) // 2, y), lane,
                fill=(240, 246, 252), font=label_font, anchor="mm")


def _draw_lifelines(img: Image.Image, sb: Storyboard, lane_y: dict[str, int]):
    """Static horizontal lane lines from right of the label to near the right edge."""
    dd = ImageDraw.Draw(img)
    for lane in sb.lanes:
        y = lane_y[lane]
        # Dashed
        for x in range(LIFELINE_X_START, LIFELINE_X_END, 14):
            dd.line([x, y, x + 8, y], fill=(78, 98, 128, 220), width=2)


def _draw_flow_pulse(base: Image.Image, x: int, y1: int, y2: int,
                     phase: float, color: tuple[int, int, int]):
    """Overlay a bright moving pulse on a completed arrow (y1 -> y2).
    Three layers: wide outer glow (blur 12) + mid-width blurred core (blur 4)
    + sharp hot-white core. Plus a decaying trailing streak behind the pulse
    that reads as energy still flowing past."""
    length = y2 - y1  # signed
    abs_len = abs(length)
    if abs_len < 20:
        return
    pulse_len = abs_len * 0.22
    tail_len = abs_len * 0.35
    pulse_center_y = y1 + length * phase
    direction = 1 if length > 0 else -1
    brighter = tuple(min(255, int(c * 0.45 + 255 * 0.55)) for c in color)
    hot = (255, 255, 255)

    glow = Image.new("RGBA", (base.width, base.height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mid = Image.new("RGBA", (base.width, base.height), (0, 0, 0, 0))
    md = ImageDraw.Draw(mid)
    core = Image.new("RGBA", (base.width, base.height), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)

    # Main pulse (cosine window).
    n = 28
    for i in range(n):
        u = i / (n - 1)
        dy = (u - 0.5) * pulse_len * direction
        py = int(pulse_center_y + dy)
        if py < -6 or py > base.height + 6:
            continue
        window = 0.5 * (1 + math.cos((u - 0.5) * 2 * math.pi))
        a_glow = int(window * 180)
        a_mid = int(window * 230)
        a_core = int(window * 255)
        gd.ellipse([x - 8, py - 8, x + 8, py + 8], fill=(*brighter, a_glow))
        md.ellipse([x - 4, py - 4, x + 4, py + 4], fill=(*brighter, a_mid))
        cd.ellipse([x - 2, py - 2, x + 2, py + 2], fill=(*hot, a_core))

    # Trail (behind the pulse, fading).
    m = 16
    for i in range(m):
        u = i / (m - 1)  # 0 = just behind pulse, 1 = far behind
        back = -direction * (pulse_len / 2 + u * tail_len)
        py = int(pulse_center_y + back)
        if py < -6 or py > base.height + 6:
            continue
        # Quadratic fade
        fade = (1 - u) ** 2
        a_glow = int(fade * 110)
        a_mid = int(fade * 150)
        gd.ellipse([x - 6, py - 6, x + 6, py + 6], fill=(*brighter, a_glow))
        md.ellipse([x - 3, py - 3, x + 3, py + 3], fill=(*brighter, a_mid))

    glow = glow.filter(ImageFilter.GaussianBlur(12))
    mid = mid.filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(glow)
    base.alpha_composite(mid)
    base.alpha_composite(core)


def _draw_event_lines(base: Image.Image, beat: Beat, lane_y: dict[str, int],
                      progress: float):
    """Lines-only pass for a beat. Labels and step chips come later, on top of
    liquid-glass panels."""
    if progress <= 0:
        return
    dd = ImageDraw.Draw(base)
    x = beat.event_world_x
    if beat.kind in ("call", "return"):
        y1 = lane_y[beat.from_lane]
        y2 = lane_y[beat.to_lane]
        color = (90, 190, 255) if beat.kind == "call" else (236, 140, 96)
        y_cur = y1 + (y2 - y1) * progress
        # Base line — dim. The flow pulse overlay is the "alive" element.
        dd.line([x, y1, x, y_cur], fill=(*color, 130), width=3)
        if progress >= 0.98:
            head = 12
            if y2 > y1:
                dd.polygon([(x - head, y2 - head), (x + head, y2 - head),
                            (x, y2)], fill=color)
            else:
                dd.polygon([(x - head, y2 + head), (x + head, y2 + head),
                            (x, y2)], fill=color)
    elif beat.kind == "self":
        y = lane_y[beat.from_lane]
        ring_alpha = min(1.0, progress / 0.8)
        ring_r = 14
        color = (244, 211, 94)
        ring = Image.new("RGBA", (ring_r * 2 + 4, ring_r * 2 + 4), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse([2, 2, ring_r * 2 + 1, ring_r * 2 + 1],
                   outline=(*color, int(220 * ring_alpha)), width=3)
        rd.ellipse([8, 8, ring_r * 2 - 5, ring_r * 2 - 5],
                   fill=(*color, int(180 * ring_alpha)))
        base.alpha_composite(ring, (int(x - ring_r - 2), int(y - ring_r - 2)))


def _beat_label_placement(beat: Beat, lane_y: dict[str, int]) -> tuple[int, int, int]:
    """Return (cx, cy, color_tag) for the beat's label center.
    color_tag is 0 for call (cyan), 1 for return (amber), 2 for self (amber)."""
    x = int(beat.event_world_x)
    if beat.kind in ("call", "return"):
        y1 = lane_y[beat.from_lane]
        y2 = lane_y[beat.to_lane]
        if beat.kind == "return":
            label_y = int(y2 + (y1 - y2) * 0.15)
            # Label will be drawn to the LEFT of the arrow; center placed so
            # the right edge of the label ends at x-18.
            return (x - 18, label_y, 1)
        return (x + 18, (y1 + y2) // 2, 0)
    # self
    y = lane_y[beat.from_lane]
    return (x + 28, y, 2)


def _draw_event_labels(base: Image.Image, sb: Storyboard, t: float, lane_y,
                       arrow_label_font, show_step: bool):
    """Render arrow/self labels as mini liquid-glass tiles ON TOP of lines.
    Also renders the step-number chips when show_step is true."""
    dd = ImageDraw.Draw(base)
    CALL_C = (90, 190, 255)
    RET_C = (236, 140, 96)
    SELF_C = (244, 211, 94)
    color_map = [CALL_C, RET_C, SELF_C]

    for beat in sb.beats:
        if beat.kind == "open":
            continue
        prog = _beat_progress(beat, t)
        reveal_thresh = 0.75 if beat.kind == "self" else 0.95
        if prog < reveal_thresh or not beat.label:
            continue
        anchor_x, anchor_y, color_tag = _beat_label_placement(beat, lane_y)
        color = color_map[color_tag]

        # Measure label
        pad_x, pad_y = 14, 10
        bbox = dd.textbbox((0, 0), beat.label, font=arrow_label_font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        tile_w = lw + pad_x * 2
        tile_h = lh + pad_y * 2

        if beat.kind == "return":
            # anchor_x is right edge
            tx = anchor_x - tile_w
            ty = anchor_y - tile_h // 2
        elif beat.kind == "self":
            tx = anchor_x
            ty = anchor_y - tile_h // 2
        else:
            tx = anchor_x
            ty = anchor_y - tile_h // 2

        # Mini liquid-glass tile with colored edge.
        LG.compose_liquid_glass(base, tx, ty, (tile_w, tile_h),
                                radius=8,
                                blur_radius=6,
                                saturation=1.4,
                                tint_rgba=(230, 240, 255, 28),
                                rim_alpha=180,
                                corner_specular_alpha=45,
                                lensing_shift_px=1,
                                ripple_alpha=5,
                                shadow_blur=10, shadow_opacity=90,
                                shadow_offset=(0, 4))
        # Colored border stroke
        dd = ImageDraw.Draw(base)
        dd.rounded_rectangle([tx, ty, tx + tile_w - 1, ty + tile_h - 1],
                             radius=8, outline=(*color, 220), width=2)
        # Label text
        dd.text((tx + tile_w // 2, ty + tile_h // 2), beat.label,
                fill=(240, 246, 252), font=arrow_label_font, anchor="mm")

    # Step number chips (finale only)
    if show_step:
        for beat in sb.beats:
            step_no = getattr(beat, "_step_no", None)
            prog = _beat_progress(beat, t)
            if step_no is None or prog < 0.95:
                continue
            if beat.kind == "open":
                continue
            x = int(beat.event_world_x)
            if beat.kind == "return":
                y1 = lane_y[beat.from_lane]
                y2 = lane_y[beat.to_lane]
                scn_x = x + 48
                scn_y = int(y2 + (y1 - y2) * 0.15)
            elif beat.kind == "call":
                y1 = lane_y[beat.from_lane]
                y2 = lane_y[beat.to_lane]
                scn_x = x - 48
                scn_y = (y1 + y2) // 2
            else:
                scn_x = x - 48
                scn_y = lane_y[beat.from_lane]
            dd.ellipse([scn_x - 20, scn_y - 20, scn_x + 20, scn_y + 20],
                       fill=(28, 36, 54), outline=(244, 211, 94), width=2)
            dd.text((scn_x, scn_y), str(step_no),
                    fill=(244, 211, 94),
                    font=_get_font(C.FONT_CAPTION_BOLD, 28), anchor="mm")


def _beat_progress(beat: Beat, t: float) -> float:
    """0 before start, 1 at/after end, smooth in between."""
    if t < beat.start_time:
        return 0.0
    if t >= beat.start_time + beat.duration:
        return 1.0
    u = (t - beat.start_time) / max(beat.duration, 0.01)
    # Skip the first 18% (hop) and the last 5% — arrow should draw during middle
    u = max(0.0, min(1.0, (u - 0.18) / 0.82))
    return E.ease_in_out(u)


# -------------------- Commands panel --------------------

def _draw_commands_panel(img: Image.Image, sb: Storyboard, t: float):
    """Draw the glass tile only — the rows are drawn by
    _draw_commands_panel_rows after the tile, so they sit on top."""
    x0, y0 = 50, COMMANDS_Y[0]
    w = C.CANVAS_W - 100
    h = COMMANDS_Y[1] - COMMANDS_Y[0] - 10
    LG.compose_liquid_glass(img, x0, y0, (w, h), radius=32,
                            blur_radius=28,
                            saturation=1.85,
                            tint_rgba=(220, 228, 242, 30),
                            rim_alpha=220,
                            corner_specular_alpha=120,
                            lensing_shift_px=8,
                            chromatic_aberration_px=2,
                            ripple_alpha=0,
                            shadow_blur=32, shadow_opacity=180,
                            shadow_offset=(0, 16))


def _draw_mini_input(img: Image.Image, dd: ImageDraw.ImageDraw,
                     display: dict, area: tuple[int, int, int, int],
                     alpha_scale: float = 1.0):
    x0, y0, x1, y1 = area
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2

    kind = display.get("type", "")
    label_font = _get_font(C.FONT_LABEL, 22)
    key_font = _get_font(C.FONT_CAPTION_BOLD, 26)
    mono_font = _get_font(C.FONT_MONO, 28)

    def _txt_alpha(rgb, base_alpha=255):
        return (*rgb, int(base_alpha * alpha_scale))

    if kind == "keycaps":
        rows = display.get("rows", [])
        x = x0 + 12
        for row in rows:
            platform = row.get("platform", "")
            keys = row.get("keys", [])
            dd.text((x, cy), f"{platform}:",
                    fill=_txt_alpha((160, 180, 210)),
                    font=label_font, anchor="lm")
            pbbox = dd.textbbox((0, 0), f"{platform}:", font=label_font)
            x += (pbbox[2] - pbbox[0]) + 10
            first = True
            for k in keys:
                if not first:
                    dd.text((x, cy), "+",
                            fill=_txt_alpha((244, 211, 94)),
                            font=key_font, anchor="lm")
                    x += 18
                kbbox = dd.textbbox((0, 0), k, font=key_font)
                kw = kbbox[2] - kbbox[0] + 22
                dd.rounded_rectangle(
                    [x, cy - 22, x + kw, cy + 22], radius=8,
                    fill=(28, 36, 54, int(255 * alpha_scale)),
                    outline=_txt_alpha((244, 211, 94), 255), width=2)
                dd.text((x + kw // 2, cy), k,
                        fill=_txt_alpha((240, 246, 252)),
                        font=key_font, anchor="mm")
                x += kw + 10
                first = False
            x += 24
    elif kind == "key":
        label = display.get("label", "")
        kbbox = dd.textbbox((0, 0), label, font=key_font)
        kw = kbbox[2] - kbbox[0] + 30
        dd.rounded_rectangle(
            [cx - kw // 2, cy - 22, cx + kw // 2, cy + 22], radius=8,
            fill=(28, 36, 54, int(255 * alpha_scale)),
            outline=_txt_alpha((244, 211, 94), 255), width=2)
        dd.text((cx, cy), label, fill=_txt_alpha((240, 246, 252)),
                font=key_font, anchor="mm")
    elif kind == "text_input":
        text = display.get("text", "")
        box_w = min(x1 - x0 - 60, 500)
        box_h = 46
        bx0 = cx - box_w // 2
        bx1 = cx + box_w // 2
        dd.rounded_rectangle(
            [bx0, cy - box_h // 2, bx1, cy + box_h // 2], radius=12,
            fill=(28, 36, 54, int(255 * alpha_scale)),
            outline=_txt_alpha((244, 211, 94), 255), width=2)
        gx = bx0 + 24
        dd.ellipse([gx - 8, cy - 8, gx + 4, cy + 4],
                   outline=_txt_alpha((160, 180, 210), 255), width=2)
        dd.line([gx + 2, cy + 2, gx + 10, cy + 10],
                fill=_txt_alpha((160, 180, 210), 255), width=2)
        dd.text((bx0 + 44, cy), text,
                fill=_txt_alpha((240, 246, 252)),
                font=key_font, anchor="lm")
    elif kind == "command":
        prompt = display.get("prompt", "$")
        text = display.get("text", "")
        box_w = min(x1 - x0 - 60, 500)
        box_h = 46
        bx0 = cx - box_w // 2
        bx1 = cx + box_w // 2
        dd.rounded_rectangle(
            [bx0, cy - box_h // 2, bx1, cy + box_h // 2], radius=10,
            fill=(10, 14, 22, int(255 * alpha_scale)),
            outline=_txt_alpha((244, 211, 94), 255), width=2)
        dd.text((bx0 + 16, cy), prompt,
                fill=_txt_alpha((244, 211, 94)),
                font=mono_font, anchor="lm")
        dd.text((bx0 + 48, cy), text,
                fill=_txt_alpha((240, 246, 252)),
                font=mono_font, anchor="lm")


# -------------------- Main compose_frame --------------------

def compose_frame(sb: Storyboard, t: float) -> Image.Image:
    # 1. Animated smoke backdrop
    base = _backdrop(t).convert("RGBA")

    header_font = _get_font(C.FONT_CAPTION_BOLD, 60)
    sub_font = _get_font(C.FONT_CAPTION, 36)
    lane_font = _get_font(C.FONT_LABEL, 28)
    arrow_label_font = _get_font(C.FONT_MONO, 24)
    caption_font = _get_font(C.FONT_CAPTION_BOLD, 42)
    watermark_font = _get_font(C.FONT_ITALIC, 26)

    # ---- 2. Header text (just type, no glass) ----
    LG.accent_glow(base, C.CANVAS_W // 2 - 200, 20, (400, 100),
                   radius=48, color=(244, 211, 94), alpha=45, blur=22)
    dd = ImageDraw.Draw(base)
    dd.text((C.CANVAS_W // 2, 28), f"DAY {sb.day_number:02d}",
            fill=(244, 211, 94), font=header_font, anchor="mt")
    dd.text((C.CANVAS_W // 2, 96), sb.learning_title.upper(),
            fill=(232, 240, 248), font=sub_font, anchor="mt")

    # ---- 3. Diagram geometry ----
    lane_y = _lane_y_map(sb)
    _draw_lifelines(base, sb, lane_y)

    # ---- 4. Arrow LINES only (no labels yet) — goes BEHIND panels ----
    last = sb.beats[-1]
    last_end = last.start_time + last.duration
    show_step_numbers = t >= last_end + 0.4
    for beat in sb.beats:
        prog = _beat_progress(beat, t)
        if prog <= 0:
            continue
        _draw_event_lines(base, beat, lane_y, prog)

    # ---- 5. Flowing pulse overlay on every completed call/return arrow ----
    for beat in sb.beats:
        prog = _beat_progress(beat, t)
        if prog < 0.98 or beat.kind not in ("call", "return"):
            continue
        # Each arrow has its own phase offset so pulses don't line up.
        x = int(beat.event_world_x)
        y1 = lane_y[beat.from_lane]
        y2 = lane_y[beat.to_lane]
        color = (90, 190, 255) if beat.kind == "call" else (236, 140, 96)
        phase_offset = (hash(beat.label or "") % 100) / 100.0
        phase = ((t / 1.6) + phase_offset) % 1.0
        _draw_flow_pulse(base, x, y1, y2, phase, color)

    # ---- 6. Electron trail + core (the active drawing agent) ----
    ex, ey, intensity = electron_xy_at(sb, t)
    if intensity > 0.02:
        trail = electron_trail_positions(sb, t)
        if trail:
            E.paste_trail(base, trail, size=50, core_r=3)
        E.paste_electron(base, ex, ey, size=66, core_r=5,
                         intensity=intensity)

    # ---- 7. LIQUID GLASS panels ON TOP of lines ----
    _draw_commands_panel(base, sb, t)
    _draw_lane_labels(base, sb, lane_y, lane_font)

    # Commands-panel content (rows) — draw on top of the glass tile
    _draw_commands_panel_rows(base, sb, t)

    # ---- 8. Event labels (mini glass tiles) + step chips ----
    _draw_event_labels(base, sb, t, lane_y, arrow_label_font, show_step_numbers)

    # ---- 9. Caption panel ----
    current = None
    for beat in sb.beats:
        if beat.start_time <= t < beat.start_time + beat.duration:
            current = beat
            break
    if t >= last_end:
        narration_text = "Day one complete. Ready for day two?"
    elif current and current.narration:
        narration_text = current.narration
    else:
        narration_text = ""
    if narration_text:
        cap_x0 = 60
        cap_w = C.CANVAS_W - 120
        dd = ImageDraw.Draw(base)
        lines = word_wrap(narration_text, caption_font, cap_w - 40, dd)
        line_h = 52
        shown = lines[:4]
        cap_h = max(130, len(shown) * line_h + 46)
        cap_y = CAPTION_Y[0] + (CAPTION_Y[1] - CAPTION_Y[0] - cap_h) // 2
        LG.compose_liquid_glass(base, cap_x0, cap_y, (cap_w, cap_h), radius=28,
                                blur_radius=26,
                                saturation=1.7,
                                tint_rgba=(220, 228, 242, 30),
                                rim_alpha=210,
                                corner_specular_alpha=110,
                                lensing_shift_px=7,
                                chromatic_aberration_px=2,
                                ripple_alpha=0,
                                shadow_blur=26, shadow_opacity=180,
                                shadow_offset=(0, 14))
        dd = ImageDraw.Draw(base)
        text_y = cap_y + (cap_h - len(shown) * line_h) // 2 + 4
        for i, line in enumerate(shown):
            dd.text((C.CANVAS_W // 2, text_y + i * line_h), line,
                    fill=(240, 246, 252), font=caption_font, anchor="mt")

    # ---- 10. Watermark ----
    dd = ImageDraw.Draw(base)
    dd.text((C.CANVAS_W - 24, C.CANVAS_H - 24), "by Elvis Jones",
            fill=(210, 210, 215), font=watermark_font, anchor="rb")

    return base.convert("RGB")


def _draw_commands_panel_rows(img: Image.Image, sb: Storyboard, t: float):
    """Render the numbered rows ON TOP of the commands glass tile."""
    x0, y0 = 50, COMMANDS_Y[0]
    w = C.CANVAS_W - 100
    h = COMMANDS_Y[1] - COMMANDS_Y[0] - 10

    dd = ImageDraw.Draw(img)
    title_font = _get_font(C.FONT_CAPTION_BOLD, 28)
    dd.text((x0 + w // 2, y0 + 26), "COMMANDS ENTERED",
            fill=(244, 211, 94), font=title_font, anchor="mt")

    slot_top = y0 + 72
    slot_h = (h - 90) // 4
    inputs = [b for b in sb.beats if b.input_display]
    step_font = _get_font(C.FONT_CAPTION_BOLD, 22)

    for i, beat in enumerate(inputs):
        if t < beat.start_time:
            continue
        alpha_scale = min(1.0, (t - beat.start_time) / 0.35)
        row_y = slot_top + i * slot_h + slot_h // 2
        cn = x0 + 36
        dd.ellipse([cn - 16, row_y - 16, cn + 16, row_y + 16],
                   fill=(244, 211, 94))
        dd.text((cn, row_y), str(i + 1),
                fill=(18, 22, 32), font=step_font, anchor="mm")
        _draw_mini_input(img, dd, beat.input_display,
                         (x0 + 64, row_y - slot_h // 2 + 4,
                          x0 + w - 20, row_y + slot_h // 2 - 4),
                         alpha_scale=alpha_scale)


def compose_finale_frame(sb: Storyboard, phase_u: float) -> Image.Image:
    """v4: the scroll frame and the finale are the same visual — the whole
    diagram is built up during playback. For the finale hold, we just pass a
    time past the last beat so everything (including step numbers) is shown.
    """
    last = sb.beats[-1]
    t = last.start_time + last.duration + sb.finale_hold * max(phase_u, 0.5)
    return compose_frame(sb, t)


# -------------------- Back-compat shims for build.py --------------------

def camera_x_at(sb: Storyboard, t: float) -> float:
    return 0.0


def robot_y_at(sb: Storyboard, t: float) -> int:
    _, y, _ = electron_xy_at(sb, t)
    return int(y)


def is_robot_moving(sb: Storyboard, t: float) -> bool:
    return False


def robot_walk_frame(t: float, moving: bool) -> str:
    return "idle_bob_0"


def lane_y_positions(n_lanes: int) -> list[int]:
    # Compatibility for smoke tests.
    y_start, y_end = DIAGRAM_Y
    top_margin = 80
    bot_margin = 60
    usable = (y_end - bot_margin) - (y_start + top_margin)
    if n_lanes == 1:
        return [y_start + usable // 2]
    step = usable / (n_lanes - 1)
    return [int(y_start + top_margin + i * step) for i in range(n_lanes)]
