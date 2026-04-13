# Cost of Running — Repository Audit Prompt (Core)

Audit this repository and implement a **reproducible, maintainable, test-backed** "Cost of Running" feature.

Your job: inspect the repository, infer its canonical unit of work, create a source-controlled cost model, expose it in the documentation, and leave behind the smallest reasonable mechanism for future contributors or coding agents to keep it accurate.

Work directly in the repository. Keep the implementation **small, readable, auditable, and easy to maintain**.

Do **not** echo or summarize this prompt in your output.



---

## Primary objective

Add a **Cost of Running** feature that answers two questions:

1. Does the deliverable hold? *(tests)*
2. What does it cost in money, energy, and CO2 — to execute this project's canonical unit of work? (cost model + benchmark)

Everything must be:

- reproducible
- explicit about assumptions
- honest about uncertainty
- source-controlled
- easy to regenerate
- useful even when the repository does not yet contain benchmarks or measurements
- backed by meaningful tests

Do not add heavy infrastructure.

Do not hallucinate facts.

Do not present estimated values as measured values.

---

## Required deliverables

You must:

1. Infer the repository's canonical unit of work (choose one primary, justify if ambiguous)
2. Add a `## Cost of Running` section to `README.md`
3. Create `cost_of_running.yaml` as the single source of truth
4. Create a small helper script to regenerate and/or validate the README section from the YAML
5. **Create or extend a meaningful test suite** (see Tests section below)
6. **Add a reproducible benchmark** targeting the canonical unit of work (see Benchmarks section below)
7. Update `AGENTS.md` if present so future agents preserve this feature
8. Make the implementation obvious enough that a human can audit it in under 5 minutes

If the repo already has relevant benchmarking, profiling, pricing, runtime, or testing documentation, reuse it.
If key data is missing, use clearly labeled estimates and explicit `TODO:` markers.

**Monorepo / multi-service note:** if the repository contains multiple independent services or packages, choose the single highest-cost or most user-facing unit of work as the canonical one. Document the others as out-of-scope exclusions.

---

## Non-negotiable cost model requirements

Estimate **per canonical unit of work**, for each scenario:

- 💰 USD or EUR
- 🪫 energy (`Wh` or `kWh`)
- 💨 carbon (`gCO2e` or `kgCO2e`)

If the repository mixes **local compute** and **paid external APIs**, separate:

- local compute cost
- external API cost (broken down per call; see LLM and API cost driver guidance below)
- total cost

If storage, network egress, or other recurring costs are materially relevant, include them. Otherwise, explicitly exclude them.

---

## Methodology

Use a **Green Algorithms-inspired** methodology:
<https://calculator.green-algorithms.org/ai>

The implementation must follow these principles:

- explicit assumptions
- scenario-based reporting
- no fake precision
- transparent distinction between: **measured** / **estimated** / **placeholder / TODO**
- conservative defaults when repo data is missing
- clear human-validation points
- auditable formulas
- minimal maintenance burden

Never invent:

- runtimes
- power draw
- hardware model
- API pricing
- token counts per API call
- carbon intensity
- electricity price
- throughput
- benchmark results

If a value is unknown, either derive it from clearly visible repo evidence, or use a conservative placeholder and mark it `TODO: human validation required`.

**API pricing provenance rule:** any API price in the YAML must include a `source_url` (the exact provider pricing page) and a `retrieved_date` (YYYY-MM-DD). If the retrieved date is more than 90 days old, downgrade the status to `placeholder` and add a `TODO: verify current pricing at <source_url>`.

---

## Platform-aware measurement guidance

If the project uses local compute, acknowledge that accurate energy measurement depends on OS and tooling. Reference these tools in methodology, TODOs, or maintenance notes when relevant:

- macOS: `powermetrics`
- Linux / Ubuntu: `powertop`, `turbostat`
- Windows: `powercfg`, `perfmon`

Do not imply these measurements were performed unless the repository already contains them or you executed them during this task and documented that clearly.

If no direct measurements exist, energy must be labeled as an estimate derived from:

```
energy_kwh = runtime_hours × average_power_kw
```

### Country-aware electricity and carbon defaults

Electricity price and grid carbon intensity vary dramatically by country — France emits ~56 gCO₂e/kWh; Australia emits ~620 gCO₂e/kWh. A flat global average of 400 would be a 7× error for a French developer. **Detect the country from the running environment and use per-country values.**

Detect in this priority order (use the first method that succeeds):

**1. System timezone** (no network required):
- macOS: `readlink /etc/localtime | sed 's|.*/zoneinfo/||'`
- Linux: `cat /etc/timezone` or `timedatectl show --property=Timezone --value`
- Windows: `tzutil /g`
- Python: `from tzlocal import get_localzone_name()` if installed

**2. System locale** (no network required):
- Python: `import locale; locale.getdefaultlocale()` → e.g. `('fr_FR', 'UTF-8')` → country `FR`

**3. IP geolocation** (standard library, requires network):
```python
import urllib.request, json
try:
    data = json.loads(urllib.request.urlopen('https://ipinfo.io/json', timeout=3).read())
    country_code = data.get('country')  # ISO 3166-1 alpha-2, e.g. "FR"
except Exception:
    country_code = None  # fall back to global average
```

**4. Manual fallback:** use global average and add `TODO: confirm region`.

Per-country reference values — mark all as `status: estimated` (source: Our World in Data / Electricity Maps 2023, Eurostat / EIA / IEA 2024):

| Country | Code | Carbon (gCO₂e/kWh) | Electricity (USD/kWh) |
|---|---|---|---|
| Norway | NO | 29 | 0.12 |
| France | FR | 56 | 0.20 |
| Switzerland | CH | 42 | 0.30 |
| Sweden | SE | 45 | 0.18 |
| New Zealand | NZ | 130 | 0.18 |
| Brazil | BR | 130 | 0.14 |
| Canada | CA | 130 | 0.12 |
| Denmark | DK | 149 | 0.36 |
| Austria | AT | 155 | 0.25 |
| Belgium | BE | 174 | 0.27 |
| Spain | ES | 182 | 0.19 |
| United Kingdom | GB | 238 | 0.27 |
| Italy | IT | 298 | 0.28 |
| Netherlands | NL | 301 | 0.28 |
| Germany | DE | 380 | 0.35 |
| United States | US | 386 | 0.17 |
| Japan | JP | 455 | 0.23 |
| China | CN | 585 | 0.09 |
| Australia | AU | 620 | 0.28 |
| India | IN | 708 | 0.09 |
| Poland | PL | 773 | 0.18 |
| South Africa | ZA | 780 | 0.12 |
| *Global average* | — | *400* | *0.15* |

Record the detected country and method in `cost_of_running.yaml` (see schema in step 5).

---

## LLM and API cost driver guidance

When the repository calls external LLM or embedding APIs (OpenAI, Anthropic, Mistral, Cohere, Google, etc.), API spend is typically the dominant cost driver. Apply the following rules strictly.

### Token-level breakdown

For every LLM or embedding API call in the canonical unit of work, record:

| Field | Meaning |
|---|---|
| `name` | Short label for the call — e.g. `embedding`, `generation`, `judge`, `reranker` |
| `provider` | API provider — e.g. `openai`, `anthropic`, `local` |
| `model` | Exact model identifier — e.g. `gpt-4o`, `text-embedding-3-small` |
| `tokens_in` | Prompt / input tokens (conservative estimate or measured) |
| `tokens_out` | Completion / output tokens (conservative estimate or measured; 0 for embeddings) |
| `price_per_1m_in` | Provider's listed price per 1 million input tokens |
| `price_per_1m_out` | Provider's listed price per 1 million output tokens |
| `cost_usd` | `(tokens_in × price_per_1m_in + tokens_out × price_per_1m_out) / 1_000_000` |
| `source_url` | Exact URL of the provider pricing page |
| `retrieved_date` | YYYY-MM-DD when the price was confirmed |
| `status` | `measured`, `estimated`, or `placeholder` |

Roll up all call costs into `total_api_usd = sum(api_calls[*].cost_usd)`.

If the project has no API calls, set `api_calls: []` and `total_api_usd: 0.0`.

### Token budget estimation

When exact token counts are unavailable:

1. Estimate prompt tokens from the code: count system prompt + expected query length + retrieval context size (number of chunks × average chunk tokens)
2. Use conservative (high) estimates for completion tokens — err toward over-counting
3. For judge calls: include the generated answer as additional input tokens (it is re-submitted)
4. Mark all estimates with `status: estimated` and add a TODO for measurement via actual API usage logs
5. Do not use round numbers (1000, 500) without an inline note explaining the estimate basis

### RAG-specific cost drivers

For retrieval-augmented pipelines, account for:

- **Embedding call** — query tokenization + embedding API or local model
- **Vector DB lookup** — typically local compute; cheap but not zero
- **Re-ranking call** — if a reranker model or API is called on retrieved candidates
- **Generation call** — full prompt includes retrieved chunks; context size is variable
- **Judge call** — input includes the generated answer; tokens_in = rubric + query + answer

---

## Tests are a first-class deliverable

Tests are **not optional polish**. The "Cost of Running" feature is only complete if its core behavior is verifiable and leaves behind at least one meaningful evaluation path that future humans or agents can run automatically.

### Rule

- If tests already exist in the repository → extend them
- If tests are missing → **create them**

Use the repository's existing testing culture. If no culture is established, use the language's standard:

| Language | Default choice |
|---|---|
| Python | `pytest` (or the repo's current choice) |
| JavaScript / TypeScript | `vitest`, `jest` (or repo's current choice) |
| Rust | built-in `#[test]` framework |
| Go | `go test` |
| Java / Kotlin | `JUnit` |
| C / C++ | `CTest`, `Catch2`, or repo's current choice |
| Any other | standard or clearly established equivalent |

In Python, use comments, docstrings, and type annotations as part of the quality standard.

### What tests must cover

Write the **main tests**, not trivial or decorative ones. Tests should validate the most important invariants:

- The YAML source parses successfully
- Required fields are present and have the right types
- `api_calls` entries are present for each expected call; each has `source_url` and `retrieved_date`
- `total_api_usd` equals the sum of `api_calls[*].cost_usd` within floating-point tolerance
- Each `api_call.cost_usd` matches the formula `(tokens_in × price_per_1m_in + tokens_out × price_per_1m_out) / 1_000_000`
- Scenario totals are **formula-coherent** — verify concretely:
  - `total_usd` equals `local_compute_usd + total_api_usd` within floating-point tolerance
  - `carbon_gco2e` equals `energy_kwh × carbon_intensity_gco2e_per_kwh` within floating-point tolerance
  - `energy_kwh` equals `(runtime_s / 3600) × average_power_kw` within floating-point tolerance
  - Do not accept "totals look reasonable" — check the arithmetic
- The README managed block can be generated reproducibly; regenerating it twice produces identical output
- Generated content stays synchronized with `cost_of_running.yaml`
- Missing data surfaces as `TODO` / placeholder rather than being silently invented
- Measured vs estimated values remain clearly distinguished

### What to avoid

- Do not create a large or flashy test harness just to satisfy this prompt
- Do not add brittle snapshot tests unless they genuinely protect against regression
- Do not write trivial tests that only assert a file exists

### Test input data

If realistic input data is required and the repo does not provide it:

1. Create **small synthetic / fake input data**, clearly labeled for testing
2. Request concrete sample inputs from the human only when domain-specific inputs are strictly necessary and cannot be reasonably invented

Prefer synthetic data when it keeps the task moving and does not compromise validity.

---

## Benchmarks are part of the cost model

A benchmark provides the empirical runtime that feeds the cost formula. Without it, every runtime figure is a placeholder. A benchmark is required unless the canonical unit of work is trivially fast (< 100 ms) and has no external cost drivers.

### Rule

- If a benchmark already exists in the repository → reuse and extend it
- If none exists → add one targeting the canonical unit of work
- Use the same input data as the test suite (synthetic or real)

### Benchmark toolchain — by language

Use the tool already present in the repo. If none is present, use the language default:

| Language | Default choice |
|---|---|
| Python | `pytest-benchmark` (integrates with `pytest`) |
| JavaScript / TypeScript | `vitest bench`, `tinybench`, or `benchmark.js` |
| Rust | `criterion` |
| Go | `go test -bench` |
| Java / Kotlin | `JMH` |
| C / C++ | `Google Benchmark`, or `perf` + manual timing |
| Any other | standard or clearly established equivalent |

### What the benchmark must do

- Run the canonical unit of work end-to-end
- Report wall-clock time at minimum
- Be runnable with a single command
- Be labeled with hardware context (machine, OS) when results are recorded

### What to avoid

- Do not benchmark micro-operations that are not representative of the unit of work
- Do not present benchmark results as proof of production performance
- Do not replace functional tests with benchmark tests

---

## Process

Follow this order.

### 1 — Inspect the repository

Determine:

- What the project does
- How users actually use it
- What the canonical unit of work is
- What components drive cost
- Whether LLM or embedding APIs are called (and how many times per unit of work)
- What existing tests validate
- What new tests are necessary for trustworthy evaluation

Look for: CLI entrypoints, scripts, notebooks, training code, inference paths, API integrations, batch jobs, test commands, benchmark files, Docker / CI workflows, README usage examples, config defaults, environment variables, pricing references, hardware hints, model usage patterns, existing test fixtures.

### 2 — Choose the canonical unit of work

Pick the most user-meaningful unit:

- one CLI invocation
- one inference request
- one processed file
- one batch run
- one report generation
- one training run
- one notebook execution
- one test suite run
- one pipeline execution
- one API request (end-to-end, including all internal LLM calls it triggers)

Choose **exactly one** canonical unit for the main table. If several are plausible, apply this tiebreaker in order:

1. Prefer the unit closest to what a paying user or operator invokes directly.
2. If still ambiguous (e.g. a library with no CLI, or a monorepo with independent services), prefer the unit with the highest estimated cost per invocation — that is where honest cost accounting matters most.
3. Document your choice and the alternatives you rejected in the final report.

### 3 — Identify cost drivers

Capture the main drivers. For standard software: local CPU/GPU usage, memory-heavy execution, external API calls, storage, network transfer, repeated retries, parallelism / batch size.

For **LLM / RAG pipelines**, also consider:

- **Token volume per call** — prompt tokens and completion tokens, separately per call
- **Number of LLM calls per unit of work** — generation call, judge call, reranker call
- **Embedding call cost** — often negligible but must be assessed
- **Context size variability** — cost grows with retrieved chunk count and chunk size
- **Model tier** — same provider at different capability tiers has very different per-token pricing

Ignore negligible drivers unless they materially affect total cost.

### 4 — Define scenarios

Create **1 to 3 realistic scenarios** using `small` / `typical` / `heavy` only if those distinctions are meaningful.

Decision rule:
- Use 1 scenario if variability is low
- Use 2 or 3 only if the unit of work materially changes in runtime, API token usage, or resource intensity
- For LLM pipelines, input size (context window fill) is usually the right axis for scenario differentiation

### 5 — Create `cost_of_running.yaml`

This is the canonical source of truth. It must contain: metadata, canonical unit of work, methodology, assumptions, formulas or formula notes, scenarios, inclusions, exclusions, TODOs, confidence level and validation notes.

Prefer values that a future contributor can update without reading your whole implementation.

Note on field names: `status` on individual assumption fields refers to data provenance (`measured`, `estimated`, `placeholder`). `data_quality` at the scenario level refers to overall scenario confidence in the data.

Schema:

```yaml
date_updated: YYYY-MM-DD

unit_of_work:
  name: "..."
  description: "..."
  rationale: "..."

methodology:
  approach: "Green Algorithms-inspired"
  measured_vs_estimated: "..."
  formula_notes:
    - "energy_kwh = runtime_hours * average_power_kw"
    - "local_compute_usd = energy_kwh * electricity_usd_per_kwh"
    - "carbon_gco2e = energy_kwh * carbon_intensity_gco2e_per_kwh"
    - "api_call.cost_usd = (tokens_in * price_per_1m_in + tokens_out * price_per_1m_out) / 1_000_000"
    - "total_api_usd = sum(api_calls[*].cost_usd)"
    - "total_usd = local_compute_usd + total_api_usd"
    - "TODO: validate runtime with an actual benchmark"
  benchmark:
    tool: "..."
    command: "..."
    status: "measured|not_run|TODO"
    last_run: "YYYY-MM-DD|not_run"
    hardware: "..."
  notes:
    - "..."

assumptions:
  currency:
    usd_to_eur: ...
    source: "..."
    status: "measured|estimated|placeholder"
  electricity:
    usd_per_kwh: ...
    region: "..."                  # e.g. "FR", "US", "global average"
    detected_country: "..."       # ISO 3166-1 alpha-2; from timezone, locale, or ip_geolocation
    detection_method: "timezone|locale|ip_geolocation|manual|unknown"
    source: "..."
    status: "measured|estimated|placeholder"
  carbon_intensity:
    gco2e_per_kwh: ...
    region: "..."                  # e.g. "FR", "US", "global average"
    detected_country: "..."       # ISO 3166-1 alpha-2; from timezone, locale, or ip_geolocation
    detection_method: "timezone|locale|ip_geolocation|manual|unknown"
    source: "..."
    status: "measured|estimated|placeholder"
  hardware:
    description: "..."
    average_power_w: ...
    source: "measured|estimated|placeholder|TODO"
  runtime:
    source: "measured|estimated|code-inferred|placeholder|TODO"
    notes:
      - "..."

scenarios:
  - name: "typical"
    description: "..."
    drivers:
      - "..."
    per_unit:
      runtime_s: ...
      energy_kwh: ...
      local_compute_usd: ...
      api_calls:
        - name: "..."            # e.g. "embedding", "generation", "judge"
          provider: "..."        # e.g. "openai", "anthropic", "local"
          model: "..."           # exact model identifier
          tokens_in: ...
          tokens_out: ...
          price_per_1m_in: ...   # from provider pricing page
          price_per_1m_out: ...  # from provider pricing page
          cost_usd: ...          # (tokens_in * price_per_1m_in + tokens_out * price_per_1m_out) / 1_000_000
          source_url: "..."      # required: exact provider pricing page URL
          retrieved_date: "YYYY-MM-DD"  # required: date price was confirmed
          status: "measured|estimated|placeholder"
      total_api_usd: ...         # sum of api_calls[*].cost_usd; 0.0 if no API calls
      total_usd: ...             # local_compute_usd + total_api_usd
      total_eur: ...
      carbon_gco2e: ...          # local compute only if API data center carbon is unavailable; note explicitly
    status:
      runtime: "measured|estimated|placeholder"
      power: "measured|estimated|placeholder"
      api_pricing: "measured|estimated|placeholder|not_applicable"
    data_quality: "low|medium|high"   # overall confidence in this scenario's data
    notes:
      - "..."

inclusions:
  - "..."

exclusions:
  - "..."

todos:
  - "TODO: ..."
```

Keep it machine-readable, easy to edit manually, and clear over abstract.

### 6 — Generate or write the README section

Add a `## Cost of Running` section to `README.md`.

Use managed markers so regeneration is safe and idempotent — running the helper script twice must produce identical output:

```
<!-- COST_OF_RUNNING:START -->
<!-- COST_OF_RUNNING:END -->
```

Preserve surrounding README content.

The section must include, in human-readable form:

- Canonical unit of work
- Scenario table (scenario / runtime / energy / API cost / local compute cost / total USD / total EUR / carbon)
- Per-call API breakdown (call name, model, tokens in, tokens out, cost) — for any scenario with API calls
- Assumptions
- Inclusions / exclusions
- Methodology note
- Date updated
- A short note on what is tested and how to rerun validation
- How to run the benchmark (one line)

The prose must clearly state what is measured, what is estimated, and what still requires human validation.

### 7 — Add or update tests

Place tests where the repository naturally expects them. Keep them small, meaningful, and runnable. Label synthetic fixtures clearly. Document how to run them.

At minimum, test:

- YAML validity
- `total_api_usd` arithmetic coherence
- Per-call `cost_usd` arithmetic coherence
- Generation or validation behavior
- Synchronization between YAML and README managed block
- Idempotency of the helper script
- At least one meaningful failure mode

### 8 — Add or update benchmark

Add or extend the benchmark targeting the canonical unit of work. Document the run command. If the benchmark was actually run, record the result and hardware context in `cost_of_running.yaml` under `methodology.benchmark`. If not run, mark it as `TODO`.

### 9 — Update `AGENTS.md` if present

Add a short maintenance note (not a long essay) stating that:

- `cost_of_running.yaml` is the source of truth
- The README section must stay synchronized with it; use the helper script
- Assumptions must remain explicit
- Measured values must be clearly distinguished from estimated values
- TODOs must remain visible until validated
- Tests for this feature must remain meaningful and maintained
- The benchmark targets the same canonical unit of work as the tests
- API prices must include `source_url` and `retrieved_date`; prices older than 90 days must be re-verified
- Platform measurement tools may be referenced: `powermetrics` (macOS), `powertop` / `turbostat` (Linux), `powercfg` / `perfmon` (Windows)

---

## Helper script requirements

Keep it very small and dependency-light. Its job: generate the README section from YAML, validate the YAML structure, or both.

- If a cost-related script already exists in the repository, **reuse and extend it** — do not create a parallel one
- Prefer standard library only where practical
- Avoid frameworks
- Place it in an existing `scripts/` or `tools/` directory if present, or create a `cost-scripts/` folder for it

---

## Decision rules

Follow strictly:

- Prefer honesty over completeness
- Prefer explicit TODOs over invented numbers
- Prefer one canonical unit of work over multiple competing tables
- Prefer conservative estimates over optimistic ones
- Prefer simple formulas over opaque logic
- Prefer generated README content if regeneration is useful
- Prefer maintainability over sophistication
- Prefer meaningful tests over impressive-looking tests
- Prefer the tool already used in the repo over introducing a new dependency

Do not add: telemetry, background services, dashboards, databases, large dependencies, CI unless already established and the change is tiny, rewrites of unrelated documentation.

---

## Handling missing data

When the repository does not contain enough information:

1. Infer only what is strongly supported by code or docs
2. Choose a conservative default assumption
3. Mark it clearly as estimated or placeholder
4. Add `TODO:` for the exact human validation needed
5. Ensure tests fail or warn appropriately when required structured information is missing

**Valid TODOs:**
- `TODO: benchmark runtime for one typical invocation on target hardware`
- `TODO: validate average power draw on macOS with powermetrics`
- `TODO: confirm production API pricing tier — current price from <source_url> retrieved <date>`
- `TODO: confirm deployment region for carbon intensity`
- `TODO: verify whether storage egress is material for this workflow`
- `TODO: measure actual token counts for generation call via API usage logs`
- `TODO: measure actual token counts for judge call via API usage logs`

**Invalid behaviors:**
- Inventing a GPU wattage with no evidence
- Inventing average token usage
- Inventing an API price
- Inventing an API price without `source_url` and `retrieved_date`
- Presenting guessed numbers with many decimal places
- Silently bypassing missing assumptions
- Presenting a local profiling result as representative of production
- Reporting a single `api_usd` total without a per-call breakdown when multiple LLM calls are made
- Treating one LLM call's latency as representative when the unit of work involves a chain of calls

---

## Expected final report

At the end, produce this report in exactly this structure — one item per numbered entry, concise, no prose padding:

1. **Canonical unit of work** — name and one-sentence rationale; alternatives considered and rejected
2. **Main assumptions** — list each assumption with its status (measured / estimated / placeholder) and source
3. **API calls** — list each call in the unit of work with model, estimated tokens, price source, and retrieved date
4. **Changed files** — list every file created or modified
5. **Tests added or updated** — list test file(s), what each test validates, and the command to run them
6. **Benchmark** — tool used, run command, status (run / not run / TODO), hardware context if run
7. **Unresolved uncertainties** — for each: the missing value, why it matters, and the exact evidence needed to resolve it (command, log file, or measurement output)

For unresolved items, name the exact artifact that would close them, for example:
- `pytest --benchmark-only > benchmark_results.txt` on target hardware
- `sudo powermetrics --samplers cpu_power -n 5 > power_log.txt` on macOS
- API usage log showing token counts for a representative request

---

## Execution quality bar

A good implementation has these properties:

- A human can understand it in under 5 minutes
- The README section is useful immediately
- The YAML is clearly the source of truth
- The script is trivial to rerun, and idempotent
- The tests are easy to run and actually protect the feature
- The benchmark exists and targets the right unit of work
- Every API call in the unit of work has its own row with token counts and a dated price source
- Uncertainty is visible rather than hidden
- Future agents know how to maintain it

Now inspect the repository and implement the feature.
