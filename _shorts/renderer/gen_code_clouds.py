"""One-off: pre-generate a large, seamless "code clouds" tile used as the
animated background. Writes _shorts/assets/backgrounds/code_clouds.png
(2160x2160 RGBA).

The tile is a loose collage of faint code snippets in multiple colors,
heavily blurred so individual characters are unreadable — what remains is
the shape and color of code-like text-mass. Per-frame rendering pans this
tile + applies a slow hue rotation, which is cheap.
"""
from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import config as C


TILE_SIZE = 2160

SNIPPETS = [
    "$ ls -la",
    "cd ~/projects",
    "echo \"hello world\"",
    "mkdir -p src/app",
    "git status",
    "git commit -m \"init\"",
    "python main.py",
    "def hello(name):",
    "    return f\"hi {name}\"",
    "import os",
    "import sys",
    "for x in range(10):",
    "    print(x)",
    "if __name__ == \"__main__\":",
    "curl https://api.example.com",
    "docker run -it ubuntu",
    "kubectl get pods",
    "npm install",
    "export PATH=$PATH:/usr/local",
    "sudo apt install jq",
    "cat /etc/hostname",
    "pwd",
    "whoami",
    "ps aux | grep python",
    "tail -f app.log",
    "chmod +x script.sh",
    "vim ~/.bashrc",
    "source venv/bin/activate",
    "pip install requests",
    "ssh user@server",
    "scp file.txt remote:",
    "async def fetch(url):",
    "    async with session.get(url):",
    "return response.json()",
    "try:",
    "except Exception as e:",
    "print(f\"err: {e}\")",
    "class Pipeline:",
    "    def run(self):",
    "# TODO: refactor",
    "git push origin main",
    "brew install ffmpeg",
    "wget https://...",
    "export DEBUG=1",
    "tar -xzf archive.tgz",
    "find . -name '*.py'",
    "grep -r 'TODO' .",
    "ls /usr/local/bin",
    "man bash",
    "htop",
]

# Accent palette for the snippets — muted so they don't dominate.
COLORS = [
    (92, 168, 232),   # cyan
    (120, 200, 176),  # mint
    (232, 180, 92),   # amber
    (208, 140, 220),  # orchid
    (236, 120, 136),  # coral
    (160, 176, 208),  # cool grey-blue
    (168, 204, 140),  # sage
]


def generate():
    rng = random.Random(0xC0DE)
    tile = Image.new("RGBA", (TILE_SIZE, TILE_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)

    # Use two font sizes for variety — small and medium.
    try:
        font_s = ImageFont.truetype(C.FONT_MONO, 30)
        font_m = ImageFont.truetype(C.FONT_MONO, 46)
        font_l = ImageFont.truetype(C.FONT_MONO, 70)
    except OSError:
        font_s = ImageFont.load_default()
        font_m = font_s
        font_l = font_s

    # Scatter ~500 snippets randomly across the tile.
    for _ in range(600):
        text = rng.choice(SNIPPETS)
        font = rng.choice([font_s, font_s, font_m, font_m, font_l])
        color = rng.choice(COLORS)
        alpha = rng.randint(80, 190)
        x = rng.randint(-120, TILE_SIZE - 60)
        y = rng.randint(-40, TILE_SIZE - 30)
        d.text((x, y), text, fill=(*color, alpha), font=font)

    # Heavy blur — we want shapes, not legibility.
    tile = tile.filter(ImageFilter.GaussianBlur(radius=7))
    # Tone down overall alpha so the clouds are faint even at 100% tile opacity.
    alpha = tile.split()[3].point(lambda v: int(v * 0.55))
    tile.putalpha(alpha)

    out_dir = C.SHORTS_DIR / "assets" / "backgrounds"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "code_clouds.png"
    tile.save(path, optimize=True)
    print(f"wrote {path} ({tile.size})")
    return path


if __name__ == "__main__":
    generate()
