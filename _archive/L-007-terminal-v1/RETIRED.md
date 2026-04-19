# RETIRED — L-007 terminal assets v1 (Bash-only)

**Status: RETIRED on 2026-04-19. Replaced by side-by-side Bash | PowerShell terminal assets at the canonical path.**

**Why this version was retired.** The week-one capstone chains `pwd`, `mkdir`, `ls`, `cd`, `touch` / `New-Item`, and `rm -r` / `Remove-Item -Recurse`. v1 of the GIF showed only the Bash chain, so the Windows half of the readership watched a Bash session while the article asked them to run PowerShell equivalents. After the L-003 v2 standard, this mismatch is now a failed quality gate (Gate 12: side-by-side, no whitespace).

**What changed in v2.**
1. Nine exchanges rendered in two columns so the learner can watch the tree being made and torn down in both shells at once. `touch` and `rm -r` (Bash) pair with `New-Item` and `Remove-Item -Recurse` (PowerShell).
2. Canvas trimmed to content; the capstone's taller stack of exchanges is handled by the shared renderer's automatic height computation.
3. GIF stays under the 2 MB cap (typing step raised to 3 frames per character, palette reduced to 20 colours) while the PNG keeps full fidelity for the static read.

**What is preserved here.** v1 GIF, PNG, and SVG as they shipped to `main`.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-007-make-and-remove-directories-capstone.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-007-make-and-remove-directories-capstone.md)
