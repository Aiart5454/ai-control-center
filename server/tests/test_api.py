from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_system_shape() -> None:
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    body = response.json()
    assert "hostname" in body
    assert "memory" in body
    assert "temperatures" in body
    assert "network" in body
    assert "gpus" in body
    assert body["network"]["external_ip"] is None


def test_status_shape() -> None:
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "idle"
    assert "system" in body
    assert "services" in body
