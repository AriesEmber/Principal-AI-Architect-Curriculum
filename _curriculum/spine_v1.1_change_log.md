# Curriculum Spine v1.0 to v1.1 Change Log

**Generated:** 2026-04-18

## Summary of changes

| Metric | v1.0 | v1.1 | Change |
|---|---|---|---|
| Total lessons | 171 | 171 | unchanged |
| Total domains | 12 | 12 | unchanged |
| Total modules | 26 | 26 | unchanged |
| Total capstones | 26 | 26 | unchanged |
| Weeks covered | 1-25 | 1-26 | metadata aligned |
| DAG violations | 0 | 0 | unchanged |
| Sequence gaps | 0 | 0 | unchanged |
| Lessons with empty acronyms_used | 66 | 5 | -61 |
| Lessons whose acronyms_used changed | - | 136 | - |
| Capture mode: terminal_auto | 87 | 87 | unchanged |
| Capture mode: rendered_auto | 23 | 23 | unchanged |
| Capture mode: script_only | 61 | 61 | unchanged |

## What changed

### Acronym field fills (the primary fix)

The v1.0 spine only populated `acronyms_used` when an acronym appeared literally in the lesson title. The v1.1 pass scans all lesson content fields (title, learning_objective, hands_on_action, verification, extension, analogy_anchor) against the canonical acronym list in `style_guide_seed.md`, plus conceptual proxies:

- "terminal", "command line", "shell", backticked shell commands, `pip`, `venv`, `python3` -> CLI
- "git", "GitHub", "repo", "commit", "branch", "clone", "push", "pull" -> VCS
- "pull request", "merge into a branch" -> PR
- "REPL", "open Python and run", "interactive" -> REPL
- "Ollama", "local model", "chat with a model" -> LLM
- "Terraform", "infrastructure as code", ".tf" -> IaC
- "portal", "console", "browser", "web UI", "installer" -> GUI
- "encryption in transit" -> TLS
- "role-based access", "least privilege" -> IAM
- "protected health" -> PHI
- "personally identifiable" -> PII
- ...and direct matches for the full style guide acronym list.

After the scan, 15 false-positive SQL tags were removed. The regex for SQL keywords ("WHERE", "LEFT") was matching ordinary English uses of those words in non-SQL lessons. SQL is now tagged only when (a) the lesson is in domain D05 (SQL & Data Manipulation) or (b) the literal string "SQL", "SELECT", or "JOIN" appears in uppercase. This conservative rule may under-tag later data lessons; the skill should do a runtime cross-check if SQL keywords appear in the final article.

### Remaining empty acronym lists (legitimate)

Five lessons genuinely have no acronyms on first use. The skill's expansion rule treats empty `acronyms_used` as "no expansion needed" and proceeds normally.

| Lesson | Title | Why empty is correct |
|---|---|---|
| L-040 | Sets and tuples | Pure Python data structure concepts. Sets and tuples are not acronyms. |
| L-044 | Why virtual environments exist | Reading-and-summary lesson. No commands run, no acronyms named. |
| L-051 | Structured, semi-structured, unstructured, the three families | One-page note exercise. Conceptual only. |
| L-167 | Executive summary, 1 page for the board | Writing exercise. Any acronyms depend on the author's content choices. |
| L-170 | Five-minute walkthrough, explain it to a non-technical executive | Recording task. No new acronyms in the lesson mechanics. |

### Style guide amendment

`PDF` (Portable Document Format) added to the style guide's canonical acronym list. L-160 uses "PDF corpus" and the acronym needs expanding on first use.

### Week alignment

- L-170 (Five-minute walkthrough) moved from week 25 to week 26
- L-171 (Publish the portfolio, final capstone) moved from week 25 to week 26
- Metadata `total_weeks` updated from 25 to 26

Weeks 1-25 carry 6-7 lessons each; week 26 is a deliberate 2-lesson portfolio-assembly week.

### Duration flags for human review (no edits made)

| Lesson | Title | Minutes | Recommended action |
|---|---|---|---|
| L-001 | Open the terminal with a keyboard shortcut | 10 | Keep. Day-1 lesson is intentionally trivial to land the psychological win. |
| L-002 | Read a prompt like a sign at a train station | 10 | Keep. Foundational mental model, brevity is a feature. |

Both flags are benign. No action required.

## The contract going forward

The downstream `lesson-author` skill treats `curriculum_spine_v1.1.yaml` as the single source of truth for:

1. Lesson ordering and prerequisites (via `sequence_number` and `prerequisite_lesson_ids`)
2. Capture mode dispatch (via `capture_mode`)
3. Acronym expansion list per lesson (via `acronyms_used`). Empty list = no expansion needed.
4. Hands-on action, verification, and extension content (the lesson skeleton)
5. Capstone flagging (via `is_capstone`)
6. Risk level for credential-handling or destructive lessons (via `risk_level`)

The skill does not re-classify any of these at production time. If something looks wrong, the skill flags and asks. The spine is the contract.

## Known limitations to revisit in v1.2

1. The SQL acronym is conservatively tagged. If the skill generates an article that uses SQL keywords and the spine didn't tag SQL, the skill should detect and expand at article-generation time.
2. Some lessons may generate articles that reference acronyms not flagged in the spine (for example, an architecture lesson might naturally mention an acronym the learning objective didn't hint at). The skill should treat `acronyms_used` as a minimum guarantee, not a closed set. Runtime acronym detection in the rendered article remains a backstop.
3. L-040, L-044, L-051, L-167, L-170 have empty acronym lists by design. If a human author decides to introduce an acronym in the article body, it still must be expanded on first use per the style guide rule. The empty list just means the skill doesn't need to proactively inject expansions.
