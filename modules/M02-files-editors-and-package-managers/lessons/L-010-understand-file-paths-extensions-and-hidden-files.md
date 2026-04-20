---
lesson_id: L-010
sequence_number: 10
module_id: M02
domain_id: D01
title: "Understand file paths, extensions, and hidden files"
week_number: 2
day_in_week: 3
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-20T00:00:00Z
primary_shell: powershell
acronyms_expanded: [CLI, OS, WSL]
---

A postal address has a country, a city, a street, and a house number. Each part narrows the search. Drop the house number and you are describing the street. Drop the street and you are describing the city. A file path works the same way. The drive letter or root stands in for the country. The deepest folder is the street. The filename is the house number. Every file on your computer has an address that looks like this, and there are two conventional ways to write it: from the root down (absolute) or from where you are standing (relative). Today you write one file's address two ways, rename it to see that its extension is a label and not a lock, and reveal the files that hide from the default directory listing. You use the Command-Line Interface (CLI) for all of it.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Seven exchanges: print the home path, write note.txt, read it with a relative path, read it with an absolute path, rename to note.md, read the renamed file, then list the directory with dotfiles revealed](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-010-terminal.gif)

## What you will do

Print your home directory's absolute path, write a short file, read it two ways (with a relative path and with an absolute path), rename it to change the extension, read it again to confirm the content is unchanged, and list the directory with hidden files revealed.

## Before you start

You need a terminal open at your home directory, the way [L-009: Edit a file with nano](./L-009-edit-a-file-with-nano.md) left you. Run `pwd` (Bash) or `Get-Location` (PowerShell) and confirm you are at your home path.

This lesson works on Windows 11 (PowerShell), macOS (Bash or Zsh), Linux (Bash or Zsh), and the Windows Subsystem for Linux (WSL). No install step is required. The commands are built into the shell.

You only need a writable home directory. The lesson creates one file called `note.txt`, renames it to `note.md`, and writes a second file called `.tag` to demonstrate dotfile listing. Nothing is deleted automatically; you can clean up at the end with `Remove-Item note.md, .tag` (PowerShell) or `rm note.md .tag` (Bash).

## Step by step

PowerShell commands are shown first because PowerShell is the default shell on Windows 11 and the primary shell of this curriculum. The Bash and Zsh equivalent follows each PowerShell block for readers on macOS, Linux, or WSL.

### 1. Print the absolute home path

```powershell
Get-Location
```

```bash
pwd
```

Both commands print the same kind of answer: the absolute path of your current working directory. On PowerShell the output starts with a drive letter (for example `C:\Users\learner`). On Bash it starts with a single forward slash (for example `/Users/learner` on macOS, `/home/learner` on Linux or WSL).

`Get-Location` is PowerShell's built-in name for this command; `pwd` is a shipped alias that matches the Bash name, so typing `pwd` in PowerShell works too.

### 2. Write a short file

```powershell
"hello paths" > note.txt
```

```bash
echo "hello paths" > note.txt
```

The `>` operator sends the output of the preceding command or expression into a file. PowerShell evaluates the quoted string as output directly; Bash needs `echo` to produce the output first. Either way, `note.txt` now contains the two words `hello paths` followed by a newline. Neither shell prints anything on success, which is the Unix convention: silence means it worked.

### 3. Read the file with a relative path

```powershell
cat note.txt
```

```bash
cat note.txt
```

Output:

```text
hello paths
```

The argument `note.txt` is a *relative path*. The shell reads it as "a file called `note.txt` in my current working directory." Because you are in your home directory, the shell resolves this to the full path `C:\Users\learner\note.txt` (or `/home/learner/note.txt`) and hands that to `cat`.

Relative paths are the form you use most of the time. They are shorter and they are portable: the same command works no matter which machine the same folder structure lives on.

### 4. Read the same file with an absolute path

```powershell
cat C:\Users\learner\note.txt
```

```bash
cat /home/learner/note.txt
```

Output:

```text
hello paths
```

Replace `learner` with your actual username. The file is the same file; the path is just longer because it names the file all the way from the root of the filesystem. An absolute path works from any working directory. You could `cd` to a different folder and the same absolute-path `cat` command would still print the same content.

The two forms (`note.txt` and `C:\Users\learner\note.txt`) are the two conventional ways to refer to a file. A third shortcut, `~`, expands to your home directory in both PowerShell 7 and Bash, so `cat ~\note.txt` (PowerShell) and `cat ~/note.txt` (Bash) also work.

### 5. Rename the file to change the extension

```powershell
Rename-Item note.txt note.md
```

```bash
mv note.txt note.md
```

Neither shell prints anything on success. The file on disk is still the same bytes; only the filename changed.

### 6. Read the renamed file

```powershell
cat note.md
```

```bash
cat note.md
```

Output:

```text
hello paths
```

Same content. The operating system (OS) does not check that a `.md` file contains Markdown or that a `.txt` file contains plain text. The extension is a naming convention, useful to humans and to programs that look at filenames to decide what to do (a double-click on `.md` usually opens a Markdown previewer; a double-click on `.txt` usually opens Notepad or TextEdit). But no part of the filesystem enforces the convention. You can rename `note.md` to `note.sql` or `note.gibberish` and the shell will read the same bytes back.

### 7. List the directory with hidden files revealed

```powershell
Get-ChildItem -Force
```

```bash
ls -a
```

Output (yours will differ):

```text
PowerShell:                 Bash:
.gitconfig                  .        ..
.ssh                        .bashrc  .gitconfig
note.md                     .ssh     note.md
```

Both commands list every file in the current directory, including the ones that the default listing hides. The specifics differ by shell:

- **Bash** hides any filename that starts with a dot. `ls` alone omits them; `ls -a` adds them. The entries `.` and `.bashrc` and `.gitconfig` are examples of such dotfiles.
- **PowerShell** does not care about the leading dot. It respects a different hiding mechanism called the Windows Hidden file *attribute*. `Get-ChildItem` alone already lists dotfiles like `.gitconfig`; the `-Force` flag adds files whose Hidden attribute is set.

Try creating a dotfile yourself:

```powershell
"sticky note" > .tag
cat .tag
```

```bash
echo "sticky note" > .tag
cat .tag
```

Both print `sticky note`. The file is there, regardless of shell. The only difference is whether the default `ls` or `Get-ChildItem` shows it.

![Side-by-side static panel of the 7-exchange walkthrough. PowerShell on the left, Bash on the right, with each exchange showing the command, its output, and a short comment line](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-010-terminal.png)

## Check it worked

Three things should be true at the end:

1. `cat note.md` prints `hello paths` (the rename kept the content).
2. `cat .tag` prints `sticky note` (the dotfile exists and is readable).
3. Running `Get-ChildItem -Force` (PowerShell) or `ls -a` (Bash) shows `note.md` and `.tag` in the listing.

If `cat note.md` prints nothing, the rename did not take; re-run step 5 and confirm there is no `note.txt` left in the directory. If `cat .tag` returns `No such file or directory`, the write in step 7 did not land in your current directory; run `pwd` or `Get-Location` and try again from your home path.

If `Get-ChildItem -Force` shows many entries you did not create, that is normal. Your home directory collects configuration files over time: `.gitconfig` from Git, `.ssh` from OpenSSH, `.wslconfig` from WSL, `.vscode` from Visual Studio Code, and so on. Every tool that needs a per-user config file lands one there.

## What just happened

Three ideas carry forward from this lesson.

**Paths are addresses.** Every file has an absolute path that names it from the root of the filesystem (a drive letter on Windows, a single forward slash on Unix). Every file also has one or more relative paths that name it from some other directory. The shortcut `~` expands to your home directory in both shells and lets you write short absolute-like paths regardless of where you are standing. Reading, writing, and renaming files does not care which form you use, as long as the path resolves to the same file.

**Extensions are labels.** The suffix after the last dot in a filename is a naming convention. It tells humans and programs what kind of content to expect. But no part of the filesystem enforces the convention. You can rename a text file to `.md`, `.sql`, or `.elvis`, and the shell reads the same bytes. Later lessons introduce the separate idea of a *content type* (the Hypertext Transfer Protocol header `Content-Type: text/markdown`), which is how web servers and browsers actually agree on how to interpret a file. The filename extension is a hint; the content type is a contract.

**Hidden is a convention, and the convention differs by platform.** On Unix, a file whose name starts with `.` is hidden from `ls` unless you add `-a`. This is not security; it is tidying. The home directory collects per-user configuration files, and hiding them out of the default listing keeps the working view uncluttered. On Windows, the shell respects a file-attribute mechanism instead: a file is hidden when its Hidden bit is set in the filesystem metadata, regardless of its name. PowerShell's `Get-ChildItem -Force` shows Hidden-attribute files; `ls -a` in Bash shows dotfile-convention files. A file named `.gitconfig` created on Windows is usually not Hidden-attribute-marked, so it shows by default in PowerShell but not in Bash. Knowing this asymmetry means you will not debug a phantom bug when the same dotfile appears or disappears between shells.

## Going further

Count the files in your home directory, both visible and hidden.

```powershell
(Get-ChildItem -Force ~).Count
```

```bash
ls -a ~ | wc -l
```

Then read one of the config files with `cat` to see what is inside. `.gitconfig` is a good candidate: it holds your Git user name and email, and occasionally other settings.

```powershell
cat ~\.gitconfig
```

```bash
cat ~/.gitconfig
```

If you have never used Git on this machine, the file may not exist; that is fine. Try `.bashrc` (Bash), `.zshrc` (Zsh), or `$PROFILE` (PowerShell) instead.

## What's next

Next is [L-011: Install a package manager](./L-011-install-a-package-manager.md). You have been creating and renaming files by hand; the next lesson installs the tool that installs every other tool, so the rest of the curriculum's commands can arrive on your machine without a web download per install.
