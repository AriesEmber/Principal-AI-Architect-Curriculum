# Assembly Phase

**Goal.** Combine the outline (design phase), research notes, and demo assets into the two final articles: the canonical GitHub Markdown and the LinkedIn-adapted variant.

## Input inventory

At the start of assembly, confirm you have:

- The lesson outline at `_state/scratch/L-###-outline.md`
- Research notes at `_state/scratch/L-###-research-notes.md` (if research was performed)
- A manifest of demo assets at `modules/M##-<slug>/assets/L-###-manifest.json`
- The spine entry for this lesson (from `curriculum_spine_v1.1.yaml`)
- The style guide (from project knowledge)

If any of these is missing, halt — do not try to reconstruct. The prior phase failed and should have been caught.

## Output 1: GitHub canonical article

Write to `modules/M##-<slug>/lessons/L-###-<slug>.md`.

**Frontmatter.** Exact YAML structure — the fields must match for downstream tooling:

```yaml
---
lesson_id: L-001
sequence_number: 1
module_id: M01
domain_id: D01
title: "Open the terminal with a keyboard shortcut"
week_number: 1
day_in_week: 1
estimated_minutes: 10
capture_mode: script_only
risk_level: low
is_capstone: false
published_at: 2026-04-20T09:00:00Z
acronyms_expanded: [CLI, OS, GUI]
---
```

`published_at` is written at commit time, not at authoring time. `acronyms_expanded` is the actual set of acronyms expanded in the body — may be a superset of the spine's `acronyms_used` if you introduced additional ones.

**Body structure.** Follow the seven sections from the design phase. Use Markdown headers exactly as below:

```markdown
<opening paragraph, no heading — the analogy anchor>

## What you will do

<one sentence>

## Before you start

<prerequisite check with links>

## Step by step

<numbered steps with code blocks>

## Check it worked

<verification expanded>

## What just happened

<conceptual explanation>

## Going further

<extension exercise>

## What's next

<one sentence linking to the next lesson>
```

**Image embedding.** Every image uses an absolute GitHub raw URL:

```markdown
![Terminal window showing prompt](https://raw.githubusercontent.com/<user>/principal-ai-architect-curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-shot-01.png)
```

The absolute URL is required so the same Markdown renders on LinkedIn. Use the repo URL from `_state/published_index.md`'s header; that file stores the canonical repo URL to avoid hardcoding.

**Code blocks.** Always fenced, always language-tagged:

```markdown
\`\`\`bash
pwd
\`\`\`
```

For terminal sessions, show the command and expected output together:

```markdown
\`\`\`bash
$ pwd
/Users/elvis
\`\`\`
```

**Links.** Inline markdown links, opening in the current tab (no `target="_blank"` — this is Markdown, not HTML). The reader should stay on the page.

**Prerequisites section links.** Use the lesson's spine title:

```markdown
## Before you start

You need to have completed [L-004: Find out where you are with pwd](../L-004-pwd.md) and have a working terminal open.
```

## Output 2: LinkedIn-adapted article

Write to `modules/M##-<slug>/lessons/L-###-<slug>-linkedin.md`.

**Length target.** 800-1,500 words. No shorter, no longer.

**Structure.** Drop these from the GitHub version:

- The frontmatter
- The "Before you start" prerequisite links
- Deep code blocks (keep one or two short illustrative snippets; link to GitHub for the full lesson)
- The "Going further" extension

Add these:

- **Personal framing at the top** — one line naming what Elvis noticed, what surprised him, what he got wrong the first time. This is what LinkedIn rewards and GitHub doesn't need. Example: "The first time I opened a terminal, I stared at a blinking cursor for two minutes before realizing I was supposed to type. Here's how to skip that moment."
- **A visible link to the GitHub version at the bottom.** "Full lesson with the full commands and exercises: <link>"
- **3-5 hashtags** at the end, specific not generic. Examples: `#HealthcareAI`, `#SolutionsArchitecture`, `#LearnToCode`, `#AIArchitect`. Avoid `#AI`, `#Tech`, `#Innovation`.

**Formatting differences from GitHub.**

- LinkedIn does not render Markdown headers (`#`, `##`, `###`). Use **bold text** for section labels instead.
- LinkedIn does render short code blocks inside backticks. Use sparingly.
- LinkedIn renders images inline. Use 3-5 images, each referencing the same GitHub raw URL as the canonical.
- The first two lines of the post must stand alone before the "see more" cutoff. These are the hook.

**Closing.** One sentence, one call to action. Examples:

- "Try it and tag me when it works."
- "Part 2 goes live Monday. Follow to get it in your feed."
- "Full code and exercises on GitHub: <link>"

No "what do you think?" closers, no comment-farming, no manufactured engagement requests.

## The production log entry

After both articles are written, append one line to `_state/production_log.jsonl`:

```json
{"timestamp":"2026-04-20T09:00:00Z","lesson_id":"L-001","status":"authored","branch":"drafts/L-001","assets_count":4,"github_words":847,"linkedin_words":1143,"acronyms_expanded":["CLI","OS","GUI"],"research_sources_count":2,"halt_reasons":[]}
```

JSON Lines format — one JSON object per line, no comma, no enclosing array. Append-only. Never rewrite this file.

## The pull request body

When the draft branch is pushed and the PR opens, the body uses this template:

```markdown
## Lesson L-### ready for review

**Title.** <title>

**Module.** M## — <module title>

**Domain.** D## — <domain name>

**Capture mode.** <mode>

**Estimated reading time.** <minutes>

**Word counts.** GitHub: <N>, LinkedIn: <N>

## Pre-flight checklist

- [ ] All acronyms expanded on first use (per style guide)
- [ ] No banned words or em dashes (quality gates passed)
- [ ] Analogy anchor threads through the lesson
- [ ] Hands-on action matches the spine
- [ ] Verification is concrete and reproducible
- [ ] Assets under 5 MB each
- [ ] Secret scrubber passed
- [ ] Both GitHub and LinkedIn variants produced

## Assets produced

- `modules/M##-<slug>/lessons/L-###-<slug>.md`
- `modules/M##-<slug>/lessons/L-###-<slug>-linkedin.md`
- `modules/M##-<slug>/assets/L-###-<asset>.png` (N assets total)

## Flagged for human attention

<any items from pending_review.md for this lesson, or "None" if clean>

## Research sources

<bulleted list of URLs consulted with brief annotation>
```

All checkboxes start unchecked. The human reviewer checks them as they verify each item. Pull request cannot be merged with unchecked boxes.

## Halt conditions

Halt the assembly phase and flag for review if:

1. Either article is outside its length band (GitHub 600-2,000; LinkedIn 800-1,500).
2. An image URL resolves to a missing file (asset manifest vs. actual file mismatch).
3. A section in the outline is empty or placeholder-only after writing (you didn't actually write the section).
4. Frontmatter fields do not match the spine (drift between contract and output).

Write the halt to `_state/pending_review.md` with lesson ID and the specific gate that failed.
