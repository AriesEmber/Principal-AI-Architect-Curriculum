# RETIRED — L-006 terminal assets v1 (Bash-only)

**Status: RETIRED on 2026-04-19. Replaced by side-by-side Bash | PowerShell terminal assets at the canonical path.**

**Why this version was retired.** The `cd` lesson's article body paired Bash and PowerShell examples (`cd Documents`, `cd ..`, `cd ~`) but the v1 GIF/PNG/SVG only showed the Bash side. The side-by-side standard from L-003 v2 now applies to every shell-command lesson in the curriculum; a Bash-only animation is out of compliance.

**What changed in v2.**
1. Two columns: the same five `cd` exchanges in Bash (left) and PowerShell (right). Prompt-path tracking updates in lockstep across both columns as the reader walks into `Documents`, back up with `..`, and home with `~`.
2. Canvas trimmed to content.
3. Bottom notes now explain the Bash vs PowerShell binding: `cd` is a builtin in Bash that uses `$OLDPWD` and `cd -`; in PowerShell it aliases `Set-Location` and the `Push-Location` / `Pop-Location` pair gives a directory stack.

**What is preserved here.** v1 GIF, PNG, and SVG as they shipped to `main`.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-006-move-around-with-cd-and-relative-paths.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-006-move-around-with-cd-and-relative-paths.md)
