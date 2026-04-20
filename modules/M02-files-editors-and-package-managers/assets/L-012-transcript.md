# L-012 transcript — install your first tool with a package manager

Screen-reader transcript of the six-exchange PowerShell-primary walkthrough in `L-012-terminal.gif` / `L-012-terminal.png` / `L-012-terminal.svg`.

**A note on the visuals.** The rendered GIF, PNG, and SVG show the PowerShell column verifying and running the GnuWin32 binary as `tree.exe`. That is the ideal end state after you extend `PATH` to include `C:\Program Files (x86)\GnuWin32\bin` (covered in L-013). The lesson article itself uses two PATH-independent substitutes on the Windows side — `winget list GnuWin32.Tree` to confirm the install, and the built-in `tree /f` to draw the outline — because the GnuWin32 installer does not always add its folder to `PATH`. This transcript records the article's commands so a reader relying on a screen reader can follow what a learner actually types today.

## PowerShell (Windows 11)

```powershell
PS C:\Users\learner> winget --version
v1.10.320

PS C:\Users\learner> winget install -e --id GnuWin32.Tree
Found GnuWin32: Tree [GnuWin32.Tree] v1.7.0.4
Downloading and verifying installer...
Successfully installed

PS C:\Users\learner> winget list GnuWin32.Tree
Name          Id             Version   Source
-----------------------------------------------
GnuWin32:Tree GnuWin32.Tree  1.7.0.4   winget
(install confirmed without relying on PATH)

PS C:\Users\learner> mkdir practice-cli\src
    Directory: C:\Users\learner
d----  practice-cli
(subfolder src created too)

PS C:\Users\learner> Set-Content -Path practice-cli\README.md -Value "hi"
(file written; no output)

PS C:\Users\learner> tree /f practice-cli
Folder PATH listing for volume Windows
Volume serial number is 70F0-03BC
C:\USERS\LEARNER\PRACTICE-CLI
│   README.md
│
└───src
(the built-in tree, with /f, prints files alongside folders)
```

## Bash (macOS; Linux/WSL use `sudo apt install tree` in place of `brew`)

```bash
learner@laptop:~$ brew --version
Homebrew 4.2.13

learner@laptop:~$ brew install tree
==> Fetching tree
==> Pouring tree--2.2.1.arm64.bottle.tar.gz
/opt/homebrew/Cellar/tree/2.2.1: 8 files
(command tree is now on your PATH)

learner@laptop:~$ tree --version
tree v2.2.1 (c) 1996 - 2024 by Steve Baker,
Thomas Moore, Francesc Rocher, Florian Sesser
(the new command is on PATH after the install)

learner@laptop:~$ mkdir -p practice-cli/src
(both folders created; no output)

learner@laptop:~$ echo hi > practice-cli/README.md
(file written; no output)

learner@laptop:~$ tree practice-cli
practice-cli
├── README.md
└── src

1 directory, 1 file
```

## Cross-shell takeaway

After `winget install -e --id GnuWin32.Tree` on Windows, the command name `tree` still resolves to the built-in `C:\Windows\System32\tree.com` because `System32` is on `PATH` and `C:\Program Files (x86)\GnuWin32\bin` often is not. The lesson therefore leans on two PATH-independent Windows tools for today: `winget list GnuWin32.Tree` confirms the package is installed (by asking the package manager, not the shell), and the built-in `tree /f` draws the folder outline with files included. L-013 covers the environment-variable plumbing that would let you call the GNU `tree.exe` by its bare name as well; here the lesson simply names the consequence and works around it.

On macOS (Homebrew) and Debian-family Linux (`apt`) there is no second binary to collide with, so `brew install tree` followed by `tree` just works. The same is true for WSL, since WSL runs a Linux user space where the Windows `tree.com` is not on `PATH`.
