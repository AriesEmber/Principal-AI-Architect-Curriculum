The first time I tried to delete the practice folder I had just made, Windows PowerShell threw a red wall of text at me and refused. Two lessons into a curriculum I am taking publicly, I had already hit the single most confusing moment of the first month of terminal use: you cannot delete the directory you are currently standing in. Nobody had told me that. The fix is two keystrokes. The rule is one sentence. Today's lesson is that rule, the two-keystroke fix, and the six commands that together give you the full vocabulary for shaping a file tree from the Command-Line Interface (CLI).

This is Day 7 of a 171-lesson path from zero to a Principal Artificial Intelligence (AI) Architect role. Today is the week-one capstone. Ten exchanges, one round trip: make a directory, put a file in it, try to delete the directory from inside (watch it fail), step out, delete it for real.

The analogy I use is a filing cabinet. Slide it into place. Pull the drawer. Drop a note. Then try to shred the cabinet while you are still standing inside it. The shredder refuses. You step out, try again, and the cabinet is gone. Every shell on every operating system enforces this one rule the same way, and it is the first rule most new learners discover the hard way.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough of the capstone, including the failed-delete-from-inside step and the cd .. recovery](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.gif)

**The ten exchanges in one flow (PowerShell on Windows 11)**

```powershell
pwd
mkdir practice-cli
ls
cd practice-cli
ni hello.txt
ls
Remove-Item -Recurse practice-cli   # fails: you are inside practice-cli
cd ..
Remove-Item -Recurse practice-cli   # works: you are now one level up
ls
```

Ten lines, thirty seconds of typing, and you have built, failed to destroy, recovered, and destroyed a complete project folder. Every real codebase, every cloud deployment, every Machine Learning (ML) experiment you will ever run starts with a version of this exact sequence.

**`mkdir` makes a directory**

On PowerShell, `mkdir` is an alias for `New-Item -ItemType Directory` and prints a confirmation line. On Bash, `mkdir` is a separate program and is silent on success. Both create the folder inside the current directory when the name has no leading slash.

**`ni` (or `touch`) makes an empty file**

PowerShell's `ni` is a short alias for `New-Item`. It creates an empty file when given a plain file name. Bash uses `touch`, which was originally designed to update a file's last-modified timestamp but which creates a file when the named file does not exist.

This is the one step where the Windows and the Unix worlds diverge. PowerShell does not ship a `touch` command. If you have ever followed a Linux-style tutorial on Windows and seen `The term 'touch' is not recognized`, this is the fix: on PowerShell, type `ni hello.txt`. On Bash, type `touch hello.txt`. Same file on disk, two names for the verb.

**The rule that step 7 teaches**

Read this carefully because it is the moment most new learners get stuck and give up.

```powershell
PS C:\Users\learner\practice-cli> Remove-Item -Recurse practice-cli
Remove-Item : Cannot find path 'C:\Users\learner\practice-cli\practice-cli' because it does not exist.
```

The path the shell tried to delete was `practice-cli\practice-cli`. That is `practice-cli` *inside* `practice-cli`. You told the shell to find a folder named `practice-cli` starting from the current working directory and remove it. The current working directory was already `practice-cli`, so the shell appended the name you passed and looked one level deeper. Nothing was there, so the shell reported a path-not-found error.

The rule: you cannot remove the directory you are currently standing in by its name. The shell resolves a bare name against the current directory, and if the current directory is already the folder you are naming, the resolved target does not exist.

The fix is one command: `cd ..`. Step up one level and the name resolves correctly. Retry the delete and it works.

This same rule applies in Bash. The error message is shorter and the command is `rm -r practice-cli` instead of `Remove-Item -Recurse practice-cli`, but the rule is identical. Every shell on every operating system enforces it the same way.

![Side-by-side static panel of the ten capstone exchanges. PowerShell on the left, Bash on the right, step 7 shown in red as the failed attempt from inside the directory](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.png)

**The symmetry is the lesson**

Two verbs create. One verb destroys. Three verbs observe and move. That is the complete vocabulary for reshaping a file tree from the CLI.

- `mkdir` creates a directory
- `ni` / `touch` creates a file
- `Remove-Item -Recurse` / `rm -r` removes a directory and everything in it
- `pwd` reports where you are standing
- `ls` reports what is here
- `cd` walks you somewhere else

Six commands. One rule about the current working directory. One keystroke of difference (`-r`) between the destroy verb and a mistake you cannot take back. This is why serious command-line users develop the habit of running `pwd` and `ls` before any delete, and of reading the line carefully before they press enter.

**Why PowerShell is the primary example in this curriculum now**

Earlier in this curriculum I led every terminal example with Bash and treated PowerShell as the alternate. I changed that after writing the first version of this lesson: I followed my own instructions on my own Windows 11 laptop, hit the "touch not recognized" error and then the "cannot remove path" error, and realized my own curriculum had quietly assumed a macOS or Linux setup. The reader on Windows was being asked to translate two commands per step and to guess why the third one errored.

Going forward, PowerShell on Windows 11 is the primary shell in every lesson that uses a terminal. Bash on macOS, Linux, and Windows Subsystem for Linux (WSL) is the alternate. The capstone image now puts PowerShell on the left and Bash on the right for exactly this reason. If you are on macOS or Linux, follow the Bash column. If you are on Windows, follow the PowerShell column. Neither one is "secondary" in the sense of being unsupported. Both are correct.

**What finishing week one actually gives you**

Seven days ago this curriculum started with opening a terminal. Today you can create a project folder, put files in it, navigate around, hit the one rule about the current working directory, recover from it, and clean up after yourself. That is the full floor of every technical job I have ever done, on Windows or macOS or Linux. Everything the next 164 lessons teach, starting tomorrow with reading files, runs on top of the thirty seconds of typing you just learned.

The thing that trips most people up is not any individual command. It is not believing the error message literally. The shell never lies about which path it tried to resolve. When it says `Cannot find path 'C:\Users\learner\practice-cli\practice-cli'`, that is the path it literally tried. Read the error, compare it to your current working directory, and the fix is almost always a `cd` move away.

**The verification**

After running the ten-line sequence, `ls` in your home directory should show the same folders it showed at the start. No `practice-cli`, no `hello.txt`. If something extra is still there, step out to home with `cd ~` and run `Remove-Item -Recurse <name>` (PowerShell) or `rm -r <name>` (Bash) on whatever leftover folder you see.

Full lesson with the `mkdir -Force` (PowerShell) and `mkdir -p` (Bash) nested-directory extension and the full set of failure modes: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M01-first-contact-with-the-terminal/lessons/L-007-make-and-remove-directories-capstone.md

Tomorrow: `cat` and `less`, the first two ways to read what is actually inside a file.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #HealthcareAI
