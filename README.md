# Faker Data Generation WebSocket & REST API

## Overview

This project is a Python-based API for generating fake data using **FastAPI** and **Faker**. The API provides both REST and WebSocket endpoints to generate single or batch records of fake data. This tool is perfect for testing, mocking data, or learning purposes, and can generate data such as names, emails, addresses, and more.

**Note:** This project is strictly intended for **simulation and testing purposes** only. It should not be used for fraudulent activities or any form of malicious use.

### Key Features:
- REST API endpoints for generating single or multiple records of fake data.
- WebSocket support for simulating real-time data generation.
- Supports schema definitions in both YAML and JSON formats.
- Rate limiting and concurrency control for handling requests.
- Pagination support for large data responses.

## File Structure

```
.
├── api.py                # Contains REST API endpoints
├── app.py                # Entry point for FastAPI including both REST and WebSocket routes
├── websocket_client.py   # WebSocket client for simulating real-time data generation
├── faker_data_generator_service.py  # Utility functions for schema loading and data generation
├── pyproject.toml        # Python dependencies for the project
└── README.md             # This README file
```

## Getting Started

### Prerequisites

To run this project, you need to have **Python 3.7+** installed. Additionally, install the required dependencies listed in the `requirements.txt` file.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/faker-data-generation-api.git
   cd faker-data-generation-api
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**:
   - To run the FastAPI server, execute:
   ```bash
   uvicorn app:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000/`.

## Usage

### REST API Endpoints

1. **Generate Single Record**
   - **Endpoint**: `/generate-single`
   - **Method**: `POST`
   - **Body** (example):
     ```json
     {
       "fields": [
         {"name": "name"},
         {"email": "email"},
         {"address": {
           "street": "street_address",
           "city": "city",
           "state": "state",
           "zipcode": "postcode"
         }}
       ]
     }
     ```
   - **Response**: Returns a single record based on the provided schema.

2. **Generate Batch Records**
   - **Endpoint**: `/generate-batch`
   - **Method**: `POST`
   - **Body** (same as `/generate-single`)
   - **Query Parameter**: `num_records` (Optional)
   - **Response**: Returns multiple records of fake data. If `num_records` is greater than 1000, the data will be saved to a file and a `task_id` will be provided to check the status.

3. **Generate Data from File**
   - **Endpoint**: `/generate-from-file`
   - **Method**: `POST`
   - **Form Data**: Upload a JSON file containing the schema.
   - **Response**: Returns generated fake data based on the uploaded schema. If `num_records` is greater than 1000, the data will be saved to a file and a `task_id` will be provided to check the status.

4. **Check Background Task Status**
   - **Endpoint**: `/task-status/{task_id}`
   - **Method**: `GET`
   - **Path Parameter**: `task_id` (Required)
   - **Response**: Returns the status of the background task (e.g., `in_progress`, `completed`, `failed`).

5. **Generate Paginated Data**
   - **Endpoint**: `/generate-paginated`
   - **Method**: `GET`
   - **Query Parameters**:
     - `page` (Optional, default: `1`): Page number to fetch.
     - `page_size` (Optional, default: `100`): Number of records per page.
   - **Response**: Returns paginated data for the given schema.

### WebSocket Simulation for Real-Time Data

You can also simulate real-time data generation using WebSockets.

1. **Start the Server**:
   ```bash
   poetry run hypercorn app:app --reload
   ```

2. **Run the WebSocket Client**:
   - The `websocket_client.py` script simulates a client connecting to the WebSocket and sending commands to generate data.
   ```bash
   poetry run python websocket_client.py
   ```
   - The client will connect to the WebSocket server and request to generate data every few seconds, simulating real-time behavior.

## Schema Examples

### JSON Schema (`schema.json`)
```json
{
  "fields": [
    { "name": "name" },
    { "email": "email" },
    { "address": {
        "street": "street_address",
        "city": "city",
        "state": "state",
        "zipcode": "postcode"
      }
    }
  ]
}
```

## Development

If you want to modify the project or add new features, consider using a virtual environment to manage your dependencies:

```bash
poetry install
poetry run uvicorn app:app --reload
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue or reach out to me at [farman.pirz@gmail.com].
