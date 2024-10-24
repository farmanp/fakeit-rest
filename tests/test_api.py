import json

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


# Test single record generation endpoint
def test_generate_single() -> None:
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"},
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
def test_generate_batch() -> None:
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"},
        ]
    }
    schema_dict = json.loads(json.dumps(schema))
    response = client.post("/generate-batch", json=schema_dict, params={"num_records": 5})
    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) == 5
    for record in response.json()["data"]:
        assert "name" in record
        assert "age" in record
        assert record["name"] is not None
        assert record["age"] is not None
