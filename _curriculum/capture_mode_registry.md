# Capture Mode Registry

**Purpose.** This document tells the downstream lesson-authoring skill how to physically capture each lesson's hands-on portion. Every one of the 171 lessons in the curriculum spine has a `capture_mode` field, and the value on that field tells the authoring pipeline whether it can auto-record a terminal session, whether a human-produced document or diagram is the deliverable, or whether a screen walkthrough is required because a GUI, signup, installer, or portal is in the critical path.

This registry groups all 171 lessons by their assigned mode, explains the reasoning, and serves as the dispatch table the content-production skill will read.

---

## Summary

| Capture mode      | Lessons | Share  |
| ----------------- | ------- | ------ |
| `terminal_auto`   | 87      | 50.9 % |
| `rendered_auto`   | 23      | 13.5 % |
| `script_only`     | 61      | 35.7 % |
| **Total**         | **171** | **100 %** |

Distribution sits on the target band (50 / 15 / 35). Variance from the exact midpoint reflects the subject matter: the curriculum front-loads command-line, Git, and Python fluency (terminal-native by nature), then shifts into cloud provisioning and governance (portal and signup heavy) in the second half.

---

## Mode definitions

### `terminal_auto`

A lesson the authoring pipeline can capture end-to-end from a scripted shell session. Inputs are text commands, outputs are text lines, and the verification step can be checked by reading stdout. No browser, no desktop app, no image asset required. The pipeline runs the commands in a reproducible container, captures the transcript, and renders it as a styled terminal asciicast plus a syntax-highlighted code block.

**Production signature.** One `.sh` or `.py` input file per lesson. Pipeline replays it, diffs expected vs. actual output, and embeds the recording. Every asset is reproducible from source.

### `rendered_auto`

A lesson whose deliverable is itself a document, diagram, SVG, markdown table, report, or notebook that renders visually. The pipeline captures the source file (markdown, SVG, CSV, or notebook) and embeds the rendered output. The learner's work product is the visual artifact, not a terminal transcript.

**Production signature.** The learner commits a file to a repo. The pipeline takes that file, renders it (GitHub markdown renderer, SVG embed, notebook-to-HTML, spreadsheet-to-image), and includes the rendering in the lesson output. No narration track needed; the artifact speaks for itself.

### `script_only`

A lesson that cannot be captured as a terminal transcript because the critical path crosses a cloud provider signup flow, an installer GUI, a desktop application, a web console, or a hosted service account. These lessons require a human to record a short screen walkthrough. The downstream skill produces a scripted voiceover, a shot list, and on-screen text to guide that recording. It does not attempt to automate the capture itself.

**Production signature.** The pipeline emits a `script.md` with: scene-by-scene shot list, voiceover lines, on-screen text overlays, expected durations, and a hand-off note like "record at 1920 x 1080 with OBS, export as MP4." The learner or author does the actual recording manually.

---

## Dispatch logic for the authoring skill

```
if lesson.capture_mode == "terminal_auto":
    produce_terminal_transcript(lesson.hands_on_action)
    produce_verification_check(lesson.verification)
elif lesson.capture_mode == "rendered_auto":
    produce_artifact_template(lesson.hands_on_action)
    produce_rendered_embed(artifact_path)
elif lesson.capture_mode == "script_only":
    produce_walkthrough_script(lesson.hands_on_action)
    produce_shot_list(lesson.verification)
```

The skill reads `lesson.capture_mode` as the sole dispatch key. It does not re-infer mode from the action text at production time. This registry is the contract.

---

## `terminal_auto` lessons (87)

These all share a common capture pattern: pure shell or REPL activity, text in and text out, reproducible in a container. Rationale groupings follow.

### Shell fundamentals and file navigation (Modules M01, M02)

The command line is by definition terminal-native. Everything here is `pwd`, `cd`, `ls`, `cat`, `nano`, shell variables, and package-manager invocations that produce text output.

- L-003 [M01]: Print your first line with echo
- L-004 [M01]: Find out where you are with pwd
- L-005 [M01]: List the contents of a directory with ls
- L-006 [M01]: Move around with cd and relative paths
- L-007 [M01]: Make and remove directories (capstone)
- L-008 [M02]: Read a file's contents with cat and less
- L-009 [M02]: Edit a file with nano
- L-010 [M02]: Understand file paths, extensions, and hidden files
- L-012 [M02]: Install your first tool with a package manager
- L-013 [M02]: Set an environment variable and read it back (capstone)

### Git local operations (Module M03)

All local Git commands produce verifiable text output. The GitHub web UI steps are in `script_only`.

- L-015 [M03]: Initialize a repository in a folder
- L-016 [M03]: Track a file with git add and git commit
- L-017 [M03]: Read the history with git log and git status
- L-018 [M03]: Undo a mistake with git restore and git reset (capstone)

### Python language and REPL (Modules M05, M06, M07, M08)

Every Python lesson where the deliverable is a running script with expected stdout. The REPL is a terminal. `pip install` and `venv` are captured as shell sessions.

- L-027 [M05]: Run your first line in the Python REPL
- L-028 [M05]: Run your first Python script from a file
- L-029 [M05]: Work with variables and basic types
- L-030 [M05]: Write a script that reads input and writes a file (capstone)
- L-031 [M06]: Booleans and conditionals
- L-032 [M06]: Loops with for and while
- L-033 [M06]: Define and call your own functions
- L-034 [M06]: Functions that work together
- L-035 [M06]: Handle errors with try and except
- L-036 [M06]: Debug a broken script by reading the traceback
- L-037 [M06]: Build a number-guessing game (capstone)
- L-038 [M07]: Lists, ordered collections
- L-039 [M07]: Dictionaries, key-value lookups
- L-040 [M07]: Sets and tuples
- L-041 [M07]: Read and write text files
- L-042 [M07]: Read and write CSV files
- L-043 [M07]: Grocery category counter (capstone)
- L-045 [M08]: Create a virtual environment with venv
- L-046 [M08]: Install a package with pip
- L-047 [M08]: Pin dependencies with requirements.txt
- L-048 [M08]: Organize code into modules
- L-049 [M08]: Use a Python package: pandas for CSV handling

### Data concepts captured through scripts (Module M09)

The conceptual lessons in M09 that involve inspecting a CSV or writing a small type-detection script. The narrative lessons (structured vs. semi-structured vs. unstructured) moved to `script_only` because they are explanatory without a capturable command.

- L-052 [M09]: Rows, columns, types, and nulls
- L-054 [M09]: Common data formats: CSV, JSON, Parquet, Avro

### SQL at the command line (Modules M10, M11)

SQLite runs in the terminal. Every SELECT, JOIN, and window function produces text output that captures cleanly. The analytical capstones that produce portfolio artifacts moved to `rendered_auto`.

- L-058 [M10]: Install SQLite and open a database
- L-059 [M10]: Generate a synthetic dataset in Python
- L-060 [M10]: Load CSV data into SQLite
- L-061 [M10]: SELECT, WHERE, ORDER BY, LIMIT
- L-062 [M10]: Aggregate with GROUP BY and HAVING
- L-063 [M10]: INNER and LEFT JOIN
- L-066 [M11]: Window functions, ranking within a group
- L-067 [M11]: Window functions, running totals and moving averages
- L-068 [M11]: Indexes, explain plans, and a taste of performance
- L-069 [M11]: SQL from Python

### Local AI via Ollama Python API (Modules M12, M13)

After the initial Ollama install (which is `script_only`), every interaction with a running local model happens through a Python script or REPL session with text prompts and text completions. Embedding math runs end-to-end at the terminal.

- L-073 [M12]: Chat with a local model from the terminal
- L-074 [M12]: Call Ollama from Python
- L-075 [M12]: System prompts vs user prompts
- L-076 [M12]: Non-deterministic outputs and temperature
- L-078 [M13]: Tokens, the atoms of a model
- L-079 [M13]: Context windows and their limits
- L-081 [M13]: Generate embeddings from a local model
- L-082 [M13]: Cosine similarity, how close are two meanings

### Prompt engineering scripts (Module M14)

Prompt engineering lessons are captured as Python scripts that call a local model with varied prompts and print the results. The capstone (a full prompt library) is `rendered_auto` because the deliverable is a README plus results tables.

- L-084 [M14]: Clear prompts beat clever prompts
- L-085 [M14]: Few-shot examples, show, don't just tell
- L-086 [M14]: Request structured output as JSON
- L-087 [M14]: Chain-of-thought and step-by-step reasoning
- L-088 [M14]: Prompt evaluation with a small test set
- L-091 [M14]: Tool-calling 101, let the model ask for help
- L-092 [M14]: Multi-step tool use

### HTTP and API interactions from Python (Module M15)

HTTP status codes, request and response inspection, JSON parsing, retry logic: all Python scripts with text output. The conceptual API lesson and the auth lesson (involves real API keys from signup) are `script_only`.

- L-095 [M15]: HTTP verbs and status codes
- L-096 [M15]: JSON, the lingua franca of APIs
- L-097 [M15]: Make your first API call from Python with requests
- L-099 [M15]: Errors, retries, and rate limits
- L-100 [M15]: Weather report tool (capstone)

### Agentic tool use in the terminal (Module M16)

Function calling from a local model, two-tool agent loops, traced reasoning logs: all Python scripts that emit a trace. The conceptual lessons and the MCP-server install are `script_only`.

- L-102 [M16]: Function calling with a local model
- L-105 [M16]: Two-tool agent from scratch
- L-106 [M16]: Agent with a traced reasoning log (capstone)

### Cloud conceptual lessons (Module M17)

The one M17 lesson that is a pure terminal comparison (benchmarking a local script vs. a hypothetical cloud equivalent) stays here. Conceptual cloud lessons are `script_only`; hands-on cloud lessons are `script_only` because they involve portals.

- L-107 [M17]: Cloud vs. your laptop, the real difference

### Azure and AWS CLI install (Modules M18, M19)

The `az` and `aws` CLI invocations themselves are terminal commands; the signup and portal-verification steps around them are `script_only`. These lessons are the pure CLI-only parts.

- L-114 [M18]: Install and authenticate the Azure CLI
- L-121 [M19]: AWS CLI install and first commands
- L-125 [M19]: Managed AI services on three clouds

### Terraform local workflow (Modules M20, M21)

Terraform is entirely driven from the CLI: `terraform init`, `plan`, `apply`, `destroy`. Even the multi-cloud module capstone is captured as a sequence of `terraform` invocations. Infrastructure-as-code is a terminal activity by design.

- L-127 [M20]: What Infrastructure as Code is for
- L-128 [M20]: Install Terraform and read the version
- L-129 [M20]: Your first main.tf
- L-130 [M20]: The init-plan-apply cycle
- L-131 [M20]: Variables and outputs
- L-133 [M20]: Terraform first principles capstone
- L-135 [M21]: Refactor a config into a local module
- L-136 [M21]: Remote state, why local state breaks teams
- L-137 [M21]: The same module, but now on AWS
- L-138 [M21]: Conditional provisioning with a cloud variable
- L-140 [M21]: Multi-cloud Terraform capstone

### Environment variable handling (Module M22)

The foundational env-var and `.env` lesson captures at the terminal with a Python script. Secret-manager and identity lessons involve cloud portals and are `script_only`.

- L-142 [M22]: Environment variables and .env files

---

## `rendered_auto` lessons (23)

These are lessons whose deliverable is a visual artifact that must render on GitHub or in a presentation. The authoring pipeline takes the artifact source and embeds the rendered form.

### Portfolio-grade README (Module M04)

- L-024 [M04]: Write a .gitignore and a useful README (capstone), The deliverable is a README that renders on GitHub, with headings, code fences, and formatted sections. The rendering is the learning outcome.

### Data quality and analytical write-ups (Modules M09, M10, M11)

- L-056 [M09]: Data quality, the things that go wrong, Produces a written catalog of issues and proposed fixes as a markdown table.
- L-064 [M10]: Five business questions answered (capstone), Produces `questions.sql` plus a results table that reads as a portfolio artifact, not a terminal transcript.
- L-065 [M11]: Subqueries and CTEs, Learner writes a side-by-side comparison showing the nested version and the CTE version; the comparison itself is the deliverable.
- L-070 [M11]: Analytical query portfolio (capstone), A commit-ready `.sql` file plus a companion notebook showing results; the notebook renders on GitHub.

### LLM conceptual summary and comparison reports (Modules M12, M13)

- L-071 [M12]: What a large language model actually is, Learner writes three plain-language sentences after reading a short explainer. The written output is the artifact.
- L-077 [M12]: System-prompted comparison report (capstone), Produces `comparison.md` with side-by-side model outputs.
- L-083 [M13]: Token and embedding lab (capstone), Produces a markdown report with tokenization examples and similarity tables.

### Prompt engineering portfolio (Module M14)

- L-093 [M14]: Prompt template library (capstone), Produces `prompts.py` plus a README with failure analysis; the README is the portfolio piece.

### Architecture diagrams (Modules M17, M23, M24, M26)

- L-112 [M17]: Three-way deployment diagram (capstone), SVG diagram exported from draw.io or Excalidraw.
- L-153 [M23]: Annotated healthcare AI data flow (capstone), SVG with PII/PHI annotations.
- L-157 [M24]: Data flow first, components second, Draft SVG showing flow arrows.
- L-158 [M24]: Security boundaries and controls on the diagram, Extended SVG with trust-boundary overlays.
- L-159 [M24]: Healthcare RAG target-state architecture (capstone), Final SVG plus a two-paragraph prose summary.
- L-168 [M26]: Reference architecture diagram, publishable quality, Capstone-grade SVG ready for LinkedIn.

### Governance write-ups (Module M23)

- L-149 [M23]: Evaluate a local model for bias on a simple test set, Produces a written analysis documenting observed patterns or a defense that no concerning pattern appeared.
- L-150 [M23]: Audit logging and why it matters, Produces an enhanced JSONL log plus a short markdown note explaining the added fields.

### RAG design artifacts and executive deliverables (Modules M25, M26)

- L-161 [M25]: RAG in detail, retrieval, reranking, generation, Produces a written design document with numbered trade-offs.
- L-162 [M25]: RAG evaluation, how you know it works, Produces an evaluation plan with concrete numbers.
- L-164 [M25]: Cost, latency, and the trade-offs that matter to executives, Produces a spreadsheet plus a three-sentence executive summary.
- L-166 [M26]: Scope your capstone: pick a realistic use case, Produces `brief.md` (a one-paragraph use case brief).
- L-167 [M26]: Executive summary, 1 page for the board, Produces `executive-summary.md` under 500 words.
- L-169 [M26]: Solution design document, full version, Produces `solution-design.md`, the central portfolio artifact.

---

## `script_only` lessons (61)

These lessons require a recorded screen walkthrough because the critical path crosses a GUI, a portal, a signup form, an installer, or a desktop application.

### First-time system setup (Modules M01, M02, M03)

The absolute opening lesson (opening a terminal) is by definition a GUI interaction; the package manager install crosses a website; installing Git requires a platform-specific installer.

- L-001 [M01]: Open the terminal with a keyboard shortcut
- L-002 [M01]: Read a prompt like a sign at a train station
- L-011 [M02]: Install a package manager
- L-014 [M03]: Install Git and confirm the version

### GitHub web interactions (Module M04)

Every lesson in M04 crosses github.com: account creation, remote setup, pull requests, merge conflict resolution in an editor. These need walkthrough recordings.

- L-019 [M04]: Create a GitHub account and a first remote repository
- L-020 [M04]: Connect a local repository to a GitHub remote
- L-021 [M04]: Make a change locally, push, pull to sync
- L-022 [M04]: Work on a branch and open a pull request
- L-023 [M04]: Deliberately create and resolve a merge conflict

### Python install and first push (Modules M05, M08)

Python install crosses python.org or an installer GUI; the first Python-project-on-GitHub capstone crosses the GitHub web UI.

- L-025 [M05]: What is a programming language
- L-026 [M05]: Install Python cleanly and confirm the version
- L-044 [M08]: Why virtual environments exist
- L-050 [M08]: Put a Python project on GitHub (capstone)

### Data concepts best taught visually (Module M09)

The conceptual lessons on data-family taxonomy, key relationships, and OLTP-vs-OLAP are explanatory rather than terminal activities. The capstone classifies everyday artifacts, which benefits from a walkthrough.

- L-051 [M09]: Structured, semi-structured, unstructured, the three families
- L-053 [M09]: Primary keys, foreign keys, and relationships
- L-055 [M09]: OLTP vs OLAP, two jobs, two designs
- L-057 [M09]: Classify ten artifacts from your day (capstone)

### Local AI install and conceptual frames (Modules M12, M13)

Ollama install is a desktop application. The base-instruct-chat distinction is a conceptual frame.

- L-072 [M12]: Install Ollama and pull a first model
- L-080 [M13]: Base, instruct, and chat models

### Prompt engineering conceptual frames (Module M14)

Anti-patterns and the RAG conceptual lesson are explanatory.

- L-089 [M14]: Prompt engineering anti-patterns
- L-090 [M14]: Retrieval-augmented prompts at a conceptual level

### API conceptual frames and auth (Module M15)

The "what is an API" explainer and the auth lesson (which involves real API key handling best shown visually) need walkthroughs.

- L-094 [M15]: What is an API, in plain English
- L-098 [M15]: Authentication: API keys, headers, and secrets

### MCP conceptual frames and servers (Module M16)

MCP is a newer protocol; the authoring pipeline captures the conceptual walkthrough, the desktop client connection, and the filesystem server demo.

- L-101 [M16]: The tool-use pattern, revisited
- L-103 [M16]: What is the Model Context Protocol
- L-104 [M16]: Use an existing MCP server

### Cloud conceptual frames and the Azure portal (Modules M17, M18)

The conceptual cloud lessons are explanatory. Every Azure hands-on lesson crosses the portal for verification, even when the primary work is CLI-driven.

- L-108 [M17]: IaaS, PaaS, SaaS, three levels of abstraction
- L-109 [M17]: Regions, availability zones, and latency
- L-110 [M17]: Console vs. CLI vs. SDK
- L-111 [M17]: Shared responsibility, who is on the hook for what
- L-113 [M18]: Create a free-tier Azure account
- L-115 [M18]: Resource groups, the organizing principle
- L-116 [M18]: Create and use a storage account
- L-117 [M18]: Spin up and SSH into a virtual machine
- L-118 [M18]: Tear down your resource group (habit from day one)
- L-119 [M18]: Azure hands-on capstone

### AWS and GCP signup and portals (Module M19)

- L-120 [M19]: Create a free-tier AWS account
- L-122 [M19]: AWS S3 and EC2 in one short session
- L-123 [M19]: Create a free-tier GCP account
- L-124 [M19]: GCP Cloud Storage and Compute Engine
- L-126 [M19]: Three-cloud equivalence table (capstone)

### Terraform state and CI (Modules M20, M21)

The state-file lesson and the GitHub Actions integration both cross the GitHub web UI.

- L-132 [M20]: The state file and why it must never be in Git
- L-134 [M21]: What a Terraform module is
- L-139 [M21]: Integrate Terraform with GitHub Actions

### Secrets and identity (Module M22)

Secret managers live in cloud portals; identity and role assignments are portal operations; encryption at rest is a portal configuration.

- L-141 [M22]: The top rule: never commit a secret
- L-143 [M22]: Secret managers, the real solution
- L-144 [M22]: Identity, roles, and least privilege
- L-145 [M22]: Encryption in transit and at rest
- L-146 [M22]: Credential cleanup capstone

### Governance conceptual frames (Module M23)

PII/PHI definitions, bias concepts, NIST AI RMF, and the regulatory landscape are explanatory.

- L-147 [M23]: PII and PHI, what counts, and what doesn't
- L-148 [M23]: Model bias and fairness, the basics
- L-151 [M23]: NIST AI Risk Management Framework at a glance
- L-152 [M23]: The regulatory landscape at a glance

### Architecture diagramming craft (Module M24)

Reading a reference architecture critically, choosing a diagramming tool, and TOGAF BDAT are conceptual lessons taught through walkthrough.

- L-154 [M24]: Read a reference architecture critically
- L-155 [M24]: Choose a diagramming tool
- L-156 [M24]: TOGAF BDAT, Business, Data, Application, Technology

### RAG pipeline mechanics and LLMOps (Module M25)

The chunking-to-embedding RAG walkthrough, the LLMOps pipeline conceptual frame, and the solution-design capstone all benefit from screen walkthroughs.

- L-160 [M25]: RAG in detail, ingestion, chunking, embedding
- L-163 [M25]: LLMOps pipeline, promoting a prompt from dev to prod
- L-165 [M25]: RAG solution design document (capstone)

### Portfolio assembly and publication (Module M26)

The five-minute walkthrough is by definition a recorded presentation; the publish-the-portfolio capstone crosses GitHub and LinkedIn.

- L-170 [M26]: Five-minute walkthrough, explain it to a non-technical executive
- L-171 [M26]: Publish the portfolio (final capstone)

---

## Notes for the downstream authoring skill

1. **Do not re-classify at production time.** The `capture_mode` field on each lesson is the contract. If a lesson's mode seems wrong at production time, flag it and ask; do not change it silently.

2. **Capstones are distributed across all three modes.** Module-ending capstones at the start of the curriculum tend to be `terminal_auto` (command-line and Python basics), middle capstones split between `rendered_auto` (reports, diagrams) and `script_only` (cloud hands-on), and the final portfolio capstones are `rendered_auto` (documents and diagrams) or `script_only` (recorded walkthroughs).

3. **Every `script_only` lesson needs a shot list.** The authoring pipeline emits a scripted shot list, voiceover lines, and on-screen text for each. The learner or author records to that script.

4. **Every `rendered_auto` lesson needs an artifact template.** The pipeline emits a skeleton of the artifact (markdown file with section headers, SVG template, notebook stub) that the learner fills in.

5. **Every `terminal_auto` lesson needs a reproducible shell script.** The pipeline emits a `lesson.sh` (or `lesson.py`) with expected stdout; the recording is a replay.

6. **The dispatch is one-way.** The skill reads the mode and routes; it does not infer. This registry plus the `curriculum_spine.yaml` is the full instruction set.
