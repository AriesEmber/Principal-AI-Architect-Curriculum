# L-008 Terminal Transcript

Accessible text-only version of the terminal session shown in
`L-008-terminal.svg`, `L-008-terminal.png`, and `L-008-terminal.gif`. Screen
readers should read this file; the images above are visual redundancy.

PowerShell is the primary shell in this lesson (left column in the paired
image). Bash is the alternate for macOS, Linux, and Windows Subsystem for
Linux (WSL) users. The PowerShell prompt is `PS C:\Users\learner> ` and the
Bash prompt is `learner@laptop:~$ `. Everything after the prompt is what the
learner types.

## PowerShell (Windows 11, primary)

```powershell
PS C:\Users\learner> "one","two","three" > notes.txt

PS C:\Users\learner> cat notes.txt

one
two
three

PS C:\Users\learner> 1..30 > notes-long.txt

PS C:\Users\learner> more notes-long.txt

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
-- More --
```

Press `q` to quit the pager. `more.com` exits and the PowerShell prompt returns.

```powershell
PS C:\Users\learner> Remove-Item notes.txt, notes-long.txt

PS C:\Users\learner>
```

## Bash (macOS / Linux / WSL, alternate)

```bash
learner@laptop:~$ printf "one\ntwo\nthree\n" > notes.txt

learner@laptop:~$ cat notes.txt
one
two
three

learner@laptop:~$ seq 1 30 > notes-long.txt

learner@laptop:~$ less notes-long.txt
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
:
```

Press `q` to quit `less`. Control returns to the shell.

```bash
learner@laptop:~$ rm notes.txt notes-long.txt

learner@laptop:~$
```

## Reading the exchanges

1. **Write `notes.txt`.** PowerShell's `"one","two","three" > notes.txt`
   pipes an array of three strings to `Out-File` (the backing cmdlet for
   `>`), which writes one string per line. Bash's `printf
   "one\ntwo\nthree\n" > notes.txt` writes the literal string with three
   embedded newline escapes. Both produce a three-line text file.
2. **Dump with `cat`.** On both shells `cat notes.txt` prints every line of
   the file to the screen. On PowerShell `cat` is an alias for
   `Get-Content`; on Bash it is a separate program named after the verb
   "concatenate." The file fits on one screen so the full contents are
   visible at once.
3. **Build a longer file.** `1..30 > notes-long.txt` on PowerShell uses
   the range operator to produce the integers 1 through 30, one per line,
   piped into `Out-File`. `seq 1 30 > notes-long.txt` on Bash does the
   same thing with the `seq` program. Both give a 30-line file too tall
   for a typical terminal.
4. **Open the pager.** PowerShell's `more notes-long.txt` opens the
   built-in `more.com` pager and shows the first screen of content with a
   `-- More --` marker at the bottom. Bash's `less notes-long.txt` opens
   the `less` pager and shows the first screen with a `:` marker at the
   bottom. Both are waiting for a keypress.
5. **Quit with `q`.** Press the `q` key (no enter required on either pager).
   The pager exits, the shell prompt returns, and you are back in the
   terminal.
6. **Clean up.** `Remove-Item notes.txt, notes-long.txt` on PowerShell or
   `rm notes.txt notes-long.txt` on Bash deletes both files. Silent on
   success.

## What the pager step teaches

`cat` dumps a file's bytes to the terminal and returns control immediately.
A short file scrolls past and you can read it. A 1,000-line file scrolls
past too, and the first 970 lines are gone before you see them. That is
what pagers exist to solve.

A pager (`less` on Bash, `more` on PowerShell) shows one screen of content
at a time and waits for your next keystroke: space to page forward, `q` to
quit. You stay in control of the flow rather than the file scrolling past
at the speed of your scrollback buffer.

On Windows 11, `more.com` only enters its pager user interface when the
content exceeds one screen. A 3-line file passed to `more` dumps directly
because there is nothing to page. `less` on Bash always enters its
interactive user interface, even on a three-line file (you will see
`(END)` at the bottom until you press `q`).
