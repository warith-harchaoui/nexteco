# Cost of Running — Repository Audit Prompt (Advanced)

> **When to use this version:** when runtime, memory, or energy cost is a primary concern for the project's users or operators — or when a benchmark already exists in the repo. For standard repositories that need honest cost accounting without deep performance investigation, use the Core version instead.

---

Audit this repository and implement a **reproducible, maintainable, test-backed, profiling-aware** "Cost of Running" feature.

Your job: inspect the repository, infer its canonical unit of work, create a source-controlled cost model, expose it in the documentation, add a reproducible benchmark, and — when warranted — add a lightweight profiling path. Leave behind the smallest reasonable mechanism for future contributors or coding agents to keep it accurate.

Work directly in the repository. Keep the implementation **small, readable, auditable, and easy to maintain**.

Do **not** echo or summarize this prompt in your output.

---

## Primary objective

Add a **Cost of Running** feature that answers three questions:

1. Does the deliverable hold? *(tests)*
2. What does it cost in money, energy, and CO2 — to execute this project's canonical unit of work? *(cost model + benchmark)*
3. Where does that cost come from? *(profiling, when warranted — see Profiling section)*

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
7. **Add a lightweight profiling path** when the canonical unit of work is non-trivial in runtime, memory, or external calls (see Profiling section below — this includes the decision rule for when profiling is warranted)
8. Update `AGENTS.md` if present so future agents preserve this feature
9. Make the implementation obvious enough that a human can audit it in under 5 minutes

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
- external API cost
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
- carbon intensity
- electricity price
- throughput
- benchmark results

If a value is unknown, either derive it from clearly visible repo evidence, or use a conservative placeholder and mark it `TODO: human validation required`.

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
- Scenario totals are **formula-coherent** — verify concretely, for example:
  - `total_usd` equals `local_compute_usd + api_usd` within floating-point tolerance
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

## Benchmarks measure the cost

Add a **reproducible benchmark** that targets the canonical unit of work. The benchmark is the empirical basis for the cost model — it must run on the same unit of work as the tests, with the same synthetic or real input data.

### Rule

A benchmark is required unless the canonical unit of work is trivially fast (< 100 ms) and has no external cost drivers.

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
- Use the same input data as the test suite (synthetic or real)
- Report wall-clock time at minimum
- Be runnable with a single command
- Export results in a stable format (JSON, CSV, or stdout) if the tool supports it

### Python example

```python
# tests/test_benchmark_main_workflow.py
def test_benchmark_main_workflow(benchmark):
    data = fake_input_data()
    result = benchmark(run_workflow, data)
    assert result.status == "ok"
```

Run with: `pytest tests/test_benchmark_main_workflow.py --benchmark-only`

### What to avoid

- Do not benchmark micro-operations that are not representative of the unit of work
- Do not present benchmark results as proof of production performance — label them with hardware context
- Do not replace functional tests with benchmark tests

---

## Profiling explains the cost

Add a **lightweight profiling path** when the canonical unit of work is non-trivial in runtime, memory usage, or external-call volume. Profiling complements tests and benchmarks; it does not replace them.

### Decision rule

Add profiling if any of the following apply:

- wall-clock time for the canonical unit of work exceeds ~1 second
- the implementation is memory-intensive or does heavy I/O
- external API calls or model inference are involved **and the cost model has more than one material external driver** (e.g. tokenization + embedding + completion — not just a single call)
- the benchmark reveals a surprisingly slow or expensive path
- the cost breakdown between drivers is unclear and profiling would resolve it

Skip profiling if the canonical unit of work is trivially fast, has a single obvious cost driver, and the benchmark explains it fully.

### Profiling toolchain — by language

Use the tool already present in the repo. If none is present, use the language default:

| Language | Default choice |
|---|---|
| Python | `cProfile` + `pstats` (standard library); optionally `Scalene` for CPU+memory |
| JavaScript / TypeScript | `--prof` (Node.js V8 profiler), or `clinic.js` |
| Rust | `cargo flamegraph`, or `perf` on Linux |
| Go | `go tool pprof` |
| Java / Kotlin | `async-profiler`, `JProfiler`, or `VisualVM` |
| C / C++ | `gprof`, `perf`, or `Valgrind/Callgrind` |
| Any other | standard or clearly established equivalent |

### What the profiling path must do

- Target the **same canonical unit of work** as tests and benchmarks
- Use the **same synthetic or real input data**
- Be runnable with a single command or short script
- Produce output that a human can interpret without external tools (stdout dump is fine)
- Be labeled with: hardware, OS, input size, and date

### Python example

```python
# scripts/profile_main_workflow.py
"""
Lightweight profiling of the canonical unit of work.
Usage: python scripts/profile_main_workflow.py
Hardware context: document here (e.g. MacBook M2, 16 GB, macOS 14)
"""
import cProfile
import pstats
from mypackage import run_workflow, fake_input_data

profiler = cProfile.Profile()
profiler.enable()
run_workflow(fake_input_data())
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative").print_stats(20)
```

### What to avoid

- Do not profile the entire repository
- Do not profile micro-cases that are not representative
- Do not present a local profiling session as a production measurement
- Do not add profiling as a test dependency unless the repo already does this

---

## Process

Follow this order.

### 1 — Inspect the repository

Determine:

- What the project does
- How users actually use it
- What the canonical unit of work is
- What components drive cost
- What existing tests validate
- What existing benchmarks or profiling scripts exist
- What new tests, benchmarks, and profiling are necessary for trustworthy evaluation

Look for: CLI entrypoints, scripts, notebooks, training code, inference paths, API integrations, batch jobs, test commands, benchmark files, profiling scripts, Docker / CI workflows, README usage examples, config defaults, environment variables, pricing references, hardware hints, model usage patterns, existing test fixtures.

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
- one API request

Choose **exactly one** canonical unit for the main table. If several are plausible, apply this tiebreaker in order:

1. Prefer the unit closest to what a paying user or operator invokes directly.
2. If still ambiguous (e.g. a library with no CLI, or a monorepo with independent services), prefer the unit with the highest estimated cost per invocation — that is where honest cost accounting matters most.
3. Document your choice and the alternatives you rejected in the final report.

This same unit of work is used by tests, benchmark, and profiling. They must be consistent.

### 3 — Identify cost drivers

Capture the main drivers: local CPU/GPU usage, memory-heavy execution, external API calls, model token usage, image/audio/video processing, storage, network transfer, repeated retries, parallelism / batch size.

Ignore negligible drivers unless they materially affect total cost.

### 4 — Define scenarios

Create **1 to 3 realistic scenarios** using `small` / `typical` / `heavy` only if those distinctions are meaningful.

Decision rule:
- Use 1 scenario if variability is low
- Use 2 or 3 only if the unit of work materially changes in runtime, API usage, or resource intensity

### 5 — Create `cost_of_running.yaml`

This is the canonical source of truth. It must contain: metadata, canonical unit of work, methodology, assumptions, formulas or formula notes, scenarios, benchmark reference, profiling status, inclusions, exclusions, TODOs, confidence level and validation notes.

Note on field names: `status` on individual assumption fields refers to data provenance (`measured`, `estimated`, `placeholder`). `data_quality` at the scenario level refers to overall confidence in that scenario's data.

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
    - "TODO: validate runtime with an actual benchmark"
  benchmark:
    tool: "..."
    command: "..."
    status: "measured|estimated|not_run|TODO"
    last_run: "YYYY-MM-DD|not_run"
    hardware: "..."
  profiling:
    tool: "..."
    script: "..."
    status: "available|not_warranted|TODO"
    notes:
      - "..."
  notes:
    - "..."

assumptions:
  currency:
    usd_to_eur: ...
    source: "..."
    status: "measured|estimated|placeholder"
  electricity:
    usd_per_kwh: ...
    region: "..."
    source: "..."
    status: "measured|estimated|placeholder"
  carbon_intensity:
    gco2e_per_kwh: ...
    region: "..."
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
      api_usd: ...
      total_usd: ...
      total_eur: ...
      carbon_gco2e: ...
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

### 6 — Generate or write the README section

Add a `## Cost of Running` section to `README.md` using managed markers so regeneration is safe and idempotent — running the helper script twice must produce identical output:

```
<!-- COST_OF_RUNNING:START -->
<!-- COST_OF_RUNNING:END -->
```

The section must include:

- Canonical unit of work
- Scenario table (scenario / runtime / energy / API cost / local compute cost / total USD / total EUR / carbon)
- Assumptions
- Inclusions / exclusions
- Methodology note
- Date updated
- How to run tests, benchmark, and profiling (one line each)

### 7 — Add or update tests

At minimum, test YAML validity, generation / validation behavior, synchronization between YAML and README, idempotency of the helper script, and at least one meaningful failure mode.

### 8 — Add benchmark

Add the benchmark targeting the canonical unit of work. Document the run command. Add a note to the README section with the benchmark command and the hardware it was run on (or a TODO if not yet run).

### 9 — Add profiling path (if warranted)

Apply the decision rule from the Profiling section above. Add a small profiling script or inline profiling block if warranted. Place it in `scripts/` or equivalent. Document how to run it. If profiling is not warranted, record `status: not_warranted` in the YAML and state the rationale briefly.

### 10 — Update `AGENTS.md` if present

Add a short maintenance note stating that:

- `cost_of_running.yaml` is the source of truth
- The README section must stay synchronized with it; use the helper script
- Assumptions must remain explicit
- Measured values must be clearly distinguished from estimated values
- TODOs must remain visible until validated
- Tests, benchmark, and profiling scripts must remain meaningful and maintained
- The benchmark and profiling path target the same canonical unit of work as the tests
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
- Do not add profiling if it is not warranted

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
- `TODO: benchmark runtime for one typical CLI invocation on target hardware`
- `TODO: validate average power draw on macOS with powermetrics`
- `TODO: confirm production API pricing tier`
- `TODO: confirm deployment region for carbon intensity`
- `TODO: verify whether storage egress is material for this workflow`
- `TODO: run profiling script and document top 5 hotspots`

**Invalid behaviors:**
- Inventing a GPU wattage with no evidence
- Inventing average token usage
- Inventing an API price
- Presenting guessed numbers with many decimal places
- Silently bypassing missing assumptions
- Presenting a local profiling result as representative of production

---

## Expected final report

At the end, produce this report in exactly this structure — one item per numbered entry, concise, no prose padding:

1. **Canonical unit of work** — name and one-sentence rationale; alternatives considered and rejected
2. **Main assumptions** — list each assumption with its status (measured / estimated / placeholder) and source
3. **Changed files** — list every file created or modified
4. **Tests added or updated** — list test file(s), what each test validates, and the command to run them
5. **Benchmark** — tool used, run command, status (run / not run / TODO), hardware context if run
6. **Profiling** — tool used, script path, status (added / not warranted / TODO), and brief rationale for the decision
7. **Unresolved uncertainties** — for each: the missing value, why it matters, and the exact evidence needed to resolve it (command, log file, or measurement output)

For unresolved items, name the exact artifact that would close them, for example:
- `pytest --benchmark-only > benchmark_results.txt` on target hardware
- `python scripts/profile_main_workflow.py > profile_output.txt`
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
- The benchmark is easy to run and produces interpretable output
- The profiling path exists and targets the right unit of work (when warranted)
- Uncertainty is visible rather than hidden
- Future agents know how to maintain it

Now inspect the repository and implement the feature.
