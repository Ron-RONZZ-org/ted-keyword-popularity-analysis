# AGENTS.md — Root Project Rules for [Project Name]

This is the canonical, repo-wide instruction file for AI agents working on
**[Project Name]** — a data-analysis research project.

## Hierarchical Context Model

Agents **must** follow this rule:

> When working inside a directory, load the nearest `AGENTS.md` file and merge it with parent `AGENTS.md` files up to root.  
> Local rules override global rules.

Context resolution order (highest priority first):
1. `AGENTS-[stage].md` in the current directory — stage-specific context
2. `AGENTS.md` in current working directory (if present)
3. Root `AGENTS.md` — global project rules

---

## Project Structure

```
project/
├── src/
│   └── pkg/                    # Rename to <your_package> per project
│       ├── __init__.py          # Version + logging setup
│       ├── config.py            # Frozen dataclass for all parameters
│       ├── acquire.py           # Data download and validation
│       ├── preprocess.py        # QC, cleaning, feature extraction
│       ├── analysis.py          # Statistical modelling
│       ├── visualize.py         # Publication-quality figures
│       └── report.py            # Summary statistics and tables
├── tests/
│   ├── conftest.py              # Shared fixtures
│   └── test_*.py                # Per-module tests
├── data/
│   ├── raw/                     # git-ignored — original downloads
│   ├── processed/               # git-ignored — cleaned outputs
│   └── external/                # Tracked — reference data, metadata
├── results/
│   └── figures/                 # git-ignored — output figures (PDF + PNG)
├── literature/
│   ├── papers/                  # PDFs from literature review
│   └── bibliography.bib         # BibTeX citation database
├── notebooks/                   # Exploration notebooks (.qmd or .ipynb)
├── manuscript/                  # Quarto manuscript (optional)
├── logs/                        # Pipeline execution logs (git-ignored)
├── pyproject.toml               # Source of truth for dependencies
├── Makefile                     # Pipeline orchestration
└── AGENTS.md                    # This file
```

---

## Language and Naming Conventions

- **Language**: Python 3.10+
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- **Imports**: Standard library first, third-party second, local package third, each group alphabetically sorted
- **Types**: Use type hints on all function signatures (`def foo(x: int) -> str:`)
- **Docstrings**: Google-style docstrings for all public functions

---

## Tech Stack

| Component | Choice (default) |
|-----------|------------------|
| Language | Python ≥ 3.10 |
| Package manager | uv (preferred) or pip via pyproject.toml |
| Data handling | pandas, numpy |
| Statistics | scipy, statsmodels |
| Visualization | matplotlib, seaborn |
| Testing | pytest, pytest-cov |
| Pipeline | Makefile |
| Manuscript | Quarto (.qmd) |
| Configuration | Frozen dataclass (stdlib) |
| Time zones | zoneinfo (stdlib) — never pytz |

---

## Dependency Management

All dependencies are declared in `pyproject.toml`. Install with:

```bash
uv pip install -e ".[dev]"
```

(`pip install -e ".[dev]"` also works if you don't have `uv` installed.)

**Do NOT** add dependencies without updating `pyproject.toml`.

For new projects using this boilerplate, create a virtual environment first:

```bash
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
```

---

## Coding Guidelines

1. **Every script runs as a module**: `python -m pkg.<module>` (update `pkg` to your package name)
2. **Every module uses Python `logging`**: Log to both `logs/` file and stdout with format `%(asctime)s | %(levelname)s | %(name)s | %(message)s`
3. **Configuration lives in `config.py`**: A frozen dataclass — never hardcode thresholds in pipeline code
4. **Pipeline stages communicate through files** (CSV/JSON in `data/` or `results/`), never through in-memory state between `make` targets
5. **Schema validation at every stage boundary**: Use pandera (preferred) or manual checks to validate column names, dtypes, and value ranges before and after each processing step
6. **Prefer vectorized operations** (pandas/numpy) over explicit loops for data transformation
7. **Synthetic data tests**: Analysis modules must include a test with known synthetic data that verifies the correct result
8. **All stochastic code uses an explicit RNG seed** (`numpy.random.default_rng(seed=42)` or similar) for reproducibility

---

## Documentation Standards

- **AGENTS.md** at root defines global project rules
- Module-level `AGENTS-[stage].md` files define domain-specific rules for each pipeline stage
- Every public function has a Google-style docstring
- Data processing decisions (thresholds, exclusion rules) are documented in `config.py` dataclass docstrings
- Pipeline stages are documented in `Makefile` comments

---

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` — New capability
- `fix:` — Bug fix
- `docs:` — Documentation
- `chore:` — Maintenance
- `test:` — Testing
- `refactor:` — Code restructuring

Reference GitHub issues by number: `feat(#1): implement pooch-based data acquisition`

---

## What to Avoid

- **Do NOT use `sys.path` hacks** — The `src/` package is always installable via `pip install -e .`
- **Do NOT use `pytz`** — It is deprecated; use `zoneinfo` (stdlib) for all timezone handling
- **Do NOT use linear statistics on circular data** — If your data is circular (hours, angles, seasons), use circular mean, circular std, and circular regression
- **Do NOT hardcode file paths** — All paths come from `config.py` pyproject.toml metadata
- **Do NOT commit raw/processed data to git** — Data goes to OSF or external archive; local copies are git-ignored
- **Do NOT skip pre-registration** — Analysis must not begin before the OSF pre-registration is submitted

---

## Module-Level AGENTS Files

| Module / Stage | AGENTS File | Purpose |
|----------------|-------------|---------|
| Planning | `AGENTS-planning.md` | Research question, OSF pre-registration |
| Literature review | `AGENTS-litreview.md` | Paper discovery, annotation, synthesis |
| `src/pkg/acquire.py` | `AGENTS-acquire.md` | Data acquisition rules |
| `src/pkg/preprocess.py` | `AGENTS-preprocess.md` | QC and preprocessing rules |
| `src/pkg/analysis.py` | `AGENTS-analysis.md` | Statistical modelling rules |
| `src/pkg/visualize.py` | `AGENTS-visualize.md` | Figure generation rules |
| `src/pkg/report.py` | `AGENTS-report.md` | Reporting and manuscript rules |
| `notebooks/` | `AGENTS-notebooks.md` | Notebook conventions |
| `tests/` | `AGENTS-tests.md` | Testing conventions |

(Update this table as new modules are added)

---

## Dependency and Inheritance Map

```
Root AGENTS.md (global rules — this file)
    │
    ├── AGENTS-planning.md     — research question + pre-registration
    ├── AGENTS-litreview.md    — literature search + synthesis
    ├── AGENTS-acquire.md      — data download + validation
    ├── AGENTS-preprocess.md   — QC, transformation, feature extraction
    ├── AGENTS-analysis.md     — statistical model + sensitivity
    ├── AGENTS-visualize.md    — figure style + export format
    ├── AGENTS-report.md       — manuscript + results compilation
    ├── AGENTS-notebooks.md    — notebook conventions
    └── AGENTS-tests.md        — test coverage + synthetic data
```

Local rules override global rules. Module-level files focus on domain-specific behavior, constraints, and invariants.
