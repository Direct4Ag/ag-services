from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_fields():
    response = client.get(f"/fields/1")
    assert response.status_code == 404
