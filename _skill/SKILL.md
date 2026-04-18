# Lesson Author Skill

**Purpose.** Produce one publication-ready lesson per run for the Principal AI & Data Architect Curriculum. Dual-output: canonical GitHub Markdown, plus a LinkedIn-adapted variant. Handles three capture modes (`terminal_auto`, `rendered_auto`, `script_only`) via dispatch.

**When to use.** Any run targeting a specific lesson ID from `curriculum_spine_v1.1.yaml`. Normally invoked by the daily scheduled task; also invoked manually for pilot runs and backfills.

**When NOT to use.** Edits to published lessons (handle manually, not through this skill — the skill is author-once, not editor). Spine updates (change the spine in a separate conversation; this skill only reads the spine). Module-level README generation (separate one-shot task).

---

## Inputs

The skill expects exactly one of:

1. **Explicit lesson ID** passed in the invocation: `"Produce lesson L-001"`
2. **"Next unpublished" directive**: `"Produce the next unpublished lesson whose prerequisites are all published"`

If neither is provided, halt and ask. Do not guess.

The skill reads these files from the project knowledge and the repo:

| File | Location | Used for |
|---|---|---|
| `curriculum_spine_v1.1.yaml` | knowledge + `_curriculum/` | Lesson metadata |
| `style_guide_seed_v1.1.md` | knowledge + `_curriculum/` | Voice, banned words, format |
| `capture_mode_registry.md` | knowledge + `_curriculum/` | Dispatch rules |
| `competency_framework.md` | knowledge + `_curriculum/` | Domain context |
| `_state/published_index.md` | repo | What has shipped |
| `_state/production_log.jsonl` | repo | Run history, recovery points |
| `_state/pending_review.md` | repo | Prior flags (may affect current run) |

## Outputs

On success, the skill produces:

1. `modules/M##-<slug>/lessons/L-###-<slug>.md` — canonical GitHub Markdown
2. `modules/M##-<slug>/lessons/L-###-<slug>-linkedin.md` — LinkedIn variant
3. `modules/M##-<slug>/assets/L-###-*` — images, diagrams, GIFs, recording scripts (varies by capture mode)
4. One appended line to `_state/production_log.jsonl`
5. One entry added to `_state/pending_review.md` (if any quality gate warnings)
6. A draft branch `drafts/L-###` with all of the above committed
7. An open pull request to `main` with a structured body (see `assembly_phase.md`)

## The five phases

Every run executes these five phases in order. Do not skip; do not reorder. Each phase has its own document in `assets/`. Read the phase document before starting the phase.

1. **Research** — `assets/research_phase.md`
2. **Design** — `assets/design_phase.md`
3. **Demo** — `assets/demo_phase.md` (dispatches by capture mode)
4. **Assembly** — `assets/assembly_phase.md`
5. **Quality gates** — `assets/quality_gates.md`

If any phase fails a hard check, halt the run, write the failure to `_state/pending_review.md`, append a "failed" line to the production log, and surface the problem. Do not limp forward with a broken lesson.

## The selection logic

If called with an explicit lesson ID, use that. Otherwise:

1. Read `_state/published_index.md` to get the set of published lesson IDs.
2. From `curriculum_spine_v1.1.yaml`, find all lessons where:
   - `lesson_id` is not in the published set
   - Every ID in `prerequisite_lesson_ids` is in the published set
3. Select the candidate with the lowest `sequence_number`.
4. If no candidate exists (curriculum complete, or every next-available has a blocked prereq), halt and report.

## The capture mode dispatch

After the design phase, the demo phase dispatches strictly on `lesson.capture_mode`:

```
if lesson.capture_mode == "terminal_auto":
    # Produce a reproducible shell session in the sandbox.
    # Capture stdout + stderr. Render as styled terminal transcript + animated GIF.
    # Scrub secrets. Commit to assets/.
    run_terminal_auto(lesson)
elif lesson.capture_mode == "rendered_auto":
    # Generate the artifact (SVG diagram, markdown table, notebook, annotated diff).
    # Render to PNG via Playwright for inline embedding. Commit source + render.
    run_rendered_auto(lesson)
elif lesson.capture_mode == "script_only":
    # Generate shot list, voiceover script, on-screen text overlays, placeholder images.
    # Commit the recording script. Human records separately and commits the final MP4/GIF.
    run_script_only(lesson)
else:
    halt(f"Unknown capture mode: {lesson.capture_mode}")
```

The dispatch is one-way. The skill never second-guesses the mode.

## One-lesson discipline

The skill authors one lesson per run. It does not:

- Batch multiple lessons
- Improve earlier lessons
- Rewrite the spine
- Produce module READMEs (separate task)
- Run in "review mode" on existing lessons

If asked to do any of those things, the skill halts and reports. The one-lesson discipline is what keeps the daily cadence sustainable.

## Read the phase documents

Every run starts by reading the five phase documents in `assets/`. Do not skim; the phase documents encode the instructional design taxonomy, the quality gates, and the dispatch implementations. Reading them on every run is cheap and prevents drift.

Begin every run by reading, in this order:
1. `assets/research_phase.md`
2. `assets/design_phase.md`
3. `assets/demo_phase.md`
4. `assets/assembly_phase.md`
5. `assets/quality_gates.md`

Then execute.
