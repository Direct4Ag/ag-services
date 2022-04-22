from fastapi.testclient import TestClient
import json

from app.main import app

client = TestClient(app)


def test_fields():
    # field = {
    #         "name": "test",
    #         "lat": "test",
    #         "lon": "test",
    #         "crop": "test"
    # }
    # response = client.post(f"/fields/", json=field)
    # gid = response.json()["gid"]
    # assert response.status_code == 200
    #
    # response = client.get(f"/fields/{gid}")
    # assert response.status_code == 200
    #
    # response = client.delete(f"/fields/{gid}")
    # assert response.status_code == 200
    response = client.get(f"/fields/1")
    assert response.status_code == 404
