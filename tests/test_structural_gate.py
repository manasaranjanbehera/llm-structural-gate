"""Tests for structural validation boundary. No semantic checks."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_valid_structure_passes(client):
    """Valid structure is accepted and returns the validated object."""
    resp = client.post("/invoke", json={"mode": "VALID"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["sentiment"] == "positive"
    assert data["confidence"] == 0.92
    assert data["summary"] == "Customer is happy"


def test_enum_violation_fails(client):
    """Enum typo (e.g. 'positve') is rejected."""
    resp = client.post("/invoke", json={"mode": "ENUM_VIOLATION"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_extra_field_fails(client):
    """Extra field (e.g. reasoning) is rejected (forbid)."""
    resp = client.post("/invoke", json={"mode": "EXTRA_FIELD"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_missing_field_fails(client):
    """Missing required field (summary) is rejected."""
    resp = client.post("/invoke", json={"mode": "MISSING_FIELD"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_numeric_bound_violation_fails(client):
    """Confidence > 1.0 is rejected."""
    resp = client.post("/invoke", json={"mode": "NUMERIC_BOUND_VIOLATION"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body


def test_malformed_json_fails(client):
    """Malformed JSON is rejected before schema validation."""
    resp = client.post("/invoke", json={"mode": "MALFORMED_JSON"})
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "rejected"
    assert "reason" in body
