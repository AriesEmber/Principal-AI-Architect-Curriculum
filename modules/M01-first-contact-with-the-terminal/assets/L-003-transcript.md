# L-003 Terminal Transcript

Plain-text transcript of the five echo exchanges demonstrated in the lesson. This file is included for screen readers, since animated GIFs are inaccessible.

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

Notes on what each exchange shows:

1. **No quotes.** The shell splits the line on whitespace and passes `Hello,` and `world` as two arguments. Echo prints them joined by a single space, which happens to look identical to the quoted versions.
2. **Double quotes.** Everything inside stays one argument, and `$` variables (if any) still expand.
3. **Single quotes.** Everything inside is literal. No variable expansion.
4. **No arguments.** Echo prints just a newline, so a blank line appears and the prompt returns.
5. **Variable expansion.** The shell replaces `$USER` with the current username before echo runs. In this transcript the username is `learner`; on your machine it will be yours.
