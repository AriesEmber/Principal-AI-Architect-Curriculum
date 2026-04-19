The first time I tried to move between folders from a terminal, I typed the full path to a folder that was right next to me. It worked, and it also took twice as long as it should have. Then someone showed me `cd Documents`, with no slash and no full path, and I realized the shell had a whole second mode I had been ignoring.

This is Day 6 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. Today is how the shell walks, and why every command you will ever run on a command line takes one of two kinds of address.

The analogy I use is a house. If someone in the hallway asks where the kitchen is, you say "go to the kitchen." If the same person calls from across town, you have to say "go to 123 Main Street, then the kitchen." Same destination, different starting point, different directions. The terminal works the same way, and the command for walking is `cd`, short for change directory (CD).

![Side-by-side typewriter walkthrough of five cd exchanges, Bash on the left and PowerShell on the right](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-006-terminal.gif)

**Relative paths start where you stand**

Type `cd Documents` and the shell walks into the `Documents` folder inside the current directory. The name `Documents` has no leading slash, so the shell interprets it starting from wherever `pwd` would return. That is what "relative" means: the starting point is here.

```bash
$ pwd
/home/learner
$ cd Documents
$ pwd
/home/learner/Documents
```

Every command that takes a filename works the same way. When you open a file in an editor, pass a file to a script, or run a program with an input argument, the shell interprets the name relative to the current directory unless you tell it otherwise.

**Two dots walk you back up**

`cd ..` walks up one level. The two dots are a special entry that exists inside every directory on Linux, macOS, and Windows. You actually already met them: when you ran `ls -la` in the previous lesson, the first two rows of the output were `.` (this directory) and `..` (the parent). The shell is not doing anything magic with `cd ..`; it is reading the same `..` entry the long-form `ls` showed you.

**Absolute paths start at the front door**

Type `cd /` on macOS or Linux, or `cd C:\` on Windows PowerShell, and the shell stops caring where you were standing. The leading slash (or drive letter) is the signal that flips the path from "starting here" to "starting at the filesystem root."

```bash
$ cd /
$ pwd
/
```

Relative paths are for short moves. Absolute paths are for jumps across the system, or for anything that needs to work the same way from any starting directory. Every production script you will ever read uses absolute paths for files that matter, for exactly this reason.

![Side-by-side static panel of the five cd exchanges in Bash (left) and PowerShell (right)](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-006-terminal.png)

**The three shortcuts worth memorizing today**

- `.` is this directory.
- `..` is the parent directory.
- `~` is your home directory.

All three work inside `cd` and inside almost every other command on a command line. `cd ~` gets you home from anywhere, and so does `cd` with no argument at all. That alone is worth the lesson: no matter how lost you feel in the shell, one keystroke puts you back at a known starting point.

**Windows PowerShell uses the same words**

On Windows PowerShell, `cd` is an alias for `Set-Location`, and every move in this lesson works with the Windows path separator. `cd Documents`, `cd ..`, `cd C:\`, and `cd ~` all land in the expected place. The operating system (OS) difference is cosmetic: the shell's walking vocabulary is the same.

**Why this is the lesson that changes the shell from intimidating to navigable**

Until you know the two kinds of path, every new folder feels like a puzzle. Once you know it, the shell becomes a map you can walk around in. Most of the "this tool is hard" feeling that new Command-Line Interface (CLI) users describe is this one trick undiscovered. Relative for short moves, absolute for long ones. Two rules, covers everything.

**The verification**

If `pwd` reported a different path after each `cd`, and you got home again with `cd ~` or `cd` alone, the lesson is done. If `pwd` did not change, `cd` silently failed, almost always because of a typo or a case mismatch (macOS and Linux are case-sensitive; Windows is not). Run `ls` first, confirm the name exists in the list, try again.

Thirteen minutes. One command, two kinds of path, three shortcuts. Tomorrow's capstone builds on all of them to make and remove a folder of your own.

Full lesson with the `cd -` extension and the Windows PowerShell details: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M01-first-contact-with-the-terminal/lessons/L-006-move-around-with-cd-and-relative-paths.md

Try it and tell me how many times you had to hit the "emergency brake" (`cd` with no argument) on your first pass. For most of us it is more than zero.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #HealthcareAI
