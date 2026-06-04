# Research Boilerplate

A **thin, personal boilerplate** for data-analysis research projects. The core
reusable asset is the **AGENTS.md process framework** — a hierarchy of AI
collaboration prompts that guide each stage of the research lifecycle.

Instead of rebuilding structural and procedural decisions for every project,
clone this repo, fill in `TODO` blocks, and start collaborating with AI agents
immediately.

## Pipeline Stages

| `make` target | AGENTS file | What it does |
|---|---|---|
| `plan` | [`AGENTS-planning.md`](AGENTS-planning.md) | Formulate research question, draft OSF pre-registration |
| `litreview` | [`AGENTS-litreview.md`](AGENTS-litreview.md) | Search, annotate, and synthesise literature |
| `acquire` | [`AGENTS-acquire.md`](AGENTS-acquire.md) | Download and validate raw data |
| `preprocess` | [`AGENTS-preprocess.md`](AGENTS-preprocess.md) | Clean, QC, transform — output feature dataset |
| `analyze` | [`AGENTS-analysis.md`](AGENTS-analysis.md) | Fit statistical model, bootstrap, sensitivity |
| `visualize` | [`AGENTS-visualize.md`](AGENTS-visualize.md) | Generate publication-quality figures |
| `report` | [`AGENTS-report.md`](AGENTS-report.md) | Compile results into manuscript / report |
| `test` | [`AGENTS-tests.md`](AGENTS-tests.md) | Run test suite (independent of data) |

## How to Adapt (~30 min)

1. **Clone or copy** this repo into your new project directory.
2. **Rename** `src/pkg/` to `src/<your_package>/`.
3. **Edit** `pyproject.toml` — name, description, author, dependencies.
4. **Edit** `AGENTS.md` (root) — project description, tech stack, language version.
5. **Edit** each `AGENTS-*.md` — fill in domain-specific `TODO` blocks.
6. **Update** `src/pkg/config.py` — add your tunable parameters.
7. **Run** `uv pip install -e ".[dev]"` (or `pip install -e ".[dev]"` without uv) and verify `make test` passes.
8. **Start** with `make plan`, using the AGENTS prompts to collaborate with an AI.

## AI Collaboration Model

The AGENTS.md files use a **hierarchical context model**:
- **Root** [`AGENTS.md`](AGENTS.md) defines global conventions (naming, imports,
  docstrings, commit format, tech stack).
- **Module-level** files (`AGENTS-{stage}.md`) override root rules with
  stage-specific constraints, data contracts, and AI prompts.

When working on a specific stage, an AI agent first reads the root AGENTS.md
for global rules, then the stage-specific AGENTS file for domain instructions.
Local rules override global rules.

## License

| Component | License | File |
|-----------|---------|------|
| **Source code** (Python scripts) | **MIT** | [`LICENSE`](LICENSE) |
| **Non-software materials** (data, figures, report, documentation) | **CC BY 4.0** | [`LICENSE.content`](LICENSE.content) |
