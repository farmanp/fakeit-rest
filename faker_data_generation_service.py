import json
import os
from typing import Any, Dict, List, Union

from faker import Faker

fake = Faker()

FIELD_GENERATORS = {
    "string": lambda _: fake.first_name(),
    "integer": lambda _: fake.random_int(min=1, max=100),
    "email": lambda _: fake.email(),
    "street": lambda _: fake.street_name(),
    "city": lambda _: fake.city(),
    "zipcode": lambda _: fake.zipcode(),
}


def load_schema(file_path: str) -> Dict[str, Any]:
    """
    Load a schema from a file.

    This function reads a schema from a file and returns its contents as a dictionary.
    It supports JSON (.json) file format.

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
        raise ValueError("Unsupported file format. Please provide a .json file.")


def generate_fake_data(schema: Dict[str, Any], num_records: int) -> List[Dict[str, Any]]:
    """
    Generate fake data based on the given schema.

    Args:
        schema (Dict[str, Any]): The schema definition as a dictionary.
        num_records (int): The number of records to generate.

    Returns:
        List[Dict[str, Any]]: A list of generated records.
    """
    return [generate_record(schema["fields"]) for _ in range(num_records)]


def generate_record(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a record based on schema fields.

    Args:
        fields (List[Dict[str, Any]]): The schema fields.

    Returns:
        Dict[str, Any]: A generated record.
    """
    record: Dict[str, Any] = {}
    for field in fields:
        field_name = field.get("name")
        field_type = field.get("type")
        children: Union[None, List[Dict[str, Any]]] = field.get("children")

        if field_type in FIELD_GENERATORS:
            record[field_name] = FIELD_GENERATORS[field_type](field_name)
        elif field_type == "object" and children:
            record[field_name] = generate_record(children)
        else:
            record[field_name] = None  # Default value for unsupported types

    return record
