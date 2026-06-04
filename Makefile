# ─────────────────────────────────────────────────────────────────────────
# TED Keyword Popularity Analysis — Pipeline Makefile
# Stages: acquire → preprocess → analyze → visualize → report
#   test (independent of data pipeline)
#   all (full pipeline end-to-end)
# ─────────────────────────────────────────────────────────────────────────

.PHONY: acquire preprocess analyze visualize report
.PHONY: test clean all dirs install

# ── Directory creation ────────────────────────────────────────────────
dirs:
	mkdir -p data/raw data/processed data/external \
	         results/figures logs \
	         literature/papers \
	         notebooks manuscript

# ── Package installation ────────────────────────────────────────────────
install:
	uv pip install -e ".[dev]"

# ── Pipeline stages ─────────────────────────────────────────────────────
acquire: dirs
	@echo "=== Stage: Data Acquisition ==="
	python -m ted_analysis.acquire

preprocess: acquire
	@echo "=== Stage: Preprocessing ==="
	python -m ted_analysis.preprocess

analyze: preprocess
	@echo "=== Stage: Analysis ==="
	python -m ted_analysis.analysis

visualize: analyze
	@echo "=== Stage: Visualization ==="
	python -m ted_analysis.visualize

report: visualize
	@echo "=== Stage: Report ==="
	python -m ted_analysis.report
	@echo "Manuscript source: manuscript/main.qmd"
	@echo "Compile with: quarto render manuscript/main.qmd --to html"

# ── Testing (independent of data pipeline) ──────────────────────────────
test:
	python -m pytest tests/ -v --cov=ted_analysis --cov-report=term-missing

# ── Housekeeping ────────────────────────────────────────────────────────
clean:
	mkdir -p logs && rm -rf logs/*.log results/figures/* data/processed/*

# ── Full pipeline ───────────────────────────────────────────────────────
all: install acquire preprocess analyze visualize report
	@echo "=== Full pipeline complete ==="
