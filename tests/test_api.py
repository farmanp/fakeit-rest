import pytest
import json
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)
# Test single record generation endpoint
def test_generate_single():
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"}
        ]
    }
    response = client.post("/generate-single", json=schema)
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], dict)
    assert "name" in response.json()["data"]
    assert "age" in response.json()["data"]
    assert response.json()["data"]["name"] is not None
    assert response.json()["data"]["age"] is not None

# Test batch generation endpoint
def test_generate_batch():
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"}
        ]
    }
    response = client.post("/generate-batch", json=schema, params={"num_records": 5})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 5
    for record in response.json()["data"]:
        assert "name" in record
        assert "age" in record
        assert record["name"] is not None
        assert record["age"] is not None

# Test large batch generation endpoint with background task
def test_generate_large_batch():
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"}
        ]
    }
    response = client.post("/generate-batch", json=schema, params={"num_records": 1500})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "output_large.json" in response.json()["message"]

# Test generate from file endpoint with JSON schema
def test_generate_from_file_json():
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"}
        ]
    }
    response = client.post("/generate-from-file", files={"file": ("schema.json", json.dumps(schema), "application/json")}, params={"num_records": 5})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 5
    for record in response.json()["data"]:
        assert "name" in record
        assert "age" in record
        assert record["name"] is not None
        assert record["age"] is not None

# Test generate from file endpoint with unsupported file type
def test_generate_from_file_unsupported():
    response = client.post("/generate-from-file", files={"file": ("schema.txt", "unsupported content", "text/plain")})
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "Unsupported file format" in response.json()["detail"]

# Test generate from file endpoint with YAML schema
def test_generate_from_file_yaml():
    schema = """
    fields:
      - name: name
        type: string
      - name: age
        type: integer
    """
    response = client.post("/generate-from-file", files={"file": ("schema.yaml", schema, "application/x-yaml")}, params={"num_records": 5})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 5
    for record in response.json()["data"]:
        assert "name" in record
        assert "age" in record
        assert record["name"] is not None
        assert record["age"] is not None
