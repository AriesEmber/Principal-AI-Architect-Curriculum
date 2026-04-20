"""Build L-007 (capstone) side-by-side Bash + PowerShell assets.

The capstone chains pwd, mkdir, ls, cd, touch/New-Item, cd .., rm/Remove-Item.
Ten exchanges total; the layout scales by height automatically.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "common"))

from side_by_side import (  # noqa: E402
    ARG_QUOTED,
    Exchange,
    LessonConfig,
    Note,
    OUTPUT_GREEN,
    OUTPUT_GREY,
    Segment,
    Side,
    TEXT_BASH,
    TEXT_PS,
    build_all,
)


ASSET_DIR = (
    HERE.parent.parent.parent
    / "modules"
    / "M01-first-contact-with-the-terminal"
    / "assets"
)


CONFIG = LessonConfig(
    lesson_id="L-007",
    title="L-007 \u00b7 capstone \u00b7 pwd + ls + cd + mkdir + rm in two shells",
    bash_prompt_path="~",
    ps_prompt_path="C:\\Users\\learner",
    caption=(
        "Week-one capstone. Same six verbs, two shells. The prompt path "
        "stays synchronised across both columns."
    ),
    note=Note(
        left_text=(
            "Bash: mkdir, touch, rm -r are separate programs. Creation is "
            "silent; removal is recursive when -r is passed."
        ),
        right_text=(
            "PowerShell: mkdir wraps New-Item -ItemType Directory. Use "
            "New-Item for files, Remove-Item -Recurse to delete trees."
        ),
    ),
    exchanges=[
        Exchange(
            step_label="1. Confirm start",
            left=Side(
                cmd=[Segment("pwd", TEXT_BASH)],
                out=[Segment("/home/learner", OUTPUT_GREEN)],
            ),
            right=Side(
                cmd=[Segment("pwd", TEXT_PS)],
                out=[Segment("C:\\Users\\learner", OUTPUT_GREEN)],
            ),
        ),
        Exchange(
            step_label="2. Make a directory",
            left=Side(
                cmd=[
                    Segment("mkdir ", TEXT_BASH),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
            right=Side(
                cmd=[
                    Segment("mkdir ", TEXT_PS),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("Directory: C:\\Users\\learner", OUTPUT_GREEN)],
            ),
        ),
        Exchange(
            step_label="3. Confirm it exists",
            left=Side(
                cmd=[Segment("ls", TEXT_BASH)],
                out=[Segment("Desktop  Documents  practice-cli", OUTPUT_GREEN)],
            ),
            right=Side(
                cmd=[Segment("ls", TEXT_PS)],
                out=[Segment("Desktop  Documents  practice-cli", OUTPUT_GREEN)],
            ),
        ),
        Exchange(
            step_label="4. Walk into it",
            left=Side(
                cmd=[
                    Segment("cd ", TEXT_BASH),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
            right=Side(
                cmd=[
                    Segment("cd ", TEXT_PS),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
        ),
        Exchange(
            step_label="5. Create a file",
            left=Side(
                cmd=[
                    Segment("touch ", TEXT_BASH),
                    Segment("hello.txt", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
            right=Side(
                cmd=[
                    Segment("New-Item ", TEXT_PS),
                    Segment("hello.txt", ARG_QUOTED),
                ],
                out=[Segment("Mode  Name -----  hello.txt", OUTPUT_GREEN)],
            ),
        ),
        Exchange(
            step_label="6. Confirm the file",
            left=Side(
                cmd=[Segment("ls", TEXT_BASH)],
                out=[Segment("hello.txt", OUTPUT_GREEN)],
            ),
            right=Side(
                cmd=[Segment("ls", TEXT_PS)],
                out=[Segment("hello.txt", OUTPUT_GREEN)],
            ),
        ),
        Exchange(
            step_label="7. Walk back up",
            left=Side(
                cmd=[
                    Segment("cd ", TEXT_BASH),
                    Segment("..", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
            right=Side(
                cmd=[
                    Segment("cd ", TEXT_PS),
                    Segment("..", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
        ),
        Exchange(
            step_label="8. Remove the tree",
            left=Side(
                cmd=[
                    Segment("rm -r ", TEXT_BASH),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
            right=Side(
                cmd=[
                    Segment("Remove-Item -Recurse ", TEXT_PS),
                    Segment("practice-cli", ARG_QUOTED),
                ],
                out=[Segment("(no output)", OUTPUT_GREY)],
            ),
        ),
        Exchange(
            step_label="9. Confirm it is gone",
            left=Side(
                cmd=[Segment("ls", TEXT_BASH)],
                out=[Segment("Desktop  Documents  Downloads", OUTPUT_GREEN)],
            ),
            right=Side(
                cmd=[Segment("ls", TEXT_PS)],
                out=[Segment("Desktop  Documents  Downloads", OUTPUT_GREEN)],
            ),
        ),
    ],
)


def main() -> None:
    # The capstone has 9 exchanges and long commands; skip every other
    # typing frame and drop to a 32-colour palette to stay under the 2 MB cap.
    paths = build_all(
        CONFIG,
        ASSET_DIR,
        file_stem="L-007-terminal",
        typing_step=3,
        colors=20,
    )
    for role, p in paths.items():
        size_kb = p.stat().st_size / 1024
        print(f"  {role}: {p.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
