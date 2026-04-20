# L-007 Terminal Transcript

Accessible text-only version of the terminal session shown in
`L-007-terminal.svg`, `L-007-terminal.png`, and `L-007-terminal.gif`. Screen
readers should read this file; the images above are visual redundancy.

The prompt `learner@laptop:~$` means the user `learner` on the machine
`laptop` is standing in the home directory (`~`). The dollar sign marks the
end of the prompt; everything after it is what the learner types.

```bash
learner@laptop:~$ pwd
/home/learner

learner@laptop:~$ mkdir practice-cli

learner@laptop:~$ ls
Desktop  Documents  Downloads  practice-cli

learner@laptop:~$ cd practice-cli

learner@laptop:~/practice-cli$ ls
(empty)

learner@laptop:~/practice-cli$ touch hello.txt

learner@laptop:~/practice-cli$ ls
hello.txt

learner@laptop:~/practice-cli$ cd ..

learner@laptop:~$ rm -r practice-cli

learner@laptop:~$ ls
Desktop  Documents  Downloads
```

Reading the exchanges:

1. `pwd` confirms the starting point is the home directory.
2. `mkdir practice-cli` creates a new directory called `practice-cli` in the current directory. The command produces no output on success.
3. `ls` shows the home directory now contains the new `practice-cli` folder alongside the existing `Desktop`, `Documents`, and `Downloads` folders.
4. `cd practice-cli` walks into the new folder. The prompt's path segment changes from `~` to `~/practice-cli`, which is the shell's way of showing the move worked.
5. `ls` inside `practice-cli` produces no output. The annotation `(empty)` is added for the transcript; the real shell prints nothing at all.
6. `touch hello.txt` creates an empty file called `hello.txt`. Silent on success.
7. `ls` now shows `hello.txt`.
8. `cd ..` walks up one level, back to the home directory. The prompt returns to `~`.
9. `rm -r practice-cli` removes the directory and everything inside it, recursively. Silent on success. There is no recycle bin; the directory and `hello.txt` are gone.
10. `ls` confirms the home directory is back to `Desktop`, `Documents`, `Downloads` — no `practice-cli`.

**Windows PowerShell equivalent, same sequence, same result:**

```powershell
PS C:\Users\learner> mkdir practice-cli
PS C:\Users\learner> cd practice-cli
PS C:\Users\learner\practice-cli> New-Item hello.txt
PS C:\Users\learner\practice-cli> cd ..
PS C:\Users\learner> Remove-Item -Recurse practice-cli
```

`New-Item` (aliased as `ni`) is PowerShell's built-in stand-in for `touch`, and
`Remove-Item -Recurse` is the PowerShell counterpart to `rm -r`. The
directory-navigation commands are identical on both platforms.
