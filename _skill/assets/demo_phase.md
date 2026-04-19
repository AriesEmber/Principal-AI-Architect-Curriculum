# Demo Phase

**Goal.** Produce the visual/recorded assets for the lesson according to its `capture_mode`. This is the phase that actually runs code, renders diagrams, or generates recording scripts.

## The dispatch table

```
lesson.capture_mode  →  handler
-------------------------------
terminal_auto        →  run_terminal_auto(lesson)
rendered_auto        →  run_rendered_auto(lesson)
script_only          →  run_script_only(lesson)
```

The dispatch is the sole control path. Do not fall through, do not combine, do not re-classify.

---

## Handler: `terminal_auto`

**What this handler does.** Produces a two-column Bash + PowerShell animated GIF, a matching static PNG, a hand-generated SVG source, and a static transcript, all from a single config passed into the shared renderer.

**Steps.**

1. **Build a lesson config** at `_state/scratch/L-###-v2/build.py`. The config is a `LessonConfig` with an `exchanges` list — each exchange carries a `left` (Bash) `Side` and a `right` (PowerShell) `Side`, so the two shells are specified in lockstep. Look at `_state/scratch/L-004-v2/build.py` for a short example and `_state/scratch/L-007-v2/build.py` for a long (capstone) example.
2. **Import the shared renderer** from `_skill/scripts/side_by_side.py`. It emits GIF + PNG + SVG from one call (`build_all(cfg, asset_dir, file_stem=...)`). Do not write per-lesson rendering code; use the library.
3. **Post-process the transcript.** Trim pre-command noise (shell init messages), normalize prompt strings to a clean `$` for Bash and `>` for PowerShell, and apply `scripts/secret_scrub.py` regex pass.
4. **Tune the GIF size if it exceeds 2 MB.** `build_all` accepts `typing_step` (default 1 — skip every N frames when typing long commands) and `colors` (default 64 — palette size). Capstone lessons typically need `typing_step=3, colors=20` to stay under the cap.
5. **Render a static transcript** as `L-###-transcript.md` with fenced code blocks for both Bash and PowerShell for screen-reader accessibility (GIFs are inaccessible to screen readers).
6. **Commit assets** to `modules/M##-<slug>/assets/`. Both the build script and the rendered outputs check in — the script is reproducible; the renders are the embeddable assets.

**What the shared renderer guarantees.** Canvas height is computed from the exchange count so no trailing whitespace ever ships (Gate 12). GIF, PNG, and SVG share identical colour tokens, layout, and captions — they cannot drift. Step labels on the right edge of each window correspond one-to-one across columns.

**Secret scrubbing.** Every transcript is piped through `scripts/secret_scrub.py` before rendering. The scrubber replaces matches of:

- API key patterns (`sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{36}`, etc.)
- Bearer tokens in headers
- Anything resembling an email address + password pair
- JWT-shaped strings
- AWS access key / secret key patterns
- Azure connection strings
- Any value assigned to an env var named `*_KEY`, `*_SECRET`, `*_TOKEN`, `*_PASSWORD`

with placeholder tokens like `<REDACTED-API-KEY>`. The scrubber's regex list is maintained in `scripts/secret_scrub.py`. Update it whenever a new credential format shows up.

**Lessons that never need secret scrubbing** (pure Python basics, pure shell basics) still run through the scrubber as a defense-in-depth measure. It's cheap.

---

## Handler: `rendered_auto`

**What this handler does.** Generates the artifact the lesson teaches (SVG diagram, markdown table, Jupyter notebook, annotated code diff), renders it to PNG, and commits both source and render.

**Steps.**

1. **Identify the artifact type** from the lesson's hands-on action. Examples:
   - Diagram → SVG
   - Table/matrix → Markdown table rendered to PNG via Playwright
   - Notebook → `.ipynb` rendered via `nbconvert` to HTML, screenshotted
   - Annotated code diff → side-by-side HTML render screenshotted
2. **Generate the source artifact.** For SVG diagrams, follow the conventions in Elvis's `elvis-jones-network-diagram` skill if available: dashed animated connectors, port/protocol labels, liquid-glass aesthetic when appropriate. For other artifacts, use project defaults.
3. **Render to PNG** via Playwright headless Chromium at 2x device pixel ratio (retina-quality). Target: under 500 KB per PNG; if over, compress with `pngquant`.
4. **Produce an SVG source when possible.** SVG is preferred over PNG for diagrams because LinkedIn renders SVG and GitHub renders SVG, and the source is scalable. Use PNG only when the render includes rasterized content.
5. **Commit both** source (`.svg`, `.ipynb`, `.md`) and render (`.png`) to `modules/M##-<slug>/assets/`.

**Branding rules.** Diagrams follow Elvis's stated preferences when he has stated them: animated dashed flow lines, labeled connectors with ports and protocols, no lines passing through boxes, liquid-glass translucent fills when requested. For diagrams where these preferences don't apply (conceptual matrices, comparison tables), use a clean neutral style.

---

## Handler: `script_only`

**What this handler does.** The skill cannot capture this lesson's demo directly — the action crosses a GUI, installer, or cloud portal. The skill produces a precise recording script that a human executes.

**Steps.**

1. **Produce a shot list** at `modules/M##-<slug>/assets/L-###-shotlist.md` with:
   - Ordered scenes numbered 1, 2, 3, ...
   - For each scene: what's on screen, what the mouse/hands do, duration estimate (seconds), any on-screen text overlay
2. **Produce a voiceover script** at `modules/M##-<slug>/assets/L-###-voiceover.md` with:
   - One line per scene, timed to match the shot list
   - Written in the curriculum's voice (same rules as the article body)
3. **Produce placeholder images** for every scene at `modules/M##-<slug>/assets/L-###-shot-##-placeholder.png`. These are wireframe-style boxes with captions like "SCREEN: Azure Portal home page, cursor on 'Create a resource'". The recorder replaces these with real captures later.
4. **Produce a recording checklist** at `modules/M##-<slug>/assets/L-###-recording-checklist.md` with:
   - Window size to record at (1920x1080 standard)
   - Tool recommendation (OBS on Windows, QuickTime on macOS, ShareX for GIFs)
   - Export format and target file size
   - Where to drop the final file (path in the repo)
5. **Do NOT commit placeholder images as-if-real.** Name them explicitly `*-placeholder.png` so no one confuses them with real captures.
6. **Flag the lesson in `pending_review.md`** with the recording assignment. The human (Elvis) records against the script and replaces placeholders before the lesson is merged to `main`.

**Why this handler does not attempt capture.** Running a desktop GUI inside the sandbox is possible in theory (xvfb, xdotool, screen recording via `ffmpeg`), but it's brittle, slow, and produces low-quality output. The gain is not worth the complexity for a curriculum with only 36% `script_only` lessons. Producing a good recording script is actually the higher-leverage automation — a 5-minute human recording against a tight script beats a 30-minute shaky automated capture every time.

**For L-001 specifically** (the pilot lesson): the recording is one scene — the learner pressing Cmd+Space on Mac or Windows key on Windows, typing "terminal", and hitting Enter. The shot list is three shots (empty desktop, search box with typing, terminal window appearing), the voiceover is 30 seconds, the recording is under 60 seconds of raw footage. This is the minimum-viable demo.

---

## Common post-conditions

After any handler runs, before committing:

- All files for this lesson live in `modules/M##-<slug>/assets/` with names prefixed `L-###-`
- No file exceeds 5 MB (LinkedIn embed limit); GIFs capped at 2 MB
- No file contains real credentials (secret scrub passed)
- A manifest file `modules/M##-<slug>/assets/L-###-manifest.json` lists every asset with its checksum, size, and role (terminal recording, diagram, shot list, etc.)

The manifest makes it possible to audit "did every expected asset get produced?" mechanically. The assembly phase reads the manifest to embed assets into the article.

## Halt conditions

Halt the demo phase and flag for review if:

1. Terminal handler produces output that differs from what the lesson's `verification` field expects. Either the command is wrong, the environment differs, or the spine needs updating. Flag, do not paper over.
2. Rendered handler produces an asset larger than 5 MB even after compression. Asset is too detailed; split or simplify.
3. Script-only handler cannot produce a coherent shot list in fewer than 10 scenes for a 12-minute lesson. The lesson is too complex; flag for possible split.
4. Secret scrubber matches something unexpected (not a real credential, but matched the regex anyway). Review the scrubber output; may need regex refinement.

All halts write to `_state/pending_review.md` with lesson ID and specifics.
