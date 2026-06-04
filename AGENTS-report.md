# AGENTS-report.md — Reporting & Manuscript Rules

## Scope

`src/pkg/report.py` (optional) + `manuscript/` — compiles analysis results
into a human-readable report and optionally a full manuscript in Quarto.

## Required Outputs

| File | Content |
|------|---------|
| `results/summary_statistics.csv` | Key descriptive statistics and model results in tabular form |
| `manuscript/results.md` | Draft results section — narrative with figures and tables |
| `manuscript/main.qmd` | Full manuscript (if using Quarto) |

## Constraints

- Do NOT fabricate or interpret beyond what the data support.
- Figures must be referenced by their saved filenames (not embedded).
- Bibliography must reference `literature/bibliography.bib`.
- Include a limitations subsection in the manuscript.
- Report version-controlled alongside analysis (reproducibility).

## AI Agent Prompt

When you call an AI agent for reporting, preface with:

> You are a scientific writer. Given:
> - Analysis output at `data/processed/`
> - Figures at `results/figures/`
> - Literature synthesis at `literature/synthesis.md`
> - Pre-registration at `planning/pre_registration_draft.md`
>
> Write a structured results section covering:
> 1. What was found (primary endpoint with uncertainty).
> 2. Sensitivity analysis results.
> 3. How findings compare to prior work (cite from `bibliography.bib`).
> 4. Limitations.
> 5. Conclusion.
>
> Reference figures by their saved filenames. Use formal scientific tone.

## References

- [Root AGENTS.md](AGENTS.md) — global conventions
- [AGENTS-litreview.md](AGENTS-litreview.md) — literature for context
- `planning/pre_registration_draft.md` — planned analyses
