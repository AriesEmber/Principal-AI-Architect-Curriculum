# Published Lesson Index

**Repository:** https://github.com/AriesEmber/Principal-AI-Architect-Curriculum

This file tracks which lessons have been published to `main`. The `lesson-author` skill reads this to compute which lesson to author next (selection = lowest `sequence_number` where `lesson_id` not in this list AND all `prerequisite_lesson_ids` are in this list).

**Do not hand-edit this file.** The skill appends to it after each successful merge to `main`. Hand-editing breaks the selection logic.

## Published lessons

<!-- The skill appends entries below this line. Format:
- L-### | M## | D## | <title> | <published date ISO8601> | <commit SHA>
-->

- L-001 | M01 | D01 | Open the terminal with a keyboard shortcut | 2026-04-19 | 6366f52
- L-002 | M01 | D01 | Read a prompt like a sign at a train station | 2026-04-18 | 7759e1d
- L-003 | M01 | D01 | Print your first line with echo | 2026-04-18 | 407973b

## Curriculum completion

- Total lessons in curriculum: 171
- Published: 3
- Remaining: 168
- Completion: 1.8%

(The skill updates the three counts above after each publication.)
