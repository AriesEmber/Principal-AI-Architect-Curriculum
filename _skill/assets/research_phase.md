# Research Phase

**Goal.** Ground the lesson in current, accurate, citable information before designing the narrative.

## When to skip research

For the first 50 lessons (command line, Git, Python basics), the topics are stable and well-documented in training knowledge. Research is optional but still recommended for currency (package manager syntax changes, new Python version defaults, etc.).

For lessons 50+ (local AI, cloud, Terraform, MCP, governance), research is mandatory. These topics change monthly; training knowledge cannot be trusted.

## Research budget

- Lessons 1-50: 1-2 web searches maximum, 5 minutes
- Lessons 51-120: 3-5 web searches, 10-15 minutes
- Lessons 121-171: 5-10 web searches, 15-20 minutes
- Do not exceed 10 searches per lesson. If you cannot ground the lesson in 10 searches, the lesson's scope is wrong — flag it.

## Source quality hierarchy

Prefer sources in this order:

1. **Official documentation** — Microsoft Learn, AWS Docs, Google Cloud Docs, Python.org, PostgreSQL Docs, Terraform Registry, GitHub Docs
2. **Primary source organizations** — NIST, OWASP, The Open Group (TOGAF), W3C
3. **Vendor engineering blogs** — Databricks Engineering, Stripe Engineering, Netflix Tech Blog, AWS Architecture Blog
4. **Reputable independent** — Julia Evans, Martin Fowler, High Scalability, The Morning Paper
5. **Stack Overflow / Stack Exchange** — only for code-level nuance, never for conceptual framing
6. **Blog aggregators, medium.com, dev.to** — last resort, and only if corroborated by a source from tier 1-4

Never cite: reddit threads, Twitter/X posts, YouTube video descriptions, LinkedIn posts, or AI-generated content farms (the `*.example.blog`, `*.medium.com/@ai-content-*` kinds of sites).

## Research output: the notes file

Write research notes to a temporary file during the run: `_state/scratch/L-###-research-notes.md`. The file is NOT committed; it exists only for the duration of the run. Format:

```markdown
# L-### Research Notes

## Question 1: <what I searched for>
- Source: <title> — <URL>
- Accessed: <date>
- Key finding: <one sentence, paraphrased>
- Relevance: <why this matters for the lesson>

## Question 2: ...
```

## Citation rule in the final article

When research informs a lesson, cite the source with an inline markdown link on the specific claim. The reader should be able to verify any factual claim by clicking through. Format:

> Python's `venv` module has been part of the standard library [since Python 3.3, released in 2012](https://docs.python.org/3/library/venv.html).

Do not reproduce text from sources. Paraphrase everything. One short quote (under 15 words, in quotation marks) per source maximum, and only when the exact wording is the point (for example, naming a standard or a definition).

## What research is NOT

- **Not a replacement for the hands-on action.** The lesson still uses the `hands_on_action` from the spine. Research informs the *framing* around the action, not the action itself.
- **Not an excuse to pad the lesson.** If research yields "there are 17 ways to do this," pick the one way the spine indicates and mention alternatives only if it helps the learner understand why this way was chosen.
- **Not copyedit fodder.** Do not copy sentence structures from sources. Write in the curriculum's voice, not the source's voice.

## Halt conditions

Halt research and flag for review if:

1. Official documentation for the tool in the lesson has changed substantially since the spine was written (for example, a renamed command, a deprecated flag). The lesson may need rewriting, not just authoring.
2. A source-quality check fails — you cannot find a tier 1-3 source for a core claim in the lesson.
3. The tool the lesson teaches is no longer current (deprecated, replaced, unmaintained). Flag for spine update.

Write the halt reason to `_state/pending_review.md` with enough context for Elvis to decide whether to re-author the spine entry or proceed with a workaround.
