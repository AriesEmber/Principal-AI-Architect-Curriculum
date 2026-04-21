# Script template — "Day X of Learning Y"

Every short narration follows this shape. Copy it, fill it in, keep the opening and closing beats pattern intact.

## Template

```
[BEAT 1 — open]
"Day <N> of learning <learning_title>. <One-sentence task statement>. <One-sentence reason it matters>."

[BEAT 2..N-1 — content, one per command / action / decision]
"<Plain description of what you are doing right now>. <What the system is doing on your behalf, if visible>."

[BEAT N — landing]
"<Confirmation: 'You are now <in/with/able to> X'>. <Handoff to the next lesson, if one exists>."
```

## Worked example — L-001

```
Beat 1 (open, lane: Desktop):
"Day one of learning the command line. Your first task — open the terminal. Every command in this course will live inside that window."

Beat 2 (self on Desktop, label: "press shortcut"):
"Start at your desktop. Press the shortcut on your keyboard. Command plus Space on Mac, the Windows key on Windows, Super on Linux."

Beat 3 (call Desktop → OS Search, label: "open search"):
"A small search panel appears on top of everything else."

Beat 4 (self on OS Search, label: "type: terminal"):
"Type the word: terminal. The top result is the built-in app."

Beat 5 (call OS Search → Terminal, label: "press enter"):
"Press enter, and your operating system launches it for you."

Beat 6 (return Terminal → Desktop, label: "window opens"):
"A new window appears. Blinking cursor. That is your workshop from here on."
```

## Words to avoid / rephrase

F5-TTS reads these slightly wrong at default settings:

| Avoid | Prefer |
|---|---|
| `CLI` (said as "klee") | "the command line" |
| `ls` | "L S" or "list" |
| `cd` | "C D" or "change directory" |
| `nano` (confusing for non-techies) | "a text editor" or the literal "the nano editor" |
| `~` (tilde) | "your home folder" |
| `$PATH` | "the PATH variable" |
| Long URLs | summarize ("the project's docs site") |

## Per-module `learning_title` values

- **M01** (first contact with the terminal): `"the command line"`
- **M02** (files, editors, package managers): `"files and editors"`
- (add as modules publish — one `learning_title` per module)
