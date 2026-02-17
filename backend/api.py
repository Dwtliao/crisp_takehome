"""
Happy Pastures Creamery - Restaurant Prospecting API
FastAPI backend for mobile app
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn

from geoapify_client import GeoapifyClient
from config import (
    GEOAPIFY_API_KEY,
    ANTHROPIC_API_KEY,
    DEFAULT_SEARCH_RADIUS,
    MAX_SEARCH_RADIUS,
    DEFAULT_RESULT_LIMIT,
    USE_LLM_FILTERING
)

app = FastAPI(
    title="Happy Pastures Creamery API",
    description="Restaurant prospecting API for artisan cheese sales",
    version="1.0.0"
)

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your mobile app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ProspectRequest(BaseModel):
    """Request body for finding restaurant prospects"""
    latitude: float = Field(..., description="Latitude of search center", ge=-90, le=90)
    longitude: float = Field(..., description="Longitude of search center", ge=-180, le=180)
    radius: Optional[int] = Field(
        DEFAULT_SEARCH_RADIUS,
        description="Search radius in meters",
        ge=100,
        le=MAX_SEARCH_RADIUS
    )
    use_llm: Optional[bool] = Field(
        USE_LLM_FILTERING,
        description="Use LLM-based filtering for better accuracy"
    )
    limit: Optional[int] = Field(
        DEFAULT_RESULT_LIMIT,
        description="Maximum number of results before filtering",
        ge=10,
        le=200
    )


class Restaurant(BaseModel):
    """Restaurant prospect information"""
    name: str
    address: Optional[str] = None
    distance: float = Field(..., description="Distance in kilometers")
    categories: List[str] = []
    price_level: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ProspectResponse(BaseModel):
    """Response containing restaurant prospects"""
    prospects: List[Restaurant]
    total_found: int
    search_radius_km: float
    filtering_method: str  # "llm" or "keyword"


@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Happy Pastures Creamery API",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/prospects", response_model=ProspectResponse)
async def find_prospects(request: ProspectRequest):
    """
    Find high-quality restaurant prospects for artisan cheese sales

    Args:
        request: ProspectRequest with latitude, longitude, and optional parameters

    Returns:
        ProspectResponse with list of restaurant prospects
    """
    try:
        # Initialize client
        client = GeoapifyClient(
            api_key=GEOAPIFY_API_KEY,
            anthropic_api_key=ANTHROPIC_API_KEY if request.use_llm else None
        )

        # Search for restaurants
        results = client.search_places(
            lat=request.latitude,
            lon=request.longitude,
            radius=request.radius,
            categories=['catering.restaurant'],
            limit=request.limit
        )

        # Apply filtering
        if request.use_llm and ANTHROPIC_API_KEY:
            filtered_results = client.filter_results_with_llm(results, target_type='upscale')
            filtering_method = "llm"
        else:
            filtered_results = client.filter_results(results, target_type='fine_dining')
            filtering_method = "keyword"

        # Format response
        prospects = []
        for feature in filtered_results.get('features', []):
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            coords = geometry.get('coordinates', [None, None])

            restaurant = Restaurant(
                name=props.get('name', 'Unknown'),
                address=props.get('address_line2', props.get('formatted', '')),
                distance=props.get('distance', 0) / 1000,  # Convert to km
                categories=props.get('categories', [])[:5],  # Limit to 5 categories
                price_level=props.get('price_level'),
                latitude=coords[1] if len(coords) > 1 else None,
                longitude=coords[0] if len(coords) > 0 else None
            )
            prospects.append(restaurant)

        return ProspectResponse(
            prospects=prospects,
            total_found=len(prospects),
            search_radius_km=request.radius / 1000,
            filtering_method=filtering_method
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding prospects: {str(e)}")


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
