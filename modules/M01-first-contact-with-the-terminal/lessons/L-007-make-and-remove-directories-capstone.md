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
published_at: 2026-04-18T00:00:00Z
acronyms_expanded: [CD, CLI, OS]
---

Picture setting up a new filing cabinet for a new project. You slide a fresh cabinet into place, pull the top drawer open, confirm the drawer is empty, and drop a single note inside. Later, when the project is over, you shred the whole cabinet and its contents in one motion. Six days of this curriculum so far have been about knowing where you stand and how to move. Today is the first day you create something of your own. You are about to build a directory, put a file in it, and take the whole thing back down, using six commands: `pwd`, `ls`, `cd`, `mkdir`, `touch`, and `rm`. That is the full vocabulary of week one, combined for the first time in one flow.

![Animated typewriter walkthrough of the ten-exchange capstone](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.gif)

## What you will do

Make a new directory called `practice-cli` in your home folder, walk into it, confirm it is empty, drop a blank text file inside, walk back out, and delete the whole directory.

## Before you start

You need an open terminal and a home directory. Four prior lessons give you everything else. [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md) taught you how to confirm you are at home. [L-005: List the contents of a directory with ls](./L-005-list-the-contents-of-a-directory-with-ls.md) taught you how to look around. [L-006: Move around with cd and relative paths](./L-006-move-around-with-cd-and-relative-paths.md) taught you how to walk into a folder and back out. This lesson adds the last two verbs you need to do real work: make and remove.

Before the first command, run `pwd` once and confirm it reports your home directory. If it does not, run `cd` with no argument to return home. The whole lesson assumes home as the starting point.

## Step by step

### 1. Confirm where you stand

```bash
pwd
```

```text
/home/learner
```

macOS will show `/Users/learner` instead, and Windows PowerShell will show `C:\Users\learner`. Any of those is the correct starting line. The path is what every command in this lesson works relative to.

### 2. Make a new directory

```bash
mkdir practice-cli
```

`mkdir` stands for "make directory." The name after it is the folder you are creating, and because the name has no leading slash the shell creates it inside the current directory. The command is silent on success, just like `cd` was.

### 3. Confirm the directory exists

```bash
ls
```

```text
Desktop  Documents  Downloads  practice-cli
```

Your exact listing will differ, but `practice-cli` should be in it. If it is not, re-read the `mkdir` line for a typo and run it again. `mkdir` on an existing folder will error; on a new name it will quietly create the folder.

### 4. Walk into the new directory

```bash
cd practice-cli
```

The prompt's path segment changes from `~` to `~/practice-cli`. That is the Command-Line Interface (CLI) showing you the change directory (CD) move worked.

### 5. Look around inside

```bash
ls
```

No output. The folder you just made is empty; `ls` prints nothing when there is nothing to list. This silence is normal and expected, not a bug.

### 6. Create an empty file

```bash
touch hello.txt
```

`touch` is a single-word command that was originally designed to update a file's last-modified timestamp. It has a side effect: if the file does not exist, `touch` creates it, empty. That side effect is why every professional uses `touch` as the one-keyword way to make an empty file.

### 7. Confirm the file exists

```bash
ls
```

```text
hello.txt
```

One file, zero bytes, ready to edit later. This is the state of every real project folder you will ever make: a directory with some number of files and sub-directories inside it. You just built the minimum version.

### 8. Walk back up

```bash
cd ..
```

The two dots take you up one level, back to your home directory. The prompt's path segment returns to `~`.

### 9. Remove the directory and its contents

```bash
rm -r practice-cli
```

`rm` means remove. The `-r` flag means recursive: remove the named directory and everything inside it, walking down through every sub-directory on the way. Silent on success.

There is one piece of this command worth reading twice. `rm -r` does not move files to a recycle bin. It deletes them. On macOS and Linux the deletion is permanent unless you are using a filesystem with snapshot support. On Windows PowerShell the equivalent (`Remove-Item -Recurse`) behaves the same way. Type the target carefully, and never run `rm -r` against a path you did not just create yourself in this lesson.

```bash
ls
```

```text
Desktop  Documents  Downloads
```

`practice-cli` is gone. The cabinet has been shredded. That is all six week-one commands, strung together in one flow.

![Static panel of the ten exchanges plus the PowerShell equivalent](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.png)

## Check it worked

At the end of the sequence, `ls` in your home directory should not show `practice-cli`. If it does, the `rm -r` line did not run or hit a typo. Run it again.

If you see `rm: cannot remove 'practice-cli': No such file or directory`, you were not standing in your home directory when you ran the removal. Run `pwd` to see where you are. If it says anything other than home, run `cd` with no argument and try the removal again.

If you see `mkdir: cannot create directory 'practice-cli': File exists` on step 2, a folder by that name is already there from a prior attempt. Remove it first with `rm -r practice-cli` and start over, or pick a different name like `practice-cli-2` for this run.

The shell is case-sensitive on macOS and Linux. `practice-cli` and `Practice-CLI` are two different directories. Windows is case-insensitive, so either works there. If you are on a team that mixes platforms, always lowercase your directory names; it avoids a class of surprises.

## What just happened

Six commands, one round trip. `pwd` reports where you are standing. `ls` reports what is in the current directory. `cd` changes the current directory. `mkdir` creates a new directory. `touch` creates an empty file. `rm -r` deletes a directory and everything in it. That is the complete vocabulary for navigating and shaping a file tree from a command line.

Two of the commands create (`mkdir`, `touch`). One destroys (`rm`). Three observe and move (`pwd`, `ls`, `cd`). The symmetry is useful to remember: for every create verb there is a corresponding destroy verb. The other half of `mkdir` is `rmdir`, which removes an empty directory. The other half of `touch` (for the purpose of removing the file it created) is plain `rm` without the `-r` flag. `rm -r` is the hammer version that handles both directories and files and their contents in one command; most of the time it is the only removal command you need.

The filing-cabinet image holds up through the whole lesson because every step maps to a physical action: mkdir slides the cabinet in, cd pulls the drawer open, ls looks inside, touch drops a note, cd .. pushes the drawer back, rm -r shreds the cabinet and everything in it. Once those mappings are in your hands, the shell stops feeling like a puzzle and starts feeling like a set of tools that match the mental model you already had for organizing paper.

## Going further

The `mkdir` command has a flag called `-p` (short for "parents") that creates a whole chain of directories in one go. Try this in your home folder:

```bash
mkdir -p work/2026/april
cd work/2026/april
pwd
```

```text
/home/learner/work/2026/april
```

Three levels of nesting, one command. Without `-p`, running `mkdir work/2026/april` would fail because the intermediate directories do not exist yet. The `-p` flag also makes the command silent-on-success when the directory already exists, which is why every shell script you will ever read that creates directories uses `-p` by default. It is safe to run twice.

Clean up afterward with one `rm -r` at the top of the branch:

```bash
cd ~
rm -r work
```

Everything under `work/`, including `2026/april/`, is removed in one pass. That is the pattern for every temporary project folder you will ever need to clean up.

## What's next

Next is [L-008: Read a file's contents with cat and less](./L-008-read-a-files-contents-with-cat-and-less.md). You just made an empty file with `touch`; the next lesson is how to open a file that has something in it and read what is inside, which is the first operating system (OS) skill most learners recognize from daily life.
