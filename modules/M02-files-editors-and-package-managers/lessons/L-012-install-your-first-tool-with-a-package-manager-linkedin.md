The first command-line tool I installed the "old" way ended up in two folders I could not remember, at two different versions, with one of them broken. The second one I installed through a package manager. That took thirty seconds, worked the first time, and I could remove it in one command. Today you install your first tool that way, and you see a folder the way a book's table of contents shows chapters.

**From zero technical knowledge to AI literacy.**
Through data, cloud, MLOps, and applied GenAI systems.

Day 12 of 171. Module 2: Files, Editors, and Package Managers (Day 5).

The tool is `tree`. Its job is to print one root, its sub-folders, and the files under each, as an American Standard Code for Information Interchange (ASCII) outline. Six steps on the Command-Line Interface (CLI): confirm the package manager, install `tree`, verify the new command, make a small sample folder, drop a file inside it, and run `tree`.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm the package manager, install tree via winget or brew, verify the install with tree.exe or tree --version, make a practice-cli folder with a src subfolder, drop a README.md inside, run tree on the result](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-012-terminal.gif)

**The analogy**

Ordering a kitchen gadget online. The catalog is the package manager's repository. The click-to-order is `winget install`, `brew install`, or `apt install`. The box showing up at your door is the binary arriving in a folder your shell already knows about. After today the same three-word command installs every command-line tool you meet in the rest of this curriculum.

**The install, side by side**

On Windows 11 (PowerShell), `tree` ships as a GNU's Not Unix (GNU) port named `GnuWin32.Tree`:

```powershell
winget install -e --id GnuWin32.Tree
```

The `-e` flag forces an exact match on the package ID instead of a substring search. Close that PowerShell window after it finishes and open a fresh one; the installer adds a new folder to the `PATH` environment variable (PATH), which is the list of folders your shell searches when you type a command name, and a new shell is the simplest way to pick the change up.

On macOS (Terminal), the command is:

```bash
brew install tree
```

On Debian-family Linux or the Windows Subsystem for Linux (WSL), use `sudo apt install tree` instead. The rest of the lesson works the same way regardless of which you ran.

**One cross-platform detail worth knowing**

On Windows, typing `tree` on its own still runs the built-in `tree.com` in `C:\Windows\System32`, because that folder comes earlier on `PATH` than the new GnuWin32 folder. The built-in is a minimal MS-DOS-era version. The GNU port is the one we just installed. To pick it up, name the binary as `tree.exe`:

```powershell
tree.exe --version
```

On macOS and Linux, there is no second tree, so `tree --version` is enough. This is the first time `PATH` ordering matters in the curriculum. Tomorrow's lesson (L-013) takes environment variables apart, starting with one you create yourself.

**The tiny sample and the payoff**

Two more commands build something for `tree` to draw:

```powershell
mkdir practice-cli\src
"hi" > practice-cli\README.md
```

```bash
mkdir -p practice-cli/src
echo hi > practice-cli/README.md
```

Then run `tree` on it. The GNU binary prints:

```text
practice-cli
├── README.md
└── src

1 directory, 1 file
```

(On the Windows GNU port the branches render as `|--` and `` `-- `` instead of `├──` and `└──`; the meaning is identical.)

That is the whole payoff. Every `├──` is a peer entry; every `└──` is the last entry in a folder. There is no information in the picture that is not on disk, so once you read a tree fluently you can picture a whole project as a small drawing. Most open-source `README.md` files paste a tree of the repository near the top for exactly this reason.

**What you are actually watching happen**

A `brew install tree` or `winget install GnuWin32.Tree` is three steps in one command. The manager looks up the name in its curated repository, downloads the build that matches your operating system (OS) and processor, and places the binary in a folder the OS already has on `PATH`. Before package managers were the default on every platform, those three steps were a browser download, an installer wizard, and usually a `PATH` edit. Every step was a place a version mismatch or a wrong architecture could eat an afternoon. One line, one answer, one version: that is the whole reason package managers won.

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
