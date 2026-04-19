---
lesson_id: L-003
sequence_number: 3
module_id: M01
domain_id: D01
title: "Print your first line with echo (RETIRED v1)"
week_number: 1
day_in_week: 3
estimated_minutes: 13
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-19T00:00:00Z
retired_at: 2026-04-19T00:00:00Z
retired_reason: "False cross-shell parity claim; Bash-only variable examples broke for PowerShell readers."
replaced_by: L-003-v2
acronyms_expanded: [CLI]
---

> **RETIRED — v1 of this lesson.** This file is a historical snapshot of L-003 as it shipped to `main` on 2026-04-18 (commit `407973b`). It was retired on 2026-04-19 because it asserted "every command below works identically on all three" shells, which is false: the `$USER`, `$HOME`, and `$SHELL` variable-expansion examples are Bash and Zsh only and produce blank output on Windows PowerShell. The live lesson at the canonical path covers Bash, Zsh, and PowerShell side by side. See [RETIRED.md](./RETIRED.md) in this folder for the full explanation, or jump straight to [the v2 lesson](../../modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md).

---

Ringing a doorbell is the simplest form of talking to a machine. You press once, it sounds once, and you know it worked because you heard it. The terminal waiting in front of you works the same way. You type one line, press Enter, and it types back whatever you asked for. That is the entire Command-Line Interface (CLI) in one gesture, and every other lesson in this curriculum is a variation on it. Your first word is `echo`. Press it like a doorbell.

![Animated typewriter walkthrough of the five echo exchanges covered in this lesson](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/_archive/L-003-v1/L-003-terminal.gif)

## What you will do

Type `echo Hello, world`, press Enter, and watch the terminal print the same text back on the next line.

## Before you start

You need an open terminal window from [L-002: Read a prompt like a sign at a train station](./L-002-read-a-prompt-like-a-sign.md), sitting at its default prompt. If you closed it, open a new one. Nothing else is required. No files will be created, nothing will be downloaded, and no settings will change. Echo is read-only: it prints to the screen and returns you to the prompt.

If your prompt ends in `$` (Bash on Linux, Windows Subsystem for Linux), `%` (Zsh on macOS), or `>` (PowerShell on Windows), you are in the right place. Every command below works identically on all three.

## Step by step

Each step is one line typed at the prompt, followed by pressing Enter. You do not need to type the prompt itself; only the characters after it.

### 1. The plain form

Type:

```bash
echo Hello, world
```

You will see:

```text
Hello, world
```

The prompt returns on the line below, ready for the next command.

### 2. With double quotes

Type:

```bash
echo "Hello, world"
```

You will see the same line:

```text
Hello, world
```

The output looks identical, but what happened inside the shell is different. The quotes told the shell to treat everything between them as one argument instead of splitting on whitespace. That distinction will matter in later lessons when the text contains a dollar sign, a backtick, or other characters the shell cares about.

### 3. With single quotes

Type:

```bash
echo 'Hello, world'
```

You will see:

```text
Hello, world
```

Same output, stricter rule. Single quotes protect the text from every form of shell interpretation. Whatever is between them is sent to echo verbatim.

### 4. With no arguments

Type:

```bash
echo
```

You will see a blank line, then the prompt back. Echo with nothing to print still prints a newline. It is a small proof that the command ran.

### 5. With a variable

Type:

```bash
echo $USER
```

You will see your own username printed on the next line. On PowerShell, use `echo $env:USERNAME` instead. In both cases the shell looked up the value of the variable before echo ever saw it, and handed echo the result as a plain argument.

## Check it worked

After step 1, the exact text `Hello, world` should appear on the line directly below your command. The prompt should return on the line after that, blinking cursor and all. If you see a message like `command not found: ech` or `'echo' is not recognized`, you typed a letter wrong. Retype and try again.

If you see literal quote marks in the output (`"Hello, world"` or `'Hello, world'`), the quote characters came from a word processor that swapped straight quotes for curly ones when you pasted. Type the line directly in the terminal instead of pasting from a document.

If steps 1, 2, and 3 each produced the exact string `Hello, world` on the next line, and step 5 produced your own username, the lesson is done. You have executed a command, confirmed its output, and returned the terminal to a ready state. Three times over.

## What just happened

Echo is a built-in command whose job is to print its arguments to the screen, joined by single spaces, followed by a newline. That is the whole of it. The interesting work happened before echo was called.

The shell, the program that reads your keystrokes, did two things to your line before echo saw anything. First, it split the line into tokens using whitespace as the separator, so `echo Hello, world` became three tokens: `echo`, `Hello,`, and `world`. Second, when it saw `$USER`, it expanded the variable to its current value and replaced the token with that value. Only after that did it hand the list of tokens to echo and ask echo to print them.

That two-step process explains the three small surprises in the exercise. No-quotes and double-quotes look identical because the whitespace inside `Hello,` and `world` lands in the same place either way. Single quotes would have mattered if you had written `echo '$USER'` (which prints the literal string `$USER`) compared with `echo "$USER"` (which prints your username). The no-arguments case printed a blank line because echo still emits the trailing newline even when it has nothing else to say.

The CLI rhythm you just felt is the atom of every interaction in this curriculum. Argument in, result out, prompt back, ready for the next one. Python will feel like this. Git will feel like this. Terraform will feel like this. The answers get more interesting, but the rhythm does not change.

## Going further

Try two more variables your shell already knows about:

```bash
echo $HOME
echo $SHELL
```

`$HOME` prints the absolute path of your home directory. `$SHELL` prints the path of the shell program reading these commands (for example, `/bin/zsh` or `/bin/bash`). Both are set automatically when you log in, and both will reappear in lessons on environment variables and on navigating the filesystem.

For one more small experiment, run:

```bash
echo "My user is $USER and my shell is $SHELL"
```

Notice how the shell expanded both variables inside the double-quoted string and handed echo the finished sentence. That is the same mechanism you just saw, used more densely.

## What's next

Next is [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md), where the command-response rhythm produces a more useful answer: the absolute path of the folder your terminal is standing in.
