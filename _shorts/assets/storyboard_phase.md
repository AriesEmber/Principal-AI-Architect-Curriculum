# Storyboard phase

Convert the beat list into a storyboard YAML file. Save it at
`_shorts/templates/L-###_storyboard.yaml`.

## Schema (see `_shorts/renderer/storyboard.py` for the source of truth)

```yaml
lesson_id: L-001           # exact id, matches published_index.md
day_number: 1              # the "Day N" in the narration
learning_title: "the command line"   # the phrase after "Day N of learning ..."
lesson_title: "Open the terminal"    # appears in the finale frame header
hook_text: "..."           # optional; currently unused by renderer
finale_hold: 3.5           # seconds the finale frame stays on screen

lanes:                     # top-to-bottom order on screen; 2-5 entries
  - "Desktop"
  - "OS Search"
  - "Terminal"

beats:
  - kind: open              # one of: open | self | call | return | finale
    to_lane: "Desktop"      # home lane (only used for `open`)
    narration: "Day one ..."
    min_duration: 2.0       # seconds; overridden by audio length if longer

  - kind: self
    from_lane: "Desktop"
    label: "press shortcut"  # short label shown in the bubble (<=16 chars)
    narration: "..."
    min_duration: 2.0

  - kind: call
    from_lane: "Desktop"
    to_lane: "OS Search"
    label: "open search"
    narration: "..."
    min_duration: 1.6

  - kind: return
    from_lane: "Terminal"
    to_lane: "Desktop"
    label: "window opens"
    narration: "..."
    min_duration: 1.8
```

## Rules

- **Lanes are ordered top-to-bottom.** Put the user-adjacent system first (usually `Desktop` or `Shell`).
- **First beat is `open`**, with `to_lane` set to the home lane.
- **No `finale` beat needed.** The renderer appends a finale frame automatically at the end.
- **`min_duration` is the floor.** The actual duration is `max(min_duration, audio_duration + 0.25s)` — the audio determines pacing.
- **Labels go on arrows and self-bubbles.** Keep them ≤ 16 characters.
- **Lane names used in beats must exactly match entries in the `lanes:` list.** The renderer does NOT lenient-match.

## Commit this file

After writing the YAML, commit it on the `shorts/L-###` branch (see assembly phase). Future runs reuse the storyboard — editing narration is editing this file.
