import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_healthchecker():
    response = client.get("/healthchecker/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}