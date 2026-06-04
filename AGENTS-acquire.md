# AGENTS-acquire.md — Data Acquisition Rules

## Scope

`src/pkg/acquire.py` — downloads data from the specified source(s),
validates the schema, and saves to the raw data directory.

## Data Source

| Item | Detail |
|------|--------|
| **Source** | TODO: e.g., API base URL, data portal, file server |
| **Access method** | TODO: e.g., pooch, requests, ftp, S3 |
| **Credentials** | TODO: env var for API token (never hardcode) |
| **Fallback** | TODO: local file path if remote unreachable |
| **Format** | TODO: CSV, NetCDF, HDF5, Parquet, etc. |
| **Reference period** | TODO: date range of interest |

## Output Schema

The output CSV is saved to `config.raw_dir / config.raw_data_filename`
with these columns (adjust per project):

| Column | Type | Description |
|--------|------|-------------|
| `id` | str | Record/sample identifier |
| `timestamp` | datetime | Observation time (UTC) |
| `value` | float | Measured variable |
| `quality_flag` | int | Quality indicator |

## Constraints & Invariants

- **Always validate after download**: Check column presence, dtypes, and basic
  value ranges before returning data to the pipeline.
- **Hash verification**: If using pooch, maintain a registry of SHA256 hashes
  for every tracked URL. Do NOT skip hash checks.
- **Retry logic**: Implement at least 1 retry with exponential backoff before
  falling back to the local copy.
- **Local fallback**: If the remote download fails, fall back to a local file
  in `config.external_dir / config.local_fallback_dir`.

## Edge Cases

- **Empty source**: Raise a clear error if the data source returns no data.
- **Network timeout**: Catch timeout exceptions, log warning, retry, then fall back.
- **Schema mismatch**: Log expected vs actual columns; raise `ValueError` with
  details.
- **Partial download**: If a multi-file download fails partway, do NOT proceed
  with incomplete data — either retry or fail cleanly.

## AI Agent Prompt

When implementing `acquire.py`, preface with:

> Given the data source table above, produce an `acquire.py` that:
> 1. Downloads data from the specified source using [method].
> 2. Validates the schema (columns, dtypes, ranges).
> 3. Saves to `config.raw_dir / config.raw_data_filename`.
> 4. Follows root AGENTS.md conventions (logging, type hints, docstrings).
>
> Include a CLI entry point (`main()`) callable via `python -m pkg.acquire`.

## References

- [Root AGENTS.md](AGENTS.md) — global coding conventions
- `config.py`: `ProjectConfig.data_dir`, `.raw_dir`, `.raw_data_filename`
