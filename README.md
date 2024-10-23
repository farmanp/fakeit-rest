# Faker Data Generation REST API

## Overview

This project is a Python-based API for generating fake data using **FastAPI** and **Faker**. The API provides endpoints to generate single or batch records of fake data. This tool is perfect for testing, mocking data, or learning purposes, and can generate data such as names, emails, addresses, and more.

**Note:** This project is strictly intended for **simulation and testing purposes** only. It should not be used for fraudulent activities or any form of malicious use.

### Key Features:
- REST API endpoints for generating single or multiple records of fake data.
- Supports schema definitions in both YAML and JSON formats.

## File Structure

```
.
├── api.py                # Contains REST API endpoints
├── app.py                # Entry point for FastAPI including both REST and WebSocket routes
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
   - **Response**: Returns multiple records of fake data.

3. **Generate Data from File**
   - **Endpoint**: `/generate-from-file`
   - **Method**: `POST`
   - **Form Data**: Upload a YAML or JSON file containing the schema.
   - **Response**: Returns generated fake data based on the uploaded schema.

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
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or suggestions, please open an issue or reach out to me at [farman.pirz@gmail.com].
