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

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm the package manager, winget install GnuWin32.Tree on PowerShell or brew install tree on Bash, verify the new binary with tree.exe --version or tree --version, make a practice-cli folder with a src subfolder, drop a README.md inside, then run tree on the result to see an ASCII-art outline](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.gif)

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

> **Heads up.** The next command writes a new program onto your machine and adds its install directory to the system `PATH` environment variable (PATH), which is the list of folders your shell searches when you type a command name. This is low-risk, signed software from a curated repository, and it is removable with `winget uninstall GnuWin32.Tree` (Windows) or `brew uninstall tree` (macOS). Still, it is a real install, not a sandboxed demo.

On Windows, the winget package for `tree` is a GNU's Not Unix (GNU) port named `GnuWin32.Tree`. Install it with:

```powershell
winget install -e --id GnuWin32.Tree
```

The `-e` flag is short for `--exact` and makes winget match the package ID exactly instead of searching by substring. Expected output is three or four lines ending in `Successfully installed`. Close the PowerShell window when it finishes and open a new one; the install added a folder to `PATH`, and a fresh shell session is the simplest way to pick it up.

On macOS, run:

```bash
brew install tree
```

Expected output ends with an install-path line like `/opt/homebrew/Cellar/tree/2.2.1: 8 files`. On Debian-family Linux or inside WSL, use `sudo apt install tree` instead (you will be asked for your password). The rest of this lesson works the same way after any of the three.

### 3. Verify the new command

```powershell
tree.exe --version
```

```bash
tree --version
```

Expected output is a tree version banner, for example `tree v1.7.0` on the GNU port for Windows or `tree v2.2.1` on current Homebrew. One cross-platform detail: on Windows, typing `tree` on its own still runs the built-in `tree.com` in `C:\Windows\System32`, because that folder comes earlier on `PATH` than the new GnuWin32 folder. The built-in has been around since MS-DOS. Adding `.exe` to the name forces PowerShell to pick up the new GNU port at `C:\Program Files (x86)\GnuWin32\bin\tree.exe`. On macOS and Linux there is no second tree, so plain `tree` works.

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
"hi" > practice-cli\README.md
```

```bash
echo hi > practice-cli/README.md
```

The `>` operator writes a line of text into a new file, the same operator you used in L-010. `practice-cli/README.md` now contains the word `hi` and a newline. Silence means the write landed.

### 6. Run tree on the sample

```powershell
tree.exe practice-cli
```

```bash
tree practice-cli
```

Expected output:

```text
practice-cli
├── README.md
└── src

1 directory, 1 file
```

The GNU port on Windows draws `|--` and `` `-- `` instead of `├──` and `└──` because the binary targets the Windows console's default code page, but the meaning is identical. Read top-down: `practice-cli` is the root, `README.md` is a file inside it, `src` is a folder inside it. `src` is empty, so tree draws nothing beneath it. The bottom line counts one folder and one file.

![Side-by-side static panel of the 6-exchange walkthrough. PowerShell on the left, Bash on the right, with each exchange showing the command, its output, and a short comment line describing what happened](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.png)

## Check it worked

Three things should be true at the end:

1. `tree.exe --version` (PowerShell) or `tree --version` (Bash) prints a `tree v...` banner.
2. `practice-cli` exists in your home directory and contains `README.md` plus a `src` folder. Run `Get-ChildItem practice-cli` or `ls practice-cli` to confirm.
3. `tree.exe practice-cli` or `tree practice-cli` prints the ASCII outline above, ending `1 directory, 1 file`.

If `tree --version` returns `tree: command not found` on macOS or Linux, the install did not finish; re-run step 2 and read the output for an error. If PowerShell prints the Windows built-in's `TREE [drive:][path]` line instead of a GNU banner, you typed `tree` instead of `tree.exe`. If `tree.exe` itself is not recognized, the new PowerShell window did not pick up the updated `PATH`; close every PowerShell window, open one fresh, and retry.

If the tree output is empty under `practice-cli`, the README did not land where you expected. Run `Get-Location` or `pwd` to confirm you are in your home directory, then repeat steps 4 and 5.

## What just happened

Three ideas carry forward from this lesson.

**A package install is three steps in one command.** The manager looks up the name in its repository, downloads the build that matches your OS and processor, and drops the binary in a folder the OS already has on `PATH`. Before package managers were the default, those three steps were a browser download, an installer wizard, and usually a manual `PATH` edit. The manager collapses all three into one line that either succeeds or prints a specific error.

**The new command is on `PATH`, which is why typing its name works.** `PATH` is an ordered list of folders. When you type `tree`, the shell walks the list and runs the first match. On macOS and Linux, `brew install tree` drops the binary in `/opt/homebrew/bin` (or `/usr/local/bin`), a folder already on `PATH`, so `tree` just works. On Windows, `winget install GnuWin32.Tree` adds a new folder, but `C:\Windows\System32` comes earlier and already contains `tree.com`, so the bare name still runs the built-in. Naming the binary as `tree.exe` matches on name and extension and skips the ordering problem. L-013 is the full lesson on environment variables; this is the first time the ordering rule matters in practice.

**The tree picture maps one-to-one onto folders on disk.** Every `├──` is a peer entry at the same nesting level; every `└──` is the last entry inside a folder. There is no information in the ASCII art that is not on your disk. Once you read a tree fluently, you can picture a project layout as a small drawing. Most open-source `README.md` files include a tree of the repository for exactly this reason.

## Going further

Install one more tool with the same pattern to confirm the loop is real. Pick `jq`, which you will use later to read Uniform Resource Locator (URL) responses that return JavaScript Object Notation (JSON):

```powershell
winget install -e --id jqlang.jq
```

```bash
brew install jq
```

On Debian-family Linux or WSL, use `sudo apt install jq`. Then verify and try it on a tiny JSON document:

```powershell
jq --version
'{"greeting":"hi","count":3}' | jq .
```

```bash
jq --version
echo '{"greeting":"hi","count":3}' | jq .
```

Both print `jq-1.7.1` (or newer) and a pretty-printed version of the input. You just installed, verified, and used a second tool in three commands. The pattern does not change as the tools get larger; later in the curriculum the same three steps install Python, Git, and the Terraform binary.

## What's next

Next is [L-013: Set an environment variable and read it back (capstone)](./L-013-set-an-environment-variable-and-read-it-back-capstone.md). You have touched `PATH` twice already (once when the installer added the `tree` folder, once when you used `.exe` to side-step its ordering); L-013 takes environment variables apart with one you create yourself.
