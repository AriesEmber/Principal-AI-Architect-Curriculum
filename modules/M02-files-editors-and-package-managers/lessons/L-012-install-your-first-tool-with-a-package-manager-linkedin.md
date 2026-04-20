The first command-line tool I installed the "old" way ended up in two folders I could not remember, at two different versions, with one of them broken. The second one I installed through a package manager. That took thirty seconds, worked the first time, and I could remove it in one command. Today you install your first tool that way, and you see a folder the way a book's table of contents shows chapters.

**From zero technical knowledge to AI literacy.**
Through data, cloud, MLOps, and applied GenAI systems.

Day 12 of 171. Module 2: Files, Editors, and Package Managers (Day 5).

The tool is `tree`. Its job is to print one root, its sub-folders, and the files under each, as an American Standard Code for Information Interchange (ASCII) outline. Six steps on the Command-Line Interface (CLI): confirm the package manager, install `tree`, verify the package landed, make a small sample folder, drop a file inside it, and run `tree` on it.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm the package manager, install tree via winget or brew, verify the install (winget list on Windows, tree --version on macOS), make a practice-cli folder with a src subfolder, drop a README.md inside, run tree on the result. The PowerShell column in the visual shows the GnuWin32 tree.exe once PATH is extended (covered in L-013); the live walkthrough in this post uses Windows' built-in tree /f, which is always on PATH](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.gif)

**The analogy**

Ordering a kitchen gadget online. The catalog is the package manager's repository. The click-to-order is `winget install`, `brew install`, or `apt install`. The box showing up at your door is the binary arriving in a folder your shell already knows about. After today the same three-word command installs every command-line tool you meet in the rest of this curriculum.

**The install, side by side**

On Windows 11 (PowerShell), `tree` ships as a GNU's Not Unix (GNU) port named `GnuWin32.Tree`:

```powershell
winget install -e --id GnuWin32.Tree
```

The `-e` flag forces an exact match on the package ID instead of a substring search. Expect three or four lines ending in `Successfully installed`.

On macOS (Terminal), the command is:

```bash
brew install tree
```

On Debian-family Linux or the Windows Subsystem for Linux (WSL), use `sudo apt install tree` instead. The rest of the lesson works the same way regardless of which you ran.

**One cross-platform detail worth knowing**

On Windows, the GnuWin32 installer drops `tree.exe` under `C:\Program Files (x86)\GnuWin32\bin`, but does not always add that folder to the `PATH` environment variable (PATH) — the list of folders your shell searches when you type a command name — so typing `tree.exe` can still return `not recognized`. A PATH-independent way to confirm the install landed is to ask the package manager directly:

```powershell
winget list GnuWin32.Tree
```

For today's folder view, reach for the `tree` that Windows already ships: a minimal MS-DOS-era `tree.com` in `C:\Windows\System32`, always on `PATH`. It hides files by default, but a one-letter switch (`/f`) makes it print them. On macOS and Linux, there is no second tree to worry about, so `tree --version` and `tree` are enough. Tomorrow's lesson (L-013) takes environment variables apart and shows how to extend `PATH` so the GnuWin32 `tree.exe` resolves by its bare name too.

**The tiny sample and the payoff**

Two more commands build something for `tree` to draw:

```powershell
mkdir practice-cli\src
Set-Content -Path practice-cli\README.md -Value "hi"
```

```bash
mkdir -p practice-cli/src
echo hi > practice-cli/README.md
```

Then run `tree` on it. On macOS or Linux, `tree practice-cli` prints:

```text
practice-cli
├── README.md
└── src

1 directory, 1 file
```

On Windows, `tree /f practice-cli` prints a volume header and the same layout using the console's box-drawing glyphs:

```text
C:\USERS\YOU\PRACTICE-CLI
│   README.md
│
└───src
```

(The `/f` switch is the one that tells the built-in to include files; without it, only `src` shows up and `README.md` appears to be missing.)

That is the whole payoff. Every `├──` is a peer entry; every `└──` is the last entry in a folder. There is no information in the picture that is not on disk, so once you read a tree fluently you can picture a whole project as a small drawing. Most open-source `README.md` files paste a tree of the repository near the top for exactly this reason.

**What you are actually watching happen**

A `brew install tree` or `winget install GnuWin32.Tree` is three steps in one command. The manager looks up the name in its curated repository, downloads the build that matches your operating system (OS) and processor, and places the binary on disk. On Homebrew the third step also extends `PATH` so the new name resolves immediately. On older Windows packages like GnuWin32 the `PATH` edit is still yours to make (covered in L-013). Before package managers were the default on every platform, all three steps were a browser download, an installer wizard, and usually a manual `PATH` edit. Every step was a place a version mismatch or a wrong architecture could eat an afternoon. One line, one answer, one version: that is the whole reason package managers won.

There is also a trust story underneath. Installing from a random website means trusting one website, one download, one time. Installing through a package manager means trusting a curated repository with maintainers, a review process, and cryptographic signatures. Microsoft's `winget-pkgs`, Homebrew's `homebrew-core`, and the Debian archive each publish their review process and let you audit the source of any package before you install. You usually will not audit, and you do not have to. But when a security advisory lands a month from now, you can name exactly which repository the binary came from. That audit trail is the feature that matters more than speed.

**A second tool, same pattern**

If you want to confirm the loop is real, install `jq` the same way.

```powershell
winget install -e --id jqlang.jq
```

```bash
brew install jq
```

Then try it on a tiny document:

```bash
echo '{"greeting":"hi","count":3}' | jq .
```

You just installed, verified, and used a second tool in three commands. The pattern does not change as the tools get larger; later in the curriculum the same three steps install Python, Git, and the Terraform binary.

Full lesson with the full command list, the three-things-should-be-true verification, and the cross-shell troubleshooting paths: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M02-files-editors-and-package-managers/lessons/L-012-install-your-first-tool-with-a-package-manager.md

Tomorrow: set and read your own environment variable, and find out why `PATH` ordering decided which `tree` ran.

#LearnToCode #AIArchitect #SolutionsArchitecture #PackageManagers #HealthcareAI
