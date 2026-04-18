# Style Guide Seed

**Purpose.** This document is the voice-and-format contract for every lesson the downstream authoring skill produces. The curriculum spine tells the skill *what* to write; this guide tells it *how*. Keep it next to the spine at all times.

---

## 1. Voice principles

1. **Write to a reader whose job title is "career-changer, week one."** The opening lessons assume zero technical prior. No jargon in the first sentence of any lesson, ever. Jargon gets introduced slowly, named explicitly, and defined in plain language before it is used a second time.

2. **Prefer short sentences, plain words, and the active voice.** "Type `pwd` and press enter" beats "The `pwd` command can be invoked by entering it at the prompt and pressing return."

3. **No hedging, no filler, no throat-clearing.** Skip "let's dive in," "in this section we will explore," "it's worth noting that." Start with the thing.

4. **Be warm without being performative.** Acknowledge difficulty when it is real ("this step trips most people up"), but never manufacture enthusiasm or apologize for the curriculum being hard.

5. **Every explanation earns its place.** If a sentence does not move the reader one step closer to the hands-on action or the next lesson, cut it.

6. **One idea per paragraph.** If a paragraph has two ideas, break it into two paragraphs.

7. **Speak to the reader directly.** Use "you" and "your." Avoid "the user," "the learner," "one may."

8. **Concrete before abstract.** Show the command, show the output, *then* name what happened. Do not define a concept for three paragraphs before anyone sees it run.

---

## 2. Non-technical life analogies

Every lesson has an `analogy_anchor` field. The authoring skill must use it as the mental hook in the opening paragraph or two of the lesson. Rules:

1. **The analogy must come from everyday life, not from adjacent tech.** A package manager is like a grocery-store checkout, not like "apt but for Mac." An environment variable is like a sticky note on the fridge, not like "a global variable in Python."

2. **The analogy must be load-bearing.** It has to explain the concept, not just decorate the lesson. If you can delete the analogy without losing meaning, it was not doing work.

3. **Pick one analogy and stick with it through the lesson.** Do not introduce a second analogy mid-way. A reader holding two analogies at once is a reader losing the thread.

4. **Do not over-extend the analogy.** An analogy is a bridge to the first landing, not a highway. Once the reader understands the concept, drop the analogy and work with the real thing.

5. **No sports analogies, no cooking analogies that assume specialized equipment, no analogies that require prior cultural knowledge.** Use analogies that a forty-year-old reader anywhere in the world can parse on first read: mailboxes, keys, sticky notes, file cabinets, maps, invoices, receipts, train stations, grocery stores, light switches, thermostats, parking spaces, libraries.

6. **The opening lesson's analogy (L-001, "read a prompt like a sign at a train station") is the anchor for the entire curriculum.** The terminal is a train station. Commands are where you are going. The prompt is the sign telling you where you stand. Later lessons can refer back to this without re-explaining.

---

## 3. Acronym expansion rule

**Every acronym is expanded on first use in every lesson.** Not on first use in the curriculum. Not on first use in the module. On first use in every lesson. No exceptions.

Format: full expansion, then the acronym in parentheses. Example:

- "Open the command-line interface (CLI)."
- "This call uses Hypertext Transfer Protocol Secure (HTTPS) on port 443."

The rule applies even to acronyms the reader has already seen many times. The reader will not be reading lessons in order on a second pass. They will open L-087 six months from now to refresh on chain-of-thought and expect to understand it without scrolling back to L-001.

Specifically required expansions across the curriculum (always expand on first use per lesson):

- TDS: Technology & Digital Solutions
- EHR: Electronic Health Record
- AI: Artificial Intelligence
- ML: Machine Learning
- LLM: Large Language Model
- GenAI: Generative Artificial Intelligence
- API: Application Programming Interface
- CLI: Command-Line Interface
- GUI: Graphical User Interface
- SQL: Structured Query Language
- RAG: Retrieval-Augmented Generation
- MCP: Model Context Protocol
- PaaS: Platform as a Service
- IaaS: Infrastructure as a Service
- SaaS: Software as a Service
- IaC: Infrastructure as Code
- CI: Continuous Integration
- CD: Continuous Deployment
- VCS: Version Control System
- SSH: Secure Shell
- DNS: Domain Name System
- HTTP: Hypertext Transfer Protocol
- HTTPS: Hypertext Transfer Protocol Secure
- TLS: Transport Layer Security
- VPC: Virtual Private Cloud
- IAM: Identity and Access Management
- SDK: Software Development Kit
- REPL: Read-Eval-Print Loop
- JSON: JavaScript Object Notation
- CSV: Comma-Separated Values
- PDF: Portable Document Format
- PHI: Protected Health Information
- PII: Personally Identifiable Information
- PR: Pull Request
- NIST: National Institute of Standards and Technology
- RMF: Risk Management Framework
- TOGAF: The Open Group Architecture Framework
- BDAT: Business, Data, Application, Technology
- OLTP: Online Transaction Processing
- OLAP: Online Analytical Processing
- TCO: Total Cost of Ownership
- PGVector: PostgreSQL Vector Extension

If the skill is uncertain whether something is an acronym, expand it. Over-expansion is always safer than under-expansion.

---

## 4. Banned words and phrases

These do not appear anywhere in published lessons, captions, summaries, or social posts.

**Banned words.** `delve`, `nuanced`, `robust`, `seamless`, `synergy`, `leverage` (as a verb), `unlock`, `unleash`, `empower`, `disruptive`, `cutting-edge`, `best-in-class`, `world-class`, `next-generation`, `game-changer`, `revolutionize`, `transform` (as hype), `journey` (as metaphor for learning or career), `tapestry`, `intricate`, `multifaceted`.

**Banned punctuation.** Em dashes (`—`). Use commas, colons, periods, or parentheses instead. The word processor autocorrect that converts `--` to `—` must be off for every lesson author.

**Banned constructions.**

- "It's not just X, it's Y." (This is a cliche rhetorical flourish. Cut it.)
- "Imagine if you could...". (Same.)
- "In today's fast-paced world..." (No.)
- "At the end of the day..." (No.)
- "Whether you're a beginner or an expert..." (No.)

**Banned self-reference.** Lessons do not refer to themselves ("in this lesson we will learn"). They do not refer to the curriculum as a "journey." They do not apologize for being introductory.

---

## 5. Dual-publishing format

Every lesson is published twice: once as the canonical GitHub markdown file, once as a LinkedIn-adapted post. The GitHub version is the source of truth. The LinkedIn version is derived.

### 5.1 GitHub markdown (canonical)

- **File name.** `L-###-kebab-case-slug.md` (example: `L-087-chain-of-thought.md`).
- **Location.** A repository structured by module: `/modules/M14-prompt-engineering/lessons/L-087-chain-of-thought.md`.
- **Frontmatter.** YAML frontmatter with the lesson metadata fields from the spine (lesson_id, sequence_number, module_id, domain_id, title, estimated_minutes, capture_mode, risk_level, is_capstone). This is machine-readable metadata; the lesson body is below it.
- **Body length.** 600 to 1,200 words for standard lessons, up to 2,000 for capstones.
- **Sections, in order.**
  1. The opening paragraph (analogy anchor, no heading).
  2. "What you will do" (one-sentence summary of the hands-on action).
  3. "Before you start" (prerequisite check, links back to prior lessons).
  4. "Step by step" (the hands-on action broken into numbered steps with command blocks).
  5. "Check it worked" (the verification step).
  6. "What just happened" (a short conceptual explanation after the learner has done the thing).
  7. "Going further" (the extension step, optional for the learner).
  8. "What's next" (one-sentence link to the next lesson).
- **Code blocks.** Always fenced with language hint (\`\`\`bash, \`\`\`python, \`\`\`sql). No inline screenshots of code.
- **Images.** All images are committed to the repo under `/modules/M##-slug/assets/`. Every `<img>` uses an absolute GitHub raw URL (example: `https://raw.githubusercontent.com/<user>/<repo>/main/modules/M14-prompt-engineering/assets/L-087-diagram.svg`). This is so LinkedIn can render the same image from the same URL.
- **Links.** Inline markdown links, no footnote-style references. Every link opens in a new tab (the reader stays on the lesson).

### 5.2 LinkedIn version (derived)

- **Length.** 800 to 1,500 words. No shorter; no longer.
- **Opening.** The first two lines are the hook. Must stand alone before the "see more" cutoff.
- **Inline images.** 3 to 5 images embedded in the post, each referenced by absolute GitHub raw URL (same URLs as the canonical). Every image must add information: a diagram, a terminal screenshot, a side-by-side comparison. Decorative stock images are not allowed.
- **Structure.** Short paragraphs (2 to 3 sentences each). Numbered or bulleted lists welcome. Sub-headings as bold text rather than markdown headers (LinkedIn does not render `#`).
- **Closing.** One concrete call to action, one sentence long. Examples: "Try it yourself and tag me," "The full lesson with the code is here: <link>," "Part 2 drops Monday." No "what do you think?" closers, no solicitation of comments for engagement.
- **Hashtags.** 3 to 5 hashtags at the end, specific rather than generic. `#HealthcareAI`, `#SolutionsArchitecture`, `#RAG` are useful; `#AI`, `#Tech`, `#Innovation` are not.
- **No tagging of real named individuals unless prior permission.** Companies and organizations are fine to tag.

### 5.3 What is dropped from the LinkedIn version

- The frontmatter.
- The "Before you start" prerequisite links (LinkedIn is a terminal, not a curriculum).
- Deep code blocks (keep to one or two short snippets; link to GitHub for the full thing).
- The "Going further" extension.

### 5.4 What is added for LinkedIn

- A one-line personal framing at the top: what the author noticed, what surprised them, what they got wrong the first time. This is the thing LinkedIn rewards and GitHub does not need.
- A visible link to the GitHub version at the bottom.

---

## 6. Voice-sample paragraph (pattern-match target)

Use this as the calibration sample for voice, cadence, and register. Every lesson the downstream skill writes should read like this in its opening paragraph.

> A terminal is a room where you type and the computer types back. Nothing else. No windows to drag, no buttons to click, no menus to hunt through. The room has one door (the prompt) and one job (to run your next command). Every professional who works with servers, cloud infrastructure, or artificial intelligence (AI) systems spends most of their day in this room. You are about to learn the first word. It is `echo`. Type `echo hello` and press enter. The computer types back `hello`. That is the whole deal.

Things to notice about the sample:

- Opens with a concrete image, not an abstract definition.
- Names the acronym (AI) on first use.
- Short sentences carry the load.
- No em dashes. No banned words. No throat-clearing.
- Hands the reader an action in the first paragraph.
- Ends with a line that rewards the reader for having read the paragraph.

---

## 7. Edge cases and overrides

1. **When a concept genuinely requires a longer explanation,** the lesson can go to 1,500 words on GitHub. But the first paragraph still opens with a concrete image.

2. **When a lesson covers a topic the reader already knows in real life** (for example, the HTTP status code lesson for a reader who has worked in customer support), the skill can acknowledge that in one sentence and move on. It does not re-explain.

3. **When a lesson's hands-on action involves a destructive command** (deleting files, tearing down cloud resources), the lesson must include a "point of no return" warning block before the command. The warning uses a clear visual marker (a blockquote with `> **Heads up.**`) and states what will be deleted and what cannot be recovered.

4. **When a lesson introduces a concept that has been named differently in different cloud providers** (example: Azure calls it a Resource Group, AWS calls it a Stack, GCP calls it a Project), the skill must name all three equivalences on first use. Elvis is building for a multi-cloud career context and the cross-cloud mapping is core curriculum value.

5. **When a lesson reuses code from an earlier lesson,** it must link back to that lesson in the "Before you start" section. It does not re-paste the code.

---

## 8. Files to keep next to this guide

- `competency_framework.md` (what we are teaching and why)
- `curriculum_spine.yaml` (the 171 lessons with all metadata)
- `capture_mode_registry.md` (how to physically produce each lesson)
- `style_guide_seed.md` (this file)

The downstream authoring skill reads all four. This guide is the one it reaches for when it needs to decide how a sentence should sound.
