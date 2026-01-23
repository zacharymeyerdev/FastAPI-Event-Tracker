from fastapi.testclient import TestClient
import pytest
import os
import tempfile
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

def test_health_check(test_app):
    """Test /health endpoint returns 200 and correct status"""
    client = test_app
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}