# L-004 Terminal Transcript

Plain-text transcript of the pwd exchanges demonstrated in the lesson. This file is included for screen readers, since animated GIFs are inaccessible.

```bash
$ pwd
/home/learner
$ pwd
/home/learner
$ pwd -L
/home/learner
$ pwd -P
/home/learner
$
```

And on PowerShell (Windows), the alias check referenced in the lesson:

```powershell
PS C:\Users\learner> Get-Command pwd

CommandType     Name                    Source
-----------     ----                    ------
Alias           pwd -> Get-Location
```

Notes on what each exchange shows:

1. **Plain pwd.** In a fresh terminal, the working directory is the home directory. The path starts with `/` on macOS and Linux (or `C:\` on Windows PowerShell).
2. **A second fresh terminal.** Opening another terminal window and running `pwd` prints the same path. Every fresh terminal starts in the home directory on every major operating system.
3. **`pwd -L` (logical path).** The default. Shows the path as the shell sees it, symbolic links left alone.
4. **`pwd -P` (physical path).** Resolves any symbolic links along the way to their real targets. Same answer in a plain home directory; matters later when you are working inside a repository mounted through a link.
5. **PowerShell alias.** On Windows PowerShell, `pwd` is an alias for `Get-Location`. Same command-response rhythm, same absolute-path answer.
