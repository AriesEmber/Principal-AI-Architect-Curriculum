# Shorts Index

**Repository:** https://github.com/AriesEmber/Principal-AI-Architect-Curriculum

Tracks which published lessons have a vertical short produced under `_deliverables/shorts/`. The `short-author` skill reads this file to decide which lesson to render when Elvis says `create next short` (selection = lowest `sequence_number` where `lesson_id` is in `published_index.md` AND NOT in this file).

**Do not hand-edit this file.** The skill appends to it after each successful PR.

## Published shorts

<!-- Format, one per line:
- L-### | M## | D## | <title> | <published date ISO8601> | <commit SHA>
-->
- L-001 | M01 | D01 | Open the terminal with a keyboard shortcut | 2026-04-21 | eff4dbf
