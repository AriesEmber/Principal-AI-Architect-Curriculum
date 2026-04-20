---
lesson_id: L-011
sequence_number: 11
module_id: M02
domain_id: D01
title: "Install a package manager"
week_number: 2
day_in_week: 4
estimated_minutes: 13
capture_mode: script_only
risk_level: medium
is_capstone: false
published_at: 2026-04-20T00:00:00Z
acronyms_expanded: [CLI, OS, URL, HTTPS]
---

Think of a package manager as a delivery subscription for software. Before the subscription, every grocery run was a separate trip: drive to the store, find the aisle, read the label, carry the bag home, repeat for the next thing. After the subscription, you text one address and the box shows up on your porch the next day. A package manager works the same way for command-line tools. You set it up once. Every future tool you want, you ask the package manager for it by name, and the tool shows up on your machine without a web download, a zip, or an installer wizard. Today you set up that subscription on whichever Operating System (OS) you use. Windows 11 and modern Linux ship the subscription already active, so the task is to confirm it. macOS needs a one-time install. Either way, at the end of this lesson a package manager answers a version check with a clean line of text.

![Three-column walkthrough: Windows 11 PowerShell on the left checking winget, macOS Terminal in the middle installing Homebrew and running brew --version, Linux Terminal on the right checking apt](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-011-walkthrough.gif)

## What you will do

Install a package manager (macOS) or confirm the one your OS already ships (Windows, Linux) and print its version number.

## Before you start

You need to have completed [L-010: Understand file paths, extensions, and hidden files](./L-010-understand-file-paths-extensions-and-hidden-files.md) and have a terminal open at your home directory. Run `Get-Location` (PowerShell) or `pwd` (Bash) if you need to confirm where you are standing.

This lesson branches by Operating System. Each block below is self-contained: pick the one that matches your machine and run only that block. The three blocks use three different package managers because each OS has its own default. You do not need the other blocks.

Two more preflight items. First, the macOS block asks for your login password, so be ready to type it once. Second, all three blocks talk to the internet: the installer on macOS downloads its script from GitHub, and both winget and apt check their repositories to report their version. A live connection is enough; no company network or special configuration is needed.

## Step by step

### On Windows 11 (PowerShell)

Windows 11 ships the Windows Package Manager, whose Command-Line Interface (CLI) is named `winget`, as part of a system component called App Installer. You do not install it; you confirm it. In your PowerShell window, type:

```powershell
winget --version
```

You should see a version string, something like:

```text
v1.10.320
```

The exact number will differ because App Installer updates itself through the Microsoft Store. Any `v1.x` line means you are ready.

![Windows 11 PowerShell window running winget --version and printing a version string like v1.10.320](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-011-screen-windows.png)

If the line `winget: The term 'winget' is not recognized` appears, the App Installer registration did not finish. This happens on a freshly imaged Windows 11 machine where you have logged in for the first time only minutes ago. Run:

```powershell
Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
winget --version
```

The first line re-registers the App Installer package for your user; the second line runs the version check again. You are done when the version prints.

### On macOS (Terminal)

macOS does not ship a default package manager, so you install one: Homebrew. Homebrew is community-maintained, and its official install command lives on its home page at [brew.sh](https://brew.sh). You paste one command into Terminal and wait.

> **Heads up.** The next command downloads an installer script over Hypertext Transfer Protocol Secure (HTTPS) from the Homebrew GitHub repository and runs it on your machine. The script is the project's official installer, and it pauses to show you exactly what it will do before acting. But once the install completes, removing Homebrew is a separate uninstall command, not a simple undo. Only paste the command if you are installing Homebrew on purpose.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The `/bin/bash -c "..."` wrapper tells your shell to run the quoted text inside a fresh Bash process, regardless of whether your interactive shell is Zsh, Bash, or Fish. Inside the quotes, `curl -fsSL <url>` downloads the installer script from the Uniform Resource Locator (URL) at `raw.githubusercontent.com`, and the `$(...)` syntax hands the downloaded text to `bash` as the script to run.

Three things happen in order. First, the installer prints a list of what it will install (the `brew` command, its support folders under `/opt/homebrew`, and a few helper tools) and pauses for you to press Return. Second, it asks for your login password so it can use `sudo` to create directories owned by root. Third, it downloads and installs Homebrew itself. The whole run takes two to five minutes on a modern machine.

![macOS Terminal paste of the Homebrew install command, the installer's password prompt and install-successful message, then brew --version printing Homebrew 4.2.13](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-011-screen-macos.png)

When the installer finishes, it prints a short "Next steps" block with two lines to paste. The first is an `eval` command that adds the `brew` command to your shell's `PATH` environment variable, which is the list of folders your shell scans when you type a command name. Paste that line into the same Terminal window and press Return. Then confirm the install with:

```bash
brew --version
```

Expected output:

```text
Homebrew 4.2.13
```

The exact number will be whatever version is current the day you run this.

### On Linux (Debian or Ubuntu, Terminal)

Debian-family Linux (Debian, Ubuntu, Linux Mint, Pop!_OS, Raspberry Pi OS, and the Windows Subsystem for Linux when you chose Ubuntu) ships the Advanced Package Tool, whose command is `apt`. It is already present on every install. Confirm with:

```bash
apt --version
```

Expected output:

```text
apt 2.7.14 (amd64)
```

Numbers will vary.

![Linux Terminal running apt --version and printing apt 2.7.14 (amd64)](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-011-screen-linux.png)

If your distribution is not Debian-family, the command name is different but the idea is the same. Fedora and Red Hat Enterprise Linux use `dnf`; Arch uses `pacman`; openSUSE uses `zypper`. Run the version check for whichever one your distribution ships:

```bash
dnf --version      # Fedora, RHEL
pacman --version   # Arch, Manjaro
zypper --version   # openSUSE
```

One of these prints a version. That is your package manager, and the next lesson works with whichever one you have.

## Check it worked

Run the version command one more time. A single line of text with a version number on it means you are done. Specifically:

- **Windows 11** prints something like `v1.10.320`. If instead you see `'winget' is not recognized`, the App Installer did not register; re-run the `Add-AppxPackage` line in the Windows block above.
- **macOS** prints `Homebrew 4.x.x`. If instead you see `brew: command not found`, the installer's PATH step did not land. Open a new Terminal window and try `brew --version` again; the PATH change only applies to shells started after the installer finished. If it still fails, re-run the two-line `eval` block from the installer's "Next steps" output.
- **Linux** prints `apt 2.x.x (amd64)` on Debian-family, or `dnf 4.x.x`, `Pacman v6.x.x`, or `zypper 1.x.x` on the other families. If the command does not print, you are on a distribution I have not listed; run `which dnf || which pacman || which zypper || which apt` to find the one that is installed.

Once any of these commands prints a version, the subscription is live. You now have a tool that knows how to install other tools.

## What just happened

A package manager is a CLI that does three jobs you used to do by hand: it finds the software you asked for in a curated repository, it downloads the right build for your OS and processor, and it installs the files into the places your system expects them. When you want to upgrade or remove the tool later, the package manager handles that too, because it recorded what it put where.

The three commands in this lesson look small but they do more than report a version. They also confirm that the manager's repository connection is working, which is what "ready to install the next tool" actually means.

The trust model is the part worth noticing. When you download a tool from a random website, you are trusting that one website, one file, one time. When you install the same tool through a package manager, you are trusting the manager's curated repository: Microsoft's `winget-pkgs` list on Windows, Homebrew's `core` tap on macOS, Debian's package archive on Linux. These repositories have maintainers, review processes, and cryptographic signatures. You still decide which repositories to trust, and you still read what you are installing, but the gap between "a random website" and "a curated repository with a paper trail" is the reason package managers have become the default way to install command-line software on every major OS.

Three quick mappings to carry forward. Windows uses winget (Microsoft, built in since Windows 10 version 1809). macOS uses Homebrew (community, installed from brew.sh). Debian and Ubuntu use apt (Debian, built in since the late 1990s); other Linux families use dnf, pacman, or zypper depending on the distribution. Every command-line install in the rest of this curriculum assumes one of these is on your machine.

## Going further

Open the home page for the package manager you set up and find the page that explains the `search` command:

- winget: [https://learn.microsoft.com/windows/package-manager/winget/search](https://learn.microsoft.com/en-us/windows/package-manager/winget/search)
- Homebrew: [https://brew.sh](https://brew.sh), then the "Documentation" link in the top navigation, then the `brew search` entry.
- apt: `man apt` in your terminal prints the manual page, and the section on subcommands lists `search`.

Run the search command with a term you care about. Try `winget search python`, `brew search ffmpeg`, or `apt search jq`. Read the first few results. You do not need to install anything yet; this is a tour of what the manager knows about.

## What's next

Next is [L-012: Install your first tool with a package manager](./L-012-install-your-first-tool-with-a-package-manager.md), where you place the first order on the subscription you just set up.
