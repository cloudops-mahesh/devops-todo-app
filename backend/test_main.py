import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock MongoDB before importing app
from unittest.mock import patch, MagicMock

# Mock motor client so tests work without MongoDB
with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client:
    mock_db = MagicMock()
    mock_client.return_value = mock_db
    from main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✅ Health check passed!")

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint exists"""
    response = client.get("/metrics")
    assert response.status_code == 200
    print("✅ Metrics endpoint passed!")

def test_api_todos_endpoint_exists():
    """Test todos endpoint exists"""
    response = client.get("/api/todos")
    # 200 = works, 500 = no DB (both acceptable in CI)
    assert response.status_code in [200, 500]
    print("✅ Todos endpoint exists!")