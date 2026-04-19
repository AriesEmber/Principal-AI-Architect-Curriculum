> **RETIRED — v1 of this LinkedIn post.** This file is a historical snapshot of the L-003 LinkedIn variant as it shipped on 2026-04-18. It was retired on 2026-04-19 because the underlying lesson assumed Bash on every shell. The live lesson covers Bash, Zsh, and PowerShell side by side. See [RETIRED.md](./RETIRED.md) in this folder, or read [the v2 lesson](../../modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md).

---

The first time I typed a command into a terminal, I sat there for a second waiting to see if I had broken something. Then a line printed, the prompt came back, and I realised the machine was answering me. That's the whole feeling.

This is Day 3 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. Today is your first actual command: you type a line, the terminal types one back. Ten minutes, zero risk, zero files changed.

The analogy I use is a doorbell. You press once, it sounds once, and you know it worked because you heard it. That is exactly what the terminal does on the first command anyone learns. The word is `echo`. Press it like a doorbell.

![Animated typewriter walkthrough of the five echo exchanges covered in this lesson](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/_archive/L-003-v1/L-003-terminal.gif)

**The five exchanges in this lesson**

Every one of these is one line at the prompt, then Enter. The terminal prints a response and returns you to a fresh prompt, ready for the next one.

1. `echo Hello, world` prints `Hello, world`.
2. `echo "Hello, world"` prints the same thing, but with double quotes the shell treats everything inside as one argument.
3. `echo 'Hello, world'` prints the same thing again, but single quotes protect the text from every form of shell interpretation. That will matter later when the text contains a dollar sign.
4. `echo` on its own prints a blank line. A small proof that the command ran.
5. `echo $USER` prints your own username, because the shell replaced `$USER` with its value before echo ever saw the line.

![Static view of the same five exchanges as they appear in the terminal](https://raw.githubusercontent.com/AriesEmber/Principal-AI-Architect-Curriculum/main/_archive/L-003-v1/L-003-terminal.png)

**What's actually happening behind the curtain**

Echo is the simplest command in the Command-Line Interface (CLI). Its job is to print its arguments to the screen, joined by single spaces, followed by a newline. That is the whole of it.

The interesting work happened before echo was called. The shell, the program that reads your keystrokes, did two things to your line first. It split the line into tokens using whitespace as the separator. Then, when it saw `$USER`, it looked up the value of the variable and replaced the token with that value. Only after that did it hand the list of tokens to echo and ask echo to print them.

That two-step process explains the three small surprises in the exercise above.

No-quotes and double-quotes look identical because the whitespace inside `Hello,` and `world` lands in the same place either way. Single quotes would have mattered if you had written `echo '$USER'` (which prints the literal string `$USER`) compared with `echo "$USER"` (which prints your username). The no-arguments case printed a blank line because echo still emits the trailing newline even when it has nothing else to say.

**Why this is the whole atom of the terminal**

Argument in, result out, prompt back, ready for the next one. That is the command-response rhythm, and it is the full pattern of every interaction you will ever have at a command line. Python will feel like this. Git will feel like this. Terraform, the Azure CLI, the AWS CLI, every tool a principal architect uses in a normal working day will feel like this. The answers get more interesting as the curriculum goes on, but the rhythm does not change.

That is also why echo is the first real command in this path. It strips the rhythm down to its bare atoms. You type, it types back. Nothing is installed, nothing is created, nothing can break. The only thing you are training is the reflex of writing a line, pressing Enter, and reading what appears.

**Two quick experiments before you move on**

Try these two with your own terminal, while you have it open:

```bash
echo $HOME
echo $SHELL
```

`$HOME` prints the absolute path of your home folder. `$SHELL` prints the path of the shell program reading the commands (probably `/bin/zsh` on macOS or `/bin/bash` on most Linux). Both are set automatically when you log in. Both will reappear in later lessons about environment variables and filesystem navigation.

One more, a little denser:

```bash
echo "My user is $USER and my shell is $SHELL"
```

The shell expanded both variables inside the double-quoted string and handed echo a finished sentence. Same mechanism as before, used more densely.

**The verification**

If `echo Hello, world` printed `Hello, world` on the next line and returned you a prompt, the lesson is done. Three times over, counting the quoted variants. If it produced `command not found`, you typed a letter wrong. If it printed quote marks in the output, your quotes were curly smart-quotes from a word processor, not straight quotes from the keyboard.

Ten minutes. One word. The first real command in the curriculum, and the whole pattern of every command after it.

Full lesson with the extension exercise and the Windows PowerShell variant: https://github.com/AriesEmber/Principal-AI-Architect-Curriculum/blob/main/modules/M01-first-contact-with-the-terminal/lessons/L-003-print-your-first-line-with-echo.md

Try it and tell me what your `echo $SHELL` printed. That will tell us which flavour of command line you are on, and which week-two lesson to read closely.

#LearnToCode #AIArchitect #SolutionsArchitecture #TerminalBasics #HealthcareAI
