# NextEco

NextEco makes the **cost of running** visible inside a repository.

![NextEco](assets/logo.png)

NextEco is an **agent-ready engineering framework** that adds a reproducible, test-backed **Cost of Running** feature to any codebase.

It helps teams estimate and document the running cost of software across three dimensions:

- 💰 **money**
- 🪫 **energy**
- 💨 **carbon**

using engineering artifacts developers already trust:

- explicit formulas
- reproducible benchmarks
- test-driven programming and thus testable outputs
- version-controlled source files
- honest handling of uncertainty

For carbon estimation, NextEco uses transparent, auditable methodology and can be aligned with references such as [Green Algorithms](https://calculator.green-algorithms.org/ai) and low-level OS routines such as `powermetrics` for macOS and equivalent for the other OSes.

This is **not** a dashboard.  
This is **not** vague ESG theater.  
This is **not** AI-made-up numbers.

Instead, NextEco helps coding agents wire a cost model directly into your repository so that the result is:

- reviewable
- reproducible
- benchmark-backed
- test-integrated
- maintainable over time

Paste one prompt into Cursor, Claude Code, Copilot Agent, Antigravity, Windsurf or another agentic IDE.  
The agent audits your repo and builds the cost-estimation layer directly into the codebase.

> **What does it actually cost to run my code?**

As software becomes more compute-heavy, model-heavy and API-heavy, teams need to understand the operational footprint of what they ship:

- What does one request cost?
- What does one job cost?
- What does one inference cost?
- What does AI training cost?
- Where is energy being wasted?
- Which part is local compute vs external API spend?
- Which assumptions are measured and which are placeholders?

That is the problem NextEco solves.

> **Treat cost estimation like engineering, not storytelling.**

That means:

- one source of truth
- one canonical unit of work
- explicit formulas
- measurable assumptions
- benchmark-backed runtime data
- generated documentation
- test-driven programming for arithmetic and synchronization
- honest `TODO`s instead of fake confidence

---

## The pitch

**NextEco turns “What does this cost to run?” into a reproducible, test-backed repository feature.**

### ⚠️ Problem / Opportunity
- Most repos ship with zero honest cost data — no money, no energy, no carbon.
- AI agents asked naively invent plausible-looking numbers with false confidence.
- Teams usually discover the gap only when an operator asks: *“What does this actually cost to run?”*

### 💎 Value proposition
- Drop one prompt, get a reproducible, test-backed cost model in minutes.
- Honest by design: a strict taxonomy — **measured / estimated / placeholder / TODO** — prevents hallucinated figures.
- Works with any agentic tool (Claude Code, Cursor, Copilot Agent, Windsurf…).

### 🧪 Secret sauce
- A single canonical unit of work anchors every number to something measurable.
- The YAML is the source of truth; the README section is generated from it.
- Formula-coherent tests catch any drift between the model and the documentation.

### 💰 Business model
- The prompts are the product — free, open, public domain ([The Unlicense](https://unlicense.org)).
- Cost models produced are source-controlled assets owned by the repo team.
- No telemetry, no SaaS, no lock-in.

### 📣 Marketing
- Storytelling: *"What does this actually cost to run?"*
- Demo: run the prompt on any repo → get an honest cost table in one pass.
- Positioning: *"An honest placeholder beats a confident lie."*

### 🦅 Competition
- Hand-written README sections (stale, unverified, untested).
- Naive AI queries (hallucinated numbers, no taxonomy, no tests).
- Heavy cost-tracking infrastructure (dashboards, telemetry agents, cloud bills).

---

## Why engineers like it

### Honest
If the agent does not know a number, it must say so.

It uses statuses such as:

- `measured`
- `estimated`
- `placeholder`
- `TODO`

A cost model becomes reviewable instead of theatrical.

### Lightweight
No dashboards. No SaaS. No lock-in.

Just a small set of files, scripts, tests and documentation inside the repo.

### Test-backed
If the model says:

```text
total_usd = local_compute_usd + external_api_usd
```

the repo should contain a test that verifies it.

### Operationally meaningful
NextEco forces the agent to choose a **canonical unit of work**, such as:

- one CLI invocation
- one API request
- one video processed
- one training job
- one report generated

Without that anchor, cost tables are usually noise.

---

## What you get

Run one prompt and the agent typically creates or updates:

| File | Purpose |
|---|---|
| `README.md` | Managed `Cost of Running` section with assumptions, scenarios and method |
| `cost_of_running.yaml` | Machine-readable source of truth |
| `scripts/update_cost_of_running.py` | Regenerates the README cost section from YAML |
| test files | Verify formulas, schema coherence and README sync |
| benchmark file | Measures the canonical unit of work reproducibly |
| profiling helper(s) | Explain where cost comes from *(advanced only)* |
| `AGENTS.md` | Maintenance hints for future coding agents, if present |

The result is not a report.  
It is a **maintainable subsystem**.

---

## Two modes

NextEco ships with two prompt depths:

- [`core.md`](core.md): default, test-first cost estimation workflow
- [`advanced.md`](advanced.md): deeper profiling and hardware-aware metrology

### Use Core when

- you want the fastest path to something useful
- you care more about reliable structure than deep profiling
- you want honest cost estimation in any repo

### Use Advanced when

- runtime or energy is a serious product concern
- a benchmark already exists
- you want to explain where cost comes from, not just report totals
- you need deeper profiling or hardware-specific metrology

When in doubt, start with [`core.md`](core.md).

---

## Methodology

NextEco follows a simple doctrine:

> A. Tests **prove** the deliverable works  
> B. AI **identifies** the cost and its canonical unit of work  
> C. The benchmark **measures** that cost  
> D. The profiler **explains** that cost *(Advanced only)*

Cost is treated as a software metric, alongside correctness, latency, memory and reliability.

That includes at least three dimensions:

- 💰 **money**
- 🪫 **energy**
- 💨 **carbon**

---

## Explicit, auditable math

NextEco is grounded in simple formulas the agent must document and preserve.

$$
E_{\text{kWh}} = t_{\text{h}} \times P_{\text{kW}}
$$

$$
C_{\text{USD}} = E_{\text{kWh}} \times p_{\text{USD/kWh}}
$$

$$
\text{CO}_2\text{e}_{\text{g}} = E_{\text{kWh}} \times I_{\text{gCO}_2\text{e/kWh}}
$$

| Symbol | Meaning | Unit |
|---|---|---|
| $E_{\text{kWh}}$ | Energy consumed | kWh |
| $t_{\text{h}}$ | Wall-clock runtime | hours |
| $P_{\text{kW}}$ | Average power draw | kW |
| $C_{\text{USD}}$ | Local compute electricity cost | USD |
| $p_{\text{USD/kWh}}$ | Electricity price | USD / kWh |
| $\text{CO}_2\text{e}_{\text{g}}$ | Carbon footprint | g CO₂e |
| $I_{\text{gCO}_2\text{e/kWh}}$ | Grid carbon intensity | g CO₂e / kWh |

The point is not sophistication.  
The point is **clarity, auditability and testability**.

---

## Metrology

NextEco pushes the agent toward actual local measurement whenever possible, using OS tools such as:

- `powermetrics` on macOS
- `powertop` on Linux
- `powercfg` on Windows

When measurement is not yet possible, the framework requires the agent to say so explicitly and leave a visible placeholder or `TODO`.

That is not a weakness, it is scientific hygiene.

---

## Example schema

A typical `cost_of_running.yaml` may look like this:

```yaml
date_updated: YYYY-MM-DD

unit_of_work:
  name: "one CLI invocation"
  description: "..."
  rationale: "..."

methodology:
  approach: "Green Algorithms-inspired"
  formula_notes:
    - "energy_kwh = runtime_hours * average_power_kw"
    - "carbon_gco2e = energy_kwh * carbon_intensity_gco2e_per_kwh"
  benchmark:
    status: "measured|not_run|TODO"

assumptions:
  electricity:
    usd_per_kwh: 0.12
    status: "estimated"

scenarios:
  - name: "typical"
    per_unit:
      runtime_s: 4.2
      energy_kwh: 0.00023
      total_usd: 0.0042
      carbon_gco2e: 0.11
    data_quality: "medium"

todos:
  - "TODO: validate runtime on target hardware"
```

Two distinctions matter:

- `status` describes the provenance of a specific assumption
- `data_quality` describes confidence in the scenario as a whole

That separation keeps the model clean.

---

## How to use

### Claude Code

```bash
claude "$(cat core.md)"
# or
claude "$(cat advanced.md)"
```

### Cursor / Windsurf / VS Code Agent / Copilot Agent

Open the agent chat, paste the contents of [`core.md`](core.md) or [`advanced.md`](advanced.md) and send.

### Any other agentic coding tool

Paste the full prompt into the agent input.  
The prompts are designed to be self-contained.

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

NextEco does not try to replace cloud billing platforms, observability suites or enterprise carbon accounting systems.

It solves a narrower problem:

> **How to add an honest, lightweight, engineering-grade cost model directly into a software repository.**

That narrowness is one of its strengths.

---

## Contributing

Issues and pull requests are welcome.

The prompts are the product.

Good contributions usually improve one or more of the following:

- agent behavior
- reproducibility
- clarity
- portability
- auditability
- testability
- honesty under uncertainty

When changing a prompt, test it on at least one real repository.

---

## Author

**Warith Harchaoui, Ph.D.**  

Head of AI at [NEXTON](https://nexton-group.com)

---

## Acknowledgments

This project grew out of discussions with:

- [Yann Lechelle](https://www.linkedin.com/in/ylechelle), leader and co-founder of [probabl.ai](https://probabl.ai)
- [Laurent Panatanacce](https://www.linkedin.com/in/panatanacce), mentor in business and AI and AI Business Enabler at [NEXTON](https://nexton-group.com)

---

## License

[The Unlicense](https://unlicense.org) — public domain, no conditions.  
See [LICENSE](LICENSE).
