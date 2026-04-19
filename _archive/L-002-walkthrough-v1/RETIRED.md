# RETIRED — L-002 walkthrough v1 (single-prompt anatomy SVG)

**Status: RETIRED on 2026-04-19. Replaced by a side-by-side Bash | PowerShell prompt walkthrough at the canonical path.**

**Why this version was retired.** v1 showed one generic shell prompt (`learner@laptop:~/projects$`) with four callouts. It never rendered the PowerShell form, so a Windows reader had to mentally translate between what the walkthrough showed and the `PS C:\Users\learner>` prompt on their screen. After L-003 v2 standardised every shell-touching asset on two-column Bash + PowerShell, the same rule applies here: show both prompts in one frame, annotate each, and let the reader read across.

**What changed in v2.**
1. Two columns: Bash prompt (four callouts: username, machine, directory, prompt character) on the left, PowerShell prompt (three callouts: shell indicator, directory, prompt character) on the right.
2. Canvas sized to content - no trailing whitespace below the callout boxes or between the callouts and the caption strip.
3. A companion `L-002-walkthrough.png` ships alongside the GIF for a no-animation static read.
4. Produced by `_state/scratch/L-002-v2/build.py` on top of the shared renderer tokens.

**What is preserved here.** The v1 GIF and SVG as they shipped to `main`, extracted from the pre-update `HEAD` commit. Nothing in this folder is referenced from any live article.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-002-read-a-prompt-like-a-sign.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-002-read-a-prompt-like-a-sign.md)
