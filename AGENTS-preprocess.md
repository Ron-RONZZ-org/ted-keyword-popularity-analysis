# AGENTS-preprocess.md — Preprocessing & QC Rules

## Scope

`src/pkg/preprocess.py` — quality control, data cleaning, transformation,
and feature extraction. Converts raw data into an analysis-ready dataset.

## Constraints & Invariants

- **Schema validation at both boundaries**: Validate input immediately after
  loading; validate output before saving.
- **Never use `pytz`**: Use `zoneinfo` (stdlib) for all timezone operations.
- **Missing data threshold**: Define a minimum fraction of valid observations
  per unit (default ≥ 75 %) — exclude units below this threshold.
- **Domain-specific filter**: TODO: e.g., physical limits, diurnal amplitude
  filter, outlier detection.
- **Tie-breaking**: If multiple values tie for the feature of interest, use a
  deterministic rule (e.g., earliest, latest, median). Do NOT average tied
  values if the feature is circular (average of 0 and 23 is 11.5 — meaningless).
- **DST edge cases** (if time-series data): 23-hour (spring-forward) and
  25-hour (autumn-back) days must be handled correctly. Do not drop or
  duplicate records on transition days.

## Output Schema

The processed CSV is saved to `config.processed_dir / config.processed_data_filename`.
Columns should include (adjust per project):

| Column | Type | Description |
|--------|------|-------------|
| `date` | datetime | Date (or datetime) of observation |
| `feature` | float | Extracted feature value |
| `qc_flag` | bool | True if excluded by QC |
| `quality_metric` | float | Auxiliary quality metric |

## Edge Cases

- **All-missing record**: Return row with NaN/None for the feature; do NOT drop.
- **Station/data gap**: Leave gaps — do NOT interpolate across extended
  missing periods unless explicitly justified.
- **Zero-variance period**: If all values are identical in a window, flag it
  (possible instrument malfunction).

## AI Agent Prompt

When implementing `preprocess.py`, preface with:

> Design and implement a preprocessing pipeline that:
> 1. Loads raw data from `config.raw_dir`.
> 2. Validates input schema.
> 3. Applies QC filters (missing data, physical limits, timezone handling).
> 4. Extracts the analysis feature(s).
> 5. Validates output schema.
> 6. Saves to `config.processed_dir`.
> 7. Follows root AGENTS.md conventions.

## References

- [Root AGENTS.md](AGENTS.md) — global coding conventions
- `config.py`: `ProjectConfig.processed_dir`, `.processed_data_filename`
