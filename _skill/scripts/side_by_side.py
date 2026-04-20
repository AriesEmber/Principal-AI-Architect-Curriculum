"""Shared side-by-side PowerShell/Bash renderer.

Produces three artifacts from one configuration:

  * ``L-###-terminal.gif`` - animated typewriter demo (Pillow, palette quantised)
  * ``L-###-terminal.png`` - static panel that matches the final GIF frame, trimmed
    to content (no trailing whitespace)
  * ``L-###-terminal.svg`` - hand-authored SVG mirroring the static panel

``LessonConfig.primary_shell`` decides which shell gets the left column.
Default is ``"powershell"`` so Windows learners see their own environment
first. When set to ``"bash"`` the renderer falls back to the pre-2026-04-19
left=Bash/right=PowerShell orientation.

When ``primary_shell == "powershell"``:
  * ``Exchange.left`` is the PowerShell side (drawn left, PS styling)
  * ``Exchange.right`` is the Bash side (drawn right, Bash styling)

When ``primary_shell == "bash"``:
  * ``Exchange.left`` is the Bash side (drawn left, Bash styling)
  * ``Exchange.right`` is the PowerShell side (drawn right, PS styling)

Build scripts must populate ``Exchange.left`` / ``Exchange.right`` to match
the ``primary_shell`` they declared.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from xml.sax.saxutils import escape as xml_escape

from PIL import Image, ImageDraw, ImageFont


# ---------- tokens ----------

BG = (11, 13, 18)          # #0b0d12 - page background

# Bash (left)
BASH_WIN = (27, 32, 41)
BASH_WIN_DK = (18, 22, 29)
BASH_TITLE = (38, 44, 56)
BASH_BORDER = (42, 49, 64)
BASH_NOTE = (20, 25, 35)
BASH_TITLE_FG = (154, 163, 178)
BASH_PROMPT_USER = (106, 167, 255)
BASH_PROMPT_PATH = (199, 146, 234)
BASH_PROMPT_PUNCT = (126, 134, 151)
TEXT_BASH = (230, 237, 243)

# PowerShell (right)
PS_WIN = (1, 36, 86)
PS_WIN_DK = (1, 23, 54)
PS_TITLE = (10, 58, 115)
PS_BORDER = (28, 77, 140)
PS_NOTE = (3, 26, 58)
PS_TITLE_FG = (207, 217, 238)
PS_PROMPT_INTRO = (207, 217, 238)
PS_PROMPT_PATH = (155, 180, 221)
PS_PROMPT_GT = (207, 217, 238)
TEXT_PS = (255, 255, 255)

# shared
OUTPUT_GREEN = (126, 231, 135)
OUTPUT_GREY = (139, 148, 165)
ARG_QUOTED = (255, 171, 112)
ARG_VAR = (242, 204, 96)
CAPTION = (154, 163, 178)
STEP_LABEL = (139, 148, 165)


def hex_of(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


# ---------- configuration dataclasses ----------


@dataclass
class Segment:
    text: str
    color: tuple[int, int, int]


@dataclass
class Side:
    cmd: list[Segment]
    out: list[Segment] = field(default_factory=list)

    def cmd_chars(self) -> int:
        return sum(len(s.text) for s in self.cmd)


@dataclass
class Exchange:
    left: Side
    right: Side
    step_label: str = ""   # e.g. "1. No quotes"


@dataclass
class Note:
    """Bottom note strip under each terminal window."""
    left_text: str
    right_text: str


@dataclass
class LessonConfig:
    lesson_id: str                  # "L-004"
    title: str                      # "pwd - identical in Bash, aliased in PowerShell"
    bash_prompt_path: str           # "~"
    ps_prompt_path: str             # r"C:\Users\learner"
    exchanges: list[Exchange]
    caption: str
    note: Note
    bash_title: str = "Bash \u00b7 macOS / Linux / WSL"
    ps_title: str = "PowerShell \u00b7 Windows"
    primary_shell: str = "powershell"
    # final-frame renderer hooks: extra trailing rows to draw in either column.
    # Used when one side "keeps going" after the last paired exchange.


# ---------- font loading ----------


def _font_candidates() -> list[str]:
    return [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in _font_candidates():
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


# ---------- layout ----------


@dataclass
class Layout:
    W: int = 1400
    top_strip_h: int = 50        # title strip above windows
    win_margin: int = 20
    title_h: int = 40
    body_pad_x: int = 22
    body_pad_y: int = 18         # inside window, below title bar
    line_h: int = 28
    note_h: int = 56
    caption_h: int = 40
    cursor_w: int = 10
    cursor_h: int = 20
    font_size: int = 16
    small_size: int = 13
    title_size: int = 13

    def compute_height(self, max_lines: int) -> int:
        """Return canvas H that exactly fits the configured number of lines
        plus the title, note, and caption - no trailing whitespace."""
        body_h = max_lines * self.line_h + 8
        win_h = self.title_h + self.body_pad_y + body_h + 10 + self.note_h
        # top_strip + margin + win_h + margin + caption
        return (
            self.top_strip_h
            + self.win_margin
            + win_h
            + self.win_margin
            + self.caption_h
        )


# ---------- renderer ----------


class SideBySideRenderer:
    def __init__(self, cfg: LessonConfig, layout: Layout | None = None):
        self.cfg = cfg
        self.layout = layout or Layout()
        self.max_lines = self._max_lines()
        self.H = self.layout.compute_height(self.max_lines)
        self.W = self.layout.W
        self.WIN_W = (self.W - self.layout.win_margin * 3) // 2
        self.WIN_Y = self.layout.top_strip_h + self.layout.win_margin
        self.WIN_H = (
            self.H
            - self.layout.top_strip_h
            - self.layout.win_margin * 2
            - self.layout.caption_h
        )
        self.LEFT_X = self.layout.win_margin
        self.RIGHT_X = self.layout.win_margin * 2 + self.WIN_W
        self.font = load_font(self.layout.font_size)
        self.small = load_font(self.layout.small_size)
        self.title_font = load_font(self.layout.title_size)

    def _max_lines(self) -> int:
        # Each exchange = 1 cmd line + len(out) lines. Plus one trailing prompt.
        total = 0
        for ex in self.cfg.exchanges:
            total += 1 + max(len(ex.left.out), len(ex.right.out))
        return total + 1  # trailing prompt

    # ---- Pillow frame rendering ----

    def _draw_window(
        self,
        im: Image.Image,
        x: int,
        *,
        is_ps: bool,
        title: str,
        is_right: bool,
    ) -> None:
        draw = ImageDraw.Draw(im)
        fill = PS_WIN if is_ps else BASH_WIN
        title_fill = PS_TITLE if is_ps else BASH_TITLE
        border = PS_BORDER if is_ps else BASH_BORDER
        title_fg = PS_TITLE_FG if is_ps else BASH_TITLE_FG
        note_fill = PS_NOTE if is_ps else BASH_NOTE

        draw.rounded_rectangle(
            [x, self.WIN_Y, x + self.WIN_W, self.WIN_Y + self.WIN_H],
            radius=12,
            fill=fill,
            outline=border,
            width=1,
        )
        draw.rounded_rectangle(
            [x, self.WIN_Y, x + self.WIN_W, self.WIN_Y + self.layout.title_h],
            radius=12,
            fill=title_fill,
        )
        draw.rectangle(
            [
                x,
                self.WIN_Y + self.layout.title_h - 10,
                x + self.WIN_W,
                self.WIN_Y + self.layout.title_h,
            ],
            fill=title_fill,
        )
        # Traffic lights
        for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
            cx = x + 22 + i * 20
            cy = self.WIN_Y + 20
            draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=c)
        tw = draw.textlength(title, font=self.title_font)
        draw.text(
            (x + (self.WIN_W - tw) / 2, self.WIN_Y + 13),
            title,
            font=self.title_font,
            fill=title_fg,
        )
        # Bottom note strip inside window
        note_top = self.WIN_Y + self.WIN_H - self.layout.note_h
        draw.rectangle(
            [x + 1, note_top, x + self.WIN_W - 1, self.WIN_Y + self.WIN_H - 1],
            fill=note_fill,
        )
        note_text = self.cfg.note.right_text if is_right else self.cfg.note.left_text
        self._draw_wrapped_note(draw, x + 16, note_top + 10, note_text, is_ps=is_ps)

    def _draw_wrapped_note(
        self,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        text: str,
        *,
        is_ps: bool,
    ) -> None:
        max_w = self.WIN_W - 32
        color = PS_TITLE_FG if is_ps else BASH_TITLE_FG
        # naive wrap by words
        words = text.split()
        line = ""
        cy = y
        for w in words:
            trial = (line + " " + w).strip()
            if draw.textlength(trial, font=self.small) <= max_w:
                line = trial
            else:
                draw.text((x, cy), line, font=self.small, fill=color)
                cy += 18
                line = w
        if line:
            draw.text((x, cy), line, font=self.small, fill=color)

    def _bash_prompt_segs(self) -> list[Segment]:
        return [
            Segment("learner@laptop", BASH_PROMPT_USER),
            Segment(":", BASH_PROMPT_PUNCT),
            Segment(self.cfg.bash_prompt_path, BASH_PROMPT_PATH),
            Segment("$ ", BASH_PROMPT_PUNCT),
        ]

    def _ps_prompt_segs(self) -> list[Segment]:
        return [
            Segment("PS ", PS_PROMPT_INTRO),
            Segment(self.cfg.ps_prompt_path, PS_PROMPT_PATH),
            Segment("> ", PS_PROMPT_GT),
        ]

    @property
    def _left_is_ps(self) -> bool:
        return self.cfg.primary_shell == "powershell"

    def _left_prompt_segs(self) -> list[Segment]:
        return self._ps_prompt_segs() if self._left_is_ps else self._bash_prompt_segs()

    def _right_prompt_segs(self) -> list[Segment]:
        return self._bash_prompt_segs() if self._left_is_ps else self._ps_prompt_segs()

    @property
    def _left_title(self) -> str:
        return self.cfg.ps_title if self._left_is_ps else self.cfg.bash_title

    @property
    def _right_title(self) -> str:
        return self.cfg.bash_title if self._left_is_ps else self.cfg.ps_title

    @property
    def _left_text_color(self) -> tuple[int, int, int]:
        return TEXT_PS if self._left_is_ps else TEXT_BASH

    @property
    def _right_text_color(self) -> tuple[int, int, int]:
        return TEXT_BASH if self._left_is_ps else TEXT_PS

    def _draw_segments(
        self,
        draw: ImageDraw.ImageDraw,
        x: int,
        y: int,
        segs: list[Segment],
        char_budget: int,
    ) -> int:
        remaining = char_budget
        cur_x = x
        for seg in segs:
            if remaining <= 0:
                break
            chunk = seg.text[:remaining]
            draw.text((cur_x, y), chunk, font=self.font, fill=seg.color)
            cur_x += int(draw.textlength(chunk, font=self.font))
            remaining -= len(chunk)
        return cur_x

    def _render_frame(
        self,
        visible_left: list,
        visible_right: list,
        typing_left: tuple | None,
        typing_right: tuple | None,
        show_cursor: bool,
    ) -> Image.Image:
        im = Image.new("RGB", (self.W, self.H), BG)
        draw = ImageDraw.Draw(im)

        # Top title strip
        tw = draw.textlength(self.cfg.title, font=load_font(18))
        draw.text(
            ((self.W - tw) / 2, 18),
            self.cfg.title,
            font=load_font(18),
            fill=(205, 213, 224),
        )

        self._draw_window(im, self.LEFT_X, is_ps=self._left_is_ps, title=self._left_title, is_right=False)
        self._draw_window(im, self.RIGHT_X, is_ps=not self._left_is_ps, title=self._right_title, is_right=True)

        body_top = self.WIN_Y + self.layout.title_h + self.layout.body_pad_y

        for origin_x, visible, typing, cursor_color in (
            (
                self.LEFT_X + self.layout.body_pad_x,
                visible_left,
                typing_left,
                self._left_text_color,
            ),
            (
                self.RIGHT_X + self.layout.body_pad_x,
                visible_right,
                typing_right,
                self._right_text_color,
            ),
        ):
            for segs, yi in visible:
                y = body_top + yi * self.layout.line_h
                self._draw_segments(
                    draw, origin_x, y, segs, sum(len(s.text) for s in segs)
                )
            if typing is not None:
                prompt_segs, cmd_segs, chars_typed, yi = typing
                y = body_top + yi * self.layout.line_h
                cur_x = self._draw_segments(
                    draw,
                    origin_x,
                    y,
                    prompt_segs,
                    sum(len(s.text) for s in prompt_segs),
                )
                cur_x = self._draw_segments(draw, cur_x, y, cmd_segs, chars_typed)
                if show_cursor:
                    draw.rectangle(
                        [
                            cur_x + 1,
                            y + 4,
                            cur_x + 1 + self.layout.cursor_w,
                            y + 4 + self.layout.cursor_h,
                        ],
                        fill=cursor_color,
                    )

        # Step label column (right-aligned strip between the two windows would
        # be messy; instead we tuck labels to the right edge of each window.)
        for i, ex in enumerate(self.cfg.exchanges):
            if not ex.step_label:
                continue
            yi = self._y_index_of_exchange(i)
            y = body_top + yi * self.layout.line_h
            label = ex.step_label
            lw = draw.textlength(label, font=self.small)
            # Place within left window right edge
            draw.text(
                (
                    self.LEFT_X + self.WIN_W - 16 - lw,
                    y + 2,
                ),
                label,
                font=self.small,
                fill=STEP_LABEL,
            )
            draw.text(
                (
                    self.RIGHT_X + self.WIN_W - 16 - lw,
                    y + 2,
                ),
                label,
                font=self.small,
                fill=STEP_LABEL,
            )

        # Bottom caption strip
        cap_y = self.H - self.layout.caption_h
        draw.rectangle(
            [self.LEFT_X, cap_y, self.W - self.LEFT_X, self.H - 6],
            fill=(20, 25, 35),
        )
        cw = draw.textlength(self.cfg.caption, font=self.small)
        draw.text(
            ((self.W - cw) / 2, cap_y + (self.layout.caption_h - 26) // 2),
            self.cfg.caption,
            font=self.small,
            fill=CAPTION,
        )
        return im

    def _y_index_of_exchange(self, idx: int) -> int:
        y = 0
        for i, ex in enumerate(self.cfg.exchanges):
            if i == idx:
                return y
            y += 1 + max(len(ex.left.out), len(ex.right.out))
        return y

    # ---- Build frames ----

    def build_frames(
        self, typing_step: int = 1, frame_ms: int = 55
    ) -> tuple[list[Image.Image], list[int]]:
        frames: list[Image.Image] = []
        durations: list[int] = []
        visible_left: list = []
        visible_right: list = []
        yi = 0

        left_prompt = self._left_prompt_segs()
        right_prompt = self._right_prompt_segs()

        # Opening hold
        frames.append(self._render_frame(visible_left, visible_right, None, None, True))
        durations.append(700)

        for ex in self.cfg.exchanges:
            lc = ex.left.cmd_chars()
            rc = ex.right.cmd_chars()
            maxc = max(lc, rc)

            step = max(1, typing_step)
            # Always include i=0 and i=maxc; stride through the rest.
            indices = list(range(0, maxc + 1, step))
            if indices[-1] != maxc:
                indices.append(maxc)
            for i in indices:
                li = min(i, lc)
                ri = min(i, rc)
                frames.append(
                    self._render_frame(
                        visible_left,
                        visible_right,
                        (left_prompt, ex.left.cmd, li, yi),
                        (right_prompt, ex.right.cmd, ri, yi),
                        show_cursor=(i == maxc),
                    )
                )
                durations.append(frame_ms * step)

            # Hold with both fully typed
            frames.append(
                self._render_frame(
                    visible_left,
                    visible_right,
                    (left_prompt, ex.left.cmd, lc, yi),
                    (right_prompt, ex.right.cmd, rc, yi),
                    show_cursor=True,
                )
            )
            durations.append(260)

            # Commit command lines
            visible_left.append((left_prompt + ex.left.cmd, yi))
            visible_right.append((right_prompt + ex.right.cmd, yi))
            yi += 1

            # Reveal outputs synchronously
            max_out = max(len(ex.left.out), len(ex.right.out))
            for k in range(max_out):
                if k < len(ex.left.out):
                    visible_left.append(([ex.left.out[k]], yi))
                if k < len(ex.right.out):
                    visible_right.append(([ex.right.out[k]], yi))
                yi += 1
                frames.append(
                    self._render_frame(
                        visible_left, visible_right, None, None, False
                    )
                )
                durations.append(300)

            # Breath
            frames.append(
                self._render_frame(visible_left, visible_right, None, None, False)
            )
            durations.append(180)

        # Final hold - show trailing prompt with cursor
        frames.append(
            self._render_frame(
                visible_left,
                visible_right,
                (left_prompt, [], 0, yi),
                (right_prompt, [], 0, yi),
                True,
            )
        )
        durations.append(1100)
        return frames, durations

    def write_gif(
        self,
        out_path: Path,
        *,
        typing_step: int = 1,
        frame_ms: int = 55,
        colors: int = 64,
    ) -> None:
        frames, durations = self.build_frames(
            typing_step=typing_step, frame_ms=frame_ms
        )
        # Build the palette from a frame that actually contains every colour
        # the animation will use (the final hold has every command, every
        # output colour, and the error-row red). Sampling from frames[0]
        # picked up only the empty-window chrome and mapped later red/green
        # segments to the nearest boring palette entry, which made the GIF
        # read as washed-out.
        palette_source = frames[-1]
        palette_frame = palette_source.convert(
            "P", palette=Image.Palette.ADAPTIVE, colors=colors
        )
        pframes = [
            f.quantize(colors=colors, palette=palette_frame, dither=Image.Dither.NONE)
            for f in frames
        ]
        # disposal=1 ("leave frame as-is") is the correct mode for a
        # typewriter animation where each frame is already a full composite
        # of the scene at that moment. disposal=2 ("restore to background")
        # combined with optimize=True made viewers clear previously typed
        # commands to the background colour between frames, which is what
        # produced the "empty windows with step labels" rendering.
        pframes[0].save(
            out_path,
            save_all=True,
            append_images=pframes[1:],
            duration=durations,
            loop=0,
            disposal=1,
            optimize=True,
        )

    def write_png_final(self, out_path: Path) -> None:
        """Render a static PNG from the final visible state (no cursor)."""
        visible_left: list = []
        visible_right: list = []
        yi = 0
        left_prompt = self._left_prompt_segs()
        right_prompt = self._right_prompt_segs()
        for ex in self.cfg.exchanges:
            visible_left.append((left_prompt + ex.left.cmd, yi))
            visible_right.append((right_prompt + ex.right.cmd, yi))
            yi += 1
            max_out = max(len(ex.left.out), len(ex.right.out))
            for k in range(max_out):
                if k < len(ex.left.out):
                    visible_left.append(([ex.left.out[k]], yi))
                if k < len(ex.right.out):
                    visible_right.append(([ex.right.out[k]], yi))
                yi += 1
        frame = self._render_frame(
            visible_left,
            visible_right,
            (left_prompt, [], 0, yi),
            (right_prompt, [], 0, yi),
            show_cursor=True,
        )
        frame.save(out_path, "PNG")

    # ---- SVG rendering (hand-built from the same config) ----

    def write_svg(self, out_path: Path) -> None:
        """Write an SVG that matches the static PNG layout precisely."""
        parts: list[str] = []
        W, H = self.W, self.H
        parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}" '
            f'font-family="\'SF Mono\',\'Fira Code\',\'Consolas\',monospace">'
        )
        parts.append(
            '<defs>'
            '<linearGradient id="bashbg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{hex_of(BASH_WIN)}"/>'
            f'<stop offset="1" stop-color="{hex_of(BASH_WIN_DK)}"/>'
            '</linearGradient>'
            '<linearGradient id="psbg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{hex_of(PS_WIN)}"/>'
            f'<stop offset="1" stop-color="{hex_of(PS_WIN_DK)}"/>'
            '</linearGradient>'
            '</defs>'
        )
        parts.append(f'<rect width="{W}" height="{H}" fill="{hex_of(BG)}"/>')

        # Top title strip
        parts.append(
            f'<text x="{W // 2}" y="32" text-anchor="middle" '
            f'fill="#cdd5e0" font-size="18" font-weight="600">'
            f'{xml_escape(self.cfg.title)}</text>'
        )

        # Windows
        bash_tuple = (
            False,
            self.cfg.bash_title,
            "bashbg",
            hex_of(BASH_TITLE),
            hex_of(BASH_BORDER),
            hex_of(BASH_TITLE_FG),
            hex_of(BASH_NOTE),
        )
        ps_tuple = (
            True,
            self.cfg.ps_title,
            "psbg",
            hex_of(PS_TITLE),
            hex_of(PS_BORDER),
            hex_of(PS_TITLE_FG),
            hex_of(PS_NOTE),
        )
        left_style = ps_tuple if self._left_is_ps else bash_tuple
        right_style = bash_tuple if self._left_is_ps else ps_tuple
        for x, style, is_right in (
            (self.LEFT_X, left_style, False),
            (self.RIGHT_X, right_style, True),
        ):
            is_ps, title, bg_id, title_fill, border, title_fg, note_fill = style
            w = self.WIN_W
            y = self.WIN_Y
            h = self.WIN_H
            parts.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" ry="12" '
                f'fill="url(#{bg_id})" stroke="{border}" stroke-width="1.5"/>'
            )
            parts.append(
                f'<rect x="{x}" y="{y}" width="{w}" height="{self.layout.title_h}" '
                f'rx="12" ry="12" fill="{title_fill}"/>'
            )
            parts.append(
                f'<rect x="{x}" y="{y + self.layout.title_h - 10}" '
                f'width="{w}" height="10" fill="{title_fill}"/>'
            )
            for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
                cx = x + 22 + i * 20
                cy = y + 20
                parts.append(
                    f'<circle cx="{cx}" cy="{cy}" r="7" fill="{c}"/>'
                )
            parts.append(
                f'<text x="{x + w // 2}" y="{y + 26}" text-anchor="middle" '
                f'fill="{title_fg}" font-size="{self.layout.title_size}">'
                f'{xml_escape(title)}</text>'
            )
            # Note strip
            note_top = y + h - self.layout.note_h
            parts.append(
                f'<rect x="{x + 1}" y="{note_top}" width="{w - 2}" '
                f'height="{self.layout.note_h - 1}" fill="{note_fill}"/>'
            )
            note_text = (
                self.cfg.note.right_text if is_right else self.cfg.note.left_text
            )
            # Simple wrap identical to the Pillow one; compute offsets by measuring
            # character widths (approximate with 8px for the small font).
            parts.extend(
                self._svg_wrapped_note(
                    x + 16,
                    note_top + 20,
                    note_text,
                    title_fg,
                    w - 32,
                )
            )

        # Body text
        body_top = self.WIN_Y + self.layout.title_h + self.layout.body_pad_y

        # Compute final state
        visible_left: list = []
        visible_right: list = []
        yi = 0
        left_prompt = self._left_prompt_segs()
        right_prompt = self._right_prompt_segs()
        for ex in self.cfg.exchanges:
            visible_left.append(("cmd", left_prompt + ex.left.cmd, yi))
            visible_right.append(("cmd", right_prompt + ex.right.cmd, yi))
            yi += 1
            max_out = max(len(ex.left.out), len(ex.right.out))
            for k in range(max_out):
                if k < len(ex.left.out):
                    visible_left.append(("out", [ex.left.out[k]], yi))
                if k < len(ex.right.out):
                    visible_right.append(("out", [ex.right.out[k]], yi))
                yi += 1

        parts.append(f'<g font-size="{self.layout.font_size}" xml:space="preserve">')
        for origin_x, visible, prompt_segs, cursor_color in (
            (
                self.LEFT_X + self.layout.body_pad_x,
                visible_left,
                left_prompt,
                hex_of(self._left_text_color),
            ),
            (
                self.RIGHT_X + self.layout.body_pad_x,
                visible_right,
                right_prompt,
                hex_of(self._right_text_color),
            ),
        ):
            for kind, segs, row_yi in visible:
                y = body_top + row_yi * self.layout.line_h + 18
                parts.extend(self._svg_line(origin_x, y, segs))
            # Trailing prompt + blinking cursor
            y = body_top + yi * self.layout.line_h + 18
            cur_x_parts, cur_x_end = self._svg_prompt_with_cursor(
                origin_x, y, prompt_segs, cursor_color
            )
            parts.extend(cur_x_parts)
        parts.append('</g>')

        # Step labels at right edge of each window
        parts.append(
            f'<g font-size="{self.layout.small_size}" fill="{hex_of(STEP_LABEL)}">'
        )
        for i, ex in enumerate(self.cfg.exchanges):
            if not ex.step_label:
                continue
            row_yi = self._y_index_of_exchange(i)
            y = body_top + row_yi * self.layout.line_h + 18
            # approximate label width for right-align
            lw = len(ex.step_label) * 7
            parts.append(
                f'<text x="{self.LEFT_X + self.WIN_W - 16}" y="{y}" '
                f'text-anchor="end">{xml_escape(ex.step_label)}</text>'
            )
            parts.append(
                f'<text x="{self.RIGHT_X + self.WIN_W - 16}" y="{y}" '
                f'text-anchor="end">{xml_escape(ex.step_label)}</text>'
            )
        parts.append('</g>')

        # Bottom caption strip
        cap_y = self.H - self.layout.caption_h
        parts.append(
            f'<rect x="{self.LEFT_X}" y="{cap_y}" '
            f'width="{self.W - self.LEFT_X * 2}" height="{self.layout.caption_h - 6}" '
            f'fill="#141923"/>'
        )
        parts.append(
            f'<text x="{self.W // 2}" y="{cap_y + 24}" text-anchor="middle" '
            f'fill="{hex_of(CAPTION)}" font-size="{self.layout.small_size + 1}">'
            f'{xml_escape(self.cfg.caption)}</text>'
        )

        parts.append('</svg>')
        out_path.write_text("\n".join(parts), encoding="utf-8")

    def _svg_line(
        self,
        x: int,
        y: int,
        segs: list[Segment],
    ) -> list[str]:
        out: list[str] = []
        cur_x = x
        # Use a fixed approximate char width for monospace at 16px (~9.6 px/char)
        char_w = 9.6
        for seg in segs:
            out.append(
                f'<text x="{cur_x}" y="{y}" fill="{hex_of(seg.color)}">'
                f'{xml_escape(seg.text)}</text>'
            )
            cur_x += int(round(char_w * len(seg.text)))
        return out

    def _svg_prompt_with_cursor(
        self,
        x: int,
        y: int,
        prompt_segs: list[Segment],
        cursor_color: str,
    ) -> tuple[list[str], int]:
        out: list[str] = []
        cur_x = x
        char_w = 9.6
        for seg in prompt_segs:
            out.append(
                f'<text x="{cur_x}" y="{y}" fill="{hex_of(seg.color)}">'
                f'{xml_escape(seg.text)}</text>'
            )
            cur_x += int(round(char_w * len(seg.text)))
        out.append(
            f'<rect x="{cur_x + 1}" y="{y - 15}" width="11" height="20" '
            f'fill="{cursor_color}">'
            f'<animate attributeName="opacity" values="1;0;1" dur="1s" '
            f'repeatCount="indefinite"/></rect>'
        )
        return out, cur_x

    def _svg_wrapped_note(
        self,
        x: int,
        y: int,
        text: str,
        color: str,
        max_w: int,
    ) -> list[str]:
        # use approximate width at 13px
        char_w = 7.0
        max_chars = max(10, int(max_w / char_w))
        words = text.split()
        lines: list[str] = []
        line = ""
        for w in words:
            trial = (line + " " + w).strip()
            if len(trial) <= max_chars:
                line = trial
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        out: list[str] = []
        for i, ln in enumerate(lines):
            out.append(
                f'<text x="{x}" y="{y + i * 18}" fill="{color}" '
                f'font-size="{self.layout.small_size}">{xml_escape(ln)}</text>'
            )
        return out


# ---------- helpers to render all three artifacts ----------


def build_all(
    cfg: LessonConfig,
    asset_dir: Path,
    *,
    file_stem: str,
    typing_step: int = 1,
    frame_ms: int = 55,
    colors: int = 64,
) -> dict[str, Path]:
    asset_dir.mkdir(parents=True, exist_ok=True)
    renderer = SideBySideRenderer(cfg)
    gif_path = asset_dir / f"{file_stem}.gif"
    png_path = asset_dir / f"{file_stem}.png"
    svg_path = asset_dir / f"{file_stem}.svg"
    renderer.write_gif(
        gif_path, typing_step=typing_step, frame_ms=frame_ms, colors=colors
    )
    renderer.write_png_final(png_path)
    renderer.write_svg(svg_path)
    return {"gif": gif_path, "png": png_path, "svg": svg_path}
