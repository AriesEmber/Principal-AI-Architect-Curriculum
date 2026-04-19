---
lesson_id: L-004
sequence_number: 4
module_id: M01
domain_id: D01
title: "Find out where you are with pwd"
week_number: 1
day_in_week: 4
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-20T00:00:00Z
acronyms_expanded: [CLI, OS]
---

Every shopping mall has a floor map with a red dot on it and the words "You Are Here." The dot is useless on its own. What it gives you is the one piece of information you need to plan any route at all: where you stand before you move. Your terminal has the same dot. It is a four-letter command called `pwd`, short for print working directory, and it is the first thing a Command-Line Interface (CLI) learner reaches for when they are not sure where they are. You are about to ask it for the dot.

![Animated typewriter walkthrough of four pwd exchanges in a fresh terminal](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-004-terminal.gif)

## What you will do

Type `pwd`, press Enter, and read back the absolute path of the folder your terminal is currently standing in.

## Before you start

You need an open terminal window from [L-003: Print your first line with echo](./L-003-print-your-first-line-with-echo.md), sitting at its default prompt. If you closed it, open a new one. Nothing else is required. No files will be created, nothing will be downloaded, no settings will change. `pwd` is a read-only question: it reads the shell's current state and prints the answer.

If your prompt ends in `$` (Bash on Linux, Windows Subsystem for Linux), `%` (Zsh on macOS), or `>` (PowerShell on Windows), you are in the right place. Every command below works identically on all three.

## Step by step

Each step is one line typed at the prompt, followed by pressing Enter. You do not need to type the prompt itself; only the characters after it.

### 1. Ask where you are

Type:

```bash
pwd
```

You will see a single line of text, starting with `/` on macOS or Linux, or with `C:\` on Windows PowerShell. For example, on a freshly opened terminal on a Linux or macOS laptop:

```text
/home/learner
```

On a Mac:

```text
/Users/learner
```

On PowerShell:

```text
C:\Users\learner
```

The prompt returns on the line below, ready for the next command.

### 2. Read the path character by character

Look at what came back. It is not random. It is a route from the root of the filesystem (the `/` on Linux and macOS, or the drive letter `C:\` on Windows) through each nested folder, separated by `/` or `\`, down to the folder your terminal is standing in.

Three pieces are worth noticing:

- **The leading separator.** `/` says "start at the root of the filesystem." `C:\` says "start at the root of the C drive." Both are absolute: they do not depend on where you are.
- **The segments.** Each folder name between separators is one step further in.
- **The final segment.** The last name is the folder you are actually in. On a fresh terminal, that is almost always your own username.

### 3. Write the path down

Copy the line somewhere you can read it later: a sticky note, a text file, the top of a notes document. You will refer back to the home path in the next three lessons.

### 4. Ask a second time in a new window

Open a second terminal window (the same shortcut you used in L-001). Run `pwd` again in it:

```bash
pwd
```

You will see the same line as the first window. Every fresh terminal starts in the home directory on every major Operating System (OS). Opening a new window is not the same as moving somewhere new.

### 5. Optional: see the logical and physical paths

On macOS and Linux, `pwd` takes two flags worth knowing about:

```bash
pwd -L
pwd -P
```

`-L` is the default and prints the logical path (the route the shell thinks you took). `-P` prints the physical path (the real location on disk, with any shortcut links resolved). In a plain home directory they return the same thing. They start to differ once you work inside a repository that was mounted through a symbolic link, which will happen later in the curriculum.

On Windows PowerShell, `pwd` is not a separate program. It is an alias for `Get-Location`. You can confirm that with:

```powershell
Get-Command pwd
```

The output names `pwd` as an alias and `Get-Location` as the real command. The answer it gives is identical.

![Static panel showing four pwd exchanges and the PowerShell alias check](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-004-terminal.png)

## Check it worked

After step 1, a single line should print on the row directly under your command, starting with `/` on macOS or Linux, or with `C:\` on Windows. The prompt should return on the line after that. If that happened, the lesson has already done its job.

If you saw `command not found: pwd` or `'pwd' is not recognized`, you typed it wrong. It is four letters: p, w, d, in that order. Retype and press Enter again.

If the output is blank, or you see an error mentioning "no such file or directory" before you have run any other command, the folder your terminal started in was deleted or unmounted from under it (rare on a fresh terminal). Close the window and open a new one; it will start in your home directory with no trouble.

## What just happened

Every running program on your computer has a current working directory attached to it. It is the filesystem location the program treats as its starting point for every file it opens or command it runs. When you open a terminal, the shell, the program that is reading your keystrokes, inherits a working directory from whatever started it. For a freshly opened terminal, that is your home directory on every mainstream operating system.

`pwd` prints that value and nothing else. There is no lookup, no guess, no calculation. The shell knows the answer already; `pwd` just asks for it and reads it back.

Knowing the working directory matters because every other command you run treats it as the default starting point. Listing files (`ls`), changing directory (`cd ..`), editing a file by a short name like `notes.txt`, running a script written as `./build.sh`, all of these resolve their names against the working directory. If you do not know where you are, you do not know what those short names actually point at. `pwd` is the safety check before anything else.

The answer is always an absolute path, a route from the root of the filesystem to where you stand. Absolute paths never depend on context. That is why `pwd` is the first command any shell hands you, and it is why every troubleshooting guide on the internet eventually asks for its output.

## Going further

Open a third terminal window and before running any other command, run `pwd`. Confirm that the path is the same as the first two. That consistency is a real property of the shell, not a coincidence: the operating system chooses the home directory as the default starting place for any new interactive shell.

Then, on Linux or macOS only, run:

```bash
pwd -P
```

In a plain home directory, the output is identical to plain `pwd`. Later, when you clone a Git repository into a folder that is actually a symbolic link to storage somewhere else, `pwd -P` will show the real storage path while plain `pwd` shows the friendlier link path. Both answers are correct; they are just answering slightly different questions.

On PowerShell, run:

```powershell
$PWD | Get-Member
```

`$PWD` is the object PowerShell uses under the hood for the current location. `Get-Member` lists every property and method it carries. You do not need to understand the list yet; it is a reference point for later lessons on PowerShell objects.

## What's next

Next is [L-005: List the contents of a directory with ls](./L-005-list-the-contents-of-a-directory-with-ls.md). Now that you know where you stand, you are ready to look around.
