# RETIRED — L-001 walkthrough v1 (scene-rotating cross-platform SVG)

**Status: RETIRED on 2026-04-19. Replaced by a side-by-side Bash | PowerShell walkthrough at the canonical path.**

**Why this version was retired.** v1 was a single-column 16-second SMIL animation that cycled through four scenes (macOS Spotlight, Windows 11 Start, GNOME Activities, and the resulting terminal window) with a progress bar along the top. After L-003 shipped in its two-column Bash + PowerShell form, Elvis standardised every lesson GIF on that pattern: two shell worlds on screen at the same time, no trailing whitespace, and a static PNG that matches the final frame. The old scene-rotating format cannot meet that bar without a full reauthor.

**What changed in v2.**
1. Single canvas split into a left column (macOS / Linux, Bash) and a right column (Windows 11, PowerShell).
2. Canvas sized to content so there is no empty strip at the bottom of the image.
3. A companion `L-001-walkthrough.png` is now shipped alongside the GIF so readers who skip the animation still see the final shell-ready state.
4. The new asset stack is produced by `_state/scratch/L-001-v2/build.py`, which calls into the shared renderer in `_state/scratch/common/side_by_side.py`.

**What is preserved here.** The exact v1 GIF and SVG as they shipped to `main`, extracted from the pre-update `HEAD` commit. Nothing in this folder is referenced from any live article.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-001-open-the-terminal-with-a-keyboard-shortcut.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-001-open-the-terminal-with-a-keyboard-shortcut.md)
