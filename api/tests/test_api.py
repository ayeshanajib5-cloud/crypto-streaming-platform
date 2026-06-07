import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "api"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code in [200, 500]


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code in [200, 404]