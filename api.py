import concurrent.futures
import datetime
import json
import os
from typing import Any, Dict, List

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel

from faker_data_generation_service import generate_fake_data

app = FastAPI()


# Define a Pydantic model for handling incoming JSON schema input
class SchemaInput(BaseModel):
    fields: List[Dict[str, Any]]


# Helper function to serialize data for JSON
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super().default(o)


# Helper function to write large data to a file
def write_large_data_to_file(data: List[dict], output_file: str = "output.json") -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, cls=EnhancedJSONEncoder)


# Helper function to generate data in batches
def generate_data_in_batches(schema: dict[str, Any], num_records: int, batch_size: int = 1000) -> List[dict]:
    data: List[dict] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(0, num_records, batch_size):
            records_to_generate = min(batch_size, num_records - len(data))
            futures.append(executor.submit(generate_fake_data, schema, records_to_generate))
        for future in concurrent.futures.as_completed(futures):
            data.extend(future.result())
    return data


# Endpoint for generating a single record of fake data
@app.post("/generate-single", response_model=None)
async def generate_single(schema: SchemaInput) -> dict[str, Any]:
    try:
        # Convert SchemaInput to dict and generate one record
        schema_dict: dict[str, Any] = schema.model_dump()
        data = generate_fake_data(schema_dict, 1)
        return {"data": data[0]}
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error


# Endpoint for generating batch fake data
@app.post("/generate-batch", response_model=None)
async def generate_batch(
    schema: SchemaInput,
    num_records: int = 10,
) -> dict[str, Any]:
    try:
        # Convert SchemaInput to dict and generate records
        schema_dict = schema.dict()
        if num_records > 1000:
            output_file = "output/output_large.json"
            if not os.path.exists("output"):
                os.makedirs("output")
            background_tasks = BackgroundTasks()
            background_tasks.add_task(
                write_large_data_to_file,
                generate_data_in_batches(schema_dict, num_records),
                output_file,
            )
            return {"message": (f"Data generation for {num_records} records " f"will be saved to '{output_file}'.")}

        # For smaller number of records, generate data and return immediately
        data = generate_data_in_batches(schema_dict, num_records)
        return {"data": data}
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error
