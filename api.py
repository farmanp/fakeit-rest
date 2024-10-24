import concurrent.futures
import datetime
import json
import os
from typing import Any, AsyncGenerator, List

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from faker_data_generation_service import generate_fake_data
from models.models import SchemaInput

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded"),
)
app.add_middleware(SlowAPIMiddleware)


# Helper function to serialize data for JSON
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super().default(o)


# Helper function to write large data to a file
def write_large_data_to_file(data, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=EnhancedJSONEncoder)
        print(f"Data successfully written to {output_file}")
    except (OSError, IOError) as e:
        print(f"Failed to write data to {output_file}: {e}")


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


# Stream data in smaller chunks
async def stream_data_in_batches(schema_dict: dict[str, Any], num_records: int) -> AsyncGenerator[bytes, None]:
    chunk_size = 100  # Define the number of records to generate per chunk
    generated_records = 0

    while generated_records < num_records:
        batch_size = min(chunk_size, num_records - generated_records)
        data_batch = generate_data_in_batches(schema_dict, batch_size)
        yield json.dumps(data_batch, cls=EnhancedJSONEncoder).encode("utf-8")
        generated_records += batch_size


# Endpoint for generating a single record of fake data
@app.post("/generate-single", response_model=None)
@limiter.limit("5/minute")
async def generate_single(request: Request, schema: SchemaInput) -> dict[str, Any]:
    try:
        # Convert SchemaInput to dict and generate one record
        schema_dict: dict[str, Any] = schema.model_dump_json()
        data = generate_fake_data(schema_dict, 1)
        return {"data": data[0]}
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error


# Endpoint for generating batch fake data
@app.post("/generate-batch", response_model=None)
@limiter.limit("10/minute")
async def generate_batch(
    request: Request, schema: SchemaInput, background_tasks: BackgroundTasks, num_records: int = 10
) -> StreamingResponse:
    try:
        # Convert SchemaInput to dict and generate records
        schema_dict = schema.dict()
        if num_records > 1000:
            output_file = "output/output_large.json"
            if not os.path.exists("output"):
                os.makedirs("output")
            background_tasks.add_task(
                write_large_data_to_file,
                generate_data_in_batches(schema_dict, num_records),
                output_file,
            )
            return {"message": f"Data generation for {num_records} records will be saved to '{output_file}'."}

        # Stream data for smaller number of records
        return StreamingResponse(stream_data_in_batches(schema_dict, num_records), media_type="application/json")
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error


# Endpoint for generating batch fake data from file
@app.post("/generate-from-file", response_model=None)
@limiter.limit("10/minute")
async def generate_from_file(
    request: Request, file: bytes, background_tasks: BackgroundTasks, num_records: int = 10
) -> StreamingResponse:
    try:
        # Assume the file is JSON formatted
        schema_dict = json.loads(file)
        if num_records > 1000:
            output_file = "output/output_large.json"
            if not os.path.exists("output"):
                os.makedirs("output")
            background_tasks.add_task(
                write_large_data_to_file,
                generate_data_in_batches(schema_dict, num_records),
                output_file,
            )
            return {"message": f"Data generation for {num_records} records will be saved to '{output_file}'."}

        # Stream data for smaller number of records
        return StreamingResponse(stream_data_in_batches(schema_dict, num_records), media_type="application/json")
    except (ValueError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
