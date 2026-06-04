# AGENTS-planning.md — Research Planning & Pre-registration

## Scope

The `make plan` stage. Guides the formulation of the research question,
primary endpoint, analysis plan, and OSF pre-registration. This is a
**human-led, AI-assisted** process — no Python code is produced.

## Lifecycle Position

This stage is **mandatory before any data acquisition or analysis**. The
OSF pre-registration must be submitted and a DOI obtained before the
`acquire` stage begins. This prevents post-hoc model shopping and
p-hacking.

## Required Outputs

| File | Content |
|---|---|
| `planning/research_question.md` | Single paragraph stating the question. Include: population, intervention/exposure, comparison, outcome (PICO-style). |
| `planning/pre_registration_draft.md` | Full OSF pre-registration text: hypothesis, sampling plan, variables, analysis plan. |
| `planning/analysis_plan.md` | Primary endpoint, secondary endpoints, sensitivity analyses, covariates, stopping rule. |
| `src/pkg/config.py` (updated) | Dataclass populated with analysis parameters. |

## AI Agent Prompt

When you call an AI agent for this stage, preface with:

> You are a research methodologist helping a scientist design a reproducible
> study. Your job is to:
>
> 1. Help the user define a focused, falsifiable research question.
> 2. Identify the primary endpoint and key covariates.
> 3. List planned sensitivity analyses (at least 3).
> 4. Draft pre-registration text suitable for OSF.
> 5. Create a stub `config.py` with relevant parameters.
>
> Output each deliverable as a separate markdown section. Use plain
> language — avoid jargon unless the user provides it.

## Constraints

- **No data peeking**: Do NOT look at any data before pre-registration is submitted.
- **Pre-registration DOI**: Record the OSF DOI in `planning/` for reference.
- **Version lock**: Commit `planning/` directory before moving to `litreview`.

## References

- [Root AGENTS.md](AGENTS.md) — global conventions
- OSF pre-registration guide: https://help.osf.io/article/438-create-a-preregistration
