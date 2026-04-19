# RETIRED — L-003 v1 (echo lesson, Bash-only assumption)

**Status: RETIRED on 2026-04-19. Replaced by L-003 v2 at the canonical path.**

**Why this version was retired.** The v1 lesson asserted that "every command below works identically on all three" shells (Bash on Linux, Zsh on macOS, PowerShell on Windows). That claim is wrong. The variable-expansion examples (`echo $USER`, `echo $HOME`, `echo $SHELL`) are Bash and Zsh only. PowerShell uses a different namespace (`$env:USERNAME`, `$env:USERPROFILE`, `$env:COMSPEC`), so a Windows reader following the lesson verbatim sees blank output and concludes they typed something wrong. A real reader hit this on day one of the curriculum and surfaced it.

**What changed in v2.**
1. Removed the false claim that every command works identically on all three shells.
2. Added a "Pick your shell" check at the top so the reader knows which column to follow before typing anything.
3. Every variable-expansion step now shows the Bash form and the PowerShell form side by side, with the same expected output.
4. The "What just happened" section explains the two namespace models (Bash auto-exposes shell variables; PowerShell scopes environment variables under `$env:`) so the reader leaves with a mental model, not a translation table.
5. The animated demo and the static panel were rebuilt as a two-column Bash | PowerShell view.
6. The skill itself was updated. A new "shell-assumption check" was added to the design phase and to the quality gates so any future shell-touching lesson must ship cross-shell or declare the platform restriction in its frontmatter. Same mistake cannot reach `main` again.

**What is preserved here.** Every file in this folder is the v1 snapshot exactly as it shipped to `main` on 2026-04-18 (commit `407973b`), so this archive is auditable. The image URLs in the two archived Markdown files have been rewritten to point to the snapshots in this folder, not the canonical asset paths, so the archived lesson stays internally consistent after the canonical assets are replaced by v2.

**Where to read the live lesson.** [`../../modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md`](../../modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md)
