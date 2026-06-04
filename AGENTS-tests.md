# AGENTS-tests.md — Testing Conventions

## Scope

All tests under `tests/` — unit tests, integration tests, and regression
tests for every pipeline module.

## Constraints & Invariants

- **Coverage targets**: ≥ 80 % line coverage overall; 100 % coverage on
  critical paths (edge-case handling, tie-breaking, QC filters).
- **Synthetic data tests**: Analysis modules must include a test with known
  synthetic data that verifies the correct result.
- **Slow tests**: Tests that take > 2 seconds must be marked with
  ``@pytest.mark.slow``. Run with ``pytest tests/ -m "not slow"`` for a
  quick check.
- **Logging suppression**: The autouse fixture in `conftest.py` keeps test
  output clean. Do NOT log at INFO or below during tests unless explicitly
  testing logging behaviour.

## Test Structure

Use ``class Test*`` for logical grouping. Each test function is a single
assertion or a small set of related assertions.

## Naming

Test functions use ``test_<scenario>_<expected_behaviour>`` pattern (snake
case). Examples:
- ``test_empty_input_raises_value_error``
- ``test_edge_case_returns_nan``
- ``test_synthetic_data_match_expected_coefficient``

## References

- [Root AGENTS.md](AGENTS.md) — global coding conventions
- `conftest.py` — fixture definitions and pytest configuration
