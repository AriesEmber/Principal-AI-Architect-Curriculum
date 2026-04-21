# Research phase

Read the lesson. Extract the beats for the warehouse analogy.

## Inputs

- `_state/published_index.md` — confirms the lesson is published
- `modules/M##-.../lessons/L-###-*.md` — the canonical article
- Any transcripts under `modules/M##-.../assets/L-###-transcript.md`

## What you're deciding

For the lesson, identify:

1. **The systems involved** — what does the user touch? What does the system touch on their behalf? Each of these becomes a **swim lane** (a left-pinned box). 2–5 lanes is the sweet spot. More than 5 gets crowded on 1080px.

   Common lanes in M01: `Desktop`, `OS Search`, `Terminal`, `Shell`, `Filesystem`, `Package Manager`, `Network`, `Editor`.

2. **The beats** — the ordered sequence of actions in the warehouse metaphor. Each beat is one of:
   - `open` — opening shot, robot at home lane, title narration
   - `self` — an action happening on a single lane (typing, pressing a key, looking something up locally). Drawn as a speech bubble to the right of the robot.
   - `call` — a downward message from lane A to lane B (user or system delegating work). Drawn as a downward arrow.
   - `return` — an upward message from lane B back to lane A (result coming back). Drawn as an upward arrow.

3. **The narration for each beat** — what the TTS will say while the robot is doing that beat. Keep each narration ≤ 30 words. Conversational. Never write the command syntax twice in the audio and on the lane — pick one.

## Rules of thumb

- **Cap at 6–8 beats.** A short is 25–60 seconds. With F5-TTS speaking at ~2.8 words/second, 8 beats × 20 words ≈ 56 seconds. More beats = over the cap.
- **Every command in the lesson becomes at most one beat.** If the lesson shows three `echo` examples, pick the best one for the short; don't animate all three.
- **The last beat should feel like a landing.** A "you did it" moment. Not a fade-to-black.
- **Don't narrate the warehouse metaphor itself.** Don't say "imagine the robot fetches…" — the visual carries the metaphor; the audio describes what the *user* does.
- **Save the beats to the working memory for the next phase.** You will convert them to YAML next.
