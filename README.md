# NextEco

**Coding prompts for adding honest cost accounting to any software repository.**

![NextEco](assets/logo.png)

Drop one of these prompts [core.md](core.md) or [advanced.md](advanced.md) into VS Code (Copilot Agent), Cursor, Antigravity, Windsurf, Claude Code, or any agentic coding tool. The AI will audit your repo and implement a reproducible, test-backed "Cost of Running" feature — covering:
  + 💰 money
  + 🪫 energy
  + 💨 $\text{CO}_2$ 

The ambition of this repository is to embody good practice in cost accounting across six dimensions:
1. *reproducibility*, so cost estimation can be regenerated from code and committed artifacts
2. *honesty*, so unknowns remain clearly marked as unknowns and assumptions are explicit
3. *traceability*, so every number has clear provenance
4. *testability*, so formulas and README synchronization are verified by tests (which is already a good practice in coding)
5. *operational relevance*, so the canonical unit of work is meaningful to real users and operators
6. *minimalism*, so the solution stays lightweight, practical, and free from observability theater (too often widespread for these subjects)

---

## Doctrine for cost of running

> A. Tests prove the deliverable works.
>
> B. The AI identifies the cost and its canonical unit of work.
>
> C. The benchmark measures that cost.
>
> D. The profiler explains that cost. *(Advanced only)*

---

## The problem these prompts solve

Most repos have no honest answer to: *"What does it actually cost to run this?"*

Cost estimation is a tedious and overlooked aspect of software development. These prompts solve this problem by providing a simple and effective way to add honest cost accounting to any software repository.  The result is a cost model that is useful immediately and honest about what it does not know.




## Which prompt to use

We have two similar prompts:
  + [core.md](core.md) which is test-oriented
  + [advanced.md](advanced.md) which is test-oriented with a profiler approach

| Situation | Use |
|---|---|
| Any repo needing honest cost accounting | **Core** |
| Runtime, memory, or energy is a primary concern for users/operators | **Advanced** |
| A benchmark already exists in the repo | **Advanced** |
| You want profiling to explain where cost comes from | **Advanced** |

When in doubt, start with Core. You can always re-run Advanced later.

---

## What the agent will produce

Both prompts instruct the agent to create or update:

| File | Purpose |
|---|---|
| `README.md` | `## Cost of Running` section with scenario table, assumptions, methodology |
| `cost_of_running.yaml` | Single source of truth for all cost data |
| `scripts/update_cost_of_running.py` (or equivalent) | Helper script to regenerate the README section from YAML |
| Test files | Formula-coherent tests, YAML validation, README sync checks |
| Benchmark file | Reproducible benchmark targeting the canonical unit of work |
| `scripts/profile_*.py` (Advanced only, when warranted) | Lightweight profiling script |
| `AGENTS.md` (if present) | Maintenance note for future agents |

---

## How to use

**Claude Code:**
```bash
claude "$(cat core.md)"
# or
claude "$(cat advanced.md)"
```

**Cursor / Antigravity / Windsurf / VS Code Agent:**
Open the agent chat, paste the contents of [`core.md`](core.md) or [`advanced.md`](advanced.md), and send.

**Any other agentic tool:**
Paste the prompt contents into the agent's input. The prompt is self-contained.

---

## Design principles

These prompts were designed around a few hard lessons:

**Honesty over completeness.** The agent is explicitly told to prefer `TODO` over invented numbers. An honest placeholder is more useful than a confident lie.

**Tests are not optional.** Every cost model the agent creates must be backed by formula-coherent tests. If `total_usd = local_compute_usd + api_usd`, a test verifies that arithmetic.

**One canonical unit of work.** The agent picks exactly one and justifies it. Multiple competing tables create confusion.

**Conservative defaults.** When data is missing, the agent uses conservative assumptions and marks them clearly.

**Minimal footprint.** No dashboards, no telemetry, no heavy infrastructure. The smallest reasonable mechanism to keep the cost model accurate.

---

## The YAML schema

Both prompts produce a `cost_of_running.yaml` with this structure:

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
    status: "estimated"   # measured | estimated | placeholder
scenarios:
  - name: "typical"
    per_unit:
      runtime_s: 4.2
      energy_kwh: 0.00023
      total_usd: 0.0042
      carbon_gco2e: 0.11
    data_quality: "medium"  # low | medium | high
todos:
  - "TODO: validate runtime with powermetrics on target hardware"
```

The `status` field on assumptions describes data provenance. The `data_quality` field on scenarios describes overall confidence in that scenario's numbers. They are intentionally distinct.

---

## Methodology

Both prompts use a [Green Algorithms](https://calculator.green-algorithms.org/ai) methodology:

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
| $P_{\text{kW}}$ | Average power draw of the hardware | kW |
| $C_{\text{USD}}$ | Local compute electricity cost | USD |
| $p_{\text{USD/kWh}}$ | Electricity price | USD / kWh |
| $\text{CO}_2\text{e}_{\text{g}}$ | Carbon footprint | g CO₂e |
| $I_{\text{gCO}_2\text{e/kWh}}$ | Grid carbon intensity | g CO₂e / kWh |

All formulas are explicit in the YAML and verified by tests.

---

## Pitch *(Guy Kawasaki style)*

#### ⚠️ Problem / Opportunity
- Most repos ship with zero honest cost data — no money, no energy, no carbon.
- AI agents asked naively invent plausible-looking numbers with false confidence.
- Teams only discover the gap when an operator asks "what does this actually cost to run?"

#### 💎 Value proposition
- Drop one prompt, get a reproducible, test-backed cost model in minutes.
- Honest by design: a strict taxonomy — **measured / estimated / placeholder / TODO** — prevents hallucinated figures.
- Works with any agentic tool (Claude Code, Cursor, Copilot Agent, Windsurf…).

#### 🧪 Secret sauce
- A single canonical unit of work anchors every number to something measurable.
- The YAML is the source of truth; the README section is generated from it.
- Formula-coherent tests catch any drift between the model and the documentation.

#### 💰 Business model
- The prompts are the product — free, open, public domain ([The Unlicense](https://unlicense.org)).
- Cost models produced are source-controlled assets owned by the repo team.
- No telemetry, no SaaS, no lock-in.

#### 📣 Marketing
- Storytelling: *"What does this actually cost to run?"*
- Demo: run the prompt on any repo → get an honest cost table in one pass.
- Positioning: "An honest placeholder beats a confident lie."

#### 🦅 Competition
- Hand-written README sections (stale, unverified, untested).
- Naive AI queries (hallucinated numbers, no taxonomy, no tests).
- Heavy cost-tracking infrastructure (dashboards, telemetry agents, cloud bills).

---

## Contributing

Issues and PRs welcome. The prompts are the product — keep changes focused on improving agent behavior, not adding infrastructure.

When editing a prompt, test it against at least one real repository before submitting.

---

## License

[The Unlicense](https://unlicense.org) — public domain, no conditions. See [LICENSE](LICENSE).
