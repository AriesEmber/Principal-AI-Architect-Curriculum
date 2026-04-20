---
lesson_id: L-012
sequence_number: 12
module_id: M02
domain_id: D01
title: "Install your first tool with a package manager"
week_number: 2
day_in_week: 5
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: medium
is_capstone: false
published_at: 2026-04-20T00:00:00Z
primary_shell: powershell
acronyms_expanded: [CLI, OS, PATH, GNU, WSL, URL, ASCII, JSON]
---

Ordering a kitchen gadget online is faster than driving to the store. You pick it from a catalog, you click once, and a day later it arrives at your door in the right box with the right plug. The package manager you set up yesterday is the same pattern for Command-Line Interface (CLI) tools. You type the name, the manager fetches the right build for your machine, and the new tool is ready in seconds. Today you place the first order. The tool is `tree`, and its job is to print a folder the way a book's table of contents shows chapters: one root, branches underneath, a clear picture of what contains what. You see your own practice folder as an American Standard Code for Information Interchange (ASCII) outline instead of a flat file listing.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm the package manager, winget install GnuWin32.Tree on PowerShell or brew install tree on Bash, verify the install (via winget list on Windows, tree --version on macOS), make a practice-cli folder with a src subfolder, drop a README.md inside, then run tree on the result to see an ASCII-art outline. The PowerShell column shows the GnuWin32 tree.exe in action, which is what you see after the PATH edit from L-013; in today's hands-on run the same outline comes from the Windows built-in tree /f, which is always on PATH](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.gif)

## What you will do

Install the `tree` command through your Operating System (OS) package manager, create a small practice folder, and run `tree` on it to see a branching outline of the folders and files inside.

## Before you start

You need to have completed [L-011: Install a package manager](./L-011-install-a-package-manager.md) and your terminal open at your home directory. Run `Get-Location` (PowerShell) or `pwd` (Bash) if you need to confirm where you are standing.

This lesson needs the internet. All three package managers from L-011 (`winget`, `brew`, `apt`) reach out to their repositories to fetch the `tree` package before they can install it. A regular home or office connection is enough.

On Windows, the first `winget install` asks you to accept the source agreements; press `Y` and `Enter`. The prompt only appears once per machine. On macOS, `brew install` does not ask for a password, because Homebrew owns the folder it installs into (`/opt/homebrew` or `/usr/local`).

## Step by step

PowerShell commands are shown first because PowerShell is the default shell on Windows 11 and the primary shell of this curriculum. The Bash equivalent follows each PowerShell block for readers on macOS, Linux, or the Windows Subsystem for Linux (WSL).

### 1. Confirm the package manager is alive

```powershell
winget --version
```

```bash
brew --version
```

Expected output is whatever version number L-011 left you on, for example `v1.10.320` for `winget` or `Homebrew 4.2.13` for `brew`. A single version line is the "subscription is live" signal. If you see `'winget' is not recognized` or `brew: command not found`, back up one lesson; nothing below will work until the package manager runs clean.

### 2. Install tree

> **Heads up.** The next command writes a new program onto your machine. On macOS and Linux the installer also adds its folder to the system `PATH` environment variable (PATH), which is the list of folders your shell searches when you type a command name, so the new command works immediately. On Windows, the GnuWin32 installer drops the binary under `C:\Program Files (x86)\GnuWin32\bin` but does not always extend `PATH`; that is fine for today and is covered in L-013. Either way the software is low-risk and signed, and it is removable with `winget uninstall GnuWin32.Tree` (Windows) or `brew uninstall tree` (macOS). It is a real install, not a sandboxed demo.

On Windows, the winget package for `tree` is a GNU's Not Unix (GNU) port named `GnuWin32.Tree`. Install it with:

```powershell
winget install -e --id GnuWin32.Tree
```

The `-e` flag is short for `--exact` and makes winget match the package ID exactly instead of searching by substring. Expected output is three or four lines ending in `Successfully installed`. Keep the PowerShell window open; the next step verifies the install without relying on `PATH`, so a fresh shell is not required today.

On macOS, run:

```bash
brew install tree
```

Expected output ends with an install-path line like `/opt/homebrew/Cellar/tree/2.2.1: 8 files`. On Debian-family Linux or inside WSL, use `sudo apt install tree` instead (you will be asked for your password). The rest of this lesson works the same way after any of the three.

### 3. Verify the package landed

```powershell
winget list GnuWin32.Tree
```

```bash
tree --version
```

On Windows, `winget list` asks the package manager what it has on record. The expected output is a one-row table with `GnuWin32.Tree` and a version like `1.7.0.4`. This check does not depend on `tree.exe` being on the `PATH` environment variable (PATH) — the list of folders your shell searches when you type a command name — so it works the moment the install finishes. On macOS, `tree --version` prints a banner like `tree v2.2.1` because Homebrew drops the binary into `/opt/homebrew/bin`, which is already on `PATH`.

Two Windows realities worth naming before the next step. First, the GnuWin32 installer places `tree.exe` in `C:\Program Files (x86)\GnuWin32\bin`, and it does not always add that folder to `PATH`, so typing `tree.exe` may still return `The term 'tree.exe' is not recognized`. Second, Windows already ships with a built-in `tree.com` in `C:\Windows\System32` (from the MS-DOS era), which is always on `PATH`, so typing plain `tree` works — but by default it prints only folders, not files. L-013 teaches the `PATH` edit that makes `tree.exe` resolve to the GnuWin32 binary. For today, the built-in is enough: a one-letter switch (`/f`) makes it print files too, which is all we need to see the outline.

### 4. Make a sample folder

```powershell
mkdir practice-cli\src
```

```bash
mkdir -p practice-cli/src
```

Both commands create two folders in one go: `practice-cli` in your home directory, and a subfolder named `src` inside it. PowerShell's `mkdir` creates missing parents by default; Bash's `-p` flag (short for `--parents`) does the same. Neither shell prints on success.

### 5. Drop a README inside the folder

```powershell
Set-Content -Path practice-cli\README.md -Value "hi"
```

```bash
echo hi > practice-cli/README.md
```

`Set-Content` is PowerShell's native "write this text to this file" cmdlet. It is more predictable than `"hi" > practice-cli\README.md` on Windows PowerShell 5.1, where the `>` operator writes UTF-16 with a byte-order mark and has tripped up more than one beginner. On Bash, the `>` operator writes a line of text the same way you saw in L-010. Either way, `practice-cli/README.md` now contains the word `hi` and a newline, and silence means the write landed.

### 6. Run tree on the sample

```powershell
tree /f practice-cli
```

```bash
tree practice-cli
```

On Windows, the `/f` switch tells the built-in `tree` to include files, not just folders. Without it, `tree practice-cli` would print only the `src` subfolder and your `README.md` would appear to be missing. Expected Windows output:

```text
Folder PATH listing for volume Windows
Volume serial number is ...
C:\USERS\YOU\PRACTICE-CLI
│   README.md
│
└───src
```

Expected Bash output:

```text
practice-cli
├── README.md
└── src

1 directory, 1 file
```

The Windows built-in draws `│` and `└───` with the console's box-drawing glyphs, and prints a volume header on top. The GNU port on macOS or Linux draws `├──` and `└──` and adds a trailing count line. The layout is the same either way: `practice-cli` is the root, `README.md` is a file inside it, `src` is a folder inside it. `src` is empty, so tree draws nothing beneath it.

![Side-by-side static panel of the 6-exchange walkthrough. PowerShell on the left, Bash on the right, with each exchange showing the command, its output, and a short comment line describing what happened. The PowerShell column in the visual invokes the newly installed GnuWin32 binary as tree.exe, which is what you will see once you apply the PATH edit from L-013; in today's lesson the same folder view comes from the built-in tree /f, which does not require a PATH change](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.png)

## Check it worked

Three things should be true at the end:

1. On Windows, `winget list GnuWin32.Tree` prints a one-row table that names the package and a version. On macOS or Linux, `tree --version` prints a `tree v...` banner.
2. `practice-cli` exists in your home directory and contains `README.md` plus a `src` folder. Run `Get-ChildItem practice-cli` or `ls practice-cli` to confirm.
3. `tree /f practice-cli` (PowerShell) or `tree practice-cli` (Bash) prints an ASCII outline with both the `README.md` file and the `src` folder visible.

If `winget list GnuWin32.Tree` prints `No installed package found matching input criteria`, the install did not finish; re-run step 2 and read the output for an error. If `tree --version` returns `tree: command not found` on macOS or Linux, the install did not finish; same fix. If `tree /f practice-cli` prints a header but only the `src` folder underneath, your README did not land where you expected. Run `Get-Location` or `pwd` to confirm you are in your home directory, then repeat steps 4 and 5. If you forgot the `/f` switch and ran plain `tree practice-cli`, the built-in only shows folders, so `README.md` appears to be missing even when it is there — add `/f` and it reappears.

## What just happened

Three ideas carry forward from this lesson.

**A package install is three steps in one command.** The manager looks up the name in its repository, downloads the build that matches your OS and processor, and drops the binary in a folder the OS already has on `PATH`. Before package managers were the default, those three steps were a browser download, an installer wizard, and usually a manual `PATH` edit. The manager collapses all three into one line that either succeeds or prints a specific error.

**The new command is on `PATH` (if you are lucky) — and today you did not need to be.** `PATH` is an ordered list of folders. When you type `tree`, the shell walks the list and runs the first match. On macOS and Linux, `brew install tree` drops the binary in `/opt/homebrew/bin` (or `/usr/local/bin`), a folder already on `PATH`, so `tree` just works. On Windows, `winget install GnuWin32.Tree` places `tree.exe` in `C:\Program Files (x86)\GnuWin32\bin`, and that folder is not always added to `PATH` by the installer — typing `tree.exe` may still fail. At the same time, `C:\Windows\System32` is on `PATH` and already contains a built-in `tree.com`, so typing `tree` runs the Windows built-in. That is the one you used in step 6 (with `/f` so it prints files as well as folders). Today's lesson therefore leaves both trees sitting on your machine: the fresh GnuWin32 binary you installed, and the old built-in you invoked. L-013 is the full lesson on environment variables; it teaches the `PATH` edit that would make the bare `tree.exe` resolve to the GnuWin32 binary so you can choose between the two.

**The tree picture maps one-to-one onto folders on disk.** Every `├──` is a peer entry at the same nesting level; every `└──` is the last entry inside a folder. There is no information in the ASCII art that is not on your disk. Once you read a tree fluently, you can picture a project layout as a small drawing. Most open-source `README.md` files include a tree of the repository for exactly this reason.

## Going further

Install one more tool with the same pattern to confirm the loop is real. Pick `jq`, which you will use later to read Uniform Resource Locator (URL) responses that return JavaScript Object Notation (JSON).

### On Windows (PowerShell)

```powershell
winget install -e --id jqlang.jq
```

Watch the install output. Unlike `GnuWin32.Tree`, this installer *does* extend `PATH`, and winget tells you so with the line `Path environment variable modified; restart your shell to use the new value.` That restart is not optional. Your current PowerShell session cached `PATH` at the moment it opened, so `jq` will not resolve in this window no matter how long you wait.

**Close the PowerShell window completely, open a new one, then run:**

```powershell
jq --version
'{"greeting":"hi","count":3}' | jq .
```

Expected output is `jq-1.8.1` (or newer) followed by a pretty-printed version of the input with one key per line. In PowerShell, the single-quoted JSON on the left of the pipe is a literal string, which `jq` reads as its input document.

If `jq` is still "not recognized" after you open a new window, ask Windows where the installer put the binary:

```powershell
where.exe jq
```

Expected output is the full path, usually `C:\Users\you\AppData\Local\Microsoft\WinGet\Links\jq.exe`. You can confirm the install by calling that path directly:

```powershell
& "$env:LOCALAPPDATA\Microsoft\WinGet\Links\jq.exe" --version
```

The `&` is PowerShell's call operator; it runs the quoted path as a program. If `where.exe` prints nothing, the install did not finish — re-run the `winget install` line and read its output for an error before continuing.

### On macOS (Terminal)

```bash
brew install jq
```

Homebrew drops `jq` onto the existing `PATH`, so no shell restart is required. Verify and try it on a tiny JSON document in the same window:

```bash
jq --version
echo '{"greeting":"hi","count":3}' | jq .
```

Expected output is `jq-1.7.1` (or newer) followed by the pretty-printed JSON.

### On Debian-family Linux (and the Windows Subsystem for Linux)

```bash
sudo apt install jq
```

Then the same `jq --version` and `echo ... | jq .` pair from the macOS block works identically.

---

You just installed, verified, and used a second tool in a handful of commands. The pattern does not change as the tools get larger; later in the curriculum the same three steps install Python, Git, and the Terraform binary.

## What's next

Next is [L-013: Set an environment variable and read it back (capstone)](./L-013-set-an-environment-variable-and-read-it-back-capstone.md). You have brushed up against `PATH` twice already (once when Homebrew's install put `tree` straight onto `PATH` on macOS, and once when Windows' GnuWin32 install left `tree.exe` sitting off `PATH` so you fell back to the built-in); L-013 takes environment variables apart with one you create yourself, and shows how to extend `PATH` so a newly installed tool resolves by its bare name.
