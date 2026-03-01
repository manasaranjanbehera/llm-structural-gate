"""Simulated probabilistic client: returns JSON strings by mode. No retries."""

OUTPUTS = {
    "VALID": '{"sentiment": "positive", "confidence": 0.92, "summary": "Customer is happy"}',
    "ENUM_VIOLATION": '{"sentiment": "positve", "confidence": 0.92, "summary": "Customer is happy"}',
    "EXTRA_FIELD": '{"sentiment": "positive", "confidence": 0.92, "summary": "Customer is happy", "reasoning": "internal chain of thought"}',
    "MISSING_FIELD": '{"sentiment": "positive", "confidence": 0.92}',
    "NUMERIC_BOUND_VIOLATION": '{"sentiment": "positive", "confidence": 1.5, "summary": "Customer is happy"}',
    "MALFORMED_JSON": '{"sentiment": "positive" "confidence": 0.92, "summary": "Customer is happy"}',
    "STRING_INSTEAD_OF_FLOAT": '{"sentiment": "positive", "confidence": "0.92", "summary": "Customer is happy"}',
    "INT_INSTEAD_OF_FLOAT": '{"sentiment": "positive", "confidence": 1, "summary": "Customer is happy"}',
    "ENUM_CASE_VARIATION": '{"sentiment": "Positive", "confidence": 0.92, "summary": "Customer is happy"}',
    "SEMANTICALLY_WRONG": '{"sentiment": "negative", "confidence": 0.92, "summary": "Customer is happy and satisfied"}',
}


def generate_output(mode: str) -> str:
    """Return raw JSON string for the given mode. No validation, no correction. Unknown mode raises."""
    if mode not in OUTPUTS:
        raise ValueError("Unknown mode")
    return OUTPUTS[mode]
