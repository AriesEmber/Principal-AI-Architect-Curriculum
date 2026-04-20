The first time I moved a project folder between my laptop and a remote machine, half my scripts broke because they had absolute paths baked into them. The fix was one rule: treat a path like a postal address, and know which form to write for which job. Today's lesson is that rule, plus two others: what a file extension actually means, and why `ls` on one machine shows different files than `ls` on another.

**From zero technical knowledge to AI literacy.**
Through data, cloud, MLOps, and applied GenAI systems.

Day 10 of 171. Module 2: Files, Editors, and Package Managers (Day 3).

Seven exchanges in the terminal: print your home path, write `note.txt`, read it with a short name and a long name, rename it to `note.md`, read it again, then list the directory with hidden files revealed. Works the same on Windows PowerShell, macOS, Linux, and the Windows Subsystem for Linux (WSL).

The analogy is a postal address. A full address has a country, a city, a street, and a house number. Each part narrows the search. Drop parts from the end and you describe something less specific. A file path works the same way. The drive letter or root is the country. The deepest folder is the street. The filename is the house number. Every file has this kind of address, and there are two conventional ways to write it down.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Seven exchanges: print the home path, write note.txt, read it with a relative path, read it with an absolute path, rename to note.md, read the renamed file, then list the directory with dotfiles revealed](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-010-terminal.gif)

**Two ways to write a path**

The file `note.txt` sitting in your home directory has two honest addresses:

- **Relative.** `note.txt`. Read as "in my current folder." Short. Portable. Stops working if you change folders.
- **Absolute.** `C:\Users\learner\note.txt` on PowerShell, or `/home/learner/note.txt` on Bash. Read as "from the root of the filesystem." Long. Works no matter which folder you are standing in.

There is also a shortcut, `~`, which expands to your home directory in both shells. `cat ~\note.txt` in PowerShell and `cat ~/note.txt` in Bash both read the same file as the absolute form, without making you spell out your username.

Relative paths are what you use most of the time. Absolute paths are what you write into scripts that will run from a scheduled task, a container, or a different person's machine, because "my current folder" means different things to different callers.

**Extensions are labels, not locks**

The suffix after the last dot in a filename is a naming convention. A `.txt` file is usually plain text. A `.md` file is usually Markdown. A `.py` file is usually Python. But no part of the filesystem enforces the convention. You can rename a text file to `.md`, `.sql`, or `.elvis`, and the shell reads the same bytes back.

```text
PS> Rename-Item note.txt note.md
PS> cat note.md
hello paths
```

The content is identical. The rename only changed the label. The operating system (OS) does not check that `.md` content is Markdown. Applications that open files by double-click use the extension to decide which program to launch (a `.md` goes to your Markdown viewer; a `.txt` goes to Notepad), but the shell's `cat` command does not care.

Later in the curriculum you will meet the separate idea of a content type, which is how a web server tells a browser how to interpret a response. The filename extension is a hint to programs on your own machine; the content type is the actual contract over the network.

**Hidden files work differently on Windows and Unix**

Run `ls` in your home directory on Bash and you will see maybe five or ten files. Run `Get-ChildItem` on PowerShell in the same directory and you will see thirty. The difference is not your directory. It is what the two shells consider hidden.

- **Bash** hides any filename that starts with a dot. `.bashrc`, `.gitconfig`, `.ssh`, `.vscode`: all invisible to `ls` until you add `-a`.
- **PowerShell** does not care about the leading dot. It respects the Windows Hidden file *attribute*, which is a separate flag in the filesystem metadata. A file named `.gitconfig` on Windows is visible by default because nothing set its Hidden attribute. `Get-ChildItem -Force` adds files whose Hidden attribute is set.

This means the same home directory, listed on Windows and on WSL, looks different. Not because the files are different. Because the two shells use different rules to decide what to hide.

![Side-by-side static panel of the 7-exchange walkthrough. PowerShell on the left, Bash on the right, with each exchange showing the command, its output, and a short comment line](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-010-terminal.png)

**Why hidden at all?**

Hiding is not security. Anyone with a terminal can list a hidden file if they know to ask for it, and anyone with read permission can read its contents. Hiding is tidying. Your home directory collects per-user configuration files over time, one per tool: Git's config, the shell's startup file, the Secure Shell client's known-hosts list, the editor's state. You almost never need to see them in a casual listing. Keeping them out of the default view is a convenience, not a protection.

The upside of this convenience is that moving a tool's settings between machines is easy. `.gitconfig` is just a text file. Copy it to a new laptop and you have brought your Git identity with you. Same for `.bashrc`, `.vscode`, and most of the others. Hidden files are often the most portable files on your machine.

**The rule worth keeping**

Three rules carry forward from this lesson.

1. **Write relative paths by default. Write absolute paths when the caller will run your command from somewhere else.** Scripts, scheduled tasks, containers, and CI jobs all count as "somewhere else."
2. **Do not trust a file's extension to tell you what it contains. Trust it to tell you what the author intended.** When you need to know what is actually inside, open the file.
3. **When the same command shows different files on different shells, check the hiding rule first.** Bash looks at the dot; PowerShell looks at the attribute. The file is almost always there; the question is whether your shell's default view is showing it.

**The one-line drill**

Count your hidden and visible files together:

```powershell
(Get-ChildItem -Force ~).Count
```

```bash
ls -a ~ | wc -l
```

On a fresh Windows install with a few developer tools installed, the count is usually around 30 to 50. On a long-lived developer laptop it is often 200+. Every line is a tool that decided it needed to store something per-user.

Full lesson with the full commands, the dotfile cleanup, and the `.gitconfig` exploration: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M02-files-editors-and-package-managers/lessons/L-010-understand-file-paths-extensions-and-hidden-files.md

Tomorrow: install the package manager that installs every other tool the rest of the curriculum uses.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #HealthcareAI
