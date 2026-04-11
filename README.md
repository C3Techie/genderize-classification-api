# Genderize Classification API - HNG Stage 0

A professional FastAPI backend that integrates with the Genderize API to determine the likely gender of a given name. This project follows strict validation and response formatting rules as required by the HNG Stage 0 Backend Task.

## Features
- **Strict Validation**: Distinct handling for 400 (missing/empty) and 422 (invalid type) errors.
- **Data Enrichment**: Calculates confidence status based on probability and sample size.
- **CORS Enabled**: Fully compliant with `Access-Control-Allow-Origin: *`.
- **Fast Performance**: Async implementation ensures sub-500ms responses (excluding upstream latency).

## Tech Stack
- Python 3.10+
- FastAPI (Web framework)
- httpx (Async HTTP client)
- Uvicorn (ASGI server)

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/C3Techie/genderize-classification-api.git
   cd genderize-classification-api
   ```

2. **Setup virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## Endpoint Description

### `GET /api/classify?name={name}`

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
    "processed_at": "2026-04-11T01:00:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing or empty name parameter.
- `422 Unprocessable Entity`: `name` is not a single string or no prediction available.

## Deployment

This API is ready for deployment on platforms like **Vercel**, **Railway**, or **Heroku**.

### Vercel Deployment
1. Install Vercel CLI: `npm install -g vercel`
2. Run `vercel` in the root directory.
3. Vercel will automatically detect the FastAPI app.

## Testing
Run the automated test script to verify all requirements:
```bash
python test_api.py
```
