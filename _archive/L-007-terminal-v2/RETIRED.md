# L-007 terminal assets, v2 (retired 2026-04-19)

**Retired on:** 2026-04-19
**Superseded by:** `modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.*` (v3)
**Reason for retirement:** v2 put Bash on the left (primary) and PowerShell on the right (alternate). Elvis's learning environment is Windows 11 + PowerShell, and the v2 lesson body led with `touch hello.txt` (which does not exist in PowerShell) and glossed over the "cannot delete the directory you are currently in" rule. He hit both failures during hands-on practice.

**What changed in v3:**

1. `primary_shell="powershell"` — PowerShell is now the left column (primary), Bash is the right column (alternate). The renderer was extended with a `primary_shell` parameter in the same change; the default for all new lessons is `"powershell"`.
2. Two new exchanges (steps 7 and 8) teach the "cannot delete cwd" rule inside the visual itself: step 7 shows both shells erroring when you run `Remove-Item -Recurse practice-cli` / `rm -r practice-cli` from inside the directory, step 8 shows `cd ..` as the one-line fix, step 9 retries and succeeds.
3. The article body now leads with PowerShell code blocks. Bash is the alternate in each step, not the canonical.
4. Dedicated "Why step 7 errored" subsection explicitly calls out the rule with the exact error messages a Windows and a macOS/Linux learner each see.

The v2 files preserved here are the exact state on `main` immediately before the v3 draft branch opened:

- `L-007-terminal.svg` — v2 SVG (Bash-left)
- `L-007-terminal.gif` and `L-007-terminal.png` — NOT preserved (binary files, easy to regenerate from `build.py` against the v2-era renderer). The v2 `build.py` is preserved so a human can regenerate the v2 binaries if needed for audit.
- `L-007-manifest.json` — v2 manifest with the v2 asset checksums
- `L-007-transcript.md` — v2 screen-reader transcript
- `build.py` — v2 build config (Bash on left, 9 exchanges, no error step)

Do not re-reference the v2 files from any live lesson. They are kept here only so the v2 state is auditable.
