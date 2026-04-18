# Competency Framework: Enterprise Principal AI & Data Architect

**Version:** 1.0
**Generated:** 2026-04-18
**Purpose:** Grounded, synthesis-based definition of what an Enterprise Principal AI & Data Architect actually knows and does in 2026, derived from real job descriptions and established architecture frameworks.

---

## Executive definition

An Enterprise Principal AI & Data Architect is the senior technical authority who designs, governs, and evolves how an organization collects, stores, moves, and uses data to power artificial intelligence (AI) and machine learning (ML) systems at production scale. The role blends hands-on engineering depth (Python, SQL, cloud infrastructure, MLOps, LLMOps, RAG, agentic systems) with enterprise-level strategy (reference architectures, governance frameworks, vendor trade-offs, regulatory compliance, cost modeling) and the communication skills to carry architectural decisions from a whiteboard conversation to a board-level business case. At the principal tier, the architect is accountable not just for building systems that work, but for setting the standards, patterns, and target-state blueprints that the rest of the organization builds against.

---

## Competency domains

Twelve domains, weighted by share of curriculum time. Weights reflect the reality that environment and programming foundations are disproportionately large for an absolute-beginner learner, while strategy-level domains are smaller in lesson count but higher in synthesis density. Total weights sum to 100%.

### D01, Command Line & Environment Fluency (7%)

Being able to operate a computer the way an engineer does, rather than the way a consumer does. This means the terminal, the file system, text editors, package managers, and the mental model of an operating system as a set of processes manipulating files. Every senior job description assumes this fluency without naming it, which is precisely why a career-changer must build it first.

Sub-competencies:
- Open and use a terminal on macOS, Windows (WSL), and Linux
- Navigate a file system with `cd`, `ls`, `pwd`, absolute vs. relative paths
- Create, move, copy, rename, and delete files and directories from the command line
- Read and edit plain-text files with a terminal editor (nano at minimum)
- Install and update software via package managers (Homebrew, apt, winget)
- Read and set environment variables; understand PATH
- Chain commands with pipes and redirects; understand stdin, stdout, stderr

### D02, Version Control with Git and GitHub (6%)

Every real engineering job description in the research set lists Git and GitHub or an equivalent as a baseline expectation. The learner must move from "never committed anything" to comfortable with branching, pull requests, merge conflicts, and the basic collaboration flow that every team uses. GitHub Actions (for CI/CD later) depends on this foundation.

Sub-competencies:
- Initialize a repository; stage, commit, and view history
- Push to and pull from a remote on GitHub
- Create branches, switch between them, and merge
- Resolve a merge conflict
- Open and review a pull request
- Read a `.gitignore` file and write one
- Recover from common mistakes (wrong branch, uncommitted changes, accidental commit)

### D03, Programming Foundations in Python (14%)

Python is the lingua franca of AI and data work. Every Stanford Health Care, Teladoc, Salesforce, Microsoft Digital, and AWS job description in the research set names Python specifically. The learner needs enough Python to read and modify production code, write data cleaning scripts, call APIs, and glue together the components of an AI pipeline. This does not mean computer-science-grade fluency; it means working literacy.

Sub-competencies:
- Run Python from a terminal REPL and as a script
- Use variables, primitive types, strings, lists, dictionaries, tuples, sets
- Write conditionals, loops, functions, and handle exceptions
- Create and activate virtual environments with `venv` and `uv`
- Install packages with `pip`, read a `requirements.txt`, pin versions
- Read and write files (text, CSV, JSON)
- Structure a small multi-file Python project
- Read code written by others and trace what it does

### D04, Data Fundamentals (6%)

Before databases, before SQL, before pipelines, the learner needs to understand what data actually is at a conceptual level: rows and columns, types, nulls, keys, relationships, the difference between structured, semi-structured, and unstructured data. Every data architect job description assumes this as bedrock.

Sub-competencies:
- Distinguish structured, semi-structured, and unstructured data
- Read a CSV and understand rows, columns, types, headers, and encoding
- Understand nulls, missing values, and data quality basics
- Understand primary keys, foreign keys, and referential integrity at a conceptual level
- Recognize common data formats (CSV, TSV, JSON, Parquet, Avro) and when each is used
- Understand the difference between OLTP and OLAP workloads conceptually

### D05, SQL & Data Manipulation (9%)

SQL appears in every data and AI architect job description in the research set. The NextGen Healthcare, Snowflake, and HCA listings explicitly require hands-on SQL. The learner moves from "never run a SELECT" to writing joins, aggregations, window functions, and CTEs against a realistic dataset. SQLite is the hands-on substrate; the patterns transfer to Postgres, Snowflake, BigQuery, and Databricks SQL.

Sub-competencies:
- Run SELECT queries with WHERE, ORDER BY, LIMIT
- Use aggregations with GROUP BY and HAVING
- Write INNER, LEFT, RIGHT, and FULL OUTER joins
- Use subqueries and common table expressions (CTEs)
- Use window functions for running totals and rankings
- Understand indexes at a conceptual level
- Load data into a SQLite database from CSV

### D06, Local AI & Model Runtime (8%)

Running a model locally, without an API key, without a credit card, is the fastest way to build intuition about what large language models (LLMs) actually do. Ollama, llama.cpp, and Hugging Face make this free and offline. Every modern AI architect job description from Teladoc, Databricks, and Microsoft Digital names this as a baseline experimentation skill. This domain also covers embeddings, tokenization, context windows, and why models fail.

Sub-competencies:
- Install Ollama and pull a model
- Run inference from the command line and from Python
- Understand tokens, context windows, and how they constrain inputs
- Understand the difference between base models, instruct models, and chat models
- Generate embeddings from a local model
- Compare the speed and quality of several small models on the same prompt
- Understand hardware constraints (CPU vs. GPU, RAM, quantization) at a conceptual level

### D07, Prompt Engineering & Agentic Patterns (6%)

The AWS AI Practitioner blueprint, the Azure AI-102 exam (which now weights generative AI at 25–30%), and every 2026 AI architect role treat prompt engineering and agentic patterns as core, not optional. This domain covers the techniques that actually work: clear instructions, examples, structured outputs, chain-of-thought, retrieval augmentation at a conceptual level, and the difference between a prompt, a tool-use loop, and an agent.

Sub-competencies:
- Write clear, structured prompts with context, instruction, and constraints
- Use few-shot examples and system messages effectively
- Request structured output (JSON) and validate it
- Use chain-of-thought and other reasoning patterns
- Understand the difference between a single-turn prompt, a tool-use loop, and a multi-step agent
- Evaluate prompts with a basic test set
- Recognize when prompting fails and a different technique is required

### D08, APIs & Integration (7%)

Everything real systems do, they do by talking to other systems over APIs. The learner must understand HTTP, REST, authentication, rate limits, error handling, and how to call an API from Python. The Model Context Protocol (MCP) gets its own lesson cluster because it has moved from novelty to expectation in enterprise AI architecture (named in the Teladoc and Microsoft Digital roles).

Sub-competencies:
- Understand HTTP verbs, status codes, headers, and JSON payloads
- Make authenticated requests using `curl` and Python's `requests`
- Read API documentation and build a working client
- Handle errors, retries, and rate limits gracefully
- Understand OAuth, API keys, and token-based auth at a conceptual level
- Build a tool-calling loop where a model invokes an API
- Understand what MCP is and why it exists

### D09, Cloud Fundamentals (10%)

Every principal-level job description in the research set (Stanford Health Care, NextGen Healthcare, Snowflake, Microsoft Digital, Infosys-for-UK-Healthcare, Caterpillar) requires fluency in at least one major cloud. Azure is the primary hands-on track because it is where the learner's current work context lives; every Azure lesson carries a cross-reference table showing the AWS and GCP equivalents. The learner ends able to spin up, use, and tear down basic compute, storage, networking, and managed AI services on all three hyperscalers through free-tier accounts only.

Sub-competencies:
- Understand the cloud service model: IaaS, PaaS, SaaS
- Navigate the Azure Portal, AWS Console, and GCP Console
- Create and destroy a virtual machine, a storage bucket, and a managed database on each cloud
- Understand regions, availability zones, and basic networking (VPCs, subnets, firewalls)
- Understand identity and access management (IAM) and least-privilege roles
- Use a managed AI service (Azure OpenAI, AWS Bedrock, GCP Vertex AI) from a script
- Tear down all resources to avoid charges

### D10, Infrastructure as Code with Terraform (8%)

Terraform is the unifying abstraction that lets an architect write cloud-agnostic-looking code that actually provisions AWS, Azure, or GCP resources. Every senior architect role in the research set names Infrastructure as Code or Terraform specifically. This domain is the bridge between "I clicked buttons in a portal" and "I can design reproducible infrastructure."

Sub-competencies:
- Install Terraform and understand the `init`, `plan`, `apply`, `destroy` cycle
- Read and write basic Terraform configuration (providers, resources, variables, outputs)
- Manage state files and understand why they matter
- Use modules to organize configuration
- Use remote state and understand why local state is insufficient for teams
- Provision the same resource on two different clouds to illustrate the abstraction
- Integrate Terraform with GitHub Actions for continuous deployment

### D11, Security, Governance & Responsible AI (8%)

Every healthcare and regulated-industry job description in the research set (Stanford Health Care, NextGen, Teladoc, Infosys UK Healthcare) names HIPAA, FHIR, responsible AI, explainability, auditability, and compliance as first-order requirements. This domain covers the practical: credentials management, secrets, encryption in transit and at rest, role-based access control, PHI/PII handling, AI governance frameworks, model evaluation, bias detection, and the EU AI Act / Colorado AI Act landscape.

Sub-competencies:
- Store secrets safely (never in code or Git) using environment variables and secret managers
- Understand encryption in transit (TLS) and at rest at a conceptual level
- Understand role-based access control (RBAC) and least privilege
- Recognize personally identifiable information (PII) and protected health information (PHI) and know what not to do with it
- Understand the core ideas in the NIST AI Risk Management Framework
- Evaluate an AI model for basic bias and fairness concerns
- Understand audit logging and why it matters for regulated AI
- Recognize the landscape of AI regulation (EU AI Act, state-level US laws)

### D12, System Design & Enterprise Architecture (11%)

The capstone domain. This is where the learner synthesizes everything into architect-level thinking: how to read a reference architecture, how to produce one, how TOGAF's four domains (Business, Data, Application, Technology) apply to an AI system, how to write a solution design document, how to compare build-vs-buy, how to model total cost of ownership, and how to communicate architectural trade-offs to non-technical executives. This is the domain that separates a senior engineer from a principal architect.

Sub-competencies:
- Read and critique an existing reference architecture diagram
- Produce a target-state architecture diagram for a realistic AI system
- Write a one-page solution design document
- Apply the TOGAF BDAT (Business, Data, Application, Technology) lens to decompose a problem
- Compare build-vs-buy and managed-vs-self-hosted trade-offs with a simple cost model
- Design a RAG system end-to-end (ingestion, chunking, embedding, retrieval, generation, evaluation)
- Design an LLMOps pipeline end-to-end (data prep, prompt versioning, evaluation gates, deployment, monitoring)
- Present an architectural decision to a non-technical audience in plain language

---

## Terminal capability profile

At the end of 26 weeks, the learner can:

- Open a terminal, navigate a file system, install software, and edit files without a mouse
- Write Python scripts that read data, transform it, and call APIs, and read other people's Python to understand what it does
- Clone a repository from GitHub, make changes on a branch, open a pull request, and respond to review
- Run a local large language model with Ollama, call it from Python, and explain what a token and a context window are
- Query a database with SQL, including joins, aggregations, and window functions, against a realistic dataset
- Design a retrieval-augmented generation (RAG) system on paper and build a working prototype against local documents
- Provision, use, and tear down cloud resources on Azure, AWS, and Google Cloud Platform (GCP) through their free tiers
- Write Terraform configuration that provisions equivalent resources on two different clouds
- Produce a reference architecture diagram for an enterprise AI system with data flow, security boundaries, and governance controls clearly marked
- Write a one-page solution design document that a principal-level architect would recognize as credible
- Explain the trade-offs in an architectural decision to someone who has never written code
- Identify where personally identifiable information or protected health information lives in a data flow, and name the controls that protect it
- Compare an AI architecture across Azure, AWS, and GCP and articulate the trade-offs

---

## Sources

Real job descriptions (2025–2026):

1. Stanford Health Care, Director Engineering, AI/ML (chatEHR platform). https://www.talent.com/view?id=613107274194816675, Accessed April 2026. Key requirements: AI/ML platform architecture, HIPAA, FHIR, Epic, MLOps, API design, microservices, CI/CD.

2. NextGen Healthcare, Principal Data Platform Architect. https://himalayas.app/companies/nextgen-healthcare/jobs/principal-data-platform-architect, Accessed April 2026. Key requirements: healthcare analytical data platforms, AI/ML deployment, modern data architecture (data lake, lakehouse, data mesh), Snowflake, Databricks, dbt, Fivetran, Spark, Airflow, Azure, AWS, GCP, HL7.

3. Amazon Web Services, Principal AI Solution Architect (Data & AI Specialist SA team), Job ID 3193875. https://www.amazon.jobs/en/jobs/3193875/, Accessed April 2026. Key requirements: hands-on AI specialist SA work, complex customer architectures, customer feedback advocacy, whitepapers and workshops.

4. Snowflake, Director, AI & Data Enterprise Architecture, Menlo Park. https://www.glassdoor.com/job-listing/director-ai-data-enterprise-architecture-snowflake, Accessed April 2026. Key requirements: MLOps and LLMOps pipeline design at enterprise scale, RAG architecture, agentic workflows, multi-model orchestration, cloud data platforms (Snowflake, Databricks, AWS, Azure, GCP), AI governance, TCO modeling, executive communication.

5. Salesforce, Principal Data and AI Architect (D360 and Agentforce). https://careers.salesforce.com/en/jobs/jr333491/principal-data-and-ai-architect/, Accessed April 2026. Key requirements: enterprise-grade data and AI architectures, integration with hyperscalers, data lakes, governance frameworks, pre-sales technical design.

6. Infosys, Principal Technology Architect, Microsoft Data & AI Platform (UK Public Healthcare). https://jobs.anitab.org/companies/infosys/jobs/73759072, Accessed April 2026. Key requirements: Microsoft Azure Data & AI stack, lakehouse, data mesh, cloud native integration, AI engineering (data pipelines, feature engineering, model lifecycle, MLOps), responsible AI, governance.

7. Caterpillar, Senior Principal Architect, Applied AI Enterprise. https://careers.caterpillar.com/en/jobs/r0000352674/, Accessed April 2026. Key requirements: enterprise AI applied at global scale, cross-functional architecture leadership.

8. Teladoc Health, Staff AI Engineer, GenAI. https://www.glassdoor.com/job-listing/staff-ai-engineer-genai-teladoc-health, Accessed April 2026. Key requirements: GenAI/LLM operationalization, RAG, vector search, prompt engineering, agentic AI, Model Context Protocol (MCP), Snowflake, Databricks, Azure ML, MLflow, Terraform, Python, SQL, regulated healthcare environments.

9. Microsoft Digital (Principal AI Architect, MSD). Cited in Jooble aggregation, https://jooble.org/jobs-ai-architect, Accessed April 2026. Key requirements: AI-first agentic enterprise transformation, platform architecture at global scale.

10. Concentrix, Principal Architect, AI & GCP Agentic Stack. https://jobgether.com/offer/69ac8ae50c855bd92b798ae2, Accessed April 2026. Key requirements: GCP-based agentic AI stack architecture.

11. HCA Healthcare, Principal Data Architect. Cited in ZipRecruiter aggregation, https://www.ziprecruiter.com/Jobs/Principal-Data-Architect, Accessed April 2026. Key requirements: enterprise data architecture at large healthcare system scale.

12. DevOpsSchool, Principal Data Architect role blueprint (industry synthesis). https://www.devopsschool.com/blog/principal-data-architect-role-blueprint-responsibilities-skills-kpis-and-career-path/, Accessed April 2026. Used as cross-validation of responsibilities across roles.

Framework and certification sources:

13. The Open Group, TOGAF Standard, 10th Edition (April 2022). https://www.opengroup.org/togaf, Accessed April 2026. BDAT domains (Business, Data, Application, Technology) and the Architecture Skills Framework informed D12 structure.

14. The Open Group, TOGAF Architecture Skills Framework. https://pubs.opengroup.org/togaf-standard/architecture-skills-framework/, Accessed April 2026. Generic skills, business skills and methods, enterprise architecture skills, and program or project management skills categories informed cross-domain weight decisions.

15. Microsoft Learn, AI-102 Study Guide (Designing and Implementing a Microsoft Azure AI Solution). https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-102, Accessed April 2026. 2026 domain weights: Plan and manage an Azure AI solution (25–30%), Decision support (10–15%), Vision (15–20%), Natural language processing (25–30%), Generative AI (10–15%). Informed D06, D07, and D09.

16. Amazon Web Services, AWS Certified AI Practitioner (AIF-C01) and AWS Certified Machine Learning Engineer – Associate (MLA-C01) exam guides. https://aws.amazon.com/certification/certified-ai-practitioner/ and https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/, Accessed April 2026. Five-domain structure (AI/ML fundamentals, generative AI, AWS AI services, responsible AI, security) informed D06, D07, D09, and D11.

17. AWS Training and Certification Blog, updated AI certification portfolio announcement. https://aws.amazon.com/blogs/training-and-certification/big-news-aws-expands-ai-certification-portfolio-and-updates-security-certification/, Accessed April 2026. Confirmed the retirement of MLS-C01 (March 31, 2026) and the current role-based path.

18. Databricks, LLMOps workflows reference architecture (on Azure Databricks docs). https://learn.microsoft.com/en-us/azure/databricks/machine-learning/mlops/llmops, Accessed April 2026. Informed the RAG and LLMOps sub-competencies in D12.
