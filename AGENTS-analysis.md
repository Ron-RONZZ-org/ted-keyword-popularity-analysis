# AGENTS-analysis.md — Statistical Modelling Rules

## Scope

`src/pkg/analysis.py` — statistical model fitting, bootstrap confidence
intervals, sensitivity analysis, and supplementary analyses.

## Analysis Method

| Parameter | Detail |
|-----------|--------|
| **Model type** | TODO: e.g., linear regression, GLM, von Mises regression, mixed effects |
| **Primary endpoint** | TODO: e.g., slope in units/decade, odds ratio, mean difference |
| **Predictor(s)** | TODO: e.g., year, treatment group, spatial coordinate |
| **Covariates** | TODO: e.g., season, sex, age |
| **Bootstrap iterations** | Default: 1000 |
| **CI level** | Default: 95 % |

## Sensitivity Variants

| # | Variant | Description |
|---|---------|-------------|
| 1 | TODO | e.g., alternative tie-breaking rule |
| 2 | TODO | e.g., reduced sample period |
| 3 | TODO | e.g., stricter outlier threshold |
| 4 | TODO | e.g., alternative model specification |

## Constraints & Invariants

- **Use the correct statistical method for the data type**: circular data →
  von Mises / circular statistics, binary → logistic regression, count →
  Poisson / negative binomial, etc.
- **Bootstrap methodology**: Resample observations with replacement, refit
  the model each iteration, extract percentile confidence intervals.
- **MLE convergence handling**: If the primary MLE fails to converge, fall
  back to a non-parametric method (e.g., rank correlation) and log the
  fallback.
- **Year centering** (if time is a predictor): Center the year at the midpoint
  of the data range to reduce correlation between intercept and slope.
- **Report both**: Effect size (β or equivalent) AND uncertainty (CI or SE).

## Data Contracts

- **Input**: CSV at `config.processed_dir / config.processed_data_filename` with
  columns for the outcome, predictor(s), and covariates.
- **Output**: JSON at `config.results_dir / config.analysis_results_filename` with
  regression coefficients, bootstrap CI bounds, and per-variant sensitivity results.

## Edge Cases

- **Fewer than 2 unique values in predictor**: Return NaN with a logged warning.
- **All outcome values identical**: Model cannot estimate slope — return NaN.
- **Empty DataFrame after filtering**: Raise `ValueError`.

## AI Agent Prompt

When implementing `analysis.py`, preface with:

> Given the analysis plan in `planning/analysis_plan.md`:
> 1. Implement the specified statistical model.
> 2. Compute the primary endpoint with bootstrap CI.
> 3. Run all sensitivity variants.
> 4. Output results to JSON in `config.results_dir`.
> 5. Include a synthetic data test that verifies the correct coefficient.
> 6. Follow root AGENTS.md conventions.

## References

- [Root AGENTS.md](AGENTS.md) — global coding conventions
- [AGENTS-planning.md](AGENTS-planning.md) — analysis plan
- `config.py`: `ProjectConfig.n_bootstrap`, `.bootstrap_ci_level`
