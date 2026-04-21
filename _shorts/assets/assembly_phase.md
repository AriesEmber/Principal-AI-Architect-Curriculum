# Assembly phase

Commit, push, PR, and update state.

## Branch + commit

```bash
git checkout -b shorts/L-###   # off current main
git add _shorts/templates/L-###_storyboard.yaml
git add _deliverables/shorts/L-###-short.mp4
git add _state/shorts_index.md
git commit -m "L-###: vertical short for '<lesson title>'"
```

(Character sprites under `_shorts/character/` are committed separately when the mascot is chosen — not per-lesson.)

## Push + PR

```bash
git push -u origin shorts/L-###
"/c/Program Files/GitHub CLI/gh.exe" pr create \
  --title "L-###: short for <lesson title>" \
  --body "<see below>"
```

PR body template:

```
## Summary
- Vertical MP4 short for L-### ([title])
- Scroll duration: Xs, finale hold: 3.5s, total: Ys
- Lanes: [list]
- Beats: [count]

## How to review
1. Download `_deliverables/shorts/L-###-short.mp4` from the PR Files tab
2. Watch on a phone or with a phone-sized window
3. Flag any audio/visual mismatch, weird F5-TTS pronunciations, or pacing issues

## Test plan
- [ ] MP4 plays to completion with audio
- [ ] Narration timing matches on-screen beats
- [ ] No frame glitches (missing sprites, clipped bubbles)
- [ ] Watermark visible bottom-right
- [ ] Finale frame shows full sequence

🤖 Generated with the short-author skill
```

## State updates

Append one line to `_state/shorts_index.md`:

```
- L-### | M## | D## | <title> | <ISO date> | <commit SHA>
```

Append one line to `_state/production_log.jsonl`:

```json
{"run_type":"short","lesson_id":"L-###","timestamp":"<ISO>","commit":"<SHA>","duration_s":<float>,"status":"pr_open"}
```

## Don't

- Do NOT merge the PR. Elvis reviews and merges.
- Do NOT re-render an already-shipped short without an explicit ask.
- Do NOT edit the `lesson-author` skill, its phase files, or `published_index.md`.
- Do NOT publish anything to TikTok/Reels/LinkedIn/YouTube. The skill produces the MP4; Elvis uploads.
