# Script phase

Draft the narration that F5-TTS will speak over the short. This is not the GitHub article — it is a spoken script with a fixed opening and closing shape.

## Fixed shape

Every short's narration follows this template:

```
Beat 1 (open): "Day N of learning [learning_title]. [The one-sentence task.] [The one-sentence why.]"
Beat 2..N-1 (content beats): conversational, one beat = one action
Beat N (landing): "[Confirmation — what the user now has.] [Lead-in to the next lesson, if any.]"
```

- `N` is the lesson's `day_number` (see storyboard YAML — one short = one day; for lessons in week 1 day 1, `day_number: 1`; day 2, `day_number: 2`; etc.)
- `learning_title` is the theme for the week/module (for M01 all day-1 lessons, use `"the command line"`; for M02, `"files and editors"`; etc.)

## Writing rules

- **Ear-readable, not eye-readable.** Contractions are fine. Avoid words that F5-TTS stumbles on (numeric codes, long acronyms, non-English proper nouns). Spell out `CLI` as "C L I" only if needed; most of the time, just say "the command line."
- **One idea per beat.** If a beat's narration has two "ands", split the beat.
- **No metaphor exposition.** Don't say "think of the robot as…" — the visual teaches that. Describe what the *human* does and what the *system* does.
- **End with a handoff.** The last beat should feel like a door opening to the next lesson.
- **25–30 words per beat max.** F5-TTS at default speed = ~2.8 words/sec. A 25-word beat = ~9 seconds of audio.

## Tone check

Read the draft out loud. If it reads like a slide deck, tighten. If it reads like a friend explaining something over coffee, you're good.

## What to hand to the next phase

A Python list-of-dicts in memory (not a file yet), one entry per beat:

```python
[
  {"kind": "open", "to_lane": "Desktop", "narration": "..."},
  {"kind": "self", "from_lane": "Desktop", "label": "press shortcut", "narration": "..."},
  {"kind": "call", "from_lane": "Desktop", "to_lane": "OS Search", "label": "open search", "narration": "..."},
  ...
]
```

`label` is the short string that appears ON the arrow / bubble in the video. Keep labels under 16 characters. They are visible for the duration of the beat.
