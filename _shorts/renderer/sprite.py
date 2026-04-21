"""Tiny animated mascot sprite.

Design: a small puck/roomba-shaped bot seen from a slight 3/4 top-down angle
(like Final Fantasy Tactics). Native 32x32, rendered on-screen at ~128 px
(scale 4). Drawn procedurally so animation frames are source-of-truth code.

Animation library — any of these can be used per-beat:

  Idle family (robot is stationary or "waiting on a lane"):
    idle_bob_0, idle_bob_1            — gentle breathing up/down
    idle_look_L_0..2                  — peek left, pause, return
    idle_look_R_0..2                  — peek right, pause, return
    idle_hop_0..3                     — squash, stretch, airborne, land
    idle_spin_0..3                    — rotate facing 4 directions
    idle_tap_0..1                     — one wheel lifts & drops

  Motion family (robot is traveling / working):
    drive_0, drive_1                  — rolling, wheel phase shift
    self_dance_0..3                   — lean L, lean R, spin, hop
    swing_0..3                        — pendulum rotation on a line

Movement is also horizontal now — scene.py's path system moves the sprite
through x/y waypoints; these frames animate the character IN PLACE while
that happens.
"""
from PIL import Image, ImageDraw

SPRITE_SIZE = 32

# Palette — white/chrome puck with blue eye + amber accents. Kept separate from
# UI palette so the character reads clearly against any background.
P = {
    "chassis_hi":  (240, 246, 252),
    "chassis":     (200, 212, 228),
    "chassis_m":   (160, 174, 196),
    "chassis_d":   (96, 108, 132),
    "chassis_d2":  (52, 62, 84),
    "eye_glow":    (132, 208, 244),
    "eye":         (64, 158, 220),
    "eye_d":       (28, 90, 148),
    "pupil":       (16, 24, 40),
    "glint":       (255, 255, 255),
    "accent":      (244, 200, 72),
    "accent_hi":   (252, 232, 148),
    "wheel":       (40, 48, 68),
    "wheel_hi":    (140, 152, 174),
    "outline":     (14, 18, 28),
    "bg_shadow":   (0, 0, 0, 90),   # ground shadow beneath the puck
}


def _px(d: ImageDraw.ImageDraw, x: int, y: int, color, w: int = 1, h: int = 1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def _ground_shadow(d: ImageDraw.ImageDraw, cx: int, bottom_y: int, w: int = 20):
    """Elliptical shadow under the puck, on the "floor"."""
    h = max(3, w // 5)
    d.ellipse([cx - w // 2, bottom_y - h // 2, cx + w // 2, bottom_y + h // 2],
              fill=P["bg_shadow"])


def _puck_base(d: ImageDraw.ImageDraw, cx: int, cy: int, tilt_x: int = 0,
               squash: int = 0, wheel_phase: int = 0):
    """Draw the disc/roomba base in a 3/4 top-down view.
    cx, cy — center of the puck (roughly the dome base).
    tilt_x — horizontal pixel offset for "leaning" effect (self-dance frames).
    squash — vertical compression for hop frames (positive = squashed).
    wheel_phase — 0 or 1, swaps wheel tread pattern.
    """
    # Disc footprint — elliptical (top-down foreshortening)
    disc_w = 22
    disc_h = 8 - squash // 2
    disc_y = cy + 4
    # Rim outline
    _px(d, cx - disc_w // 2 + tilt_x, disc_y, P["outline"], disc_w, disc_h)
    # Disc top surface (lighter)
    _px(d, cx - disc_w // 2 + 1 + tilt_x, disc_y + 1, P["chassis"], disc_w - 2, disc_h - 2)
    _px(d, cx - disc_w // 2 + 1 + tilt_x, disc_y + 1, P["chassis_hi"], disc_w - 2, 1)
    # Disc ring (darker shadow below rim)
    _px(d, cx - disc_w // 2 + 1 + tilt_x, disc_y + disc_h - 2, P["chassis_m"], disc_w - 2, 1)

    # Side wheels peeking out (left + right)
    for side in (-1, 1):
        wx = cx + side * (disc_w // 2 - 1) + tilt_x
        wy = disc_y + 1
        _px(d, wx - 1, wy, P["outline"], 3, disc_h - 1)
        _px(d, wx, wy + 1, P["wheel"], 1, disc_h - 3)
        # Phase-shifted tread
        if wheel_phase == 0:
            _px(d, wx, wy + 1, P["wheel_hi"], 1, 1)
        else:
            _px(d, wx, wy + 3, P["wheel_hi"], 1, 1)


def _puck_dome(d: ImageDraw.ImageDraw, cx: int, cy: int, tilt_x: int = 0,
               eye_dir: int = 0, eye_blink: bool = False, squash: int = 0):
    """Draw the dome body + eye on top of the disc.
    eye_dir: -1 (left), 0 (center), 1 (right).
    eye_blink: draw closed eye line instead of circle.
    """
    # Dome silhouette
    dome_w = 16
    dome_h = 14 - squash
    dome_x0 = cx - dome_w // 2 + tilt_x
    dome_y0 = cy - dome_h // 2 - 3
    # Body outline
    d.ellipse([dome_x0, dome_y0, dome_x0 + dome_w - 1, dome_y0 + dome_h - 1],
              fill=P["outline"])
    # Body fill
    d.ellipse([dome_x0 + 1, dome_y0 + 1, dome_x0 + dome_w - 2, dome_y0 + dome_h - 2],
              fill=P["chassis"])
    # Top highlight (sphere-ish)
    d.ellipse([dome_x0 + 2, dome_y0 + 1, dome_x0 + dome_w - 4, dome_y0 + 4],
              fill=P["chassis_hi"])

    # Eye
    eye_cx = cx + tilt_x + eye_dir
    eye_cy = cy - 3 + squash // 2
    if eye_blink:
        _px(d, eye_cx - 3, eye_cy, P["outline"], 7, 1)
    else:
        # Soft glow behind eye
        d.ellipse([eye_cx - 4, eye_cy - 3, eye_cx + 3, eye_cy + 3],
                  fill=P["eye_glow"])
        # Iris
        d.ellipse([eye_cx - 3, eye_cy - 2, eye_cx + 2, eye_cy + 2], fill=P["eye"])
        # Deep center
        _px(d, eye_cx - 1 + eye_dir, eye_cy - 1, P["eye_d"], 2, 2)
        # Pupil
        _px(d, eye_cx + eye_dir, eye_cy, P["pupil"], 1, 1)
        # Glint
        _px(d, eye_cx - 2, eye_cy - 2, P["glint"], 1, 1)

    # Antenna on top
    antenna_x = cx + tilt_x
    _px(d, antenna_x, dome_y0 - 3, P["outline"], 1, 3)
    # Antenna bulb (amber)
    _px(d, antenna_x - 1, dome_y0 - 5, P["accent"], 3, 2)
    _px(d, antenna_x, dome_y0 - 5, P["accent_hi"], 1, 1)


def _render(frame_func) -> Image.Image:
    """Create a 32x32 RGBA canvas, draw via frame_func(d), return."""
    img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    frame_func(d)
    return img


# -------------------- Individual frames --------------------

_CX = SPRITE_SIZE // 2
_BASE_Y = SPRITE_SIZE // 2 + 2


def _frame_idle_bob(bob_offset: int):
    def fn(d):
        _ground_shadow(d, _CX, 29)
        _puck_base(d, _CX, _BASE_Y - bob_offset)
        _puck_dome(d, _CX, _BASE_Y - bob_offset)
    return fn


def _frame_look(eye_dir: int, tilt: int = 0):
    def fn(d):
        _ground_shadow(d, _CX, 29)
        _puck_base(d, _CX, _BASE_Y, tilt_x=tilt)
        _puck_dome(d, _CX, _BASE_Y, tilt_x=tilt, eye_dir=eye_dir)
    return fn


def _frame_hop(stage: int):
    """0=squash, 1=stretch, 2=airborne, 3=land."""
    if stage == 0:
        def fn(d):
            _ground_shadow(d, _CX, 29, w=22)
            _puck_base(d, _CX, _BASE_Y + 1, squash=2)
            _puck_dome(d, _CX, _BASE_Y, squash=2)
        return fn
    if stage == 1:
        def fn(d):
            _ground_shadow(d, _CX, 29, w=18)
            _puck_base(d, _CX, _BASE_Y - 2)
            _puck_dome(d, _CX, _BASE_Y - 3, squash=-1)
        return fn
    if stage == 2:
        def fn(d):
            _ground_shadow(d, _CX, 30, w=14)
            _puck_base(d, _CX, _BASE_Y - 5)
            _puck_dome(d, _CX, _BASE_Y - 6)
        return fn
    # land
    def fn(d):
        _ground_shadow(d, _CX, 29, w=20)
        _puck_base(d, _CX, _BASE_Y + 1, squash=1)
        _puck_dome(d, _CX, _BASE_Y + 1, squash=1)
    return fn


def _frame_drive(phase: int):
    """Rolling. The x-motion happens via scene.py waypoints; this just cycles
    the wheel tread so forward motion reads at the sprite level too."""
    def fn(d):
        _ground_shadow(d, _CX, 29)
        _puck_base(d, _CX, _BASE_Y, wheel_phase=phase)
        _puck_dome(d, _CX, _BASE_Y)
    return fn


def _frame_self_dance(stage: int):
    """Stages: lean L, center, lean R, center."""
    lean = [-3, 0, 3, 0][stage % 4]
    eye = [-1, 0, 1, 0][stage % 4]
    def fn(d):
        _ground_shadow(d, _CX, 29)
        _puck_base(d, _CX, _BASE_Y, tilt_x=lean)
        _puck_dome(d, _CX, _BASE_Y, tilt_x=lean, eye_dir=eye)
    return fn


def _frame_swing(stage: int):
    """Pendulum. Stage 0..3 maps to angles [-8, 0, +8, 0] applied as tilt."""
    tilt = [-4, 0, 4, 0][stage % 4]
    def fn(d):
        _ground_shadow(d, _CX, 30, w=14)
        _puck_base(d, _CX, _BASE_Y - 2, tilt_x=tilt)
        _puck_dome(d, _CX, _BASE_Y - 2, tilt_x=tilt)
        # Swing line attachment
        dx = tilt // 2
        d.line([_CX + dx, _BASE_Y - 12, _CX + dx, 0], fill=P["chassis_d"], width=1)
    return fn


# -------------------- Frame registry --------------------

FRAME_CACHE: dict[str, Image.Image] = {}


def get_frame(name: str) -> Image.Image:
    """Return the cached sprite image for a frame name."""
    if name in FRAME_CACHE:
        return FRAME_CACHE[name]
    img = _render(_FRAME_MAP[name])
    FRAME_CACHE[name] = img
    return img


_FRAME_MAP = {
    # Idle
    "idle_bob_0":  _frame_idle_bob(0),
    "idle_bob_1":  _frame_idle_bob(1),
    "idle_look_L_0": _frame_look(-1),
    "idle_look_L_1": _frame_look(-1, tilt=-1),
    "idle_look_L_2": _frame_look(0),
    "idle_look_R_0": _frame_look(1),
    "idle_look_R_1": _frame_look(1, tilt=1),
    "idle_look_R_2": _frame_look(0),
    "idle_hop_0":  _frame_hop(0),
    "idle_hop_1":  _frame_hop(1),
    "idle_hop_2":  _frame_hop(2),
    "idle_hop_3":  _frame_hop(3),
    # Motion
    "drive_0":     _frame_drive(0),
    "drive_1":     _frame_drive(1),
    # Self-dance
    "self_dance_0": _frame_self_dance(0),
    "self_dance_1": _frame_self_dance(1),
    "self_dance_2": _frame_self_dance(2),
    "self_dance_3": _frame_self_dance(3),
    # Swing
    "swing_0":     _frame_swing(0),
    "swing_1":     _frame_swing(1),
    "swing_2":     _frame_swing(2),
    "swing_3":     _frame_swing(3),
}


# Animation = ordered list of frame names with total cycle duration in seconds.
ANIMATIONS: dict[str, tuple[list[str], float]] = {
    "idle_bob":    (["idle_bob_0", "idle_bob_1"], 1.0),
    "idle_look_L": (["idle_look_L_0", "idle_look_L_1", "idle_look_L_2"], 1.4),
    "idle_look_R": (["idle_look_R_0", "idle_look_R_1", "idle_look_R_2"], 1.4),
    "idle_hop":    (["idle_hop_0", "idle_hop_1", "idle_hop_2", "idle_hop_3"], 0.9),
    "drive":       (["drive_0", "drive_1"], 0.25),
    "self_dance":  (["self_dance_0", "self_dance_1", "self_dance_2", "self_dance_3"], 1.2),
    "swing":       (["swing_0", "swing_1", "swing_2", "swing_3"], 1.0),
}

IDLE_POOL = ["idle_bob", "idle_look_L", "idle_look_R", "idle_hop"]
SELF_POOL = ["self_dance", "swing"]


def pick_idle(seed: int) -> str:
    """Deterministic idle pick based on `seed` (usually beat index)."""
    return IDLE_POOL[seed % len(IDLE_POOL)]


def pick_self(seed: int) -> str:
    return SELF_POOL[seed % len(SELF_POOL)]


def frame_at(anim: str, t: float) -> Image.Image:
    """Pick the current frame from animation `anim` at local time `t`
    (seconds since animation start). Loops."""
    frames, cycle = ANIMATIONS[anim]
    u = (t % cycle) / cycle
    idx = min(int(u * len(frames)), len(frames) - 1)
    return get_frame(frames[idx])


def upscale_pixel(img: Image.Image, factor: int) -> Image.Image:
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


# Backward-compat shims used elsewhere in the codebase.

def placeholder_robot(frame: str = "idle_bob_0") -> Image.Image:
    return get_frame(frame)


def placeholder_user(frame: str = "idle_0") -> Image.Image:
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    return img
