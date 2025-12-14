"""
My Personal Map - Main Application Entry Point

FastAPI backend per la gestione di segnaposti geografici personalizzati.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="My Personal Map API",
    description="API REST per gestione segnaposti geografici personalizzati",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Models ====================

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    message: str


class Coordinates(BaseModel):
    """Geographical coordinates"""
    latitude: float
    longitude: float


class MarkerCreate(BaseModel):
    """Marker creation request"""
    name: str
    coordinates: Coordinates
    description: Optional[str] = None
    address: Optional[str] = None
    label_ids: Optional[List[int]] = []
    is_favorite: bool = False


class MarkerResponse(BaseModel):
    """Marker response"""
    id: int
    name: str
    coordinates: Coordinates
    description: Optional[str]
    address: Optional[str]
    labels: List[str]
    is_favorite: bool
    created_at: str


# ==================== Routes ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to My Personal Map API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint

    Returns the status of the application and its version.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="My Personal Map API is running"
    )


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def api_health_check():
    """
    API v1 health check endpoint

    Returns the status of the API v1 and its version.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="API v1 is operational"
    )


# ==================== Markers Endpoints (Placeholder) ====================

@app.get("/api/v1/markers", tags=["Markers"])
async def get_markers(
    label_ids: Optional[str] = None,
    search: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Get list of markers with optional filters

    - **label_ids**: Comma-separated label IDs to filter
    - **search**: Search text in name/description
    - **is_favorite**: Filter by favorite status
    - **limit**: Maximum number of results
    - **offset**: Offset for pagination
    """
    # TODO: Implement database query
    return {
        "total": 0,
        "limit": limit,
        "offset": offset,
        "markers": []
    }


@app.get("/api/v1/markers/{marker_id}", response_model=MarkerResponse, tags=["Markers"])
async def get_marker(marker_id: int):
    """
    Get single marker by ID

    - **marker_id**: Marker ID to retrieve
    """
    # TODO: Implement database query
    raise HTTPException(status_code=404, detail="Marker not found")


@app.post("/api/v1/markers", response_model=MarkerResponse, status_code=201, tags=["Markers"])
async def create_marker(marker: MarkerCreate):
    """
    Create new marker

    - **name**: Marker name (required)
    - **coordinates**: Latitude and longitude (required)
    - **description**: Optional description
    - **address**: Optional address
    - **label_ids**: List of label IDs to assign
    - **is_favorite**: Mark as favorite
    """
    # TODO: Implement database insert
    # Validate coordinates
    if not (-90 <= marker.coordinates.latitude <= 90):
        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and 90"
        )
    if not (-180 <= marker.coordinates.longitude <= 180):
        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180"
        )

    # Placeholder response
    return MarkerResponse(
        id=1,
        name=marker.name,
        coordinates=marker.coordinates,
        description=marker.description,
        address=marker.address,
        labels=[],
        is_favorite=marker.is_favorite,
        created_at="2025-12-13T00:00:00Z"
    )


@app.put("/api/v1/markers/{marker_id}", response_model=MarkerResponse, tags=["Markers"])
async def update_marker(marker_id: int, marker: MarkerCreate):
    """
    Update existing marker

    - **marker_id**: Marker ID to update
    """
    # TODO: Implement database update
    raise HTTPException(status_code=404, detail="Marker not found")


@app.delete("/api/v1/markers/{marker_id}", status_code=204, tags=["Markers"])
async def delete_marker(marker_id: int):
    """
    Delete marker

    - **marker_id**: Marker ID to delete
    """
    # TODO: Implement database delete
    raise HTTPException(status_code=404, detail="Marker not found")


# ==================== Labels Endpoints (Placeholder) ====================

@app.get("/api/v1/labels", tags=["Labels"])
async def get_labels():
    """
    Get all labels (system + custom user labels)
    """
    # TODO: Implement database query
    return {"labels": []}


@app.post("/api/v1/labels", status_code=201, tags=["Labels"])
async def create_label(name: str, color: str, icon: str):
    """
    Create custom label

    - **name**: Label name
    - **color**: Hex color code
    - **icon**: Icon identifier
    """
    # TODO: Implement database insert
    return {
        "id": 1,
        "name": name,
        "color": color,
        "icon": icon,
        "is_system": False
    }


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": "2025-12-13T00:00:00Z"
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": "2025-12-13T00:00:00Z"
            }
        }
    )


# ==================== Startup & Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """
    Execute on application startup
    """
    print("=" * 50)
    print("My Personal Map API Starting...")
    print(f"Version: 1.0.0")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Debug Mode: {os.getenv('DEBUG', 'true')}")
    print("=" * 50)
    # TODO: Initialize database connection
    # TODO: Run database migrations
    # TODO: Load system labels


@app.on_event("shutdown")
async def shutdown_event():
    """
    Execute on application shutdown
    """
    print("=" * 50)
    print("My Personal Map API Shutting down...")
    print("=" * 50)
    # TODO: Close database connections
    # TODO: Cleanup resources


# ==================== Main Entry Point ====================

if __name__ == "__main__":
    """
    Run the application directly with uvicorn

    Usage:
        python main.py

    Or with uvicorn command:
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    """
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("DEBUG", "true").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
