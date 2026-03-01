# Structural Gate — Deterministic Structural Validation

Service that validates raw JSON output against a fixed Pydantic schema before it is returned. No output is accepted unless it conforms to the SentimentResult shape and types; the LLM is simulated locally. Structural validation only—no semantic checks, retries, or coercion.

## Technology Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Uvicorn
- Structlog
- Pytest

No LangChain, database, or external LLM.

## Schema: SentimentResult

All fields required; extra properties forbidden.

| Field       | Type   | Constraint                                |
|------------|--------|-------------------------------------------|
| sentiment  | enum   | `"positive"` \| `"negative"` \| `"neutral"` |
| confidence | float  | 0.0 ≤ value ≤ 1.0 (strict, no coercion)   |
| summary    | string | minLength = 5                             |

Types must match exactly; string/int are not coerced to float. Enum values are case-sensitive.

## API

**POST /invoke**

Request body: `{ "mode": "<mode>" }`.

Supported modes: `VALID`, `ENUM_VIOLATION`, `EXTRA_FIELD`, `MISSING_FIELD`, `NUMERIC_BOUND_VIOLATION`, `MALFORMED_JSON`, `STRING_INSTEAD_OF_FLOAT`, `INT_INSTEAD_OF_FLOAT`, `ENUM_CASE_VARIATION`, `SEMANTICALLY_WRONG`. Any other mode returns 400.

- Validation passes: 200 with the validated JSON object.
- Validation fails: 400 with `{"status": "rejected", "reason": "<message>"}`.

No silent correction or auto-fix.

## Run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server: `http://127.0.0.1:8000`

## curl examples

Valid request (200):

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "VALID"}'
```

Invalid request (400), e.g. enum violation:

```bash
curl -s -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"mode": "ENUM_VIOLATION"}'
```

## What This Enforces

- JSON is well-formed and matches the expected shape.
- Types (string, float, enum) match the schema exactly; no coercion.
- All required fields are present.
- Enum values are in the allowed set with exact, case-sensitive matching.
- No extra keys (extra properties forbidden).
- Unknown `mode` returns 400; no fallback to valid output.
