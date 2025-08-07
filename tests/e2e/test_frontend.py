from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Hexagonal Architecture" in response.text
    assert "API Status" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
