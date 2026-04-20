# L-012 transcript — install your first tool with a package manager

Screen-reader transcript of the six-exchange PowerShell-primary walkthrough in `L-012-terminal.gif` / `L-012-terminal.png` / `L-012-terminal.svg`.

## PowerShell (Windows 11)

```powershell
PS C:\Users\learner> winget --version
v1.10.320

PS C:\Users\learner> winget install -e --id GnuWin32.Tree
Found GnuWin32: Tree [GnuWin32.Tree] v1.7.0.4
Downloading and verifying installer...
Successfully installed
(open a new PowerShell window to refresh PATH)

PS C:\Users\learner> tree.exe --version
tree v1.7.0 (c) 1996 - 2014 by Steve Baker,
Thomas Moore, Francesc Rocher, and others.
(tree.exe = GnuWin32; tree alone still runs tree.com)

PS C:\Users\learner> mkdir practice-cli\src
    Directory: C:\Users\learner
d----  practice-cli
(subfolder src created too)

PS C:\Users\learner> "hi" > practice-cli\README.md
(file written; no output)

PS C:\Users\learner> tree.exe practice-cli
practice-cli
|-- README.md
`-- src

1 directory, 1 file
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

After `winget install -e --id GnuWin32.Tree` on Windows, the command name `tree` still resolves to the built-in `C:\Windows\System32\tree.com` because `System32` comes before `C:\Program Files (x86)\GnuWin32\bin` on the default `PATH`. Invoke the GNU tree as `tree.exe` to pick up the new binary, or prepend the GnuWin32 bin directory to `PATH` if you want the bare name to resolve to it. L-013 covers the environment-variable plumbing that makes this choice; here the lesson simply names the consequence.

On macOS (Homebrew) and Debian-family Linux (`apt`) there is no second binary to collide with, so `brew install tree` followed by `tree` just works. The same is true for WSL, since WSL runs a Linux user space where the Windows `tree.com` is not on `PATH`.
