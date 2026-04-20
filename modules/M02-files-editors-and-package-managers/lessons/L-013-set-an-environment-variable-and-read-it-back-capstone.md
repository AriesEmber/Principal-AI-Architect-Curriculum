---
lesson_id: L-013
sequence_number: 13
module_id: M02
domain_id: D01
title: "Set an environment variable and read it back (capstone)"
week_number: 2
day_in_week: 6
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: true
published_at: 2026-04-20T20:00:00Z
primary_shell: powershell
acronyms_expanded: [CLI, OS, PATH, WSL, ASCII, API, PR]
---

A shop has a whiteboard in the back office. You write a note on it, anyone who walks into the room can read it, anyone can wipe it and write over it. Leave the room and close the door, and the board stays put with the note still on it. Walk into the next room and there is a different board: blank, its own marker tray, its own set of old scratches. An environment variable in a Command-Line Interface (CLI) shell is that whiteboard. Every terminal window you open gets its own board at startup. The value you write stays visible until the window closes, and the next window starts clean. You are about to write a note called `MY_NAME`, read it back, use it in a greeting, confirm that any program you launch from this window can see the note too, and then open a fresh window and find it gone. That last step is the capstone move for Module 2.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm MY_NAME does not exist yet, set it to Elvis, read it back, use it in a greeting, list it in the process environment with Get-ChildItem Env:MY_NAME on Windows or printenv on Bash, then open a fresh terminal window and see the read return a blank line](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-013-terminal.gif)

## What you will do

Set a variable called `MY_NAME` in your current terminal window, read it back, use it in a one-line greeting, confirm it lives in the process environment, then open a fresh terminal window and watch the same read return a blank line.

## Before you start

You need to have completed [L-012: Install your first tool with a package manager](./L-012-install-your-first-tool-with-a-package-manager.md) and have a terminal open at your home directory. Run `Get-Location` (PowerShell) or `pwd` (Bash) if you want to confirm where you are standing.

No install is needed today. Everything happens in-memory, inside the shell window you already have open. The whole lesson is reversible: the variable you create vanishes the moment you close the window.

One recall from L-012: you saw that the `tree.exe` from `GnuWin32.Tree` landed in `C:\Program Files (x86)\GnuWin32\bin` but that folder was not always on `PATH`, so your Windows shell still ran the built-in `tree.com` instead. `PATH` is an environment variable, and the reason a freshly-installed program sometimes does not resolve is exactly the thing you are about to see with `MY_NAME`: an environment variable belongs to the shell that reads it, and every shell reads its own copy at startup.

## Step by step

Commands are paired: PowerShell first (the default shell on Windows 11 and the primary shell of this curriculum), Bash second (for macOS, Linux, and the Windows Subsystem for Linux (WSL)). The two shells use different syntax for the same idea. Run the block that matches the terminal in front of you.

### 1. Confirm the whiteboard is blank

```powershell
echo $env:MY_NAME
```

```bash
echo "$MY_NAME"
```

Expected output is a single blank line in both shells. That blank line is your first real result, not an error. The shell looked up a variable that does not exist yet, substituted nothing, and printed nothing followed by a newline. In PowerShell, `$env:` is a drive prefix that reads the current process environment; typing `$env:MY_NAME` returns the value or `$null` when the name is absent. In Bash, `$MY_NAME` expands to the empty string when the name is absent; wrapping it in double quotes is habit, so you do not trip on a name that happens to contain spaces later.

### 2. Set the variable

```powershell
$env:MY_NAME = "Elvis"
```

```bash
export MY_NAME="Elvis"
```

Replace `Elvis` with whatever name you want to see echoed back. Both shells produce no output on success; silence is the "done" signal. PowerShell's `$env:NAME = "..."` always writes to the current process environment, so every program launched from this window inherits the value. Bash splits the idea in two: a bare `MY_NAME="Elvis"` creates a shell variable visible only to the current shell, and `export` is the word that promotes it to an environment variable that child programs can read too. The `export` form is the one that matches PowerShell's behaviour, which is why both sides of the block use it.

### 3. Read it back

```powershell
echo $env:MY_NAME
```

```bash
echo "$MY_NAME"
```

Expected output is the value you just set, one line, no quotes, no prefix. This is the same read from step 1 running against a live value instead of an empty one. In PowerShell you will also see the same result if you type `$env:MY_NAME` on its own: the interactive prompt auto-prints the value of any bare expression.

### 4. Use it in a greeting

```powershell
echo "Hello, $env:MY_NAME"
```

```bash
echo "Hello, $MY_NAME"
```

Expected output: `Hello, Elvis` (with your name in place of `Elvis`). Both shells support double-quoted string interpolation, which is a formal way of saying that `"$env:MY_NAME"` or `"$MY_NAME"` inside double quotes is replaced by the value of the variable before the string is handed to `echo`. Single quotes do not interpolate in either shell, so `'Hello, $MY_NAME'` would print the literal dollar sign and name. This is the same trick every shell script uses to stitch values into file names, paths, and log messages.

### 5. Confirm it lives in the process environment

```powershell
Get-ChildItem Env:MY_NAME
```

```bash
printenv MY_NAME
```

On PowerShell, `Get-ChildItem Env:` walks the `Env:` PSDrive, which is a view onto the process environment; asking for a single name prints a one-row table with the name and its value. On Bash, `printenv NAME` prints the value or prints nothing and exits with a non-zero status if the name is not in the environment. The reason these commands matter is that they distinguish a real environment variable from a plain shell variable. A Bash assignment without `export` would succeed in step 2 and echo back in step 3, but `printenv MY_NAME` would print an empty line, and programs launched from the shell would not see the name. Running the check now makes the lesson honest: you set an environment variable, not a shell variable.

### 6. Open a fresh terminal and check again

Close the terminal window you have been working in, then open a brand-new one. On Windows, press the Windows key, type `PowerShell`, and press Enter. On macOS, open Terminal.app or iTerm and press `Cmd+N` for a new window (or open the application from scratch). On Linux, use the terminal's File menu or the keyboard shortcut for your desktop environment. In the fresh window, repeat the step 3 read:

```powershell
echo $env:MY_NAME
```

```bash
echo "$MY_NAME"
```

Expected output is a blank line again, matching step 1. The assignment from step 2 lived inside the first window's process environment; closing the window ended that process; the new window started from a fresh copy of the parent environment, which never had `MY_NAME` in it. That is the whole capstone payoff. You wrote a note on one room's whiteboard, and the next room is a blank board.

![Static side-by-side panel of the six-exchange walkthrough. The final exchange in each column is drawn in a new window; both reads return a blank line to make the session-scoped lifetime of the variable visible at a glance](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-013-terminal.png)

## Check it worked

Three things should be true at the end. Run them in the original window (before you close it in step 6) and in the fresh window (after you close and re-open).

1. In the original window, `echo $env:MY_NAME` (PowerShell) or `echo "$MY_NAME"` (Bash) prints your value on its own line.
2. In the original window, `Get-ChildItem Env:MY_NAME` (PowerShell) or `printenv MY_NAME` (Bash) shows the variable listed. This is the proof that the value is in the process environment, not just a shell-only variable.
3. In the fresh window, both reads print a blank line.

If the original-window read prints a blank line when you expected a value, you are almost certainly in a second window. Run `Get-Location` or `pwd` as a sanity check and then repeat step 2 in the window you meant to use. If `Get-ChildItem Env:MY_NAME` errors with `Cannot find path 'Env:MY_NAME' because it does not exist`, the assignment in step 2 did not run; re-type it exactly. If you used a plain Bash assignment (`MY_NAME="Elvis"` without `export`), step 3 will echo the value but step 5 (`printenv MY_NAME`) will print nothing and exit with a non-zero status; rerun step 2 with `export` at the front and the rest of the lesson lines up.

## What just happened

Three ideas carry forward from this lesson.

**Every shell window is its own process with its own environment.** When your desktop opens a terminal, the operating system (OS) creates a new process and hands it a copy of the parent's environment. Every assignment you make inside that window writes to the copy; when the process exits, the copy is discarded. The next window starts with a fresh copy from the same parent. That is why the step 6 read returns blank: the new window was never handed the `MY_NAME` you set in the old one.

**PowerShell and Bash draw the shell-versus-environment line differently.** Bash separates shell variables (`MY_NAME="Elvis"`, visible only in this shell) from environment variables (`export MY_NAME="Elvis"`, visible to child processes as well). PowerShell collapses the two cases: `$env:NAME = "..."` always writes to the process environment. The distinction matters when you move to scripts and subshells. A Bash script that sets a variable without `export` and then calls `python my_script.py` will find that `os.environ["MY_NAME"]` is blank inside Python, because Python is a child process and only sees exported variables. PowerShell's `$env:` writes do not have this trap.

**`PATH` is an environment variable just like `MY_NAME`.** The reason the `tree.exe` you installed in L-012 was sometimes "not recognized" is that every shell reads its own copy of `PATH` at startup. When an installer edits the system or user `PATH` in the Windows registry, every already-open shell keeps using its cached copy; only windows opened after the edit see the new entry. Your new `MY_NAME` and the system's `PATH` follow the same rule: the shell that does the read is reading its own copy, not a live link. The American Standard Code for Information Interchange (ASCII) tree you drew yesterday and the `Hello, Elvis` you printed today are the same pattern underneath.

## Going further

You have seen that closing the window wipes the value. The obvious next question is how to keep a value around across windows. The answer is different on each OS; both are previewed here so you know the shape of the fix, and later lessons return to both in full.

### Windows (persist into your user environment)

```powershell
[Environment]::SetEnvironmentVariable("MY_NAME", "Elvis", "User")
```

This call writes to the per-user environment stored in the Windows registry under `HKCU\Environment`. The write survives reboots. Every process started after the call (not the one that ran it) sees the new value. To confirm, close your PowerShell window, open a new one, and run `echo $env:MY_NAME`. To remove it, pass `$null` as the value: `[Environment]::SetEnvironmentVariable("MY_NAME", $null, "User")`. The third argument can also be `"Machine"` to write to the system-wide environment, but that requires administrator rights and affects every user on the box, so stay with `"User"` unless a later lesson tells you otherwise.

### macOS and Linux (append to your shell startup file)

```bash
echo 'export MY_NAME="Elvis"' >> ~/.bashrc
```

On modern macOS the default shell is Zsh, so use `~/.zshrc` instead. The append adds one line to the file that the shell reads at startup; every new login shell sees the variable. To confirm, close and reopen the terminal and run `echo "$MY_NAME"`. To remove it, open the file in an editor (`nano ~/.bashrc` from L-009 still works) and delete the line, then close and reopen the terminal again.

Both approaches are cheap to set up and cheap to undo, but neither is free. A typo in a persistent file follows you into every new shell until you fix it. For credentials and Application Programming Interface (API) keys the story changes further: persisting them in plain text is a security issue, and later lessons move secret values out of `~/.bashrc` and the user registry into a tool designed for them. For today, `MY_NAME = "Elvis"` is a safe value to practice with.

## What's next

Next is [L-014: Install Git and confirm the version](../M03-version-control-first-principles/lessons/L-014-install-git-and-confirm-the-version.md). You use the same package manager from L-011 one more time, this time to install the tool that every remaining module in this curriculum leans on, including the pull request (PR) workflow that arrives in Module 4.
