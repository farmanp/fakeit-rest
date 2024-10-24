# faker_data_generation.py

import yaml
import json
from faker import Faker
import os

# Initialize Faker instance
fake = Faker()

def load_schema(file_path):
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
    with open(file_path, 'r', encoding='utf-8') as file:
        if file_extension in ['.yaml', '.yml']:
            return yaml.safe_load(file)
        if file_extension == '.json':
            return json.load(file)
        raise ValueError("Unsupported file format. Please provide a .yaml, .yml, or .json file.")

    
def generate_fake_data(schema, num_records=10):
    """
    Generate fake data based on a given schema.

    Args:
        schema (dict): A dictionary defining the structure of the data to be generated.
                       The schema should have a 'fields' key containing a list of field definitions.
                       Each field definition is a dictionary with keys 'name' and 'type'.
        num_records (int, optional): The number of records to generate. Defaults to 10.

    Returns:
        list: A list of dictionaries, each representing a record with generated fake data.
    """

    # Map generic field types to Faker methods
    faker_type_map = {
        "string": fake.name,
        "integer": lambda: fake.random_int(min=0, max=100),
        "email": fake.email,
        "address": fake.address,
        # Add more mappings as needed
    }

    def generate_value(field_type):
        """Get Faker method based on the type provided in the schema."""
        faker_method = faker_type_map.get(field_type)
        if callable(faker_method):
            return faker_method()
        else:
            print(f"Warning: '{field_type}' is not a valid type. Returning None.")
            return None

    data = []
    for _ in range(num_records):
        record = {}
        for field in schema['fields']:
            field_name = field.get('name')
            field_type = field.get('type')
            if field_name and field_type:
                record[field_name] = generate_value(field_type)
            else:
                record[field_name] = None
        data.append(record)

    return data
