from fastapi import FastAPI, Request, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import httpx
from datetime import datetime, timezone
import logging

app = FastAPI(title="Genderize Classification API", version="1.0.0")

# Enable CORS (allow all origins, headers, methods)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# Override the default RequestValidationError to return the specific error structure
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # This captures validation constraints like empty or missing query parameter string
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "error", "message": "Missing or empty name parameter"}
    )

# Override HTTP exception to force the format globally
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail}
    )

# Fallback generic exception handler (e.g. 500 upstreams)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Internal server error"}
    )

@app.get("/api/classify")
async def classify_name(name: str = Query(..., min_length=1)):
    """
    Classify a given name based on the Genderize API.
    """
    url = f"https://api.genderize.io/?name={name}"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        # 500/502 upstream errors
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream API error"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reach external API"
        )

    # 1. Edge Case Checking
    # If the response comes back with gender: null or count: 0 
    if not data.get("gender") or data.get("count", 0) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, # Or consider returning 422 if specified
            content={
                "status": "error", 
                "message": "No prediction available for the provided name"
            }
        )

    # 2. Extract Data
    gender = data.get("gender")
    probability = data.get("probability", 0.0)
    sample_size = data.get("count", 0)

    # 3. Compute confident status
    is_confident = (probability >= 0.7) and (sample_size >= 100)
    
    # 4. Generate processed_at timestamp in UTC, ISO 8601
    processed_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 5. Build Final Response
    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }
