# L-009 Terminal Transcript

Accessible text-only version of the terminal session shown in
`L-009-terminal.svg`, `L-009-terminal.png`, and `L-009-terminal.gif`. Screen
readers should read this file; the images above are visual redundancy.

PowerShell is the primary shell in this lesson (left column in the paired
image). Bash is the alternate for macOS, Linux, and Windows Subsystem for
Linux (WSL) users. The PowerShell prompt is `PS C:\Users\learner> ` and the
Bash prompt is `learner@laptop:~$ `. Everything after the prompt is what the
learner types. Inside nano, the editor paints a full-screen text user
interface (TUI); the lines with `GNU nano` at the top and `^O Write Out`
near the bottom are drawn by nano, not by the shell.

## PowerShell (Windows 11, primary)

On Windows 11 the one-time setup is `winget install GNU.Nano`. After that
install the transcript below runs identically to the Bash version.

```powershell
PS C:\Users\learner> nano hello.txt

 GNU nano 7.2      hello.txt                          [ New File ]

 ^O Write Out   ^X Exit   ^W Where Is   ^G Help
```

Type three lines into the buffer. The top title strip now reads
`Modified`, and the three lines appear where the cursor is.

```text
 GNU nano 7.2      hello.txt                          Modified
 hello from nano
 this is line two
 good night

 ^O Write Out   ^X Exit   ^W Where Is
```

Press `Ctrl+O`. Nano shows the file-name prompt.

```text
 File Name to Write: hello.txt
```

Press `Enter` to confirm, then `Ctrl+X` to exit nano.

```text
 [ Wrote 3 lines ]
```

Nano closes and the PowerShell prompt returns.

```powershell
PS C:\Users\learner> cat hello.txt

hello from nano
this is line two
good night

PS C:\Users\learner>
```

## Bash (macOS / Linux / WSL, alternate)

Nano ships with the operating system on macOS and most Linux distributions,
and is present inside any WSL distribution. No install step is needed.

```bash
learner@laptop:~$ nano hello.txt

 GNU nano 7.2      hello.txt                          [ New File ]

 ^O Write Out   ^X Exit   ^W Where Is   ^G Help
```

Type three lines.

```text
 GNU nano 7.2      hello.txt                          Modified
 hello from nano
 this is line two
 good night

 ^O Write Out   ^X Exit   ^W Where Is
```

Press `Ctrl+O`. Nano shows the file-name prompt.

```text
 File Name to Write: hello.txt
```

Press `Enter` to confirm, then `Ctrl+X` to exit.

```text
 [ Wrote 3 lines ]
```

Nano closes and the Bash prompt returns.

```bash
learner@laptop:~$ cat hello.txt
hello from nano
this is line two
good night

learner@laptop:~$
```

## Reading the exchanges

1. **Open nano on `hello.txt`.** `nano hello.txt` launches the editor with a
   new, empty buffer. The top strip shows `GNU nano`, the current
   filename, and `[ New File ]` to signal that the file does not yet
   exist on disk. The bottom strip lists the shortcut keys. The caret
   symbol (`^`) is nano's way of writing "Ctrl" in the help text.
2. **Type three lines.** Each keystroke goes into the buffer, which is held
   in memory. The top strip changes to `Modified` as soon as you type a
   character, reminding you the on-disk file is out of date with what is
   in the buffer. Nothing is saved yet.
3. **Save with `Ctrl+O`.** Nano asks `File Name to Write: hello.txt`. The
   `O` is for "Out" (as in "write out"), not "Save". Nano calls it
   "Write Out" because the editor writes the buffer out to a file on
   disk.
4. **Confirm with `Enter`, then `Ctrl+X` to exit.** Enter accepts the
   filename nano proposed. The status strip reports `[ Wrote 3 lines ]`.
   `Ctrl+X` is the exit key. Nano closes and the shell prompt returns.
5. **Verify with `cat`.** `cat hello.txt` reads the file back and prints
   its contents. The three lines match what was typed, which confirms the
   save worked.

## What the editor step teaches

Nano is a full-screen text editor that runs inside the terminal. Unlike
`cat` or `less`, nano draws its own user interface over the terminal
window: a title strip at the top, a scrollable editing area in the middle,
and a help strip at the bottom. The help strip is what makes nano friendly
for new users. Every other terminal editor (vi, emacs, vim) expects you to
memorise its shortcuts before you can use it. Nano prints them right on the
screen.

The Ctrl-key convention is printed with the caret notation: `^O` means hold
Ctrl and press O. This is the same notation used by older Unix terminal
manuals and by the `stty` command, so when the reader meets `^C`, `^D`, or
`^Z` in a future lesson, the symbol will already be familiar.

The workflow is the same in both shells because nano is a separate program,
not a shell feature. The only cross-shell difference is how the editor is
installed and launched: Windows 11 needs a one-time `winget install
GNU.Nano`; macOS, Linux, and WSL already have it.
