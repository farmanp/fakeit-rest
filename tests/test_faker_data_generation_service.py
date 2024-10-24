import json

import pytest

from faker_data_generation_service import generate_fake_data, load_schema


def test_load_schema_json(tmp_path):
    # Create a temporary JSON schema file
    schema_content = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"},
            {"name": "email", "type": "email"},
        ]
    }
    schema_file = tmp_path / "schema.json"
    schema_file.write_text(json.dumps(schema_content))

    # Load the schema using the function
    loaded_schema = load_schema(str(schema_file))

    # Assert the loaded schema matches the original content
    assert loaded_schema == schema_content


def test_load_schema_unsupported_format(tmp_path):
    # Create a temporary unsupported schema file
    schema_file = tmp_path / "schema.txt"
    schema_file.write_text("unsupported content")

    # Assert that loading an unsupported schema raises a ValueError
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_schema(str(schema_file))


def test_generate_fake_data():
    # Define a schema
    schema = {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "integer"},
            {"name": "email", "type": "email"},
            {
                "name": "address",
                "type": "object",
                "children": [
                    {"name": "street", "type": "string"},
                    {"name": "city", "type": "string"},
                    {"name": "zipcode", "type": "string"},
                ],
            },
        ]
    }

    # Generate fake data
    num_records = 5
    fake_data = generate_fake_data(schema, num_records)

    # Assert the number of generated records is correct
    assert len(fake_data) == num_records

    # Assert each record has the correct fields and types
    for record in fake_data:
        assert "name" in record and isinstance(record["name"], str)
        assert "age" in record and isinstance(record["age"], int)
        assert "email" in record and isinstance(record["email"], str)
        assert "address" in record and isinstance(record["address"], dict)
        assert "street" in record["address"] and isinstance(record["address"]["street"], str)
        assert "city" in record["address"] and isinstance(record["address"]["city"], str)
        assert "zipcode" in record["address"] and isinstance(record["address"]["zipcode"], str)
