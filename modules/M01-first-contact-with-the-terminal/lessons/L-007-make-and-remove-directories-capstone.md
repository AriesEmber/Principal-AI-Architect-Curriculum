---
lesson_id: L-007
sequence_number: 7
module_id: M01
domain_id: D01
title: "Make and remove directories (capstone)"
week_number: 1
day_in_week: 7
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: true
published_at: 2026-04-19T00:00:00Z
revision: 3
revises: L-007-v2
revision_reason: "PowerShell primary (left); v2 led with bash and omitted the cannot-delete-cwd rule"
primary_shell: powershell
acronyms_expanded: [CD, CLI, CWD, OS]
---

Picture setting up a new filing cabinet for a new project. You slide a fresh cabinet into place, pull the top drawer open, confirm the drawer is empty, and drop a single note inside. Later, when the project is over, you try to shred the cabinet while you are still standing inside it. The shredder refuses. You step out, try again, and the cabinet is gone. Six days of this curriculum have been about knowing where you stand and how to move. Today is the first day you create something of your own, hit the one rule the shell has about destruction, and learn the two-keystroke recovery.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough of the capstone. Steps 1-6 build the directory and drop a file; step 7 shows the failed delete from inside the folder; step 8 is cd .. as the fix; steps 9 and 10 remove the tree and confirm it is gone](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.gif)

## What you will do

Make a new directory called `practice-cli` in your home folder, walk into it, drop a blank text file inside, try to delete the directory from inside (this will fail on purpose), step back out with `cd ..`, and delete the directory.

## Before you start

You need Windows 11 with PowerShell open, or macOS or Linux with a Bash or Zsh terminal open. Four prior lessons give you everything else. [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md) taught you how to confirm you are at home. [L-005: List the contents of a directory with ls](./L-005-list-the-contents-of-a-directory-with-ls.md) taught you how to look around. [L-006: Move around with cd and relative paths](./L-006-move-around-with-cd-and-relative-paths.md) taught you how to walk into a folder and back out. This lesson adds the last two verbs you need to do real work, and the one rule of the Command-Line Interface (CLI) that trips every new learner at least once.

Before the first command, run `pwd` once and confirm it reports your home directory. On Windows PowerShell that looks like `C:\Users\<yourname>`. On macOS it looks like `/Users/<yourname>`. On Linux it looks like `/home/<yourname>`. If you are anywhere else, run `cd` (Bash) or `cd ~` (PowerShell) to return home. The whole lesson assumes home as the starting point.

## Step by step

The PowerShell command is shown first in every step because PowerShell is the default shell on Windows 11. The Bash/Zsh equivalent follows each PowerShell block for readers on macOS, Linux, or the Windows Subsystem for Linux (WSL).

### 1. Confirm where you stand

```powershell
pwd
```

```text
Path
----
C:\Users\learner
```

Bash/Zsh equivalent:

```bash
pwd
```

```text
/home/learner
```

The exact path depends on your account name and your operating system (OS). Any home-directory path is the correct starting line.

### 2. Make a new directory

```powershell
mkdir practice-cli
```

PowerShell's `mkdir` is an alias for `New-Item -ItemType Directory`. It prints a confirmation line showing the mode, the last-write time, and the new directory's name.

Bash/Zsh equivalent:

```bash
mkdir practice-cli
```

Bash's `mkdir` is a separate program, not an alias, and it is silent on success. The name after `mkdir` is the folder you are creating, and because the name has no leading slash the shell creates it inside the current directory.

### 3. Confirm the directory exists

```powershell
ls
```

Your listing should include `practice-cli` among whatever folders your home directory already had. On PowerShell, `ls` is an alias for `Get-ChildItem`; on Bash it is a separate program. Both produce the same answer here.

### 4. Walk into the new directory

```powershell
cd practice-cli
```

The prompt path changes from `C:\Users\learner` to `C:\Users\learner\practice-cli`. That is the shell showing you the change-directory (CD) move worked. On Bash the prompt path segment changes from `~` to `~/practice-cli`.

### 5. Create an empty file

This is the one step where PowerShell and Bash use different verbs.

```powershell
ni hello.txt
```

`ni` is PowerShell's alias for `New-Item`. Typed out, the full form is `New-Item hello.txt` or `New-Item -ItemType File hello.txt`. PowerShell prints a confirmation row showing the mode, the last-write time, the file size (zero bytes), and the file name.

Bash/Zsh equivalent:

```bash
touch hello.txt
```

`touch` was originally designed to update a file's last-modified timestamp. Its side effect is that if the file does not exist, `touch` creates it, empty. PowerShell does not ship a `touch` command. If you type `touch hello.txt` on Windows PowerShell you will get `The term 'touch' is not recognized`, which is the first gotcha Windows learners hit when they follow along with a Bash-only tutorial.

### 6. Confirm the file exists

```powershell
ls
```

```text
hello.txt
```

One file, zero bytes, ready to edit later. This is the state of every real project folder you will ever make: a directory with some number of files inside it. You just built the minimum version.

### 7. Try to remove the directory from inside (this fails)

Do not skip this step. The error you are about to trigger is the single most common "why doesn't this work?" moment in the first month of using a terminal, and seeing it once removes the mystery forever.

You are currently standing inside `practice-cli`. Run this anyway:

```powershell
Remove-Item -Recurse practice-cli
```

PowerShell responds with a long red error that ends with:

```text
Remove-Item : Cannot find path 'C:\Users\learner\practice-cli\practice-cli' because it does not exist.
```

Bash/Zsh equivalent (same failure, different wording):

```bash
rm -r practice-cli
```

```text
rm: cannot remove 'practice-cli': No such file or directory
```

Read the error on the PowerShell side one more time. The path the shell tried to delete was `C:\Users\learner\practice-cli\practice-cli`. That is `practice-cli` *inside* `practice-cli`. The shell did exactly what you told it to, which was "find a folder named `practice-cli` starting from the current working directory (CWD) and delete it." Your current working directory was already `practice-cli`, so the shell appended the name you passed and looked one level deeper. Nothing was there, so it reported a path-not-found error.

The rule this step teaches: **you cannot remove the directory you are currently standing in by its name.** The shell resolves a bare name like `practice-cli` against the current directory, and the current directory is already `practice-cli`. Every shell on every operating system enforces this rule the same way. It is not a Windows quirk, not a PowerShell quirk, and not a permissions issue.

### 8. Step out of the directory

The fix is one command, the same on every shell:

```powershell
cd ..
```

```bash
cd ..
```

Now your current working directory is back to home. The name `practice-cli` now resolves to `C:\Users\learner\practice-cli` (or `/home/learner/practice-cli`), which is a real folder.

### 9. Remove the directory and its contents

```powershell
Remove-Item -Recurse practice-cli
```

`Remove-Item` is the PowerShell cmdlet for deletion, and `-Recurse` tells it to walk into every sub-directory and remove every file on the way down before removing the top-level directory itself. Silent on success.

Bash/Zsh equivalent:

```bash
rm -r practice-cli
```

`rm` means remove, and the `-r` flag means recursive. Same behavior, shorter name.

There is one piece of both commands worth reading twice: neither moves files to a recycle bin. They delete them. On macOS and Linux the deletion is permanent unless your filesystem has snapshot support. On Windows PowerShell with a standard NTFS filesystem the deletion is also permanent; the Recycle Bin only receives files that you delete through the graphical shell (File Explorer), not through PowerShell. Type the target carefully, and never run `Remove-Item -Recurse` or `rm -r` against a path you did not just create yourself in this lesson.

### 10. Confirm the directory is gone

```powershell
ls
```

`practice-cli` is gone. The cabinet has been shredded, after you stepped out of it. That is all six week-one commands, plus the one rule about the current working directory, strung together in one flow.

![Side-by-side static panel of the ten capstone exchanges in PowerShell (left, primary) and Bash (right, alternate), with the failed step 7 shown in red](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.png)

## Check it worked

At the end of the sequence, `ls` in your home directory should not show `practice-cli`. If it does, the `Remove-Item -Recurse` line at step 9 did not run cleanly. Run `pwd` to see where you are. If you are not at home, run `cd ~` (PowerShell) or `cd` with no argument (Bash), then run `Remove-Item -Recurse practice-cli` or `rm -r practice-cli` again.

If you ran step 7 and saw the error but then typed `cd ..` followed by `Remove-Item -Recurse practice-cli` and got another path-not-found error, you probably overshot: you may now be two levels above the directory. Run `pwd` and walk back to home with `cd ~` before retrying.

If you see `mkdir : An item with the specified name ... already exists` on step 2, a folder by that name is already there from a prior attempt. Remove it first (from home, not from inside it) with `Remove-Item -Recurse practice-cli` on PowerShell or `rm -r practice-cli` on Bash, then start over.

## What just happened

Six commands, one round trip, one failure, one recovery. `pwd` reports where you are standing. `ls` reports what is in the current directory. `cd` changes the current directory. `mkdir` creates a new directory. `ni` (PowerShell) or `touch` (Bash) creates an empty file. `Remove-Item -Recurse` (PowerShell) or `rm -r` (Bash) deletes a directory and everything in it. That is the complete vocabulary for navigating and shaping a file tree from a CLI.

Two of the commands create (`mkdir`, `ni` / `touch`). One destroys (`Remove-Item -Recurse` / `rm -r`). Three observe and move (`pwd`, `ls`, `cd`). The symmetry is useful to remember: for every create verb there is a corresponding destroy verb.

The one rule that step 7 taught is bigger than this lesson. Any command that takes a path argument resolves that path against the current working directory unless you give it an absolute path. That is why `cd practice-cli` works from home, and why `Remove-Item -Recurse practice-cli` fails from inside `practice-cli`. The next module teaches absolute paths, relative paths, and the dot-and-double-dot notation that makes all of this explicit. For now, the takeaway is simpler: if a path-based command fails with "cannot find path" or "No such file or directory" and you can see the thing with your own eyes, you are almost always in the wrong directory. Run `pwd` and go from there.

## Going further

The PowerShell `mkdir` and the Bash `mkdir` both accept a flag that creates a whole chain of directories in one go. On PowerShell that flag is `-Force` combined with a nested path:

```powershell
mkdir -Force work\2026\april
cd work\2026\april
pwd
```

```text
Path
----
C:\Users\learner\work\2026\april
```

On Bash the flag is `-p` (short for "parents"):

```bash
mkdir -p work/2026/april
cd work/2026/april
pwd
```

Three levels of nesting, one command. Without the flag, creating `work/2026/april` when `work` does not exist yet would fail because the intermediate directories do not exist. The flag is also silent when the directories already exist, which is why every shell script that creates directories uses it by default.

Clean up afterward with one remove from the top of the branch, run from home:

```powershell
cd ~
Remove-Item -Recurse work
```

```bash
cd ~
rm -r work
```

Everything under `work/`, including `2026/april/`, is removed in one pass. That is the pattern for every temporary project folder you will ever need to clean up.

## What's next

Next is [L-008: Read a file's contents with cat and less](./L-008-read-a-files-contents-with-cat-and-less.md). You just made an empty file with `ni` or `touch`; the next lesson is how to open a file that has something in it and read what is inside, which is the first OS skill most learners recognize from daily life.
