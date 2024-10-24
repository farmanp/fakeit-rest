import json

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


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
