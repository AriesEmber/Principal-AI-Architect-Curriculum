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

# Default palette (Palette B "Warm Chrome" - placeholder until mascot locked)
COLOR_BG = (18, 24, 36)
COLOR_LANE_LINE = (58, 70, 88)
COLOR_LANE_LABEL_BG = (44, 62, 77)
COLOR_LANE_LABEL_TEXT = (240, 228, 211)
COLOR_ACCENT = (133, 220, 176)
COLOR_PRIMARY = (232, 168, 124)
COLOR_OUTLINE = (26, 31, 43)
COLOR_TEXT = (240, 228, 211)
COLOR_TEXT_DIM = (170, 160, 145)
COLOR_ARROW = (232, 168, 124)
COLOR_SHADOW = (184, 116, 80)
COLOR_USER_SKIN = (240, 210, 170)
COLOR_USER_SHIRT = (100, 130, 180)

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
