I almost shipped a broken Day-3 lesson this week. The thing that caught it was being my own first reader.

**From zero technical knowledge to AI literacy.**
Through data, cloud, MLOps, and applied GenAI systems.

Day 3 of 171. Module 1: First Contact with the Terminal (Day 3).

Before each lesson goes live, I sit at my own machine and follow it. On Day 3 (the first real command in the curriculum: `echo`), I followed my own steps inside Windows PowerShell, typed the example for printing my username, and got a blank line back. The lesson said the commands would work the same in any shell. They do not.

Here is what the lesson teaches, what I missed the first time, and the small fix that makes the next 168 lessons safer.

![Animated typewriter walkthrough of the five echo exchanges, shown side by side in Bash and Windows PowerShell](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-003-terminal.gif)

**What L-003 teaches**

Day 3 is the first real command in the path: `echo`. You type a line, the terminal prints the same line back, and you walk away with the rhythm every command after this one shares. Argument in, result out, prompt back, ready for the next one.

Five short exchanges, each one line at the prompt followed by Enter:

1. `echo Hello, world` prints `Hello, world`. The plain form. The shell splits on whitespace and passes two arguments to echo, which joins them with a space.
2. `echo "Hello, world"` prints the same line, but with double quotes the shell treats everything inside as a single argument. That distinction matters as soon as the text contains a dollar sign or a backtick.
3. `echo 'Hello, world'` prints the same line again with a stricter rule. Single quotes block every form of shell substitution. Whatever is inside is sent to echo verbatim.
4. `echo` on its own prints a blank line and returns the prompt. A small proof that the command ran.
5. The variable example. In Bash or Zsh: `echo $USER`. In PowerShell: `echo $env:USERNAME`. Both print your own username.

That fifth exchange is where v1 of the lesson broke.

**The bug I almost shipped**

The v1 article said "every command below works identically on all three" shells. Steps 1 through 4 do. Step 5 does not. `$USER` is a Bash and Zsh idiom. PowerShell uses a different namespace, and a reader who types `$USER` in PowerShell gets a silent blank line because PowerShell treats it as an undeclared user variable, defaults it to `$null`, and has nothing to print.

That is exactly the wrong takeaway from Day 3. The first command in any learning path is the one that has to confirm the machine is talking back to you. If the very first variable example fails silently on the most popular shell on Windows, the rhythm breaks before it has a chance to form.

**The fix: two columns**

The new v2 lesson splits step 5 (and the extension experiments at the end) into two columns. The shared steps stay shared.

```bash
# Bash or Zsh
echo $USER
```

```powershell
# PowerShell
echo $env:USERNAME
```

Same observable result, different syntax.

![Static side-by-side panel showing the five echo exchanges in Bash on the left and PowerShell on the right](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/modules/M01-first-contact-with-the-terminal/assets/L-003-terminal.png)

The "What just happened" section now explains the underlying difference. Bash keeps shell variables, environment variables, and built-ins like `USER` in one flat namespace, where `$name` means "look it up here." PowerShell separates user-defined variables (in the bare `$name` namespace) from inherited environment variables (under `$env:name`). Same idea, two cabinets. The price PowerShell pays for cleaner separation is the extra prefix you have to type. The price Bash pays is exactly the silent blank line a Windows reader gets when they follow a Bash example verbatim.

If you are following along on your own machine: the trick to telling which shell you are in is to look at the prompt. If it ends in `$` or `%`, you are in Bash or Zsh. If it starts with `PS C:\...` and ends in `>`, you are in PowerShell. The lesson has a "Pick your shell" check at the top so a reader knows which column to follow before they touch the keyboard.

**The bigger fix: a new pre-flight check**

A broken Day 3 is recoverable. A pattern of broken cross-shell lessons across 171 lessons would not be. So the authoring skill itself was updated. From this point forward, any new lesson that introduces a shell command has to do one of two things:

1. Show every command in Bash, Zsh, and PowerShell forms when behavior actually differs.
2. Declare the shell restriction in the lesson's frontmatter (`shells_supported: [bash, zsh]`) and say so in the prerequisites section.

A pre-flight check in the assembly phase refuses to ship a lesson that uses a shell-specific construct without either treatment. Same mistake cannot reach `main` again, on this lesson or any lesson after it.

**The lesson behind the lesson**

I caught this by using the lesson, not by reviewing it. Reviewing your own writing is fine for grammar, voice, and flow. It does not catch "this command does not actually work in the shell my reader is most likely to be in." The only thing that catches that is sitting at the same prompt the reader will see and typing what the lesson tells you to type, on the operating system the reader is most likely to be using.

For a curriculum aimed at career-changers, that operating system is more often Windows than the macOS the author lives on. The implication for me, and for anyone publishing a path like this: the validation environment has to look like the reader's environment, not the author's. If you cannot run two operating systems on your bench, run the riskiest one.

Day 3 of a 171-lesson path. First real fix in the curriculum, and probably not the last.

Full lesson with the exact two-column commands, the shell-detection check, and the v1 archive: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md

If you ran the v1 commands on PowerShell and got a blank line back, that was not you. Try the v2 column for your shell and tell me which one matched your prompt.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #PowerShell
