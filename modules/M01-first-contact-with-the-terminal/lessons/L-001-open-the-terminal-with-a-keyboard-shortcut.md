---
lesson_id: L-001
sequence_number: 1
module_id: M01
domain_id: D01
title: "Open the terminal with a keyboard shortcut"
week_number: 1
day_in_week: 1
estimated_minutes: 10
capture_mode: script_only
risk_level: low
is_capstone: false
published_at: 2026-04-18T00:00:00Z
acronyms_expanded: [AI, CLI, OS]
---

Think of the terminal as the kitchen of your computer. The door is closed most of the time. You can see the rest of the house, the windows and menus and apps, but the kitchen is sealed. Nothing gets cooked in there until someone actually opens the door and walks in. Every professional who works with servers, cloud infrastructure, or Artificial Intelligence (AI) systems spends their day in that kitchen. The first skill, before any command or syntax, is opening the door. You are about to do exactly that, using only your keyboard, on whichever Operating System (OS) you use.

![Side-by-side walkthrough of opening a terminal, Bash (macOS Spotlight / Linux GNOME) on the left and PowerShell (Windows 11 Start) on the right](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-walkthrough.gif)

## What you will do

Open the built-in terminal application on your computer using a keyboard shortcut, and leave the window on screen for the next lesson.

## Before you start

This is the first lesson, so there is no prior lesson to check. What you need is simpler than that:

- A personal computer running macOS, Windows 11, or a recent Linux distribution with the GNOME desktop (Ubuntu, Fedora, or Debian all qualify).
- A regular user account on that machine. You do not need administrator rights for this lesson. You do not need to install anything.
- Five to ten minutes of quiet time.

If you are borrowing a locked-down work laptop that blocks the built-in terminal, stop and use a personal machine instead. Everything in this curriculum assumes you can open the terminal without a ticket to IT.

## Step by step

Pick the block that matches your Operating System. Run those three keystrokes and nothing else for now.

### On macOS

1. Press **Command + Space**. A small search panel appears in the middle of your screen. This is Spotlight.
2. Type the word `terminal`. The top result is the built-in Terminal application.
3. Press **Return**. The Terminal window opens.

![macOS Spotlight search with "terminal" typed and the Terminal app highlighted](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-screen-macos.png)

### On Windows 11

1. Press the **Windows key** (the one with the four-square logo, bottom-left of the keyboard). The Start menu appears with a search box at the top.
2. Type the word `terminal`. The top result under "Best match" is Windows Terminal.
3. Press **Enter**. The Terminal window opens.

![Windows 11 Start menu with "terminal" typed and Windows Terminal highlighted as the best match](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-screen-windows.png)

Windows 11 ships with Windows Terminal as the default terminal application. If you are on Windows 10, you may see "Command Prompt" or "Windows PowerShell" at the top instead. Either is fine for this lesson; pick whichever is highlighted.

### On Linux (GNOME)

1. Press the **Super key** (the Windows key, by another name). The Activities overlay appears with a search bar at the top.
2. Type the word `terminal`. The top result is GNOME Terminal, shown as "Terminal" with a square icon.
3. Press **Enter**. The Terminal window opens.

![GNOME Activities overlay with "terminal" typed and the Terminal app highlighted](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-screen-linux.png)

Most Linux distributions also honor the shortcut **Ctrl + Alt + T** as a direct keypress to open a terminal, skipping the search entirely. If that combination does nothing on your distribution, the search-based path above always works.

## Check it worked

A Terminal window is on your screen. It looks something like this:

![An open terminal window with a prompt and a blinking cursor](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-001-terminal-window.png)

Three specific things should be visible.

1. A **window** with its own title bar and controls, separate from your browser and other applications.
2. A line of text ending in a character like `$`, `%`, or `>`. That line is called the prompt. You decode it in the next lesson.
3. A **cursor** to the right of the prompt, blinking on and off about once per second.

If all three are there, you are in.

If nothing happens when you press Enter in the search box, the shortcut may be rebinding. Open Settings, look for "Keyboard shortcuts," and confirm that the system-wide search shortcut is still set to the default. If the search returns no result for the word `terminal`, your system may use a different name for it. On macOS, you can also open Finder, navigate to Applications, then Utilities, and double-click Terminal. On Windows 11, open the Start menu with the mouse and scroll to Windows Terminal under the pinned apps. On Linux, open the app grid and look under System Tools. These fallbacks are slower than the keyboard, which is exactly why the keyboard shortcut is worth the minute it takes to remember.

## What just happened

You launched a Command-Line Interface (CLI) program. A CLI is any program whose primary way of taking input is text typed at a prompt, not a mouse pointer aimed at a button. The Terminal application is the container for that text. Everything else in this curriculum, running code, moving files around, talking to a cloud, training a small model, happens inside some form of this window.

Using the keyboard to open the terminal is a small choice with a long payoff. Every time you reach for the mouse to hunt through menus, you break the rhythm of typing. Reaching the terminal with three keystrokes and leaving the mouse alone is the first rep of a motion you will repeat many thousands of times.

Leave the window open for the next lesson.

## Going further

If the text in the terminal looks too small to read comfortably, fix that now. Eye strain is the reason people stop practicing.

- **macOS Terminal:** Press **Command + ,** (comma) to open Settings. Under the Profile tab, set Font to a size between 14 and 16 points.
- **Windows Terminal:** Press **Ctrl + ,** (comma) to open Settings. Under Defaults, set Font size to 14 or 16.
- **GNOME Terminal:** Open the hamburger menu in the top-right corner, choose Preferences, then set Font to 14 or 16.

Then resize the window by dragging a corner until it covers about half your screen. That is the size you will use for every lesson in this module.

## What's next

Next is [L-002: Read a prompt like a sign at a train station](../L-002-read-a-prompt-like-a-sign.md), where you learn to decode the text to the left of the cursor so the prompt stops being a mystery and starts being a map.
