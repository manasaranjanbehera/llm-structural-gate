# llm-structural-gate

![CI](https://github.com/manasaranjanbehera/llm-structural-gate/actions/workflows/ci.yml/badge.svg)

A minimal prototype that implements a **Structural Constraint Gate** for LLM outputs: a deterministic contract boundary between probabilistic generation and downstream application logic.

---

## Problem Statement

LLM outputs are probabilistic. Tokens are sampled; formatting and structure vary. Downstream systems often assume a fixed contract (e.g. JSON with required fields and types). Using raw LLM output as if it were a deterministic API response leads to parse failures, type errors, and undefined behavior.

A **Structural Constraint Gate** is a validation layer that accepts or rejects output strictly against a schema. Only well-formed, schema-compliant data crosses the boundary. Rejected output does not reach the rest of the system.

This is **structural validation**, not semantic safety filtering. The gate checks shape, types, required fields, and allowed values. It does not evaluate truthfulness, intent, or business rules. A structurally valid response can still be wrong or misleading.

---

## What This Project Does

- Validates raw LLM output (here, simulated as JSON strings) against a single fixed schema.
- Enforces **strict** structural rules: no type coercion (e.g. string or int to float is rejected), exact enum matching (case-sensitive), no extra fields.
- Returns either the validated structured object (accept) or a rejection with reason (reject). No silent correction, retries, or auto-fix.
- This project intentionally avoids semantic judgment, business rule validation, or auto-correction. It enforces structure only.


The prototype uses a simulated LLM client (no external API). The validation path is local and deterministic.

---

## How It Works

1. Raw output (e.g. from an LLM) is passed as a string.
2. The string is parsed as JSON. Parse failure → reject.
3. The parsed object is validated against the schema. Validation failure → reject.
4. Success yields a typed instance; failure yields an error reason.

Core API: `validate(raw_output: str) → ValidationSuccess | ValidationFailure`.

---

## Architecture Overview

```
    User Input
         │
         ▼
   Prompt Builder
         │
         ▼
        LLM
         │
         ▼
   ┌─────────────────────────────────────────┐
   │  Structural Gate                        │
   │  (Deterministic Contract Boundary)      │
   │  Schema Validation Layer                │
   └─────────────────────────────────────────┘
         │
         ▼
   Accept / Reject
         │
         ▼
   Downstream System
```

The Structural Gate is the single place where output is checked against the contract. Nothing that fails validation reaches the downstream system.

---

## Structural Constraint Examples

### Schema (fixed in this prototype)

**SentimentResult** — all fields required, no extra properties:

| Field       | Type  | Constraint                                      |
|------------|-------|--------------------------------------------------|
| sentiment  | enum  | `"positive"` \| `"negative"` \| `"neutral"`      |
| confidence | float | 0.0 ≤ value ≤ 1.0 (strict float; no int/string)  |
| summary    | string| minLength 5                                     |

### Example: passes validation

```json
{"sentiment": "positive", "confidence": 0.92, "summary": "Customer is happy"}
```

### Example: fails validation

- Malformed JSON: `{"sentiment": "positive" "confidence": 0.92, ...}` → reject (parse error).
- Wrong type: `"confidence": "0.92"` (string) or `"confidence": 1` (int) → reject (strict float).
- Enum: `"sentiment": "Positive"` or `"positve"` → reject (exact enum only).
- Extra field: `"reasoning": "..."` → reject (additional properties forbidden).
- Missing field: no `summary` → reject.

### Python usage

```python
from app.validator import validate

raw = '{"sentiment": "positive", "confidence": 0.92, "summary": "Customer is happy"}'
result = validate(raw)

if hasattr(result, "instance"):
    # Accepted: use result.instance (typed SentimentResult)
    print(result.instance.model_dump())
else:
    # Rejected: result.reason describes the failure
    print("Rejected:", result.reason)
```

---

## Example Usage

### Run the API

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server: `http://127.0.0.1:8000`

### Invoke (simulator modes)

**POST /invoke** body: `{"mode": "VALID"}`.

Modes include: `VALID`, `ENUM_VIOLATION`, `EXTRA_FIELD`, `MISSING_FIELD`, `NUMERIC_BOUND_VIOLATION`, `MALFORMED_JSON`, `STRING_INSTEAD_OF_FLOAT`, `INT_INSTEAD_OF_FLOAT`, `ENUM_CASE_VARIATION`, `SEMANTICALLY_WRONG`. Any other `mode` returns 400 (unknown mode).

- **Validation passes:** 200 with the validated JSON.
- **Validation fails:** 400 with `{"status": "rejected", "reason": "<message>"}`.

```bash
# Accepted
curl -s -X POST http://127.0.0.1:8000/invoke -H "Content-Type: application/json" -d '{"mode": "VALID"}'

# Rejected (e.g. enum typo)
curl -s -X POST http://127.0.0.1:8000/invoke -H "Content-Type: application/json" -d '{"mode": "ENUM_VIOLATION"}'
```

---

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## Roadmap

This prototype focuses exclusively on structural validation.
Future exploration may include:

- Multi-schema support (contract per workflow).
- Structured output prompting integration.
- Typed client SDK generation from schema.
- Integration with execution workflows (e.g., reject → retry policy at application layer).

The gate itself will remain a deterministic boundary. Retry logic, fallback policy, and business rules belong outside this layer.

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests, and pull request guidelines. Security issues: see [SECURITY.md](SECURITY.md); do not report them as public issues.

---

## License

MIT.
