# faker_data_generation.py
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Union

from faker import Faker

# Initialize Faker instance
fake = Faker()


def load_schema(file_path: str) -> Dict[str, Any]:
    """
    Load a schema from a file.

    This function reads a schema from a file and returns its contents as a dictionary.
    It supports YAML (.yaml, .yml) and JSON (.json) file formats.

    Args:
        file_path (str): The path to the schema file.

    Returns:
        dict: The contents of the schema file.

    Raises:
        ValueError: If the file format is not supported.
    """
    file_extension = os.path.splitext(file_path)[-1].lower()
    with open(file_path, "r", encoding="utf-8") as file:
        if file_extension == ".json":
            return json.load(file)
        raise ValueError("Unsupported file format. Please provide a .yaml, .yml, or .json file.")


def generate_fake_data(schema: Dict[str, Any], num_records: int) -> List[Dict[str, Any]]:
    """
    Generate fake data based on the given schema.

    Args:
        schema (Dict[str, Any]): The schema definition as a dictionary.
        num_records (int): The number of records to generate.

    Returns:
        List[Dict[str, Any]]: A list of generated records.
    """
    data = []

    def generate_record(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        record: Dict[str, Any] = {}
        for field in fields:
            field_name = field.get("name")
            field_type = field.get("type")
            children: Union[None, List[Dict[str, Any]]] = field.get("children")

            # Generate value based on field type
            if field_type == "string":
                record[field_name] = generate_specific_string(field_name)
            elif field_type == "integer":
                record[field_name] = fake.random_int(min=1, max=100)
            elif field_type == "email":
                record[field_name] = fake.email()
            elif field_type == "object" and children:
                # Recursively generate nested fields if type is object
                record[field_name] = generate_record(children)
            else:
                record[field_name] = None  # Default value for unsupported types
        return record

    def generate_specific_string(field_name: str) -> str:
        field_generators = {
            "street": fake.street_name,
            "city": fake.city,
            "zipcode": fake.zipcode,
        }
        return field_generators.get(field_name, fake.name)()

    for _ in range(num_records):
        data.append(generate_record(schema["fields"]))

    return data
