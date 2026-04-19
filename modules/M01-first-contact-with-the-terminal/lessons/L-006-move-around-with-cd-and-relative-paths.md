---
lesson_id: L-006
sequence_number: 6
module_id: M01
domain_id: D01
title: "Move around with cd and relative paths"
week_number: 1
day_in_week: 6
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-21T00:00:00Z
acronyms_expanded: [CD, CLI, OS]
---

Picture yourself standing in the hallway of a house. Someone asks where the kitchen is and you say, "go to the kitchen." That answer works because you are both already inside the house. If the same person calls you from across town, the answer has to change. Now you have to say, "go to 123 Main Street, then to the kitchen." Same destination, different starting point, different directions. Your terminal works the same way. When you say "go to Documents," the Command-Line Interface (CLI) uses your current directory as the starting point. When you say "go to the root of the disk," you give the full address from the front door of the operating system (OS). You are about to give your terminal both kinds of directions, with a two-letter command called `cd`, short for change directory (CD).

![Side-by-side typewriter walkthrough of five cd exchanges, Bash on the left and PowerShell on the right, prompt path updating in lockstep](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-006-terminal.gif)

## What you will do

Run `cd` three times, once with a relative path (`cd Documents`), once to walk back up (`cd ..`), and once with an absolute path (`cd /` on macOS or Linux, `cd C:\` on Windows), confirming each move with `pwd`.

## Before you start

You need an open terminal from [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md), with the prompt at your home directory. Run `pwd` first and confirm it returns your home path before you move. You also need the `ls` command from [L-005: List the contents of a directory with ls](./L-005-list-the-contents-of-a-directory-with-ls.md) so you know a `Documents` folder exists to walk into. If `ls` does not show a `Documents` folder, substitute any other folder name you see in the list.

Nothing will be created, nothing will be deleted, no settings will change. `cd` rearranges where the shell is standing; it does not touch any file.

## Step by step

### 1. Confirm where you stand

Type:

```bash
pwd
```

You should see your home path, something like `/home/learner` on Linux, `/Users/learner` on macOS, or `C:\Users\learner` on Windows. This is the starting point for every path in this lesson.

### 2. Walk into a subdirectory with a relative path

Type:

```bash
cd Documents
```

The shell says nothing. That silence is normal: `cd` is quiet on success and only speaks when something goes wrong. Check that the move happened by asking `pwd` again.

```bash
pwd
```

```text
/home/learner/Documents
```

The path has grown by one segment. You did not tell `cd` where home was; the shell used where you were standing as the starting point. That is what "relative" means: relative to here.

### 3. Walk back up one level

Type:

```bash
cd ..
```

The two dots are a special entry that exists inside every directory on every mainstream OS. You saw `..` yourself when you ran `ls -la` in the previous lesson. It points at the directory's parent. Use `pwd` to confirm the walk.

```bash
pwd
```

```text
/home/learner
```

You are back where you started. `..` is still a relative path; it just happens to always point at one specific place.

### 4. Jump to an absolute location

Type, on macOS or Linux:

```bash
cd /
```

Or on Windows PowerShell:

```powershell
cd C:\
```

The leading slash (or the drive letter) is the signal that flips the shell from "starting here" to "starting at the root of the filesystem." Check it:

```bash
pwd
```

```text
/
```

You have jumped all the way to the top of the disk. Nothing about where you were before matters; an absolute path names the destination from the front door.

### 5. Return home

Type:

```bash
cd ~
```

The tilde is shorthand that every modern shell expands to your home directory. You can also type `cd` with no argument at all and land in the same place.

```bash
pwd
```

```text
/home/learner
```

You are home again, having walked there with an absolute path. That is five moves, three flavors of path, one command.

![Side-by-side static panel of the five cd exchanges in Bash (left) and PowerShell (right)](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-006-terminal.png)

## Check it worked

After each `cd`, `pwd` should report a new path. If `pwd` does not change, the `cd` silently failed, which usually means a typo in the folder name. The shell is case-sensitive on macOS and Linux: `cd documents` is not the same as `cd Documents`. On Windows it is case-insensitive, so both will work there.

If you see `cd: no such file or directory: Documents`, the folder you named does not exist in the current directory. Run `ls` first, pick a name you actually see in the list, and try again.

If you get stuck in an unfamiliar directory, type `cd` with no argument and press enter. The shell puts you back in your home directory no matter where you were. That is the emergency brake for this lesson.

## What just happened

A path is the name of a location on the disk. Every path is interpreted one of two ways:

- **Relative.** Starts without a leading slash, like `Documents` or `..`. The shell uses your current working directory (the one `pwd` returns) as the starting point and walks from there.
- **Absolute.** Starts with `/` on macOS and Linux, or with a drive letter like `C:\` on Windows. The shell ignores where you are standing and walks from the filesystem root.

`cd` is the verb that takes a path, of either kind, and changes the shell's current working directory to match. That change is why the prompt in the animation above shifts from `~` to `~/Documents` to `/` and back: the prompt is showing you the new `pwd` after each successful move, which is how most shells are configured out of the box.

There is one more piece to notice. The special names `.` (this directory), `..` (parent directory), and `~` (home directory) are the three shortcuts every professional relies on in daily work. `.` matters less for `cd` (running `cd .` does nothing useful) but shows up constantly with other commands. `..` is the way you walk up. `~` is the way you go home from anywhere. Memorize those three and most of the shell's movement vocabulary is already in your hands.

## Going further

The shell remembers the directory you were in before the most recent `cd`. You can jump back to it with `cd -`.

```bash
cd Documents
cd -
```

```text
/home/learner
```

The shell prints the destination, which is a quiet confirmation that the jump worked. This is how experienced users bounce between two working directories without retyping their full paths. `cd -` is supported on bash, zsh, and PowerShell version 6 or later. If you are on an older Windows PowerShell, it will not recognize the dash; just type the full path instead.

## What's next

Next is [L-007: Make and remove directories (capstone)](./L-007-make-and-remove-directories-capstone.md). Now that you can stand somewhere (`pwd`), look around (`ls`), and walk (`cd`), you have every skill you need to build your first folder of your own.
