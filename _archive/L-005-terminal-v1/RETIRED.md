# RETIRED — L-005 terminal assets v1 (Bash-only)

**Status: RETIRED on 2026-04-19. Replaced by side-by-side Bash | PowerShell terminal assets at the canonical path.**

**Why this version was retired.** The `ls` lesson's article body noted that in PowerShell `ls` is an alias for `Get-ChildItem`, and that its flags differ (`-Force` instead of `-la`), but the v1 assets showed only the Bash form. Windows readers had to read the article plus a single-column animation that didn't reflect what they would see on their own machine. The new two-column standard makes the mapping visible in the image itself.

**What changed in v2.**
1. Two columns: Bash `ls`, `ls -la`, `ls /etc`, `type ls` on the left; PowerShell `ls`, `ls -Force`, `ls C:\Windows`, `Get-Command ls` on the right.
2. Canvas height trimmed to the content; no trailing whitespace below the notes strip.
3. Alias-binding step (`type ls` vs `Get-Command ls`) is now visible in the animation rather than buried in prose.

**What is preserved here.** v1 GIF, PNG, and SVG as they shipped to `main`.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-005-list-the-contents-of-a-directory-with-ls.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-005-list-the-contents-of-a-directory-with-ls.md)
