# Changelog

All notable changes to this project will be documented in this file.

Deterministic structural validation service for enforcing strict JSON schema contracts.

This project follows Semantic Versioning.

---

## [Unreleased]

_No changes yet._

---

## [0.1.0] - 2026-03-01

### Added

- Deterministic structural validation gate implemented using Pydantic v2
- Defined `SentimentResult` schema:
  - `sentiment` enum (`positive`, `negative`, `neutral`)
  - `confidence` strict float (0.0 ≤ value ≤ 1.0)
  - `summary` string (min length 5)
- Strict type enforcement (no string/int → float coercion)
- Exact, case-sensitive enum matching
- `extra="forbid"` (no additional fields allowed)
- Explicit two-valued contract: `ValidationSuccess | ValidationFailure`
- FastAPI `/invoke` endpoint
- Local LLM output simulator (development/testing only)
- Unit and integration tests covering:
  - Valid structure
  - Enum violations
  - Missing fields
  - Extra fields
  - Numeric bound violations
  - Malformed JSON
  - Type violations
  - Unknown mode handling
- Ruff-based linting and formatting
- GitHub Actions CI:
  - `ruff check .`
  - `ruff format --check .`
  - `pytest --tb=short -q`
- Open-source repository structure:
  - MIT License
  - CONTRIBUTING.md
  - SECURITY.md
  - CODE_OF_CONDUCT.md
  - Issue templates

### Guarantees

- No output is accepted unless it matches the schema exactly
- No automatic correction or fallback behavior
- No semantic validation
- Deterministic structural enforcement only

---

[0.1.0]: https://github.com/manasaranjanbehera/llm-structural-gate/releases/tag/v0.1.0