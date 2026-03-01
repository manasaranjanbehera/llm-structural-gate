"""Strict structural gate tests: no coercion, exact enum, unknown mode rejected."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_string_instead_of_float_rejected(client):
    """String for confidence (e.g. \"0.92\") is rejected; no coercion to float."""
    resp = client.post("/invoke", json={"mode": "STRING_INSTEAD_OF_FLOAT"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_int_instead_of_float_rejected(client):
    """Int for confidence (e.g. 1) is rejected when strict float is required."""
    resp = client.post("/invoke", json={"mode": "INT_INSTEAD_OF_FLOAT"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_enum_case_variation_rejected(client):
    """Enum value with wrong case (e.g. \"Positive\" vs \"positive\") is rejected."""
    resp = client.post("/invoke", json={"mode": "ENUM_CASE_VARIATION"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_unknown_mode_rejected(client):
    """Unknown simulator mode returns 400; no fallback to VALID."""
    resp = client.post("/invoke", json={"mode": "UNKNOWN_MODE"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_structurally_valid_semantically_wrong_accepted(client):
    """Semantically inconsistent payload (negative sentiment + happy summary) is accepted; structural validation only."""
    resp = client.post(
        "/invoke",
        json={"mode": "SEMANTICALLY_WRONG"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sentiment"] == "negative"
    assert data["confidence"] == 0.92
    assert data["summary"] == "Customer is happy and satisfied"
