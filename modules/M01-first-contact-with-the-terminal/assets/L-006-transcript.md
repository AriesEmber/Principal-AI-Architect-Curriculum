# L-006 Terminal Transcript

Plain-text transcript of the `cd` exchanges demonstrated in the lesson. This file is included for screen readers, since animated GIFs are inaccessible.

```bash
$ pwd
/home/learner

$ cd Documents

$ pwd
/home/learner/Documents

$ cd ..

$ pwd
/home/learner

$ cd /

$ pwd
/

$ cd ~

$ pwd
/home/learner
```

The same five moves on Windows PowerShell:

```powershell
PS C:\Users\learner> pwd

Path
----
C:\Users\learner

PS C:\Users\learner> cd Documents
PS C:\Users\learner\Documents> cd ..
PS C:\Users\learner> cd C:\
PS C:\> cd ~
PS C:\Users\learner>
```

Extension: `cd -` returns to the previous directory.

```bash
$ cd Documents

$ cd -
/home/learner

$ pwd
/home/learner
```

Notes on what each exchange shows:

1. **`pwd` before moving.** Confirms the starting directory. Here it is the learner's home folder, the directory a fresh terminal lands in.
2. **`cd Documents` (relative).** The argument `Documents` has no leading slash, so the shell interprets it against the current directory. The shell now considers `/home/learner/Documents` the current working directory.
3. **`pwd` after the relative move.** Reports the new location. No other output appears, which is normal: `cd` is silent on success.
4. **`cd ..` (relative, up one).** `..` is a special entry that exists in every directory and points to the parent. This walks back to `/home/learner`.
5. **`cd /` (absolute).** A leading slash tells the shell to interpret the path from the filesystem root, not from the current directory. On Windows PowerShell the equivalent is `cd C:\`.
6. **`cd ~` or plain `cd`.** A tilde is shorthand for the user's home directory. Running `cd` with no argument has the same effect on bash, zsh, and PowerShell. Always a safe way to get back to a known starting point.
7. **`cd -` (extension).** Returns to whichever directory you were in before the most recent `cd`. The shell prints the destination, which is a cue that the jump worked. Supported in bash, zsh, and PowerShell version 6 or later.
