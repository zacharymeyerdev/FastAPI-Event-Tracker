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

def test_create_event(test_app):
    """Test creating an event returns id"""
    client = test_app

    response = client.post(
        "/events",
        json={
            "ts": "2026-01-21T12:00:00",
            "label": "note",
            "description": "test event",
            "x": 1.5,
            "y": 2.5,
            "source": "manual"
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["label"] == "note"
    assert data["description"] == "test event"

def test_get_event(test_app):
    """Test fetching an event by id"""
    client = test_app

    # First, create an event
    create_response = client.post(
        "/events",
        json={
            "ts": "2026-01-21T12:00:00",
            "label": "crack",
            "description": "found a crack",
        },
    )
    event_id = create_response.json()["id"]

    # Now, fetch the event
    get_response = client.get(f"/events/{event_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == event_id
    assert data["label"] == "crack"

def test_delete_event(test_app):
    """Test deleting an event"""
    client = test_app

    # First, create an event
    create_response = client.post(
        "/events",
        json={
            "ts": "2026-01-21T12:00:00",
            "label": "rust",
        },
    )
    event_id = create_response.json()["id"]

    # Now, delete the event
    delete_response = client.delete(f"/events/{event_id}")
    assert delete_response.status_code == 204

    # Verify the event is gone
    get_response = client.get(f"/events/{event_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_event(test_app):
    """Test fetching an event that doesn't exist returns 404"""
    client = test_app

    # Attempt to fetch a non-existent event
    get_response = client.get("/events/999")
    assert get_response.status_code == 404

def test_delete_nonexistent_event(test_app):
    """Test deleting an event that doesn't exist returns 404"""
    client = test_app

    # Attempt to delete a non-existent event
    delete_response = client.delete("/events/999")
    assert delete_response.status_code == 404
