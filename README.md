# NextEco

![NextEco](assets/logo.png)

**NextEco** turns **cost of running** into a small, repository-native engineering subsystem.

It helps teams make one thing explicit:

> **what does this code actually cost to run?**

Not in vague storytelling terms, but in four concrete dimensions:

- 💰 **money**
- ⏱️ **time**
- 🪫 **energy**
- 💨 **CO₂**

NextEco exists in **two complementary forms**:

1. **this OSS repository** — for humans, open discussion, code, tests, examples, and releases
2. **an embedded skill** in [`skill/nexteco/`](skill/nexteco/) — for Claude-style agents and AI-powered IDE workflows

That split is intentional.

- the **repository** is the public source of truth
- the **skill** is the agent-native execution layer

---

## Why NextEco exists

Modern software is increasingly:

- compute-heavy
- API-heavy
- model-heavy
- geographically sensitive in cost and CO₂ terms

Yet most repositories still cannot answer a basic engineering question:

> **what is the cost of one representative unit of work?**

What does one request cost?  
What does one batch job cost?  
What does one inference cost?  
What does one training run cost?  
Which part is local compute, and which part is external API spend?

NextEco helps teams answer those questions with a workflow that is:

- small
- explicit
- reviewable
- reproducible
- benchmark-aware
- honest about uncertainty

It is **not** a dashboard.  
It is **not** SaaS.  
It is **not** ESG theater.  
It is **not** AI-made-up numbers.

It is a lightweight developer tool plus an agent workflow.

---

## The pitch

**NextEco turns “What does this cost to run?” into a reproducible, test-backed repository feature.**

### Problem
- Most repositories ship with no honest cost model at all
- Naive AI prompting often produces plausible-looking but ungrounded numbers
- Teams usually discover the gap only when an operator, client, or reviewer asks a very practical question

### Value
- Drop one workflow into a repo, get a reusable cost model
- Keep assumptions visible instead of hidden
- Treat cost as an engineering concern, not a marketing narrative
- Make future maintenance easier for both humans and agents

### Secret sauce
- one canonical unit of work
- one YAML source of truth
- one generated Markdown report
- explicit formulas
- meaningful validation
- benchmark-aware reasoning
- honest uncertainty through a strict taxonomy

> **An honest placeholder beats a confident lie.**

---

## What you get

### In the OSS repo

- a Python CLI
- reusable YAML templates
- Markdown report generation
- validation logic
- tests
- examples
- docs
- GitHub-ready project structure
- an embedded skill package

### In the embedded skill

- trigger-aware [SKILL.md](skill/nexteco/SKILL.md)
- progressive-disclosure references
- reusable templates and helper scripts
- a Claude-style workflow for creating or improving a `cost_of_running` subsystem directly inside another repo

The result is not a one-off report.

It is a **maintainable subsystem**.

---

## Install the CLI

### From source

```bash
pip install .
```

### For development

```bash
pip install -e .[dev]
pytest
```

---

## Quick start

### 1. Initialize a model

```bash
nexteco init --template min
```

This creates `cost_of_running.yaml`.

### 2. Validate the model

```bash
nexteco validate cost_of_running.yaml
```

### 3. Render the report

```bash
nexteco render cost_of_running.yaml --output cost_of_running.md
```

---

## CLI reference

### `nexteco init`

Create a starter YAML file.

```bash
nexteco init --template min --output cost_of_running.yaml
nexteco init --template full --force
```

### `nexteco validate`

Validate structure, statuses, arithmetic coherence, and provenance freshness signals.

```bash
nexteco validate cost_of_running.yaml
```

### `nexteco render`

Generate a Markdown report from the YAML source of truth.

```bash
nexteco render cost_of_running.yaml
nexteco render cost_of_running.yaml --output docs/cost_of_running.md
```

### Lightweight benchmark helper

A tiny benchmark helper is included for smoke-level performance visibility:

```bash
python scripts/benchmark_render.py cost_of_running.full.yaml.example --iterations 5
```

---

## Philosophy

NextEco follows a simple doctrine:

1. **choose one canonical unit of work**
2. **keep one YAML source of truth**
3. **generate human-readable Markdown from it**
4. **test the logic that matters**
5. **benchmark when warranted**
6. **never blur measured and estimated values**

The honesty taxonomy is central:

- `measured`
- `estimated`
- `placeholder`
- `TODO`

An honest placeholder beats a confident lie.

---

## Why engineers like it

### Honest
If the system does not know a number, it must say so.

### Lightweight
No dashboards. No SaaS. No lock-in. Just files, scripts, validation, and documentation inside the repo.

### Test-backed
If the model says:

```text
total_cost_usd = local_compute_cost_usd + external_api_cost_usd
```

the repo should be able to verify that logic.

### Operationally meaningful
NextEco forces the system to choose a **canonical unit of work**, such as:

- one CLI invocation
- one API request
- one inference
- one batch job
- one training run
- one report generation

Without that anchor, cost discussions usually become noise.

---

## Methodology

NextEco treats cost as a software metric, alongside correctness, latency, memory, and reliability.

The model is expressed per **canonical unit of work** across four dimensions:

- 💰 **money**
- ⏱️ **time**
- 🪫 **energy**
- 💨 **CO₂**

The math is intentionally simple and auditable:

$$
E_{kWh} = t_h \times P_{kW}
$$

$$
C_{USD} = E_{kWh} \times p_{USD/kWh}
$$

$$
CO2e_g = E_{kWh} \times I_{gCO2e/kWh}
$$
| Symbol | Meaning | Unit |
|---|---|---|
| $E_{\mathrm{kWh}}$ | Energy consumed | kWh |
| $t_{\mathrm{h}}$ | Wall-clock runtime | hours |
| $P_{\mathrm{kW}}$ | Average power draw | kW |
| $C_{\mathrm{USD}}$ | Local compute electricity cost | USD |
| $p_{\mathrm{USD}/\mathrm{kWh}}$ | Electricity price | USD / kWh |
| $\mathrm{CO_2e}_{\mathrm{g}}$ | CO₂ footprint | g CO₂e |
| $I_{\mathrm{g\ CO_2e}/\mathrm{kWh}}$ | Grid CO₂ intensity | g CO₂e / kWh |
The point is not sophistication.  
The point is **clarity, auditability, and testability**.

For CO₂ estimation, NextEco can align with Green Algorithms-style reasoning and low-level OS routines such as `powermetrics` on macOS and equivalent tools on Linux and Windows when real measurement is possible.

---

## Metrology and scientific hygiene

NextEco pushes toward actual local measurement whenever possible, using OS-level tools such as:

- `powermetrics` on macOS
- `powertop` or `turbostat` on Linux
- `powercfg` or `perfmon` on Windows

When direct measurement is not available, the framework requires the result to remain explicit about estimation and to leave a visible placeholder or `TODO`.

That is not a weakness.  
That is scientific hygiene.

---

## Repository structure

```text
nexteco/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── pyproject.toml
├── core.md
├── advanced.md
├── docs/
├── nexteco/
├── tests/
├── examples/
├── skill/
│   └── nexteco/
└── .github/
```

---

## The two forms of NextEco

## 1. OSS repository

This is the canonical public project.

It is for:

- GitHub visibility
- community discussion
- open-source credibility
- candidate signaling
- releases and versioning
- code review and contribution

## 2. Embedded skill

This is the canonical agent interface.

It is for:

- Claude-style agents
- AI-powered IDEs
- repeatable workflow execution
- trigger-aware behavior
- progressive disclosure of methodology

The repo owns the source of truth.  
The skill inherits the workflow.

---

## Documentation map

- [`docs/methodology.md`](docs/methodology.md)
- [`docs/yaml-schema.md`](docs/yaml-schema.md)
- [`docs/repo-archetypes.md`](docs/repo-archetypes.md)
- [`docs/benchmark-patterns.md`](docs/benchmark-patterns.md)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`skill/nexteco/SKILL.md`](skill/nexteco/SKILL.md)

---

## Examples

Illustrative examples are included to show different cost profiles:

- [`examples/rag_llm_judge_chatgpt4o.md`](examples/rag_llm_judge_chatgpt4o.md) — API-dominated
- [`examples/rag_llm_judge_ollama_gemma3_4b.md`](examples/rag_llm_judge_ollama_gemma3_4b.md) — local-compute-dominated
- [`examples/generated_from_full_example.md`](examples/generated_from_full_example.md) — generated from the current full template

The goal is not fake precision.  
The goal is honest, reusable engineering structure.

---

## How to use NextEco with agents

### Claude Code

```bash
claude "$(cat core.md)"
# or
claude "$(cat advanced.md)"
```

### Cursor / Windsurf / Copilot Agent / other AI IDE workflows

Open the agent chat, paste the contents of [`core.md`](core.md) or [`advanced.md`](advanced.md), and let the agent work directly in the repository.

### Embedded skill

The embedded skill in [`skill/nexteco/`](skill/nexteco/) is the more structured, reusable agent-native version of the same workflow.

---

## Who this is for

NextEco is especially relevant for:

- teams using paid APIs
- AI products with nontrivial inference costs
- developer tools with meaningful local compute usage
- data workflows with recurring jobs
- repositories where users or operators care about runtime footprint
- engineering organizations that want trustworthy sustainability discussions instead of theater

---

## What NextEco is not

NextEco does not try to replace:

- cloud billing platforms
- observability suites
- enterprise CO₂ accounting systems

It solves a narrower problem:

> **how to add an honest, lightweight, engineering-grade cost model directly into a software repository**

That narrowness is one of its strengths.

---

## Roadmap

Near-term priorities:

- strengthen validation ergonomics
- improve report rendering quality
- expand repo archetype guidance
- refine the embedded skill
- make polyglot usage even clearer
- richer JSON/YAML Schema export
- optional HTML rendering
- stronger scenario arithmetic checks
- more end-to-end examples from real repositories
- lightweight CI for tests, example validation, skill packaging, and benchmark smoke checks
- cautious CD for release artifacts once the project surface is stable

See [`docs/roadmap.md`](docs/roadmap.md).

---

## Contribution philosophy

NextEco should remain:

- small
- sharp
- auditable
- boring in the best sense
- honest about uncertainty

We prefer durable engineering assets over polished theater.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Author

[Warith Harchaoui, Ph.D.](https://www.linkedin.com/in/warith-harchaoui/)
Head of AI at [NEXTON](https://nexton-group.com)

---

## Acknowledgments

This project grew out of discussions with:

- [Yann Lechelle](https://www.linkedin.com/in/ylechelle), leader and co-founder of [probabl.ai](https://probabl.ai)
- [Laurent Panatanacce](https://www.linkedin.com/in/panatanacce), AI Business Enabler at [NEXTON](https://nexton-group.com)

---

## License

[The Unlicense](https://unlicense.org) — public domain, no conditions.  
See [LICENSE](LICENSE).
