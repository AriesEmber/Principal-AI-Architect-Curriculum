"""
One-off: refresh the opening banner in the 10 published LinkedIn-post docx
deliverables so they match the new tagline/module-descriptor format.

Strategy: for each lesson, locate the paragraph in _deliverables/L-###-post.docx
whose text starts with the old role-specific tagline prefix. Strip that prefix
from the first run (leaving the lesson-specific prose intact, including any
code-formatted sibling runs). Then insert three new paragraphs before it:
bold title, plain subtitle, plain banner line.

Run from the repo root:  python _skill/scripts/refresh_linkedin_banner_docx.py
"""
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

REPO = Path(__file__).resolve().parents[2]
DELIVERABLES = REPO / "_deliverables"

LESSONS = [
    {"n": 1, "mod": 1, "title": "First Contact with the Terminal", "modday": 1,
     "prefix": "This is Day 1 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. "},
    {"n": 2, "mod": 1, "title": "First Contact with the Terminal", "modday": 2,
     "prefix": "This is Day 2 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence Architect role. Week one is the command line. "},
    {"n": 3, "mod": 1, "title": "First Contact with the Terminal", "modday": 3,
     "prefix": "I am building a 171-lesson public path from zero to a Principal Artificial Intelligence (AI) Architect role. "},
    {"n": 4, "mod": 1, "title": "First Contact with the Terminal", "modday": 4,
     "prefix": "This is Day 4 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. "},
    {"n": 5, "mod": 1, "title": "First Contact with the Terminal", "modday": 5,
     "prefix": "This is Day 5 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. "},
    {"n": 6, "mod": 1, "title": "First Contact with the Terminal", "modday": 6,
     "prefix": "This is Day 6 of a 171-lesson path I am taking publicly, from zero to a Principal Artificial Intelligence (AI) Architect role. Week one is the command line. "},
    {"n": 7, "mod": 1, "title": "First Contact with the Terminal", "modday": 7,
     "prefix": "This is Day 7 of a 171-lesson path from zero to a Principal Artificial Intelligence (AI) Architect role. Today is the week-one capstone. ",
     "capstone": True},
    {"n": 8, "mod": 2, "title": "Files, Editors, and Package Managers", "modday": 1,
     "prefix": "This is Day 8 of a 171-lesson path from zero to a Principal Artificial Intelligence (AI) Architect role. First day of module 2. "},
    {"n": 9, "mod": 2, "title": "Files, Editors, and Package Managers", "modday": 2,
     "prefix": "This is Day 9 of a 171-lesson path from zero to a Principal Artificial Intelligence (AI) Architect role. Second day of module 2. "},
    {"n": 10, "mod": 2, "title": "Files, Editors, and Package Managers", "modday": 3,
     "prefix": "This is Day 10 of a 171-lesson path from zero to a Principal Artificial Intelligence (AI) Architect role. Module 2, Day 3. "},
]


def descriptor(lesson):
    if lesson.get("capstone"):
        return f"Day {lesson['modday']}, capstone"
    return f"Day {lesson['modday']}"


def banner_text(lesson):
    return (f"Day {lesson['n']} of 171. "
            f"Module {lesson['mod']}: {lesson['title']} ({descriptor(lesson)}).")


def make_para_like(template_p, text, bold=False):
    """Build a new <w:p> copying the template's pPr, with a single Calibri run."""
    p = OxmlElement("w:p")
    template_pPr = template_p.find(qn("w:pPr"))
    if template_pPr is not None:
        p.append(deepcopy(template_pPr))

    r = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        rFonts.set(qn(attr), "Calibri")
    rPr.append(rFonts)
    if bold:
        rPr.append(OxmlElement("w:b"))
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "22")
    rPr.append(sz)
    r.append(rPr)

    t = OxmlElement("w:t")
    t.set(qn("xml:space"), "preserve")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def refresh(lesson):
    docx_path = DELIVERABLES / f"L-{lesson['n']:03d}-post.docx"
    if not docx_path.exists():
        return f"L-{lesson['n']:03d}: MISSING docx"

    doc = Document(str(docx_path))
    prefix = lesson["prefix"]

    target = None
    for p in doc.paragraphs:
        if p.text.startswith(prefix):
            target = p
            break
    if target is None:
        return f"L-{lesson['n']:03d}: FAILED — no paragraph starts with prefix"

    # Strip the prefix from the first run(s) that hold it
    remaining = prefix
    for run in target.runs:
        if not remaining:
            break
        if run.text.startswith(remaining):
            run.text = run.text[len(remaining):]
            remaining = ""
        elif remaining.startswith(run.text) and run.text:
            remaining = remaining[len(run.text):]
            run.text = ""
        else:
            return f"L-{lesson['n']:03d}: FAILED — prefix spans runs unexpectedly"
    if remaining:
        return f"L-{lesson['n']:03d}: FAILED — prefix not fully matched; leftover {remaining!r}"

    target_elem = target._element
    target_elem.addprevious(make_para_like(target_elem,
        "From zero technical knowledge to AI literacy.", bold=True))
    target_elem.addprevious(make_para_like(target_elem,
        "Through data, cloud, MLOps, and applied GenAI systems."))
    target_elem.addprevious(make_para_like(target_elem, banner_text(lesson)))

    doc.save(str(docx_path))
    return f"L-{lesson['n']:03d}: OK"


def main():
    for lesson in LESSONS:
        print(refresh(lesson))


if __name__ == "__main__":
    main()
