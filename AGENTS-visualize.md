# AGENTS-visualize.md — Figure Generation Rules

## Scope

`src/pkg/visualize.py` — publication-quality figures for the analysis.
All figures are exported as PDF (vector) and PNG (raster) at 300 DPI.

## Constraints & Invariants

- **Figure dimensions**: Single-column journal width = 3.5 in (88.9 mm);
  full-page width = 7.0 in (177.8 mm). Use these as default widths.
- **DPI**: Minimum 300 DPI for raster export; 150 DPI for interactive display.
- **Color palette**: Use a colorblind-safe palette (e.g.,
  `seaborn.color_palette("colorblind")`). Avoid red-green contrasts.
- **Dual export**: Every figure is saved as **PDF** (vector, for publication)
  and **PNG** (raster, for quick viewing) at 300 DPI.
- **Font sizes**: Axis labels ≥ 10 pt, tick labels ≥ 8 pt, title ≥ 12 pt.
  Use sans-serif font (Helvetica or DejaVu Sans).
- **File naming**: Lowercase, underscored, descriptive:
  `{variant}_{description}.{ext}`

## Specific Plots

| Function | Description | TODO |
|----------|-------------|------|
| `plot_main_effect` | Main result figure — trend or comparison | Fill in plot type, axes, styling |
| `plot_distribution` | Distribution of the outcome variable | Fill in histogram/rose/density details |
| `plot_faceted` | Faceted plot by subgroup (e.g., season, region) | Fill in grouping variable |

## Data Contracts

- **Input**: Processed data CSV (DataFrame with analysis columns).
- **Output**: Figure files saved to `config.figures_dir`.

## Edge Cases

- **Zero variance**: If all values are identical, the trend line is flat.
  Plot it as a horizontal line.
- **Gappy data**: Do NOT interpolate across extended gaps.
- **Missing figure data**: If a required column is missing, skip that figure
  and log a warning (do NOT crash the entire stage).

## AI Agent Prompt

When implementing `visualize.py`, preface with:

> Produce publication-quality figures from the analysis output. For each figure:
> 1. Export as both PDF and PNG at 300 DPI.
> 2. Use a colorblind-safe palette.
> 3. Apply the font size and dimension conventions above.
> 4. Wrap each figure in a try/except so one failure doesn't block others.
> 5. Follow root AGENTS.md conventions.

## References

- [Root AGENTS.md](AGENTS.md) — global coding conventions
- `config.py`: `ProjectConfig.figures_dir`
