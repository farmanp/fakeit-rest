# import concurrent.futures
# import datetime
# from typing import Any, AsyncGenerator, Dict, List

# # Helper function to serialize data for JSON
# class EnhancedJSONEncoder(json.JSONEncoder):
#     def default(self, o: Any) -> Any:
#         if isinstance(o, (datetime.date, datetime.datetime)):
#             return o.isoformat()
#         return super().default(o)


# # Helper function to write large data to a file
# def write_large_data_to_file(data, output_file, task_id):
#     try:
#         with open(output_file, "w", encoding="utf-8") as f:
#             json.dump(data, f, cls=EnhancedJSONEncoder)
#         task_status[task_id] = "completed"
#         print(f"Data successfully written to {output_file}")
#     except (OSError, IOError) as e:
#         task_status[task_id] = "failed"
#         print(f"Failed to write data to {output_file}: {e}")
#     finally:
#         background_task_semaphore.release()


# # Helper function to generate data in batches
# def generate_data_in_batches(schema: Dict[str, Any], num_records: int, batch_size: int = 1000) -> List[Dict]:
#     data: List[Dict] = []
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = []
#         for _ in range(0, num_records, batch_size):
#             records_to_generate = min(batch_size, num_records - len(data))
#             futures.append(executor.submit(generate_fake_data, schema, records_to_generate))
#         for future in concurrent.futures.as_completed(futures):
#             data.extend(future.result())
#     return data
