# Stage 0: API Integration & Data Processing Assessment

A FastAPI backend that calls the Genderize API to determine the likely gender of a given name, returning a structured response with processed confidence data.

## Features
- Validates query parameters
- Integrates with external API (api.genderize.io)
- Computes confidence variables
- Handles edge cases and upstream errors
- Supports full CORS functionality

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/C3Techie/genderize-classification-api.git
   cd genderize-classification-api
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate # on Windows
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Test the endpoint:**
   Open your browser or use Postman/curl:
   ```bash
   curl http://127.0.0.1:8000/api/classify?name=john
   ```

## Endpoint Description

### `GET /api/classify`
**Query Parameters:**
- `name` (string, required): The name to classify.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```
