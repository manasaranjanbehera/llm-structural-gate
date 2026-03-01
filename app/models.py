"""Strict schema: source of truth for structural contract boundary."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SentimentResult(BaseModel):
    """Contract: all fields required, no extra properties. No type coercion."""

    model_config = ConfigDict(extra="forbid")

    sentiment: Sentiment
    confidence: float = Field(ge=0.0, le=1.0, strict=True)
    summary: str = Field(min_length=5)

    # This enforces strict structural type compliance.
    # It intentionally rejects int to prevent coercion.
    # It is structural enforcement, not semantic validation.
    @field_validator("confidence", mode="before")
    @classmethod
    def confidence_must_be_float(cls, v: object) -> object:
        """Reject int; only float allowed (no int->float coercion)."""
        if isinstance(v, int):
            raise ValueError("Input must be a float, not an int")
        return v
