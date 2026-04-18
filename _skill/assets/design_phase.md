# Design Phase

**Goal.** Turn the spine's skeleton (learning_objective, hands_on_action, verification, extension, analogy_anchor, acronyms_used) into a lesson structure that follows instructional design best practices adapted for the 12-15 minute micro-lesson format.

## The micro-lesson structure (hybrid ID taxonomy)

Every lesson follows this seven-section structure. The section order is fixed. The section *weight* (how much of the lesson each section occupies) varies by lesson type.

1. **Anchor** (opening paragraph, no heading) — the analogy anchor from the spine. One concrete image. No acronyms until expanded. Ends with a concrete action preview ("you are about to ___").
2. **What you will do** — one-sentence summary of the hands-on action. This is the promise.
3. **Before you start** — prerequisite check. Links to prior lessons by ID and title. Explicitly names what environment / tools / state the learner should have.
4. **Step by step** — the hands-on action broken into numbered steps with command blocks. Every command is in a fenced code block with a language hint. Every step has an expected-output description.
5. **Check it worked** — the verification from the spine, expanded. What the learner sees when it works. What they see when it fails, and how to recover.
6. **What just happened** — the conceptual explanation. Comes *after* the doing, not before. This is where the lesson explains why it worked.
7. **Going further** — the extension from the spine. Explicitly optional for the learner, but rich enough for a motivated reader to engage with.
8. **What's next** — one sentence naming the next lesson by ID and title.

## Section weights by lesson type

Different lesson categories need different section weights. Use these as targets:

| Lesson type | Anchor | Do-it | Verify | Explain | Extend |
|---|---|---|---|---|---|
| Pure hands-on (e.g., L-005 `ls`) | 15% | 40% | 15% | 20% | 10% |
| Conceptual (e.g., L-025 "what is a programming language") | 25% | 15% | 10% | 40% | 10% |
| Capstone (e.g., L-037 number-guessing game) | 10% | 50% | 15% | 15% | 10% |
| Cloud portal (e.g., L-113 "create free-tier Azure account") | 20% | 35% | 20% | 15% | 10% |
| Architecture (e.g., L-160 RAG design) | 20% | 20% | 10% | 40% | 10% |

The skill reads the lesson's `module_id` and `domain_id` to infer the lesson type and adjust section weights accordingly. If unclear, default to pure hands-on.

## The acronym expansion rule applied

For every acronym in `lesson.acronyms_used` (plus any acronym you introduce during writing):

1. On its first appearance in the body of the lesson, write: *full expansion* (ACRONYM). Example: "Command-Line Interface (CLI)".
2. After the first expansion, use the acronym alone.
3. The expansion rule resets per lesson. A learner reading L-087 in isolation must see every acronym expanded on first use there, even if L-001 through L-086 have expanded it already.

If the spine's `acronyms_used` is empty, no proactive expansion is needed for that lesson. But if you *do* introduce an acronym in the body, expand it.

## The analogy discipline

The `analogy_anchor` in the spine is the mental hook for the opening. Use it exactly:

- Introduce the analogy in the first two sentences of the lesson.
- Return to the analogy when introducing the core action. Example: "Just as the You Are Here arrow tells you where you stand, `pwd` tells your terminal the same thing."
- Do not introduce a second analogy mid-lesson. One concept, one bridge.
- Drop the analogy once the real thing is working. A reader who has `pwd` running does not need to keep thinking about shopping mall maps.

## Voice calibration

Every opening paragraph is pattern-matched against the voice sample in the style guide:

> A terminal is a room where you type and the computer types back. Nothing else. No windows to drag, no buttons to click, no menus to hunt through. The room has one door (the prompt) and one job (to run your next command). Every professional who works with servers, cloud infrastructure, or artificial intelligence (AI) systems spends most of their day in this room. You are about to learn the first word. It is `echo`. Type `echo hello` and press enter. The computer types back `hello`. That is the whole deal.

The opening paragraph of every lesson you write should:

- Start with a concrete image, not an abstract definition
- Use short sentences carrying real meaning
- Expand acronyms on first use (even in the opener)
- Hand the reader a concrete preview of what they will do
- Avoid em dashes, banned words, and throat-clearing

## The "point of no return" rule

Lessons with `risk_level: medium` or `risk_level: high` involve credentials, payments, or destructive actions. Before any command in the Step-by-step section that deletes something, exposes a credential, or incurs cost, insert a block:

```markdown
> **Heads up.** The next command will <specific consequence>. This cannot be undone without <recovery cost or impossibility>.
```

The block must name the specific consequence and the recovery path. Generic "be careful!" warnings are not allowed.

## What the design phase outputs

By the end of the design phase, you have a lesson *outline* — the seven sections populated with placeholder content, no full prose yet. Save this to `_state/scratch/L-###-outline.md` (not committed). The outline includes:

- The analogy anchor and how it threads through the lesson
- The exact commands for the Step-by-step section
- The expected output for each command (verification material)
- The conceptual explanation for "What just happened"
- The extension exercise
- The acronyms that need expansion and where they first appear
- The capture-mode-specific notes (what kind of demo asset is needed)

The prose is written in the assembly phase, using the outline as scaffolding.

## Halt conditions

Halt the design phase and flag for review if:

1. The spine's `hands_on_action` does not actually achieve the `learning_objective` (spine bug — flag it).
2. The analogy anchor does not map cleanly to the concept (analogy is decorative, not load-bearing).
3. The estimated minutes do not fit the content after outlining (too much or too little).
4. The capture mode assignment looks wrong given the hands-on action. Flag, but do not re-classify.

In all cases, write the halt to `_state/pending_review.md` with the lesson ID and specific issue.
