# AGENTS-litreview.md — Literature Review

## Scope

The `make litreview` stage. Discovers, reads, annotates, and synthesises
relevant prior work for the research question. This is a **human-led,
AI-assisted** process.

## Lifecycle Position

Runs after `plan` (the research question must exist) and before `acquire`
(the literature may influence data source decisions).

## Workflow

1. **Search**: Google Scholar, Semantic Scholar, Web of Science, arXiv
   using keywords derived from the research question in `planning/`.
2. **Collect**: Download PDFs to `literature/papers/{AuthorYear}.pdf`.
   For paywalled papers, note the DOI and accessibility.
3. **Annotate**: For each paper, capture:
   - Research question
   - Dataset and methods
   - Key quantitative findings
   - Limitations noted by authors
4. **Populate bibliography**: Add BibTeX entries to `literature/bibliography.bib`.
5. **Synthesise**: Write `literature/synthesis.md` — a 3-5 paragraph narrative
   with a summary table and identification of gaps.

## AI Agent Prompt

When you call an AI agent for this stage, preface with:

> You are a research assistant conducting a systematic literature review.
> Given the research question in `planning/research_question.md`:
>
> 1. Search for 15-20 relevant papers across major databases.
> 2. For each paper, extract: research question, methods used, key
>    quantitative findings, limitations.
> 3. Return results as a markdown table with columns: Author (Year),
>    Question, Methods, Key Findings, Limitations.
> 4. Append BibTeX entries for each paper in a code block.
> 5. Write a 3-5 paragraph synthesis identifying gaps in the literature.
>
> Prioritise recent (last 10 years) and highly cited papers. Flag any
> direct replications or contradictory findings.

## Output Checklist

- [ ] `literature/bibliography.bib` contains ≥ 15 entries
- [ ] `literature/synthesis.md` written with gap analysis
- [ ] PDFs saved to `literature/papers/` (at least for open-access papers)
- [ ] Research question refined/updated based on literature findings

## References

- [Root AGENTS.md](AGENTS.md) — global conventions
- [AGENTS-planning.md](AGENTS-planning.md) — research question
