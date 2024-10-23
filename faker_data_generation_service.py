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
                       Each field definition is a dictionary where the key is the field name and the value is the Faker method name.
        num_records (int, optional): The number of records to generate. Defaults to 10.
        
    Returns:
        list: A list of dictionaries, each representing a record with generated fake data.
    """
    
    def generate_value(field):
        """Get Faker method or recursively process nested fields."""
        if isinstance(field, dict):
            return {key: generate_value(value) for key, value in field.items()}
        faker_method = getattr(fake, field, None)
        return faker_method() if faker_method else None

    return [
        {key: generate_value(value) for field in schema['fields'] for key, value in field.items()}
        for _ in range(num_records)
    ]