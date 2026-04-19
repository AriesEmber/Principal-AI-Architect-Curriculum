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
