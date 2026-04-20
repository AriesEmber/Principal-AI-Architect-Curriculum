---
lesson_id: L-009
sequence_number: 9
module_id: M02
domain_id: D01
title: "Edit a file with nano"
week_number: 2
day_in_week: 2
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-19T00:00:00Z
primary_shell: powershell
acronyms_expanded: [CLI, OS, REPL, TUI, WSL]
---

Picture a typewriter with a help menu along the bottom edge. Every shortcut it understands is printed right there on the carriage: hit this key to insert a page, that key to underline, a third key to eject the page. You do not have to remember the shortcuts. You only have to read them. A terminal text editor called nano works the same way. Today you open a file in nano, type three lines, save with `Ctrl+O`, exit with `Ctrl+X`, and read the file back to confirm it stuck. By the end you will have edited a text file from the Command-Line Interface (CLI) for the first time.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Five exchanges: launch nano on hello.txt, type three lines, save with Ctrl+O, confirm with Enter and exit with Ctrl+X, read back with cat](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-009-terminal.gif)

## What you will do

Open nano on a new file named `hello.txt`, type three lines, save with `Ctrl+O` then `Enter`, exit with `Ctrl+X`, and verify with `cat hello.txt`.

## Before you start

You need a terminal at your home directory, the way [L-008: Read a file's contents with cat and less](./L-008-read-a-files-contents-with-cat-and-less.md) left you. Run `pwd` and confirm you are at your home path (`C:\Users\<yourname>` on Windows PowerShell, `/Users/<yourname>` on macOS, `/home/<yourname>` on Linux or the Windows Subsystem for Linux (WSL)).

Nano ships with the operating system (OS) on macOS and almost every Linux distribution, so if you are in Bash or Zsh there is nothing to install. PowerShell on Windows 11 does not include nano. A one-time install puts it on your PATH:

```powershell
winget install GNU.Nano
```

`winget` is the package manager built into Windows 11. The first time you run it, Windows will ask you to accept the source agreement; type `Y` and press `Enter`. The install takes under a minute. You only run this once. After that, `nano` works from every new PowerShell window you open.

If you are on Windows 10 or on a machine without `winget`, two good alternatives are the portable binary from [nano-editor.org](https://www.nano-editor.org/) or the nano bundled with [Git for Windows](https://gitforwindows.org/), both of which run from a PowerShell or Git Bash prompt.

Today you only need to remember two keystrokes: `Ctrl+O` to save and `Ctrl+X` to exit. Nano prints both of them at the bottom of the screen, so you do not actually have to remember anything.

## Step by step

PowerShell commands are shown first because PowerShell is the default shell on Windows 11 and the primary shell of this curriculum. The Bash and Zsh equivalent follows each PowerShell block for readers on macOS, Linux, or WSL.

### 1. Open nano with a new file

```powershell
nano hello.txt
```

```bash
nano hello.txt
```

The command is the same in both shells. Nano clears the terminal and paints its own screen. The top strip reads:

```text
 GNU nano 7.2      hello.txt                          [ New File ]
```

The title bar tells you which version of GNU nano is running, which file is open, and whether the file is new. The bottom strip lists the shortcuts:

```text
 ^O Write Out   ^X Exit   ^W Where Is   ^G Help
```

The caret symbol (`^`) means hold `Ctrl` and press the key that follows it. `^O` is `Ctrl+O`. `^X` is `Ctrl+X`.

### 2. Type three lines

Type these three lines into the buffer, pressing `Enter` between each line:

```text
hello from nano
this is line two
good night
```

As soon as you type the first character, the top strip changes from `[ New File ]` to `Modified`. That word is nano's way of saying the on-disk file no longer matches what is in the editor. Your work exists only in memory until you save.

### 3. Save the file with Ctrl+O

Press `Ctrl+O`. The bottom of the screen changes to show:

```text
 File Name to Write: hello.txt
```

Nano is asking which filename to write to. It already proposed `hello.txt` because that is what you passed on the command line.

### 4. Confirm with Enter, then exit with Ctrl+X

Press `Enter` to accept the filename. Nano writes the buffer to disk and shows a short confirmation:

```text
 [ Wrote 3 lines ]
```

Now press `Ctrl+X`. Nano closes and hands control back to the shell. The PowerShell or Bash prompt returns.

### 5. Verify with cat

Read the file back to confirm it saved correctly.

```powershell
cat hello.txt
```

```bash
cat hello.txt
```

```text
hello from nano
this is line two
good night
```

Three lines, in the order you typed them. The save worked.

![Side-by-side static panel of the 5 exchanges: launch nano, type three lines, save with Ctrl+O, confirm with Enter and exit with Ctrl+X, verify with cat](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-009-terminal.png)

## Check it worked

`cat hello.txt` should print exactly the three lines you typed. If nothing prints, the file did not save; repeat steps 3 and 4.

If you pressed `Ctrl+X` before `Ctrl+O`, nano noticed the buffer was modified and asked `Save modified buffer?`. Type `Y` then `Enter`, and nano will ask for the filename (same as `Ctrl+O`). Type `Y` and `Enter` again and nano exits cleanly, with the file on disk.

If the filename prompt shows a path you did not expect, press `Ctrl+C` to cancel the save, then press `Ctrl+O` again and retype `hello.txt`.

If `nano hello.txt` returns `nano: command not found` on PowerShell, the `winget install GNU.Nano` step did not run or did not finish. Close and reopen PowerShell (so it picks up the new PATH), run `nano --version` to confirm, and try again.

## What just happened

Nano is a full-screen text editor that runs inside the terminal. Unlike `cat` (which dumps a file to stdout) or `less` (which pages through a file), nano draws its own text user interface (TUI) on top of the terminal window: the title strip at the top, the editing area in the middle, and the help strip at the bottom.

The help strip is why nano exists. Every other long-running Unix editor (vi, vim, emacs) expects you to learn its shortcuts before you can use it; nano prints the shortcuts on the screen. That single design choice is the reason nano is the default editor most Linux distributions put in front of a first-time user when they run `visudo`, `crontab -e`, or any other command that drops them into an editor.

Two rules carry forward from this lesson. First, the caret notation (`^O` for `Ctrl+O`) is standard across Unix terminal tools, so when you see `^C` or `^D` in a future lesson, you already know they mean `Ctrl+C` and `Ctrl+D`. Second, any tool that drops you into a full-screen interface keeps the terminal until you intentionally exit. Pagers use `q`, nano uses `Ctrl+X`, a Python Read-Eval-Print Loop (REPL) uses `exit()`. Each tool has its own exit verb. Learning them is part of the price of admission.

## Going further

`Ctrl+W` is nano's "Where Is" (search) shortcut. Open a longer file and try it.

```bash
nano /etc/services
```

```powershell
nano $Env:SystemRoot\System32\drivers\etc\services
```

On Bash, `/etc/services` is the text file the OS uses to look up standard network ports. On Windows, `$Env:SystemRoot` is the environment variable that holds the Windows install path (usually `C:\Windows`), and Windows ships a very similar services file.

Inside nano, press `Ctrl+W`. Nano prompts `Search:`. Type `http` and press `Enter`. Nano jumps to the first line that contains `http`. Press `Alt+W` (or `Meta+W` on macOS) to jump to the next match. Press `Ctrl+X` to exit when you have seen enough.

## What's next

Next is [L-010: Understand file paths, extensions, and hidden files](./L-010-understand-file-paths-extensions-and-hidden-files.md). You now know how to read a file two ways and how to edit one; the next lesson names the rules that govern the paths those files live at.
