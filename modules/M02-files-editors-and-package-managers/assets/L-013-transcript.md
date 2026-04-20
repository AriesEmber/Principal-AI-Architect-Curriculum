# L-013 transcript — set an environment variable and read it back

Screen-reader transcript of the six-exchange PowerShell-primary walkthrough in `L-013-terminal.gif` / `L-013-terminal.png` / `L-013-terminal.svg`.

The variable used in both columns is `MY_NAME` with the value `Elvis`. Exchange 6 opens a brand-new terminal window; the read returns a blank line on purpose, because the assignments in exchanges 1 through 5 were scoped to the first window's process environment only.

## PowerShell (Windows 11)

```powershell
PS C:\Users\learner> echo $env:MY_NAME

(no variable yet; blank line)

PS C:\Users\learner> $env:MY_NAME = "Elvis"
(assignment; no output)

PS C:\Users\learner> echo $env:MY_NAME
Elvis

PS C:\Users\learner> echo "Hello, $env:MY_NAME"
Hello, Elvis

PS C:\Users\learner> Get-ChildItem Env:MY_NAME

Name     Value
----     -----
MY_NAME  Elvis

# --- close the window, open a new PowerShell window ---

PS C:\Users\learner> echo $env:MY_NAME

(blank again; the value was session-only)
```

## Bash (macOS; Linux and WSL use the same commands)

```bash
learner@laptop:~$ echo "$MY_NAME"

(no variable yet; blank line)

learner@laptop:~$ export MY_NAME="Elvis"
(assignment; no output)

learner@laptop:~$ echo "$MY_NAME"
Elvis

learner@laptop:~$ echo "Hello, $MY_NAME"
Hello, Elvis

learner@laptop:~$ printenv MY_NAME
Elvis
(printenv only prints exported vars)

# --- close the window, open a new terminal window ---

learner@laptop:~$ echo "$MY_NAME"

(blank again; the value was session-only)
```

## Cross-shell takeaway

PowerShell's `$env:NAME = "..."` always writes to the process environment, so any child program launched from the same window sees the value. Bash draws a line between a plain shell variable (`NAME=...`, visible only inside the current shell) and an environment variable (`export NAME=...`, visible to child programs as well). Both shells agree on the lifetime: when the window closes, the value goes with it. Persisting a value across windows needs a separate write — `[Environment]::SetEnvironmentVariable("MY_NAME", "Elvis", "User")` in PowerShell, or a line appended to `~/.bashrc` (or `~/.zshrc`) in Bash. That persistence path is the "Going further" section in the article.
