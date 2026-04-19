---
lesson_id: L-002
sequence_number: 2
module_id: M01
domain_id: D01
title: "Read a prompt like a sign at a train station"
week_number: 1
day_in_week: 2
estimated_minutes: 10
capture_mode: script_only
risk_level: low
is_capstone: false
published_at: 2026-04-19T00:00:00Z
acronyms_expanded: [CLI, OS, PS1]
---

A sign at a train station does three quiet jobs. It tells you where you are (the platform), who is there with you (the line or carriage), and that a train is about to depart (the next destination). The prompt on your terminal does the same three jobs. It is a status bar disguised as a handful of symbols. Once you can point at each piece and name what it is, the Command-Line Interface (CLI) stops looking like a riddle and starts looking like a sign. You are about to walk over to your prompt, label the parts, and write them down.

![Animated walkthrough of the four parts of a shell prompt on macOS, Linux, and Windows](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-002-walkthrough.gif)

## What you will do

Look at the prompt in your open terminal window, identify the four parts, and write them down on paper or in a note app so you can recite them from memory.

## Before you start

You need an open terminal window from [L-001: Open the terminal with a keyboard shortcut](./L-001-open-the-terminal-with-a-keyboard-shortcut.md). If you closed it, reopen it now. You also need something to write with. A sticky note, the Notes app, a text file, any of them works. The point is to move the information out of the screen and into your own handwriting or typing, which is how the four names stick.

No commands will be run that change anything on your machine. This lesson is pure observation, with one optional peek at the template string in the final section.

## Step by step

Below are three annotated screens, one for each Operating System (OS) you are likely to be in front of. Find the block that matches yours. Your prompt will look almost exactly like the picture, with your own username, your own machine name, and your own folder name in place of the examples.

### The pattern, on paper

![A generic shell prompt with four callouts naming the username, machine name, current directory, and prompt character](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-002-anatomy.png)

Regardless of your OS, the four questions are always the same:

1. **Who am I on this machine?** Username.
2. **Which machine am I on?** Hostname.
3. **Where in the filesystem am I standing?** Current directory.
4. **Is the machine waiting for my next command?** Prompt character.

Write those four questions down before you look at your own prompt. That is the template you will fill in.

### On macOS (Zsh)

Your prompt looks something like `learner@MacBook-Pro ~ %`.

![Annotated macOS Zsh prompt with callouts for username, machine name, directory, and prompt character](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-002-prompt-macos.png)

1. The piece before the `@` is your **username**. In the picture it is `learner`; yours will be whatever you signed into the Mac with.
2. The piece after the `@` and before the space is the **machine name**. In the picture it is `MacBook-Pro`; yours might be `Elvis-MacBook-Air`, `Jane-iMac`, or anything you chose in System Settings.
3. After another space comes the **current directory**. The tilde character `~` is shorthand for your home folder, `/Users/<your-username>`. A fresh terminal window always opens in your home folder.
4. The `%` is the **prompt character**. On Zsh, the default Mac shell since macOS Catalina, it is always `%` for a regular user. The cursor blinks to the right of it.

### On Linux (Bash on Ubuntu, Fedora, or Debian)

Your prompt looks something like `learner@laptop:~/projects$`.

![Annotated Linux Bash prompt with callouts for username, machine name, directory, and prompt character](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-002-prompt-linux.png)

1. The piece before the `@` is your **username**.
2. The piece between `@` and `:` is the **machine name** (hostname).
3. The piece after the `:` and before the `$` is the **current directory**. The tilde `~` means home; `~/projects` means a folder called `projects` inside your home folder.
4. The `$` is the **prompt character**. On Bash as a regular user it is always `$`. If you ever see `#` here, you are running as the root user, which is a risk topic for a later lesson.

### On Windows 11 (PowerShell in Windows Terminal)

Your prompt looks something like `PS C:\Users\learner>`.

![Annotated Windows PowerShell prompt with callouts for shell indicator, directory, and prompt character](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-002-prompt-windows.png)

PowerShell hides two of the four tokens to keep the line short. Name what you see:

1. `PS` is the **shell indicator**. It tells you that PowerShell, not Command Prompt, is the program reading your keystrokes. Command Prompt has no `PS` in front, it just shows the path.
2. `C:\Users\learner` is the **current directory**, written in the full Windows style with the drive letter and backslashes. PowerShell does not use the tilde shorthand.
3. `>` is the **prompt character**.

The other two tokens still exist, they are just not in the line. To see your username, type `whoami` and press Enter. To see your machine name, type `hostname` and press Enter. Both commands print one line and return you to the prompt.

### Write it down

Now open your note and write four lines:

```text
Username: <what you see in your prompt, or the output of whoami>
Machine: <what you see, or the output of hostname>
Directory: <the path or the ~ you see>
Prompt character: <$ or % or >>
```

Fill in your own values. This is the entire hands-on step. Two minutes.

## Check it worked

Close the note. Look away from the screen. From memory, recite the four pieces of your own prompt out loud (or to a rubber duck, or a housemate who will humor you). Then look back at the terminal and confirm each one.

You pass the check if you can name all four without looking. If one slips, read it again and try once more. The names are what you will use every time you ask for help on Stack Overflow, every time a tutorial says "your working directory", every time a colleague pastes a snippet into Slack and you have to read it.

If the Windows PowerShell prompt only gives you two of the four, pass the check with the two you can see (shell indicator, directory, prompt character counted as three since `PS` is really an indicator). The missing two are recoverable with `whoami` and `hostname` whenever you want them.

## What just happened

You read the prompt as information instead of noise. That reframe is the whole lesson.

The prompt is generated by your shell every time it is ready to accept a command. A shell is the program that sits between you and the computer, taking your text and turning it into work. Bash and Zsh are the common shells on macOS and Linux; PowerShell is the default on Windows 11. Each shell has a template that describes what to print: usernames, hostnames, directories, colors, the time, the battery level, whatever you want. The template is kept in an environment variable.

On Bash and Zsh, that variable is called Prompt String 1 (PS1). The default template on a Debian-family Linux is roughly `\u@\h:\w\$`, where `\u` is username, `\h` is hostname, `\w` is working directory, and `\$` is the prompt character. On Zsh the same four pieces use different codes: `%n@%m %1~ %#`. PowerShell uses a function called `prompt` rather than a variable, but the idea is identical: a template is evaluated every time the shell returns control to you.

You do not need to memorize those codes. You do need to remember that the prompt is made of pieces, each piece answers a question, and any of the pieces can be changed or hidden.

## Going further

Peek at the raw template. Nothing is saved or changed; you are reading, not editing.

On macOS or Linux, run:

```bash
echo $PS1
```

The output looks like `%n@%m %1~ %# ` on Zsh or a string with `\u`, `\h`, `\w`, `\$` on Bash. Notice how each of your four tokens maps to one of those escape codes.

On Windows PowerShell, run:

```powershell
Get-Content Function:prompt
```

The output is a short PowerShell function that builds the line you see. It is more readable than the Bash escape codes, but it does the same job.

Changing the template is a later lesson. The point of peeking now is to prove to yourself that the prompt is software, not a fixed feature of the window.

## What's next

Next is [L-003: Print your first line with echo](./L-003-print-your-first-line-with-echo.md), where you type your first actual command, and the terminal types something back. That is the full command-response rhythm in one keystroke.
