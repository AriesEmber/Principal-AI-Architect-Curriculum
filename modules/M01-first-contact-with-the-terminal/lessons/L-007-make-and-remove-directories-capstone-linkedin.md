The first folder I ever created from a terminal sat on my desktop untouched for a week because I did not know how to delete it. I could make things; I could not unmake them. The `rm -r` command was two keystrokes away the whole time, but nobody had told me. The fix is a 90-second lesson that everybody skips and everybody needs.

This is Day 7 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Today is the week-one capstone. Six commands, one round trip: make a directory, put a file in it, take the whole thing back down.

The analogy I use is a filing cabinet. Slide it in. Pull the drawer. Drop a note. Push it back. Shred the whole thing when the project is over. The terminal has one verb for each of those motions, and by the end of today you will know them all.

![Animated typewriter walkthrough of the ten-exchange capstone](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.gif)

**The six commands in one flow**

```bash
pwd
mkdir practice-cli
ls
cd practice-cli
ls
touch hello.txt
ls
cd ..
rm -r practice-cli
```

Nine lines, ten seconds of typing, and you have built and destroyed a complete project folder. Every real codebase, every cloud deployment, every Machine Learning (ML) experiment you will ever run starts with this exact sequence.

**`mkdir` makes a directory**

`mkdir` is short for "make directory." The name after it is the folder you are creating, and because the name has no leading slash the shell creates it inside the current directory. It is silent on success, loud on failure. If you see no output, the folder was made.

**`touch` makes an empty file**

`touch` was originally designed to update a file's last-modified timestamp. Its useful side effect is that if the file does not exist, `touch` creates it, empty. Every professional I know uses `touch` as the one-keyword way to make a new empty file. There is a longer way involving redirection (`echo > hello.txt`), but `touch` is shorter and more honest about what it does.

**`rm -r` deletes a directory and everything in it**

`rm` means remove. The `-r` flag is "recursive": walk into every sub-directory and remove every file on the way down, then remove the directories themselves, then remove the top-level directory you named. One command cleans up a whole project folder.

```bash
$ ls
Desktop  Documents  Downloads  practice-cli
$ rm -r practice-cli
$ ls
Desktop  Documents  Downloads
```

Read that carefully because it matters: `rm -r` does not move files to a recycle bin. It deletes them. On macOS and Linux the deletion is permanent unless your filesystem has snapshots. On Windows PowerShell the equivalent is `Remove-Item -Recurse`, which behaves the same way. The cost of being careless with `rm -r` is a project you cannot get back.

The mental habit that keeps you safe: never type `rm -r` against a path you did not just create yourself, and always run `ls` first to see what is actually there before you delete.

![Static panel of the ten exchanges plus the PowerShell equivalent](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-007-terminal.png)

**The symmetry is the lesson**

Two verbs create. One verb destroys. Three verbs observe and move. That is the complete vocabulary for reshaping a file tree from a Command-Line Interface (CLI), and every tool you will ever install on top (Git, Docker, Terraform, the cloud command-line tools) assumes you already have this vocabulary.

- `mkdir` creates a directory
- `touch` creates a file
- `rm -r` removes a directory and everything in it
- `pwd` reports where you are standing
- `ls` reports what is here
- `cd` walks you somewhere else

Six commands. One keystroke of difference between the destroy verb and a mistake you cannot take back. This is why serious command-line users develop the habit of reading the line before they press enter.

**Windows PowerShell uses the same words**

`mkdir practice-cli`, `cd practice-cli`, `cd ..`, `rm -r practice-cli` all work on Windows PowerShell with identical behavior. The only swap is the `touch` step: PowerShell does not have `touch` by default, but it has `New-Item hello.txt` (or the shorter alias `ni hello.txt`), which creates an empty file the same way. If you are on Windows, write `ni hello.txt` anywhere you see `touch hello.txt` in this curriculum and the rest reads the same.

**What finishing week one actually gives you**

Seven days ago this curriculum started with opening a terminal. Today you can create a project folder, put files in it, navigate around, and clean up after yourself, on any operating system (OS) a professional will ever hand you. That is the full floor of every technical job I have ever done. Everything the next 164 lessons teach, starting tomorrow with reading files, runs on top of the ten seconds of typing you just learned.

The thing that trips most people up is not any individual command. It is not believing that the command actually worked, because the shell does not say anything back. Silent success is the shell's default, and it takes a few rounds of `mkdir`, `ls`, `mkdir`, `ls` before the silence stops feeling like failure. Run the sequence twice today. The second time will feel different.

**The verification**

After running the nine-line sequence, `ls` in your home directory should show the same folders it showed at the start. No `practice-cli`, no `hello.txt`. If something extra is still there, `rm -r <name>` it and run `ls` again until the directory is clean.

Full lesson with the `mkdir -p` nested-directory extension and the full set of failure modes: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M01-first-contact-with-the-terminal/lessons/L-007-make-and-remove-directories-capstone.md

Tomorrow: cat and less, the first two ways to read what is actually inside a file.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #HealthcareAI
