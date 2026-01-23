import os
import tempfile
import pytest
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

def test_filter__by_label(test_app):
    """Test filtering events by label"""
    # Create events with different labels
    client = test_app
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

    # Filter by label 'note'
    response = client.get("/events?label=crack")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
    assert all(item["label"] == "crack" for item in data["items"])
    
def test_filter_by_time_range(test_app):
    """Test filtering events by time range"""
    # Create events with different timestamps
    client = test_app

    client.post(
        "/events",
        json={
            "ts": "2026-01-20T10:00:00",
            "label": "early",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-22T12:00:00",
            "label": "middle",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-24T15:00:00",
            "label": "late",
        },
    )

    # Filter by time range
    response = client.get("/events?start=2026-01-21T00:00:00&end=2026-01-23T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["label"] == "middle"


def test_filter_by_bbox(test_app):
    """Test filtering events by bounding box"""
    client = test_app
    # Create events with different coordinates
    client.post(
        "/events",
        json={
            "ts": "2026-01-21T10:00:00",
            "label": "in",
            "x": 5.0,
            "y": 5.0,
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-22T11:00:00",
            "label": "out",
            "x": 15.0,
            "y": 15.0,
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-23T12:00:00",
            "label": "in",
            "x": 3.5,
            "y": 4.5,
        },
    )

    # Filter by bounding box
    response = client.get("/events?min_x=0&max_x=10&min_y=0&max_y=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert all(item["label"] == "in" for item in data["items"])

def test_pagination(test_app):
    """Test pagination of event listings"""
    client = test_app

    # Create multiple events
    for i in range(5):
        client.post(
            "/events",
            json={
                "ts": f"2026-01-21T{10+i:02d}:00:00",
                "label": f"event_{i}",
            },
        )

    # Fetch first 5 events
    response1 = client.get("/events?limit=2&offset=0")
    data1 = response1.json()
    assert data1["total"] == 5
    assert data1["limit"] == 2
    assert data1["offset"] == 0
    assert len(data1["items"]) == 2

    # Fetch next 5 events
    response2 = client.get("/events?limit=2&offset=2")
    data2 = response2.json()
    assert data2["total"] == 5
    assert len(data2["items"]) == 2

    assert data1["items"][0]["id"] != data2["items"][0]["id"]

def test_newest_first_sorting(test_app):
    """Test that events are sorted newest first by default"""
    client = test_app
    # Create events with different timestamps
    client.post(
        "/events",
        json={
            "ts": "2026-01-20T10:00:00",
            "label": "third",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-22T12:00:00",
            "label": "second",
        },
    )
    client.post(
        "/events",
        json={
            "ts": "2026-01-24T11:00:00",
            "label": "first",
        },
    )

    # Fetch events and check order
    response = client.get("/events?limit=10")
    data = response.json()
    items = data["items"]

    assert items[0]["label"] == "first"
    assert items[1]["label"] == "second"
    assert items[2]["label"] == "third"
