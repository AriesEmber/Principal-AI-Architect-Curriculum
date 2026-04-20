# L-007 Terminal Transcript

Accessible text-only version of the terminal session shown in
`L-007-terminal.svg`, `L-007-terminal.png`, and `L-007-terminal.gif`. Screen
readers should read this file; the images above are visual redundancy.

PowerShell is the primary shell in this lesson (left column in the paired
image). Bash is the alternate for macOS, Linux, and Windows Subsystem for
Linux (WSL) users. The prompt on PowerShell is `PS C:\Users\learner> ` and
on Bash is `learner@laptop:~$ `. Everything after the prompt is what the
learner types.

## PowerShell (Windows 11, primary)

```powershell
PS C:\Users\learner> pwd

Path
----
C:\Users\learner

PS C:\Users\learner> mkdir practice-cli

    Directory: C:\Users\learner

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d----          4/19/2026  5:18 PM                 practice-cli

PS C:\Users\learner> ls

Desktop  Documents  practice-cli

PS C:\Users\learner> cd practice-cli

PS C:\Users\learner\practice-cli> ni hello.txt

    Directory: C:\Users\learner\practice-cli

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          4/19/2026  5:18 PM              0 hello.txt

PS C:\Users\learner\practice-cli> ls

hello.txt

PS C:\Users\learner\practice-cli> Remove-Item -Recurse practice-cli

Remove-Item : Cannot find path 'C:\Users\learner\practice-cli\practice-cli' because it does not exist.
At line:1 char:1
+ Remove-Item -Recurse practice-cli
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\learner\practice-cli\practice-cli:String) [Remove-Item], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.RemoveItemCommand

PS C:\Users\learner\practice-cli> cd ..

PS C:\Users\learner> Remove-Item -Recurse practice-cli

PS C:\Users\learner> ls

Desktop  Documents  Downloads
```

## Bash (macOS / Linux / WSL, alternate)

```bash
learner@laptop:~$ pwd
/home/learner

learner@laptop:~$ mkdir practice-cli

learner@laptop:~$ ls
Desktop  Documents  practice-cli

learner@laptop:~$ cd practice-cli

learner@laptop:~/practice-cli$ touch hello.txt

learner@laptop:~/practice-cli$ ls
hello.txt

learner@laptop:~/practice-cli$ rm -r practice-cli
rm: cannot remove 'practice-cli': No such file or directory

learner@laptop:~/practice-cli$ cd ..

learner@laptop:~$ rm -r practice-cli

learner@laptop:~$ ls
Desktop  Documents  Downloads
```

## Reading the exchanges

1. `pwd` confirms the starting point is the home directory.
2. `mkdir practice-cli` creates a new directory called `practice-cli` in the current directory.
3. `ls` shows the home directory now contains the new `practice-cli` folder.
4. `cd practice-cli` walks into the new folder. The prompt path segment changes.
5. `ni hello.txt` on PowerShell (alias for `New-Item`) or `touch hello.txt` on Bash creates an empty file called `hello.txt`.
6. `ls` shows the new file.
7. `Remove-Item -Recurse practice-cli` on PowerShell or `rm -r practice-cli` on Bash **fails** because the learner is currently inside `practice-cli`, so the shell resolves the relative name `practice-cli` against the current directory and looks for `practice-cli\practice-cli` on Windows or `practice-cli/practice-cli` on macOS/Linux. Neither exists, so the shell reports the path is not found.
8. `cd ..` walks up one level, back to the home directory. The prompt returns to the parent path.
9. `Remove-Item -Recurse practice-cli` (or `rm -r practice-cli`) now succeeds because the target is resolved against the home directory. Silent on success; the directory and `hello.txt` are gone.
10. `ls` confirms the home directory is back to `Desktop`, `Documents`, `Downloads` — no `practice-cli`.

## The rule that step 7 teaches

You cannot remove the directory you are currently standing in by name. The shell resolves a bare name like `practice-cli` against the current working directory. If the current directory is already named `practice-cli`, the resolved target becomes `practice-cli\practice-cli`, which does not exist.

The fix is always the same: walk up one level with `cd ..`, then remove the directory by name. Two lines, one rule, applies to every shell you will ever use.
