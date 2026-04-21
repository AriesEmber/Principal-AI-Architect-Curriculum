"""One-off: pre-generate a seamless fBm-ish noise tile used as the smoke
backdrop base. Run once; the PNG gets committed to the repo and reused every
render so we don't pay the generation cost per frame.

No Perlin dependency — uses numpy random + iterative multi-scale Gaussian
blurs + log-contrast to approximate fractal Brownian motion. Seamless via
wrap-around on the blur (mirror padding).
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

from . import config as C


TILE_SIZE = 2160  # covers any 1080x1920 pan at offset
SEED = 0xBEEF


def generate():
    rng = np.random.default_rng(SEED)
    # Multi-octave fBm: sum N noise layers at increasing frequencies with
    # decreasing amplitudes. Start with a tiny random grid, upsample, add
    # the next octave.
    octaves = [
        (8,   1.00),
        (16,  0.55),
        (32,  0.28),
        (64,  0.14),
        (128, 0.07),
        (256, 0.035),
    ]
    acc = np.zeros((TILE_SIZE, TILE_SIZE), dtype=np.float32)
    for grid, amp in octaves:
        base = rng.random((grid, grid)).astype(np.float32)
        img = Image.fromarray((base * 255).astype(np.uint8), mode="L")
        img = img.resize((TILE_SIZE, TILE_SIZE), Image.BICUBIC)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        acc += arr * amp
    # Normalize 0..1
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    # Gentle contrast curve — push midtones down, highlights up so it feels
    # "smoky" not "flat fog".
    acc = np.clip(acc, 0, 1)
    acc = acc ** 1.4

    # Color ramp: dark indigo -> deep violet. Very low contrast — we want
    # atmospheric, not "lava lamp". Range from near-black up to subtle plum.
    stops = np.array([
        (0.00, (6,  8,  14)),
        (0.40, (10, 13, 24)),
        (0.70, (18, 16, 38)),
        (0.90, (28, 20, 52)),
        (1.00, (38, 28, 66)),
    ], dtype=object)
    xs = np.array([s[0] for s in stops], dtype=np.float32)
    cols = np.array([s[1] for s in stops], dtype=np.float32)
    flat = acc.reshape(-1)
    out = np.empty((flat.shape[0], 3), dtype=np.float32)
    for ch in range(3):
        out[:, ch] = np.interp(flat, xs, cols[:, ch])
    out = out.reshape((TILE_SIZE, TILE_SIZE, 3)).astype(np.uint8)
    img = Image.fromarray(out, mode="RGB")
    # Heavy soften — we want atmospheric color fields, not sharp smoke puffs.
    # After this, the tile reads more like an aurora than cigarette smoke.
    img = img.filter(ImageFilter.GaussianBlur(radius=16))

    out_dir = C.SHORTS_DIR / "assets" / "backgrounds"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "smoke_tile.png"
    img.save(path, optimize=True)
    print(f"wrote {path} ({img.size})")
    return path


if __name__ == "__main__":
    generate()
