# L-010 Terminal Transcript

Accessible text-only version of the terminal session shown in
`L-010-terminal.svg`, `L-010-terminal.png`, and `L-010-terminal.gif`. Screen
readers should read this file; the images above are visual redundancy.

PowerShell is the primary shell in this lesson (left column in the paired
image). Bash is the alternate for macOS, Linux, and the Windows Subsystem
for Linux (WSL). The PowerShell prompt is `PS C:\Users\learner> ` and the
Bash prompt is `learner@laptop:~$ `. Everything after the prompt is what
the learner types.

Seven exchanges, executed in order. Exchange 1 prints the absolute home
path. Exchanges 2 through 6 teach the two conventional ways to write a
path (relative and absolute) and that a file extension is a naming
convention, not a content-type enforcement. Exchange 7 teaches how each
shell handles files whose names begin with a dot.

## PowerShell (Windows 11, primary)

```powershell
PS C:\Users\learner> Get-Location

Path
----
C:\Users\learner

PS C:\Users\learner> "hello paths" > note.txt
(file written; no output)

PS C:\Users\learner> cat note.txt
hello paths

PS C:\Users\learner> cat C:\Users\learner\note.txt
hello paths
(same file, longer address)

PS C:\Users\learner> Rename-Item note.txt note.md
(renamed; no output)

PS C:\Users\learner> cat note.md
hello paths
(extension is a label, not a lock)

PS C:\Users\learner> Get-ChildItem -Force

Name
----
.gitconfig
.ssh
note.md
(dotfiles shown by default; -Force adds Hidden-attribute files)

PS C:\Users\learner>
```

`Get-Location` prints the current working directory as an absolute path.
`pwd` is the built-in PowerShell alias for the same command, so either
works.

The `>` operator writes the quoted string into `note.txt` and returns no
output on success. If `note.txt` already existed the content is
overwritten.

Reading with a relative path (`cat note.txt`) and an absolute path
(`cat C:\Users\learner\note.txt`) returns the same bytes because they
name the same file. The relative form is shorter; the absolute form
works regardless of which directory you are in.

`Rename-Item note.txt note.md` changes the filename. The content does
not change. `cat note.md` shows the same text as before.

`Get-ChildItem -Force` lists files including those with the Windows
Hidden attribute. PowerShell does not hide filenames that start with a
dot by default, so dotfiles like `.gitconfig` show up even without the
`-Force` flag. The flag adds any file whose Hidden attribute is set.

## Bash (macOS, Linux, WSL)

```bash
learner@laptop:~$ pwd
/home/learner

learner@laptop:~$ echo "hello paths" > note.txt
(file written; no output)

learner@laptop:~$ cat note.txt
hello paths

learner@laptop:~$ cat /home/learner/note.txt
hello paths
(same file, longer address)

learner@laptop:~$ mv note.txt note.md
(renamed; no output)

learner@laptop:~$ cat note.md
hello paths
(extension is a label, not a lock)

learner@laptop:~$ ls -a
.        ..
.bashrc  .gitconfig
.ssh     note.md

(-a reveals any name starting with a dot)

learner@laptop:~$
```

`pwd` prints the absolute path of the current directory. On macOS the
path usually starts with `/Users/<you>`; on most Linux distributions
and in WSL it is `/home/<you>`.

The `>` redirection works the same way in Bash as in PowerShell: it
writes the output of the preceding command (here, `echo`'s stdout) into
the file.

Reading with a relative path (`cat note.txt`) and an absolute path
(`cat /home/learner/note.txt`) returns the same bytes. The relative
form is shorter; the absolute form works from anywhere.

`mv note.txt note.md` renames the file. `cat note.md` shows the
original content; the OS does not check that `.md` content is Markdown.

`ls` alone hides any file whose name starts with a dot. `ls -a` adds
those files to the listing. `.` and `..` refer to the current and
parent directories; every other entry starting with a dot is a regular
file or directory that the shell keeps out of the default listing.
`ls -la` also shows the owner, size, and modification time of each
entry.

## The cross-shell takeaway

PowerShell and Bash treat hidden files differently:

- **Bash** hides every filename starting with a dot. `ls -a` reveals them.
- **PowerShell** respects the Windows Hidden file *attribute*, not the
  leading dot. A file named `.gitconfig` is visible by default because
  nothing set its Hidden attribute. `Get-ChildItem -Force` adds files
  whose Hidden attribute is set.

Both shells allow you to create, read, and rename dotfiles exactly the
same way. The difference is only in what the default listing shows.
