"""Structural gate: validate(output) → valid | invalid against fixed SentimentResult schema. No coercion."""

import json

from pydantic import ValidationError

from app.models import SentimentResult


class ValidationSuccess:
    """Output passed the structural boundary."""

    def __init__(self, instance: SentimentResult) -> None:
        self.instance = instance


class ValidationFailure:
    """Output rejected at the boundary."""

    def __init__(self, reason: str) -> None:
        self.reason = reason


def validate(raw_output: str) -> ValidationSuccess | ValidationFailure:
    """
    Validate raw_output against the SentimentResult schema (the single fixed schema for this prototype).
    Performs structural validation only; does not perform semantic validation.
    Parses JSON then validates. No correction, no coercion.
    Returns success with instance or failure with reason.
    """
    try:
        data = json.loads(raw_output)
    except json.JSONDecodeError as e:
        return ValidationFailure(reason=str(e))

    try:
        instance = SentimentResult.model_validate(data)
    except ValidationError as e:
        errs = e.errors()
        parts = [err.get("msg", str(e)) for err in errs if err.get("msg")]
        reason = "; ".join(parts) if parts else str(e)
        return ValidationFailure(reason=reason)

    return ValidationSuccess(instance=instance)
