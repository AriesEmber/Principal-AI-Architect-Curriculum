# Pending Review

Items the `lesson-author` skill has flagged for human attention. Items are appended after each run; resolve and remove when handled.

## Format

Each entry follows this structure:

```
### [DATE] L-### — <gate or phase that flagged>

**Lesson:** <title>
**Flagged at:** <phase>
**Severity:** <halt | warning>
**Issue:** <concise description>
**Evidence:** <line numbers, file paths, specific strings>
**Suggested fix:** <if obvious>
**Status:** <open | resolved>
```

## Open items

### [2026-04-20] Housekeeping — published_index.md out of date

**Lesson:** L-010 (and now L-011)
**Flagged at:** research phase (selection sanity check for L-011)
**Severity:** warning
**Issue:** `_state/published_index.md` still lists L-009 as the most recent publication, but L-010 was merged into `main` as commit `ce07351` via PR #16 on 2026-04-20. The index append for L-010 did not run after that merge, which means Gate 8 cannot verify the L-010 prerequisite for L-011 against the index alone. The prerequisite is in fact satisfied: L-010 is present on `main` under `modules/M02-.../lessons/` and is referenced in the curriculum spine.
**Evidence:** `git log --oneline main -- _state/published_index.md` shows the last content change was `91104ae chore: record L-007 publication in published_index`. L-008, L-009, and L-010 merges all landed without an index append (the L-009 entry at line 23 predates the L-010 merge). See also commit `b51091a` (Merge PR #16 from AriesEmber/drafts/L-010).
**Suggested fix:** One housekeeping commit on `main` that appends three lines to `_state/published_index.md`, mirroring the existing format:
```
- L-010 | M02 | D01 | Understand file paths, extensions, and hidden files | 2026-04-20 | ce07351
- L-011 | M02 | D01 | Install a package manager | <merge date> | <merge SHA>
```
and updates the completion counts at the bottom. The L-011 run proceeded because the prerequisite is verifiably satisfied by the repo state even if the index lags.
**Status:** open

### [2026-04-19] L-009 — gate 11 reading-time sanity

**Lesson:** Edit a file with nano
**Flagged at:** quality_gates
**Severity:** warning
**Issue:** Computed reading time ~31 minutes vs spine estimate 13 minutes; delta 18 minutes exceeds the 5-minute band.
**Evidence:** `gate11_code_blocks=13, prose_word_count=1167, prose_minutes=5.3, hands_on_minutes=26`. Same Gate 11 heuristic issue documented for L-003, L-006, L-007 and L-008: 2 minutes per fenced code block is an over-count for one-line `nano hello.txt`, `cat hello.txt`, and the single-key editor keystroke blocks (`^O`, `<Enter> ^X`) that take under 15 seconds each. Ten of the thirteen blocks are one-line commands or their short output; only two (the typed three-line buffer and the `winget install GNU.Nano` block followed by the `Y` agreement prompt) consume any real time.
**Suggested fix:** No article change needed. Same recalibration recommendation as prior lessons: weight single-command blocks at 15 seconds, multi-line at 2 minutes. Lesson ships per the soft-warning rule.
**Status:** open

### [2026-04-19] L-008 — gate 11 reading-time sanity

**Lesson:** Read a file's contents with cat and less
**Flagged at:** quality_gates
**Severity:** warning
**Issue:** Computed reading time ~34 minutes vs spine estimate 13 minutes; delta 21 minutes exceeds the 5-minute band.
**Evidence:** `gate11_code_blocks=14, prose_word_count=~1497, prose_minutes=6.8, hands_on_minutes=28`. Same Gate 11 heuristic issue documented for L-003 and L-006: 2 minutes per fenced code block is an over-count for one-line `cat` / `less` / `more` / `printf` exchanges that run in under 15 seconds each. Twelve of the fourteen code blocks are single-line commands or their short output; only two (the `1..30 > notes-long.txt` generator and the pager interaction) take more than 30 seconds of reader time.
**Suggested fix:** No article change needed. Same recalibration recommendation: weight single-command blocks at 15 seconds, multi-line at 2 minutes. Lesson ships per the soft-warning rule.
**Status:** open

### [2026-04-19] L-006 — gate 10 reading-time sanity

**Lesson:** Move around with cd and relative paths
**Flagged at:** quality_gates
**Severity:** warning
**Issue:** Computed reading time 37.2 minutes vs spine estimate 13 minutes; delta 24.2 minutes exceeds the 5-minute band.
**Evidence:** `gate10_reading_time_min=37.2, gate10_spine_est=13, code_blocks=16`. Same Gate 10 heuristic issue documented for L-003: 2 minutes per fenced code block is an over-count for one-line `cd` / `pwd` exchanges that run in under 15 seconds each. Fourteen of the sixteen blocks are single-line commands or their immediate output.
**Suggested fix:** No article change needed. Same recalibration recommendation as L-003: weight single-command blocks at 15 seconds, multi-line at 2 minutes. Lesson ships per the soft-warning rule.
**Status:** open

### [2026-04-19] L-003 — gate 10 reading-time sanity

**Lesson:** Print your first line with echo
**Flagged at:** quality_gates
**Severity:** warning
**Issue:** Computed reading time 24.5 minutes vs spine estimate 13 minutes; delta 11.5 minutes exceeds the 5-minute band.
**Evidence:** `gate10_reading_time_min=24.5, gate10_spine_est=13`. Heuristic charges 2 minutes per fenced code block, and this lesson has 7 blocks. Each block is a one-line echo exchange that takes roughly 10 seconds to execute, so the heuristic over-counts. The 13-minute spine estimate matches the actual hands-on time.
**Suggested fix:** No article change needed. Recalibrate the Gate 10 heuristic to weight single-command code blocks at 15 seconds instead of 2 minutes, or only charge 2 minutes for multi-line blocks. Lesson ships per the soft-warning rule in quality_gates.md.
**Status:** open

## Resolved items (recent 20)

<!-- Archive of resolved flags; everything older moves to _state/archive/pending_review_archive.md -->
