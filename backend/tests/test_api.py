import os
import sys
import pytest

# Add backend directory to path so pytest can import app from anywhere
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Verify the root / endpoint returns running message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Flask REST API + MongoDB is running" in response.get_data(as_text=True)


def test_ping_db(client):
    """Verify the /api/ping-db endpoint connects to MongoDB Atlas and returns 200."""
    response = client.get("/api/ping-db")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True
    assert "MongoDB Atlas is reachable and connected!" in data["message"]


def test_health_check(client):
    """Verify the /api/health endpoint returns 200 and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_get_cds_stub(client):
    """Verify the GET /api/cds stub returns catalog items."""
    response = client.get("/api/cds")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0


def test_create_order_stub(client):
    """Verify the POST /api/orders stub processes an order payload."""
    payload = {"items": [{"id": 1, "title": "Dark Side of the Moon", "price": 14.99, "quantity": 2}]}
    response = client.post("/api/orders", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["order"]["total"] == 29.98


def test_chat_stub(client):
    """Verify the POST /api/chat stub returns an assistant reply."""
    response = client.post("/api/chat", json={"message": "Recommend a rock album"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "reply" in data
