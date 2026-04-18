# Quality Gates

**Goal.** Every lesson passes every gate before the pull request opens. No exceptions. Gate failures halt the run and write to `_state/pending_review.md`.

The gates are run in order. Earlier gates catch simpler issues; later gates catch higher-order concerns.

## Gate 1: Banned words and punctuation

**Check.** Scan both articles for banned words and em dashes. The banned list is in `style_guide_seed_v1.1.md`. Case-insensitive match, whole-word boundaries.

**Fail action.** Halt. Write the exact occurrence(s) to `pending_review.md` with line numbers and suggested replacements.

**Banned words recap (not exhaustive — read the style guide):**
`delve`, `nuanced`, `robust`, `seamless`, `synergy`, `leverage` (as verb), `unlock`, `unleash`, `empower`, `disruptive`, `cutting-edge`, `best-in-class`, `world-class`, `next-generation`, `game-changer`, `revolutionize`, `transform` (as hype), `journey` (as learning metaphor), `tapestry`, `intricate`, `multifaceted`. Em dashes always.

**Automated scrubber.** A regex scan implemented in `scripts/banned_words_check.py`. The scrubber also catches common banned constructions ("it's not just X, it's Y", "imagine if you could", "in today's fast-paced world").

## Gate 2: Acronym expansion coverage

**Check.** For every acronym in `lesson.acronyms_used` plus every acronym introduced in the body, verify that the full expansion appears before the acronym's first standalone use in each article (GitHub and LinkedIn independently).

**Fail action.** Halt. Write the missed acronym(s) and the location(s) to `pending_review.md`.

**Edge cases.**
- If an acronym only appears once in the article (in its expanded form), no further expansion is needed.
- If the same acronym appears in both articles, it must be expanded in both — the first-use rule applies per article, not per lesson.
- Common English words that happen to be acronyms (OS, AI, IT, AT) still require expansion when used in their acronym sense.

## Gate 3: Analogy discipline

**Check.** Confirm:
- The analogy_anchor from the spine is used in the opening paragraph.
- The analogy does not persist past the third section (it's a bridge, not a highway).
- No second analogy is introduced.

**Fail action.** Halt. Name the violation and write to `pending_review.md`.

**Automation.** Partial. Counting word overlap with the analogy_anchor field works for the first check; the others need semantic judgment. When uncertain, flag with a question rather than halt.

## Gate 4: Length targets

**Check.** Word counts within bands:

| Article | Minimum | Maximum | Capstone override |
|---|---|---|---|
| GitHub canonical | 600 | 1,500 | 2,000 |
| LinkedIn variant | 800 | 1,500 | 1,500 (no override) |

**Fail action.** Halt. Report word counts and suggest which sections to expand or trim.

**Rationale.** Short GitHub lessons are fine for pure hands-on topics; anything under 600 words isn't a lesson, it's a snippet. Long lessons break the daily cadence. LinkedIn has hard performance cliffs at these lengths.

## Gate 5: Asset integrity

**Check.**
- Every image URL in both articles resolves to a file in `modules/M##-<slug>/assets/`.
- Every file referenced in the manifest exists.
- No file exceeds 5 MB (LinkedIn embed limit); GIFs capped at 2 MB.
- The manifest checksums match the files on disk.

**Fail action.** Halt. Name the missing or oversized asset.

**Automation.** Full. A Python script at `scripts/asset_check.py` handles this in one pass.

## Gate 6: Secret scrub

**Check.** Run `scripts/secret_scrub.py` against every text file in the lesson's output (both articles, the manifest, shot lists, voiceover scripts). The scrubber reports any regex hits.

**Fail action.** Halt. Any match is treated as a potential real credential. Review the specific string before proceeding.

**False positives.** The scrubber may flag example tokens like `sk-EXAMPLE-1234`. These are intentional. Confirm each flagged string is a placeholder before proceeding.

## Gate 7: Frontmatter-spine consistency

**Check.** The frontmatter of the canonical GitHub article matches the spine entry for this lesson. Fields checked:

- `lesson_id`
- `sequence_number`
- `module_id`
- `domain_id`
- `title`
- `week_number`
- `day_in_week`
- `estimated_minutes`
- `capture_mode`
- `risk_level`
- `is_capstone`

**Fail action.** Halt. Any mismatch is a drift between the contract and the output.

**Automation.** Full. A Python script compares YAML frontmatter to the spine entry. `acronyms_expanded` is allowed to be a superset of `acronyms_used` (you may have introduced new acronyms during writing).

## Gate 8: Prerequisite-state consistency

**Check.**
- Every ID in `lesson.prerequisite_lesson_ids` is in `_state/published_index.md`.
- The lesson itself is NOT already in `_state/published_index.md` (don't re-publish).

**Fail action.** Halt. The skill should not have selected this lesson; the selection logic has a bug. Report it.

**Automation.** Full, in the selection phase. This gate is a double-check.

## Gate 9: Dual-variant completeness

**Check.** Both files exist and are non-empty:
- `modules/M##-<slug>/lessons/L-###-<slug>.md`
- `modules/M##-<slug>/lessons/L-###-<slug>-linkedin.md`

And both have each required section (check for section headers on canonical; check for bolded labels on LinkedIn variant).

**Fail action.** Halt. Partial output is not acceptable.

## Gate 10: Reading-time sanity check

**Check.** Compute estimated reading time from word count (standard 220 wpm for technical prose) and compare to the spine's `estimated_minutes`. Include time for hands-on action (assume 2 minutes per command block) and extension.

**Fail action.** Soft warning, not a halt. If the gap is more than 5 minutes in either direction, flag it in `pending_review.md` for spine review — but the lesson still ships. The spine's time estimates can be calibrated over time.

**Automation.** Full.

---

## Gate sequence summary

1. Banned words — hard halt
2. Acronym expansion — hard halt
3. Analogy discipline — hard halt
4. Length targets — hard halt
5. Asset integrity — hard halt
6. Secret scrub — hard halt
7. Frontmatter-spine consistency — hard halt
8. Prerequisite-state consistency — hard halt
9. Dual-variant completeness — hard halt
10. Reading-time sanity — soft warning

All gates except #10 will stop a lesson from shipping. The tenth calibrates the curriculum over time without blocking publication.

## When a gate fails

1. Write the failure to `_state/pending_review.md` with:
   - Lesson ID
   - Gate name
   - Specific evidence (line numbers, word counts, file names, hashes)
   - Suggested fix, if obvious
2. Append a `"halt_reasons": [...]` entry to the production log for this run
3. Do NOT open the pull request
4. Do NOT commit the half-finished lesson to `main`
5. The draft branch may remain (so Elvis can see what was produced and fix it manually), but with a clear halt marker

The discipline is: no lesson ships broken. It's better to miss a day's cadence than to publish sloppy work under your name.
