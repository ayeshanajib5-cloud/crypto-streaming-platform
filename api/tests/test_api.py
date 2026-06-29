import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "api"))

import main
from fastapi.testclient import TestClient


client = TestClient(main.app)


class DummyConnection:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class DummyRedis:
    def ping(self):
        return True

    def get(self, key):
        return None

    def setex(self, key, ttl, value):
        return True


def test_root_endpoint_returns_service_metadata():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Real-Time Crypto Streaming Analytics API",
        "status": "running",
    }


def test_health_endpoint_reports_dependencies(monkeypatch):
    monkeypatch.setattr(main, "get_connection", lambda: DummyConnection())
    monkeypatch.setattr(main, "redis_client", DummyRedis())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
    }


def test_openapi_schema_contains_core_routes():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert "/prices/latest" in paths
    assert "/analytics/top-movers" in paths
    assert "/analytics/average-price/{symbol}" in paths


def test_metrics_endpoint_returns_prometheus_payload():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "api_requests_total" in response.text
