import os
import tempfile
import pytest
import csv
import io
from fastapi.testclient import TestClient
from src.event_tracker.db import init_db

@pytest.fixture
def test_app():
    """Create a fresh app with isolated DB for each test"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = f.name
    
    os.environ["EVENTS_DB_PATH"] = db_path
    init_db()
    
    # Import app AFTER setting env var
    from src.event_tracker.main import app
    
    yield TestClient(app)
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)

def test_export_csv_header(test_app):
    """Test that CSV export includes correct header"""
    client = test_app

    # Create a sample event
    client.post(
        "/events",
        json={
            "ts": "2026-01-21T12:00:00",
            "label": "test",
            "description": "test event",
            "x": 1.5,
            "y": 2.5,
            "source": "manual"
        },
    )

    # Export events as CSV
    response = client.get("/events/export")
    print(f"Status: {response.status_code}, Body: {response.text}")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]

    # Read CSV content
    csv_reader = csv.DictReader(io.StringIO(response.text))
    rows = list(csv_reader)

    # Check header
    assert csv_reader.fieldnames == ["id", "ts", "label", "description", "x", "y", "source"]

    assert len(rows) == 1
    assert rows[0]["label"] == "test"
    assert rows[0]["description"] == "test event"

def test_export_csv_filtered(test_app):
    """Test that CSV export respects filters"""
    client = test_app

    # Create multiple events
    client.post(
        "/events",
        json={
            "ts": "2026-01-21T10:00:00",
            "label": "crack",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-22T11:00:00",
            "label": "rust",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-22T12:00:00",
            "label": "crack",
        },
    )

    # Export events filtered by label 'crack'
    response = client.get("/events/export?label=crack")
    assert response.status_code == 200

    # Read CSV content
    csv_reader = csv.DictReader(io.StringIO(response.text))
    rows = list(csv_reader)

    # Check that only events with label 'crack' are exported
    assert len(rows) == 2
    assert all(row["label"] == "crack" for row in rows)

def test_export_csv_empty(test_app):
    """Test that CSV export works when no events match filters"""
    client = test_app
    # Export events with no events
    response = client.get("/events/export")
    assert response.status_code == 200

    # Read CSV content
    csv_reader = csv.DictReader(io.StringIO(response.text))
    rows = list(csv_reader)

    # Check that no rows are returned
    assert csv_reader.fieldnames == ["id", "ts", "label", "description", "x", "y", "source"]
    assert len(rows) == 0
