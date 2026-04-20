---
lesson_id: L-008
sequence_number: 8
module_id: M02
domain_id: D01
title: "Read a file's contents with cat and less"
week_number: 2
day_in_week: 1
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-19T00:00:00Z
primary_shell: powershell
acronyms_expanded: [CLI, DOS, HTTP, OS, UI, UTF-16, WSL]
---

Picture a letter arriving in your mailbox. You can unfold the whole thing at once and read it in a glance. You can also hold it at the top, read a page, slide it down, read the next page, and stop whenever you like. A text file works the same way. Today you learn the two verbs for each style of reading: `cat` dumps the whole letter onto your terminal in one move, and a pager (`less` on macOS and Linux, `more` on Windows) hands you one screen at a time. You will build a short file, dump it with `cat`, build a longer file, open the pager, press `q` to quit, and clean up.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: write notes.txt, dump with cat, build notes-long.txt, open with more or less, quit with q, clean up](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-008-terminal.gif)

## What you will do

Create a three-line text file, read it with `cat`, create a thirty-line file, open it in a pager, quit the pager with `q`, then delete both files.

## Before you start

You need a terminal open at your home directory, the way [L-007: Make and remove directories (capstone)](../../M01-first-contact-with-the-terminal/lessons/L-007-make-and-remove-directories-capstone.md) left you. On Windows 11 that is PowerShell showing `C:\Users\<yourname>`. On macOS or Linux or the Windows Subsystem for Linux (WSL) that is a Bash or Zsh shell showing your home path (`/Users/<yourname>` or `/home/<yourname>`). Run `pwd` once and confirm you are home before starting.

You also need the pager your operating system (OS) ships by default. Windows 11 includes `more.com` out of the box; every PowerShell install can call it as `more`. macOS and Linux include `less`. If you are on Windows PowerShell and want `less` as well, you can get it from [Git for Windows](https://gitforwindows.org/) or from a WSL distribution, but this lesson uses the pager your OS already has.

## Step by step

Every step shows PowerShell first, because PowerShell is the default shell on Windows 11 and the primary shell of this curriculum. The Bash and Zsh equivalent follows each PowerShell block for readers on macOS, Linux, or WSL.

### 1. Write a three-line text file

```powershell
"one","two","three" > notes.txt
```

PowerShell evaluates the expression on the left side of `>` as an array of three strings. The `>` operator sends the array to `Out-File`, which writes one element per line. The result is a file named `notes.txt` with three lines of text in your current directory.

Bash equivalent:

```bash
printf "one\ntwo\nthree\n" > notes.txt
```

Bash's `printf` prints its first argument, interpreting `\n` as a line break, and the `>` sends the output to `notes.txt` instead of the screen. Same three-line file, different path through the shell.

### 2. Read the file with cat

```powershell
cat notes.txt
```

```text
one
two
three
```

On PowerShell, `cat` is an alias for `Get-Content`, which reads the file and writes each line to the screen. On Bash the same command works because `cat` is a separate program; the name is short for "concatenate," because the original Unix `cat` was built to join several files end to end. With one file argument, both forms do the same thing: dump every line to the terminal.

Bash equivalent:

```bash
cat notes.txt
```

The output is identical. Three lines on the screen, then the prompt returns, ready for your next command.

### 3. Build a longer file

A three-line file fits on one screen, so `cat` is the right verb for it. Real files are often thousands of lines long. To see why pagers exist, build a file that is bigger than your terminal window.

```powershell
1..30 > notes-long.txt
```

`1..30` is PowerShell's range operator. It produces the integers from 1 to 30, one per line, and `>` redirects that output to a new file.

Bash equivalent:

```bash
seq 1 30 > notes-long.txt
```

The `seq` program prints integers in a range, one per line. Same thirty-line file.

### 4. Open the file in a pager

```powershell
more notes-long.txt
```

The terminal fills with the first screen of numbers and shows `-- More --` at the bottom. That strip is `more.com` telling you it is holding the rest of the file and waiting for a keystroke. Press the spacebar to advance one screen, or the enter key to advance one line.

Bash equivalent:

```bash
less notes-long.txt
```

On Bash, `less` does the same job with a different user interface (UI). You see the first screen of numbers and a single colon (`:`) at the bottom. That colon is the `less` command prompt. Space advances a screen, `b` goes back a screen, arrow keys move one line at a time.

### 5. Quit the pager

```text
q
```

Press the `q` key. No enter needed. The pager exits, the shell prompt returns, and you are back where you started. Both `more` and `less` use `q` for quit. Muscle-memory `q` is the single most-used pager keystroke in professional Command-Line Interface (CLI) work, because every log viewer, man-page reader, and help-text tool in the Unix lineage uses the same convention.

### 6. Clean up

```powershell
Remove-Item notes.txt, notes-long.txt
```

The comma between the two paths is PowerShell's array syntax. `Remove-Item` accepts an array and deletes each file.

Bash equivalent:

```bash
rm notes.txt notes-long.txt
```

A space-separated list of paths is how Bash passes multiple arguments to `rm`. Same result: both files are gone.

![Side-by-side static panel of the 6 exchanges in PowerShell (left) and Bash (right), with the pager row showing the -- More -- marker (PowerShell) and the colon prompt (Bash)](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-008-terminal.png)

## Check it worked

Run `ls`. Neither `notes.txt` nor `notes-long.txt` should appear. If one is still there, the step 6 cleanup did not run; re-run it.

If `cat notes.txt` on step 2 printed something other than `one`, `two`, `three`, the step 1 write did not land as expected. The most common cause on PowerShell is an encoding mismatch: `>` on older PowerShell versions writes 16-bit Unicode Transformation Format (UTF-16) with a byte-order mark. If you see strange characters, use `Set-Content notes.txt "one`ntwo`nthree"` instead.

If step 4 dumped all thirty numbers at once and never showed the `-- More --` or `:` prompt, your terminal window is tall enough to show the whole file. Resize the terminal shorter and retry, or jump to the extension and use the pager on a longer system file.

## What just happened

Two verbs, two styles of reading. `cat` dumps every byte of a file to the screen and returns control immediately. It is the right choice when the file fits in one glance, or when you want to pipe the contents into another command. A pager shows one screen at a time and holds control until you let it go. It is the right choice when the file is bigger than the screen, when you want to search inside it (`/pattern` works in both `less` and `more`), or when you want to read deliberately.

PowerShell and Bash both recognise `cat` because PowerShell ships a handful of Unix-style aliases (`cat`, `ls`, `cp`, `mv`, `rm`, `pwd`) on top of its own longer cmdlet names (`Get-Content`, `Get-ChildItem`, and so on). Pagers were less lucky: `less` never shipped with Windows, and `more.com` has lived in Windows since the Disk Operating System (DOS) days with a much simpler UI. If you need the full `less` feature set on Windows, install it through WSL or Git for Windows.

The other rule in this lesson is about where control lives. `cat` gives control back right away. `more` and `less` keep control until you press `q`. Any command that drops you into a sub-interface (a pager, a text editor, an interactive Python session) works the same way: it holds the terminal until you intentionally exit. The keystroke varies (`q` for pagers, `Ctrl-X` for nano, `exit` for shells), and learning each tool's exit verb is part of the price of admission.

## Going further

Both `more` and `less` really shine on files much bigger than your screen. Linux and macOS ship a file called `/etc/services` that lists every standard networking service and port, usually around six hundred lines long.

```bash
less /etc/services
```

Press space to page forward. Type `/http` to search for Hypertext Transfer Protocol (HTTP) entries (forward slash followed by a pattern is the `less` search syntax). Press `q` to quit.

Windows ships an equivalent file. From PowerShell:

```powershell
more $Env:SystemRoot\System32\drivers\etc\services
```

`$Env:SystemRoot` is the environment variable that points at the Windows install directory, usually `C:\Windows`. `more` paginates through the file the same way.

## What's next

Next is [L-009: Edit a file with nano](./L-009-edit-a-file-with-nano.md). You now know how to read a file two ways; the next lesson is how to change what is inside one, using the simplest terminal editor in wide use.
