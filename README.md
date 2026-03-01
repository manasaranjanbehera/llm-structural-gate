# Structural Gate — Deterministic Contract Boundary

![CI](https://github.com/manasaranjanbehera/llm-structural-gate/actions/workflows/ci.yml/badge.svg)

Minimal runnable prototype that enforces **structural constraint as a deterministic contract boundary**: no output crosses the boundary unless it is valid against the schema. The schema is the source of truth; the LLM is simulated as an untrusted probabilistic client. This project implements **structural validation only** (no semantic validation, retries, business logic, or resilience modeling).

**Strict structural hardening:**

- **Strict structural validation:** Validation enforces strict type compliance (no coercion).
- **No type coercion**: string→float and int→float (when strict float is required) are rejected; types must match the schema exactly.
- **Exact enum matching**: enum values are matched exactly and case-sensitively (e.g. `"Positive"` is rejected; only `"positive"` is accepted).
- **Unknown simulator modes are rejected**: if an unknown `mode` is passed, the API returns 400 and does not fall back to valid output.

## Technology Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Uvicorn
- Structlog (structured logging)
- Pytest

No LangChain, database, or external LLM. LLM output is simulated locally.

## Project Structure

```
app/
├── main.py           # API and /invoke endpoint
├── llm_simulator.py  # Simulated client output by mode
├── models.py         # SentimentResult schema
├── validator.py      # validate(raw_output: str) → ValidationSuccess | ValidationFailure
└── logging_config.py # Structlog setup
tests/
├── test_structural_gate.py
└── test_strict_structural_gate.py
requirements.txt
README.md
```

This prototype demonstrates a single fixed schema structural gate. Schema parameterization is intentionally out of scope.

## Schema (Strict)

**SentimentResult** — all fields required, `additionalProperties` forbidden:

| Field       | Type   | Constraint                          |
|------------|--------|-------------------------------------|
| sentiment  | enum   | `"positive"` \| `"negative"` \| `"neutral"` |
| confidence | float  | 0.0 ≤ value ≤ 1.0                   |
| summary    | string | minLength = 5                       |

Enforced with Pydantic `ConfigDict(extra="forbid")` and strict float (no string/int coercion); exact types and enum values required.

## API

Validation is `validate(raw_output: str)` → `ValidationSuccess` | `ValidationFailure` against the **fixed SentimentResult schema**; the prototype does not accept a schema parameter. API request body models (e.g. `InvokeRequest` for `/invoke`) are defined in `main.py`.

**POST /invoke**

Request body:

```json
{ "mode": "VALID" }
```

Supported modes: `VALID`, `ENUM_VIOLATION`, `EXTRA_FIELD`, `MISSING_FIELD`, `NUMERIC_BOUND_VIOLATION`, `MALFORMED_JSON`, `STRING_INSTEAD_OF_FLOAT`, `INT_INSTEAD_OF_FLOAT`, `ENUM_CASE_VARIATION`, `SEMANTICALLY_WRONG`. Any other mode returns 400 (unknown mode).

- **If validation passes:** response 200 with the validated structured object.
- **If validation fails:** response 400 with:

```json
{
  "status": "rejected",
  "reason": "<validation error message>"
}
```

No silent correction, retries, or auto-fix.

## Run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server: `http://127.0.0.1:8000`

## Examples (with curl)

Assume the server is running at `http://127.0.0.1:8000`.

### Example 1 — Valid Structure

**Expected: ACCEPTED**

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "VALID"}'
```

Expected response (200): `{"sentiment":"positive","confidence":0.92,"summary":"Customer is happy"}`

---

### Example 2 — Enum Typo

**Expected: REJECTED**

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "ENUM_VIOLATION"}'
```

Expected response (400): `{"status":"rejected","reason":"..."}` (enum / input constraint message).

---

### Example 3 — Extra Field

**Expected: REJECTED** (additionalProperties equivalent via forbid)

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "EXTRA_FIELD"}'
```

Expected response (400): `{"status":"rejected","reason":"..."}` (extra fields not allowed).

---

### Example 4 — Missing Required Field

**Expected: REJECTED**

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "MISSING_FIELD"}'
```

Expected response (400): `{"status":"rejected","reason":"..."}` (missing field).

---

### Example 5 — Numeric Bound Violation

**Expected: REJECTED**

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "NUMERIC_BOUND_VIOLATION"}'
```

Expected response (400): `{"status":"rejected","reason":"..."}` (e.g. confidence &gt; 1.0).

---

### Example 6 — Malformed JSON

**Expected: REJECTED** (before schema validation)

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "MALFORMED_JSON"}'
```

Expected response (400): `{"status":"rejected","reason":"..."}` (JSON decode error).

---

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Tests in `test_structural_gate.py` and `test_strict_structural_gate.py`: valid passes; enum violation, extra field, missing field, numeric bound, malformed JSON, string/int instead of float, enum case variation, and unknown mode each fail with 400 and `status: rejected`.

## Development

Format code:

```bash
ruff format .
```

Lint code:

```bash
ruff check .
```

## Continuous Integration

All pull requests and pushes to `main` run:

- `ruff check .`
- `ruff format --check .`
- `pytest`

via GitHub Actions (Python 3.11).

## What the Structural Gate Guarantees

This prototype intentionally uses a single fixed schema (SentimentResult) to demonstrate deterministic structural enforcement.

- **Structural correctness** — JSON is well-formed and matches the expected shape.
- **Type correctness** — Types (string, float, enum) match the schema exactly; no coercion (e.g. string or int to float is rejected).
- **Field presence** — All required fields are present.
- **Enum membership** — Values are in the allowed set with exact, case-sensitive matching (no fuzzy matching).
- **No unexpected fields** — `extra="forbid"` so additional keys are rejected.
- **No simulator fallback** — Unknown modes return 400; no default to valid output.

## What It Does NOT Guarantee

- Factual correctness  
- Truthfulness  
- Business rule validity  
- Intent alignment  

**A perfectly structured lie passes the structural gate.**

---

## Audit metadata and behaviour

**Audit environment.** Audit performed on local read-only checkout, Python 3.11; Ruff and Pytest as declared in `requirements.txt`. That adds reproducibility metadata.

**No outbound network calls in validation path.** The validation path (request → simulator → `validate(raw)` → response) performs no outbound network calls. Parsing and schema checks are local only; determinism does not depend on network state.

**FastAPI error handling.**  
- **ValidationFailure → HTTP 400:** In `main.py`, when `validate(raw)` returns a `ValidationFailure`, the handler returns `JSONResponse(status_code=400, content={"status": "rejected", "reason": reason})`. All schema and JSON-parse failures are mapped to 400.  
- **Request body errors → HTTP 422:** Invalid request bodies (e.g. missing `mode`, wrong types for `InvokeRequest`) are validated by FastAPI/Pydantic before `invoke()` runs; FastAPI returns 422 Unprocessable Entity for those.  
- **Deterministic boundary:** Both 400 (gate rejection) and 422 (request validation) are deterministic. They do not violate the deterministic boundary claim; 422 is input validation at the API boundary.

**Residual risks.** For completeness, enterprise-style audits might note:

- No dependency pinning (only minimum versions in `requirements.txt`)
- No supply-chain verification
- No SAST/DAST
- No coverage measurement threshold

Not required for this small repo, but improves audit completeness.

---

## Open Source Readiness

This project is MIT licensed. Contributions are welcome; please see [CONTRIBUTING.md](CONTRIBUTING.md). Security issues must be reported in accordance with [SECURITY.md](SECURITY.md)—do not file them as public issues.

---

No try/except that hides validation failure, no default values added silently, no coercion, no fuzzy enum matching, no semantic checks, no retry loop. This is a pure deterministic structural gate.
