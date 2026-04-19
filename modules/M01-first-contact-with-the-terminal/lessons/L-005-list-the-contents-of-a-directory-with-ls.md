---
lesson_id: L-005
sequence_number: 5
module_id: M01
domain_id: D01
title: "List the contents of a directory with ls"
week_number: 1
day_in_week: 5
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-20T00:00:00Z
acronyms_expanded: [CLI, OS]
---

Every office has a file cabinet with drawers. A drawer sits closed most of the time, holding its contents out of sight. Pulling the drawer open is the cheapest gesture in the room: no paper is read, no folder is removed, you are just looking at what is in there before you reach for anything. Your terminal has the same gesture. It is a two-letter command called `ls`, short for list, and it is how a Command-Line Interface (CLI) learner answers the sibling question to "where am I?": what is in here with me. You are about to open the drawer.

![Animated typewriter walkthrough of the four ls exchanges](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-005-terminal.gif)

## What you will do

Type `ls`, see the names of everything in the current folder, then type `ls -la` to see the same list with every detail the shell can print about each entry.

## Before you start

You need an open terminal from [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md), sitting at its default home-directory prompt. If you are not sure where you are, run `pwd` first and confirm it returns your home path. Nothing will be created, nothing will be deleted, no settings will change. `ls` is another read-only question.

If your prompt ends in `$` (Bash on Linux or Windows Subsystem for Linux), `%` (Zsh on macOS), or `>` (PowerShell on Windows), every command below works identically.

## Step by step

### 1. Ask what is here

Type:

```bash
ls
```

You will see a short list of names, either spread across the window in columns or one per line if the window is narrow. On a fresh home directory the names are almost always the top-level folders the operating system (OS) created for you.

```text
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
```

You did not tell `ls` where to look, so it used the working directory, which is what `pwd` would return: your home folder.

### 2. Ask for every detail

Type:

```bash
ls -la
```

The output grows in two directions. The rows now include entries whose names start with `.`, which the plain `ls` hid from you. And each row is a full tabular record:

```text
total 28
drwxr-xr-x 12 learner learner 4096 Apr 18 10:15 .
drwxr-xr-x  3 root    root    4096 Apr 10 14:22 ..
-rw-------  1 learner learner  128 Apr 18 10:15 .bash_history
-rw-r--r--  1 learner learner 3771 Apr 10 14:22 .bashrc
drwxr-xr-x  2 learner learner 4096 Apr 15 11:00 Documents
drwxr-xr-x  2 learner learner 4096 Apr 15 11:00 Downloads
```

Read across each row and you get, in order: a permissions string, a link count, an owner, a group, a size in bytes, a modification date and time, and finally the name.

The two entries named `.` and `..` are not decoration. Every directory on every mainstream operating system has them. `.` is the directory itself; `..` is its parent. They are the reason `cd ..` works in the next lesson, and you have already met them here.

### 3. Tell ls to look somewhere else

`ls` takes an argument: the path of the directory to list. Try the root of the filesystem.

On macOS or Linux:

```bash
ls /
```

```text
bin  boot  dev  etc  home  lib  opt  proc  root  sbin  tmp  usr  var
```

On Windows PowerShell:

```powershell
ls C:\
```

Same command-response rhythm, same idea, different target. You did not leave the home directory; you asked `ls` to report on somewhere else.

### 4. Optional: see the PowerShell alias

On Windows PowerShell, `ls` is not a separate program. It is an alias for `Get-ChildItem`.

```powershell
Get-Command ls
```

```text
CommandType     Name    Source
-----------     ----    ------
Alias           ls -> Get-ChildItem
```

`dir` is also an alias for the same command. The column format of the output is slightly different from the bash version (PowerShell shows `Mode`, `LastWriteTime`, `Length`, `Name`), but the question being asked is identical.

![Static panel showing the four ls exchanges and the PowerShell alias check](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-005-terminal.png)

## Check it worked

After step 1, you should see a single row (or a short stack of rows) of folder names with no error. After step 2, you should see a header row `total N` and a block of rows with ten characters in the first column of each. If the first character is `d`, that entry is a folder. If it is `-`, that entry is a file.

If you see `command not found: ls` or `'ls' is not recognized`, you typed it wrong. It is two letters: `l` and `s`.

If the output of step 2 looks different from the example but has the same shape (ten-character permission field, size, date, name), you are on a Linux or macOS system and everything is working. If the output uses column headers like `Mode` and `LastWriteTime`, you are on PowerShell and everything is also working.

If `ls -la` returned no rows at all, not even `.` and `..`, the directory you were in was deleted from under the shell while you were reading. Close the window and open a new one; it will land back in your home directory.

## What just happened

`ls` prints the list of names the directory holds. By default it skips entries whose names start with a dot and it prints only the names, in columns, without any trailing details. That default is tuned for the most common use of `ls`, which is a quick glance at what is visible in the current folder.

The flags change the shape of the report without changing the question. `-a` says "include every entry, even the hidden ones." `-l` says "give me the long form, one row per entry, with permissions, owner, size, date, and name." You can combine them as `-la`, which is what most people run in practice.

Knowing the long form matters because it is how you answer the question the spine set up at the top of this lesson: what is the difference between a file and a folder? The answer is the very first character of each long-format row. `d` is a directory you can step into (with the command you will learn next) and list further. `-` is a regular file with content inside it and no children below it. That is the whole distinction, at the shell level.

`ls` is also the answer to the question "what is around me?" which is the sibling of "where am I?" from the previous lesson. `pwd` returns the address; `ls` returns the inventory. Together they give you complete situational awareness of a directory before you do anything else in it.

## Going further

Try `ls` on a directory you have never stood in. On macOS or Linux:

```bash
ls /etc
```

`/etc` is where most system programs store their configuration files. The output is long; that is by design, because this is where the operating system keeps its settings.

On Windows PowerShell:

```powershell
ls C:\Windows
```

Pass `-la` on the same directory and look at the permission columns. You will see that not every entry on the system is owned by your user account, and some entries are not readable by you at all. That is a preview of the permissions model you will meet in module two.

One small quality-of-life flag for later: on macOS or Linux, `ls -lh` prints sizes in kilobytes, megabytes, and gigabytes instead of raw bytes. Experienced users turn it on by default.

## What's next

Next is [L-006: Move around with cd and relative paths](./L-006-move-around-with-cd-and-relative-paths.md). Now that you know where you stand and what is around you, it is time to actually move.
