# L-003 Terminal Transcript (Bash and PowerShell)

Plain-text transcript of the five echo exchanges demonstrated in the lesson, captured in both shells side by side. This file is included for screen readers, since animated GIFs are inaccessible.

## Bash (or Zsh) on macOS, Linux, or Windows Subsystem for Linux

```bash
$ echo Hello, world
Hello, world
$ echo "Hello, world"
Hello, world
$ echo 'Hello, world'
Hello, world
$ echo

$ echo $USER
learner
$
```

## Windows PowerShell

```powershell
PS C:\Users\learner> echo Hello, world
Hello, world
PS C:\Users\learner> echo "Hello, world"
Hello, world
PS C:\Users\learner> echo 'Hello, world'
Hello, world
PS C:\Users\learner> echo

PS C:\Users\learner> echo $env:USERNAME
learner
PS C:\Users\learner>
```

## Notes on what each exchange shows

1. **No quotes (identical in both shells).** The shell splits the line on whitespace and passes `Hello,` and `world` as two arguments. Echo prints them joined by a single space, which happens to look identical to the quoted versions.
2. **Double quotes (identical in both shells).** Everything inside the quotes stays one argument, and `$` variables (if any) still expand.
3. **Single quotes (identical in both shells).** Everything inside is literal. No variable expansion.
4. **No arguments (identical in both shells).** Echo prints just a newline, so a blank line appears and the prompt returns.
5. **Variable expansion (different in each shell).** Bash exposes the username as `$USER` in its flat namespace. PowerShell exposes the same value as `$env:USERNAME` under its environment-variable prefix. Same observable result, different syntax. In this transcript the username is `learner`; on your machine it will be yours.
