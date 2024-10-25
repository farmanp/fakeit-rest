import concurrent.futures
import datetime
import json
import os
import uuid
from threading import Semaphore
from typing import Any, AsyncGenerator, Dict, List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import StreamingResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from faker_data_generation_service import generate_fake_data
from models.models import SchemaInput

# Create an instance of APIRouter
rest_router = APIRouter()

# Create a limiter instance for rate limiting
limiter = Limiter(key_func=get_remote_address)

# Middleware setup should be done in the main app, not in the router
# Semaphore to limit the number of concurrent background tasks
MAX_CONCURRENT_TASKS = 5
background_task_semaphore = Semaphore(MAX_CONCURRENT_TASKS)

# Store background task status
task_status: Dict[str, str] = {}


# Helper function to serialize data for JSON
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super().default(o)


# Helper function to write large data to a file
def write_large_data_to_file(data, output_file, task_id):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=EnhancedJSONEncoder)
        task_status[task_id] = "completed"
        print(f"Data successfully written to {output_file}")
    except (OSError, IOError) as e:
        task_status[task_id] = "failed"
        print(f"Failed to write data to {output_file}: {e}")
    finally:
        background_task_semaphore.release()


# Helper function to generate data in batches
def generate_data_in_batches(schema: Dict[str, Any], num_records: int, batch_size: int = 1000) -> List[Dict]:
    data: List[Dict] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(0, num_records, batch_size):
            records_to_generate = min(batch_size, num_records - len(data))
            futures.append(executor.submit(generate_fake_data, schema, records_to_generate))
        for future in concurrent.futures.as_completed(futures):
            data.extend(future.result())
    return data


# Stream data in smaller chunks
async def stream_data_in_batches(schema_dict: Dict[str, Any], num_records: int) -> AsyncGenerator[bytes, None]:
    chunk_size = 100  # Define the number of records to generate per chunk
    generated_records = 0

    while generated_records < num_records:
        batch_size = min(chunk_size, num_records - generated_records)
        data_batch = generate_data_in_batches(schema_dict, batch_size)
        yield json.dumps(data_batch, cls=EnhancedJSONEncoder).encode("utf-8")
        generated_records += batch_size


# Health check endpoint
@rest_router.get("/api/health")
async def health_check():
    return {"status": "healthy"}


# Endpoint for generating single fake data record
@rest_router.post("/generate-single", response_model=None)
@limiter.limit("5/minute")
async def generate_single(request: Request) -> Dict[str, Any]:
    try:
        # Parse incoming JSON request body
        schema = await request.json()  # Parse JSON data from request body
        if isinstance(schema, str):
            schema = json.loads(schema)

        data = generate_fake_data(schema, 1)
        return {"data": data[0]}
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error


# Endpoint for generating batch fake data
@rest_router.post("/generate-batch", response_model=None)
@limiter.limit("10/minute")
async def generate_batch(
    request: Request, schema: SchemaInput, background_tasks: BackgroundTasks, num_records: int = 10
) -> StreamingResponse:
    try:
        # Convert SchemaInput to dict and generate records
        schema_dict = schema.dict()
        if num_records > 1000:
            if not background_task_semaphore.acquire(blocking=False):
                raise HTTPException(
                    status_code=429, detail="Too many concurrent background tasks. Please try again later."
                )

            task_id = str(uuid.uuid4())
            output_file = f"output/output_{task_id}.json"
            if not os.path.exists("output"):
                os.makedirs("output")
            task_status[task_id] = "in_progress"
            background_tasks.add_task(
                write_large_data_to_file, generate_data_in_batches(schema_dict, num_records), output_file, task_id
            )
            return StreamingResponse(
                iter(
                    [
                        json.dumps(
                            {
                                "message": f"Data generation for {num_records} records will be saved to '{output_file}'.",
                                "task_id": task_id,
                            }
                        )
                    ]
                ),
                media_type="application/json",
            )

        # Stream data for smaller number of records
        return StreamingResponse(stream_data_in_batches(schema_dict, num_records), media_type="application/json")
    except ValueError as value_error:
        raise HTTPException(status_code=400, detail=str(value_error)) from value_error


# Ensure the router is exported
__all__ = ["rest_router"]
