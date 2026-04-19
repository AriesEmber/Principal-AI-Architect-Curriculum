# RETIRED — L-004 terminal assets v1 (Bash-only)

**Status: RETIRED on 2026-04-19. Replaced by side-by-side Bash | PowerShell terminal assets at the canonical path.**

**Why this version was retired.** v1 of the `pwd` lesson shipped with a single-column Bash GIF and PNG. The article body already called out that `pwd` is a builtin in Bash and an alias for `Get-Location` in PowerShell, so readers on Windows had to hold the PowerShell form in their head while looking at a Bash-only animation. L-003 v2 established the two-column Bash + PowerShell standard; this version violated it.

**What changed in v2.**
1. Two terminal windows on one canvas - Bash on the left, PowerShell on the right - with four matched exchanges: plain `pwd`, the logical / physical variants, a builtin check (`type pwd` vs `Get-Command pwd`), and a fresh-window re-run.
2. Canvas sized to the content; no trailing whitespace in the still image.
3. The shared renderer (`_state/scratch/common/side_by_side.py`) produces the GIF, PNG, and SVG from one configuration so they cannot drift.

**What is preserved here.** The single-column v1 GIF, PNG, and SVG as they shipped to `main`, extracted from the pre-update `HEAD` commit.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-004-find-out-where-you-are-with-pwd.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-004-find-out-where-you-are-with-pwd.md)
