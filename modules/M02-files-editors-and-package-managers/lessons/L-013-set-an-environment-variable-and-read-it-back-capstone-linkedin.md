The first time I set a variable in a terminal and then rebooted my laptop, I spent half an hour wondering why my script had gone blind. The variable had done its job and died with the window, exactly as designed, and nobody had told me that was the deal. Today's capstone is the tiny experiment that makes the rule visible.

**From zero technical knowledge to AI literacy.**
Through data, cloud, MLOps, and applied GenAI systems.

Day 13 of 171. Module 2: Files, Editors, and Package Managers (Day 6, capstone).

The analogy is a whiteboard in one room of a shop. You write a note on it, anyone in that room can read or change the note, and when you close the door the board stays put with the note on it. Walk into the next room and there is a different board: blank, its own markers, its own old scratches. An environment variable in a Command-Line Interface (CLI) shell is that whiteboard. Every terminal window you open gets its own board at startup; the note you write survives until the window closes; the next window starts clean. Today you write a note called `MY_NAME`, read it back, use it in a one-line greeting, confirm it lives in the process environment, then open a fresh window and find it gone.

![Side-by-side PowerShell (left, primary) and Bash (right) walkthrough. Six exchanges: confirm MY_NAME is empty, set it to Elvis, read it back, use it in a greeting, list it in the process environment with Get-ChildItem Env:MY_NAME on Windows or printenv on Bash, then open a fresh terminal window and see the read return a blank line](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-013-terminal.gif)

**The core pair of commands**

On Windows 11 (PowerShell), the set-and-read pair is:

```powershell
$env:MY_NAME = "Elvis"
echo $env:MY_NAME
```

On macOS, Linux, or the Windows Subsystem for Linux (WSL):

```bash
export MY_NAME="Elvis"
echo "$MY_NAME"
```

Both pairs print `Elvis` the first time the read runs, and a blank line after you close the window and open a new one. That blank line is the capstone payoff: the value was scoped to the window that set it, and the next window starts from a fresh copy of the parent environment.

**Why the Bash side uses `export` (and the PowerShell side does not need it)**

Bash draws a line between two kinds of names. A plain assignment (`MY_NAME="Elvis"`) creates a shell variable that is visible only inside the current shell; a bare `echo "$MY_NAME"` will still print it, but any program the shell launches (Python, Git, a build tool) will not see the name. `export` is the word that promotes a shell variable to an environment variable, which is the list any child process inherits. PowerShell collapses the two cases into one: writing to the `$env:` drive always writes to the process environment. That is why the Bash side explicitly uses `export` and the PowerShell side does not.

You can see the distinction with a single command. After `export MY_NAME="Elvis"` on Bash, `printenv MY_NAME` prints `Elvis`. After a plain `MY_NAME="Elvis"` without `export`, the same `printenv` prints nothing and exits with a non-zero status even though `echo` still sees the value. That difference is not a trivia point: it is the reason a Bash user's first Python script sometimes reads `os.environ["MY_NAME"]` and gets an empty string back.

**Opening a fresh window to prove the lifetime**

```powershell
# close the window, open a new PowerShell window, then:
echo $env:MY_NAME
```

```bash
# close the window, open a new terminal window, then:
echo "$MY_NAME"
```

Blank line. That single blank line is the whole point of the capstone.

![Static side-by-side panel of the six-exchange walkthrough. The final exchange in each column is drawn in a fresh window; both reads return a blank line so the session-scoped lifetime is visible at a glance](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M02-files-editors-and-package-managers/assets/L-013-terminal.png)

**The connection back to `PATH` from yesterday**

Yesterday's lesson installed `tree` through a package manager and watched Windows fall back to a built-in `tree.com` because the GnuWin32 `tree.exe` landed in a folder that was not always on `PATH`. `PATH` is an environment variable. Every already-open shell had read its own copy of `PATH` at startup; when the installer edited the user `PATH` in the registry, the live window did not pick up the new entry. The American Standard Code for Information Interchange (ASCII) tree you drew and the `Hello, Elvis` you printed today follow the same rule: the shell that does the read is reading its own copy, not a live link. Today's `MY_NAME` is a small and reversible version of the same behaviour that decided which `tree` ran yesterday.

**Persisting the value across windows (preview)**

You have seen that closing the window wipes the value. The natural next question is how to keep a value around.

On Windows, the persistent write is a single call to a built-in operating system (OS) helper:

```powershell
[Environment]::SetEnvironmentVariable("MY_NAME", "Elvis", "User")
```

That line stores the value in the Windows registry under `HKCU\Environment`. Every process started after the call picks it up; the window that ran the call still will not see it, because that window cached its environment at startup. Passing `$null` in place of the value removes the entry.

On macOS or Linux, the persistent write is an append to the shell's startup file:

```bash
echo 'export MY_NAME="Elvis"' >> ~/.bashrc
```

On modern macOS use `~/.zshrc` instead; the mechanism is the same. Every new shell reads the file at startup and recreates the variable. Removing the line is an edit away.

Both paths are cheap to set up and cheap to undo. Both are also, for anything sensitive, the wrong answer: persisting credentials or Application Programming Interface (API) keys in plain text inside `~/.bashrc` or the user registry is a security issue, and a later lesson moves secret values out of these files into a dedicated secrets tool. For today, `MY_NAME = "Elvis"` is a safe value to practice with.

**What Module 2 added to your toolbox**

Reading a file, editing a file, walking a folder tree, installing a tool through a package manager, and now setting and reading a shell variable. Every lesson in this curriculum from here on leans on one or more of these. The version-control module starts tomorrow; Git's first install uses the package manager from L-011, and its very first config line (`git config --global user.name ...`) is an environment-variable-shaped idea: a value the tool reads out of its own storage every time you commit.

Full lesson with the full step-by-step, the three-things-should-be-true verification, and the cross-shell troubleshooting paths: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M02-files-editors-and-package-managers/lessons/L-013-set-an-environment-variable-and-read-it-back-capstone.md

Tomorrow: install Git, confirm the version, and set your first two persistent config values.

#LearnToCode #AIArchitect #SolutionsArchitecture #PowerShell #HealthcareAI
