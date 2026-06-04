# ─────────────────────────────────────────────────────────────────────────
# Research Pipeline — Makefile
# Stages: plan → litreview → acquire → preprocess → analyze → visualize → report
#   test (independent of data pipeline)
#   all (full pipeline end-to-end)
# ─────────────────────────────────────────────────────────────────────────

.PHONY: plan litreview acquire preprocess analyze visualize report
.PHONY: test clean all dirs install

# ── Directory creation ────────────────────────────────────────────────
dirs:
	mkdir -p data/raw data/processed data/external \
	         results/figures logs \
	         literature/papers \
	         notebooks manuscript

# ── Package installation ────────────────────────────────────────────────
install:
	pip install -e ".[dev]"

# ── Pipeline stages ─────────────────────────────────────────────────────
plan:
	@echo "=== Stage: Planning ==="
	@echo "Read AGENTS-planning.md, then work through:"
	@echo "  1. Define research question"
	@echo "  2. Draft pre-registration"
	@echo "  3. Update src/pkg/config.py"
	@echo "Output → planning/ directory."

litreview: plan
	@echo "=== Stage: Literature Review ==="
	@echo "Read AGENTS-litreview.md."
	@echo "Output → literature/ directory (papers + bibliography.bib + synthesis.md)."

acquire: dirs litreview
	@echo "=== Stage: Data Acquisition ==="
	python -m pkg.acquire

preprocess: acquire
	@echo "=== Stage: Preprocessing ==="
	python -m pkg.preprocess

analyze: preprocess
	@echo "=== Stage: Analysis ==="
	python -m pkg.analysis

visualize: analyze
	@echo "=== Stage: Visualization ==="
	python -m pkg.visualize

report: visualize
	@echo "=== Stage: Report ==="
	python -m pkg.report
	@echo "Manuscript source: manuscript/main.qmd"
	@echo "Compile with: quarto render manuscript/main.qmd --to html"

# ── Testing (independent of data pipeline) ──────────────────────────────
test:
	python -m pytest tests/ -v --cov=src --cov-report=term-missing

# ── Housekeeping ────────────────────────────────────────────────────────
clean:
	rm -rf logs/*.log results/figures/* data/processed/*

# ── Full pipeline ───────────────────────────────────────────────────────
all: install plan litreview acquire preprocess analyze visualize report
	@echo "=== Full pipeline complete ==="
