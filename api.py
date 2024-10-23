from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from faker_data_generation_service import generate_fake_data
import yaml
import json
import concurrent.futures
import datetime

app = FastAPI()

# Define a Pydantic model for handling incoming JSON schema input

class SchemaInput(BaseModel):
    fields: List[dict]

# Helper function to serialize data for JSON
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

# Helper function to write large data to a file
def write_large_data_to_file(data, output_file="output.json"):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)

# Helper function to generate data in batches
def generate_data_in_batches(schema, num_records, batch_size=1000):
    data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(0, num_records, batch_size):
            records_to_generate = min(batch_size, num_records - len(data))
            futures.append(executor.submit(generate_fake_data, 
                                           schema, 
                                           records_to_generate))
        for future in concurrent.futures.as_completed(futures):
            data.extend(future.result())
    return data

# Endpoint for generating a single record of fake data


@app.post("/generate-single")
async def generate_single(schema: SchemaInput):
    try:
        # Convert SchemaInput to dict and generate one record
        schema_dict = schema.dict()
        data = generate_fake_data(schema_dict, num_records=1)
        return {"data": data[0]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Endpoint for generating batch fake data
@app.post("/generate-batch")
async def generate_batch(schema: SchemaInput, num_records: Optional[int] = 10,
                         background_tasks: BackgroundTasks = None):
    try:
        # Convert SchemaInput to dict and generate records
        schema_dict = schema.dict()
        if num_records > 1000:
            # For large number of records, generate data in the background and write to a file
            output_file = "output_large.json"
            background_tasks.add_task(write_large_data_to_file,
                                      generate_data_in_batches(schema_dict,
                                                               num_records),
                                      output_file)
            return {"message": f"Data generation for {num_records} records is in progress. "
                    f"The output will be saved to '{output_file}'."}
            # For smaller number of records, generate data and return immediately
        data = generate_data_in_batches(schema_dict, num_records)
        return {"data": data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# Endpoint for generating data by uploading a schema file
@app.post("/generate-from-file")
async def generate_from_file(file: UploadFile = File(...), 
                             num_records: Optional[int] = 10, 
                             background_tasks: BackgroundTasks = None):
    try:
        # Read the file and determine its type (YAML or JSON)
        content = await file.read()
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension in ['yaml', 'yml']:
            schema = yaml.safe_load(content)
        elif file_extension == 'json':
            schema = json.loads(content)
        else:
            raise ValueError("Unsupported file format. Please provide a .yaml, .yml, or .json file.")
        
        # Generate the fake data
        if num_records > 1000:
            # For large number of records, generate data in the background and write to a file
            output_file = "output_large.json"
            background_tasks.add_task(write_large_data_to_file,
                                      generate_data_in_batches(schema,
                                                               num_records),
                                      output_file)
            return {"message": f"Data generation for {num_records} records is in progress. "
                    f"The output will be saved to '{output_file}'."}
        # For smaller number of records, generate data and return immediately
        data = generate_data_in_batches(schema, num_records)
        return {"data": data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e