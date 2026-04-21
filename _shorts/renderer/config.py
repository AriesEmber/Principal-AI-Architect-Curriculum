"""Shared constants for the shorts renderer.

All coordinates are in pixels on a 1080x1920 canvas. The "world" (scrolling
timeline) uses the same pixel units; camera_x(t) = t * PIXELS_PER_SECOND.
"""
from pathlib import Path

CANVAS_W = 1080
CANVAS_H = 1920
FPS = 30

HEADER_Y = (0, 200)
USER_Y = (200, 480)
TIMELINE_Y = (600, 1480)
CAPTION_Y = (1500, 1820)
FOOTER_Y = (1820, 1920)

LANE_LABEL_X = (24, 280)
TIMELINE_VIEWPORT_X = (280, 1080)
ROBOT_SCREEN_X = 540

PIXELS_PER_SECOND = 220

# Locked palette: Industrial Workshop (from Crate-Bot mascot pick).
# Saturated terracotta does the heavy lifting; amber is the sparing accent;
# slate carries the UI chrome so the mascot stays the loudest thing on screen.
COLOR_BG = (14, 19, 28)                  # very dark slate, cooler than outline
COLOR_LANE_LINE = (62, 76, 94)           # #3E4C5E slate
COLOR_LANE_LABEL_BG = (46, 58, 74)       # slate, one notch darker than lanes
COLOR_LANE_LABEL_TEXT = (242, 230, 209)  # warm cream
COLOR_ACCENT = (244, 211, 94)            # #F4D35E safety amber
COLOR_PRIMARY = (210, 105, 59)           # #D2693B terracotta
COLOR_OUTLINE = (31, 36, 48)             # #1F2430
COLOR_TEXT = (242, 230, 209)             # warm cream
COLOR_TEXT_DIM = (170, 160, 145)
COLOR_ARROW = (210, 105, 59)             # same as primary (returns)
COLOR_SHADOW = (138, 79, 46)             # #8A4F2E burnt sienna
COLOR_USER_SKIN = (236, 198, 164)        # slightly warmer skin tone
COLOR_USER_SHIRT = (82, 108, 156)        # cool blue — complementary to terracotta

FONT_CAPTION = r"C:\Windows\Fonts\segoeui.ttf"
FONT_CAPTION_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_LABEL = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_ITALIC = r"C:\Windows\Fonts\segoeuii.ttf"

REPO_ROOT = Path(__file__).resolve().parents[2]
SHORTS_DIR = REPO_ROOT / "_shorts"
CHARACTER_DIR = SHORTS_DIR / "character"
TEMPLATES_DIR = SHORTS_DIR / "templates"
AUDIO_DIR = SHORTS_DIR / "audio"
OUTPUT_DIR = REPO_ROOT / "_deliverables" / "shorts"
WORK_DIR = SHORTS_DIR / "_work"
