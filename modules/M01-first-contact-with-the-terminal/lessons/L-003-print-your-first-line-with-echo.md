---
lesson_id: L-003
sequence_number: 3
module_id: M01
domain_id: D01
title: "Print your first line with echo"
week_number: 1
day_in_week: 3
estimated_minutes: 14
capture_mode: terminal_auto
risk_level: low
is_capstone: false
published_at: 2026-04-19T17:00:00Z
revision: 2
revises: L-003-v1
revision_reason: "Added Bash, Zsh, and PowerShell parity for variable-expansion steps; v1 falsely claimed identical behavior across all three shells."
acronyms_expanded: [CLI, WSL]
---

Ringing a doorbell is the simplest form of talking to a machine. You press once, it sounds once, and you know it worked because you heard it. The terminal waiting in front of you works the same way. You type one line, press Enter, and it types back whatever you asked for. That is the entire Command-Line Interface (CLI) in one gesture, and every other lesson in this curriculum is a variation on it. Your first word is `echo`. Press it like a doorbell.

![Animated typewriter walkthrough of the five echo exchanges, shown side by side in Bash and Windows PowerShell](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-003-terminal.gif)

## What you will do

Type `echo Hello, world`, press Enter, and watch the terminal print the same text back on the next line.

## Before you start

You need an open terminal window from [L-002: Read a prompt like a sign at a train station](./L-002-read-a-prompt-like-a-sign.md), sitting at its default prompt. If you closed it, open a new one. Nothing else is required. No files will be created, nothing will be downloaded, and no settings will change. Echo is read-only: it prints to the screen and returns you to the prompt.

### Pick your shell

The first four steps below work the same in every shell. Step 5, and the experiments at the end, depend on which shell you opened. There are two flavors in this lesson:

- **Bash or Zsh.** The default on Linux and macOS. Also available on Windows through Windows Subsystem for Linux (WSL) or Git Bash. The prompt usually ends in `$` (Bash) or `%` (Zsh).
- **PowerShell.** The default on Windows 10 and Windows 11. The prompt usually starts with `PS C:\...` and ends in `>`.

Look at your prompt. If the last character is `$` or `%`, you are in Bash or Zsh; the left column in step 5 is yours. If you see `PS C:\...>`, you are in PowerShell; the right column is yours. Both columns produce the same observable result.

## Step by step

Each step is one line typed at the prompt, followed by pressing Enter. You do not need to type the prompt itself; only the characters after it.

### 1. The plain form (Bash, Zsh, PowerShell behave identically)

Type:

```bash
echo Hello, world
```

You will see:

```text
Hello, world
```

The prompt returns on the line below, ready for the next command.

### 2. With double quotes (Bash, Zsh, PowerShell behave identically)

Type:

```bash
echo "Hello, world"
```

You will see the same line:

```text
Hello, world
```

The output looks identical, but what happened inside the shell is different. The quotes told the shell to treat everything between them as one argument instead of splitting on whitespace. That distinction will matter in later lessons when the text contains a dollar sign, a backtick, or other characters the shell cares about.

### 3. With single quotes (Bash, Zsh, PowerShell behave identically)

Type:

```bash
echo 'Hello, world'
```

You will see:

```text
Hello, world
```

Same output, stricter rule. Single quotes protect the text from every form of shell interpretation. Whatever is between them is sent to echo verbatim.

### 4. With no arguments (Bash, Zsh, PowerShell behave identically)

Type:

```bash
echo
```

You will see a blank line, then the prompt back. Echo with nothing to print still prints a newline. It is a small proof that the command ran.

### 5. With a variable (different in each shell)

Variable expansion is where Bash and PowerShell stop agreeing. Run the version that matches the prompt you saw in **Pick your shell** above.

If your prompt ends in `$` or `%` (Bash or Zsh):

```bash
echo $USER
```

If your prompt starts with `PS C:\...>` (PowerShell):

```powershell
echo $env:USERNAME
```

In both cases you will see your own username printed on the next line. Same observable result, different syntax. The shell looked up the variable before echo ever saw it, and handed echo the result as a plain argument. The "What just happened" section below explains why the two shells use different syntax for the same lookup.

If you ran the wrong column, the output tells you. In PowerShell, `$USER` is an undeclared variable (empty by default), so you get a blank line. In Bash or Zsh, `$env:USERNAME` parses as the empty `$env` followed by literal `:USERNAME`, so the line `:USERNAME` is printed. Check your prompt, pick the right column, and re-run.

![Static side-by-side panel showing the same five echo exchanges in Bash on the left and PowerShell on the right](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-003-terminal.png)

## Check it worked

After step 1, the exact text `Hello, world` should appear on the line directly below your command. The prompt should return on the line after that, blinking cursor and all. If you see a message like `command not found: ech` or `'echo' is not recognized`, you typed a letter wrong. Retype and try again.

If you see literal quote marks in the output (`"Hello, world"` or `'Hello, world'`), the quote characters came from a word processor that swapped straight quotes for curly ones when you pasted. Type the line directly in the terminal instead of pasting from a document.

If steps 1, 2, and 3 each produced the exact string `Hello, world` on the next line, step 4 produced a blank line followed by the prompt, and step 5 produced your own username, the lesson is done. You have executed a command, confirmed its output, and returned the terminal to a ready state. Three times over, in the shell you actually have open.

## What just happened

Echo is a built-in command whose job is to print its arguments to the screen, joined by single spaces, followed by a newline. That is the whole of it. The interesting work happened before echo was called.

The shell, the program that reads your keystrokes, did two things to your line before echo saw anything. First, it split the line into tokens using whitespace as the separator, so `echo Hello, world` became three tokens: `echo`, `Hello,`, and `world`. Second, when it saw a variable reference (`$USER` in Bash, `$env:USERNAME` in PowerShell), it expanded the variable to its current value and replaced the token with that value. Only after that did it hand the list of tokens to echo and ask echo to print them.

That two-step process explains the three small surprises in the exercise. No-quotes and double-quotes look identical because the whitespace inside `Hello,` and `world` lands in the same place either way. Single quotes would have mattered if you had written `echo '$USER'` (which prints the literal string `$USER`) compared with `echo "$USER"` (which prints your username). The no-arguments case printed a blank line because echo still emits the trailing newline even when it has nothing else to say.

The split between `$USER` and `$env:USERNAME` is the deliberate design of the two shells. Bash keeps shell variables, environment variables, and built-ins like `USER` in one flat namespace, where `$name` means "look it up." PowerShell separates user-defined variables (in the bare `$name` namespace) from inherited environment variables (under `$env:name`). Same idea, two cabinets. The price of the cleaner separation is the extra prefix; the price of the flat namespace is the silent blank line a Windows reader gets when they type a Bash example.

The CLI rhythm you just felt is the atom of every interaction in this curriculum. Argument in, result out, prompt back, ready for the next one. Python will feel like this. Git will feel like this. Terraform will feel like this. The answers get more interesting, but the rhythm does not change.

## Going further

Try two more variables your shell already knows about. Use the column that matches the shell you have open.

Bash or Zsh:

```bash
echo $HOME
echo $SHELL
```

`$HOME` prints the absolute path of your home directory. `$SHELL` prints the path of the shell program reading these commands (for example, `/bin/zsh` or `/bin/bash`).

PowerShell:

```powershell
echo $env:USERPROFILE
echo $env:COMSPEC
```

`$env:USERPROFILE` prints the absolute path of your home directory (for example, `C:\Users\elvis`). `$env:COMSPEC` prints the path of the legacy command interpreter Windows still ships (`C:\Windows\system32\cmd.exe`); it is the closest single-line analogue to `$SHELL`. All four variables are set automatically when you log in, and all will reappear in later lessons on environment variables and on filesystem navigation.

For one more small experiment, run the dense version that puts a variable inside a sentence. Pick your column.

Bash or Zsh:

```bash
echo "My user is $USER and my shell is $SHELL"
```

PowerShell:

```powershell
echo "My user is $env:USERNAME and my shell is $env:COMSPEC"
```

Notice how the shell expanded the variables inside the double-quoted string and handed echo a finished sentence. Same mechanism as before, used more densely.

## What's next

Next is [L-004: Find out where you are with pwd](./L-004-find-out-where-you-are-with-pwd.md), where the command-response rhythm produces a more useful answer: the absolute path of the folder your terminal is standing in.
