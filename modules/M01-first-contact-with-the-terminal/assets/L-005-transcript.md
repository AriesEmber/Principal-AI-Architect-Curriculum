# L-005 Terminal Transcript

Plain-text transcript of the `ls` exchanges demonstrated in the lesson. This file is included for screen readers, since animated GIFs are inaccessible.

```bash
$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos

$ ls -la
total 28
drwxr-xr-x 12 learner learner 4096 Apr 18 10:15 .
drwxr-xr-x  3 root    root    4096 Apr 10 14:22 ..
-rw-------  1 learner learner  128 Apr 18 10:15 .bash_history
-rw-r--r--  1 learner learner 3771 Apr 10 14:22 .bashrc
drwxr-xr-x  2 learner learner 4096 Apr 15 11:00 Documents
drwxr-xr-x  2 learner learner 4096 Apr 15 11:00 Downloads

$ ls /
bin  boot  dev  etc  home  lib  opt  proc  root  sbin  tmp  usr  var
```

And on PowerShell (Windows), the alias check referenced in the lesson:

```powershell
PS C:\Users\learner> Get-Command ls

CommandType     Name    Source
-----------     ----    ------
Alias           ls -> Get-ChildItem
```

Notes on what each exchange shows:

1. **Plain `ls`.** With no arguments, `ls` lists the non-hidden entries of the current working directory. A fresh home directory typically shows the top-level folders the operating system (OS) created for you.
2. **`ls -la` (long format, include hidden).** Adds two kinds of detail. First, the columns: permissions, link count, owner, group, size in bytes, modification time, and finally the name. Second, the extra rows: entries whose names start with `.` (dotfiles), plus `.` (this directory) and `..` (the parent directory). The first character of each row encodes the type: `d` is a directory, `-` is a regular file.
3. **`ls /`.** Same command, different target. Passing a path as an argument tells `ls` to list that directory instead of the current one. The root of the filesystem on Linux and macOS is `/`; on Windows PowerShell the equivalent is `C:\`.
4. **PowerShell alias.** On Windows PowerShell, `ls` is an alias for the PowerShell command `Get-ChildItem`. `dir` is another alias for the same command. The command-response rhythm and the idea of "list what is here" are identical; only the column layout of the output differs.
