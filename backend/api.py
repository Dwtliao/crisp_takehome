"""
Happy Pastures Creamery - Unified API
Simple, pragmatic backend for the mobile/web app
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

from geoapify_client import GeoapifyClient
from google_places_client import GooglePlacesClient
from sales_pitch_generator import SalesPitchGenerator
from config import GEOAPIFY_API_KEY, ANTHROPIC_API_KEY, GOOGLE_PLACES_API_KEY

# Initialize FastAPI
app = FastAPI(
    title="Happy Pastures Creamery API",
    description="Restaurant prospecting system for artisan cheese sales",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving the frontend)
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/app", StaticFiles(directory=static_dir, html=True), name="frontend")


# Response Models
class RestaurantProspect(BaseModel):
    """A restaurant prospect with sales pitch"""
    name: str
    address: str
    distance_km: float
    rating: Optional[float] = None
    price: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Sales pitch data
    recommended_cheese_id: str
    recommended_cheese_name: str
    cheese_subtitle: str
    cheese_price: str
    match_confidence: str

    # Pitch content (optional - can fetch separately)
    opening_hook: Optional[str] = None
    menu_pairings: Optional[List[dict]] = None
    selling_points: Optional[List[str]] = None


class ProspectsResponse(BaseModel):
    """List of restaurant prospects"""
    prospects: List[RestaurantProspect]
    total: int
    search_center: dict
    search_radius_km: float


@app.get("/")
async def root():
    """API root"""
    return {
        "message": "Happy Pastures Creamery API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "prospects": "/api/prospects?lat=X&lon=Y",
            "pitch": "/api/pitch?name=RestaurantName&lat=X&lon=Y",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.get("/api/prospects", response_model=ProspectsResponse)
async def get_prospects(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius: int = Query(2500, description="Search radius in meters", ge=100, le=5000),
    limit: int = Query(20, description="Max results", ge=5, le=50)
):
    """
    Get restaurant prospects near a location

    This is the main endpoint that Hillary uses:
    1. Find restaurants nearby (Geoapify)
    2. Filter for quality (LLM)
    3. Match cheese to each restaurant (AI)
    4. Return list ready for display

    Note: Full pitch generation happens on-demand (see /api/pitch)
    to save API costs - we only generate when Hillary selects a restaurant
    """
    try:
        # Initialize clients
        geo_client = GeoapifyClient(GEOAPIFY_API_KEY, ANTHROPIC_API_KEY)
        pitch_generator = SalesPitchGenerator(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

        # Step 1: Search nearby restaurants
        results = geo_client.search_places(
            lat=lat,
            lon=lon,
            radius=radius,
            categories=['catering.restaurant'],
            limit=150  # Get lots of results to filter
        )

        # Step 2: Filter for quality
        if ANTHROPIC_API_KEY:
            filtered = geo_client.filter_results_with_llm(results, target_type='upscale')
        else:
            filtered = geo_client.filter_results(results, target_type='fine_dining')

        features = filtered.get('features', [])

        # Limit to requested number
        features = features[:limit]

        # Step 3: Build prospect list with cheese matches
        prospects = []
        for feature in features:
            props = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            coords = geometry.get('coordinates', [None, None])

            # Skip if no name
            restaurant_name = props.get('name', '').strip()
            if not restaurant_name:
                continue

            # Basic restaurant info
            prospect = {
                "name": restaurant_name,
                "address": props.get('address_line2', 'No address'),
                "distance_km": round(props.get('distance', 0) / 1000, 2),
                "rating": props.get('rating'),
                "price": None,  # Geoapify doesn't have price
                "phone": props.get('phone'),
                "latitude": coords[1],
                "longitude": coords[0],
            }

            # Quick cheese match (rule-based, fast)
            if pitch_generator:
                # Simple matching based on categories
                categories = [c.lower() for c in props.get('categories', [])]

                # Fine dining → Pasture Bloom
                if any(x in ' '.join(categories) for x in ['french', 'italian', 'fine', 'european', 'seafood']):
                    cheese_id = "pasture_bloom"
                    cheese_name = "Pasture Bloom Triple Crème"
                    cheese_subtitle = "Seasonal, Bloomy-Rind"
                    cheese_price = "$32-38/lb"
                    confidence = "high"
                # Gastropub → Smoky Alder
                elif any(x in ' '.join(categories) for x in ['pub', 'american', 'bar', 'grill', 'tavern']):
                    cheese_id = "smoky_alder"
                    cheese_name = "Smoky Alder Wash Rind"
                    cheese_subtitle = "Small-Batch, Semi-Soft"
                    cheese_price = "$24-28/lb"
                    confidence = "high"
                else:
                    # Default to more versatile option
                    cheese_id = "smoky_alder"
                    cheese_name = "Smoky Alder Wash Rind"
                    cheese_subtitle = "Small-Batch, Semi-Soft"
                    cheese_price = "$24-28/lb"
                    confidence = "medium"

                prospect.update({
                    "recommended_cheese_id": cheese_id,
                    "recommended_cheese_name": cheese_name,
                    "cheese_subtitle": cheese_subtitle,
                    "cheese_price": cheese_price,
                    "match_confidence": confidence
                })
            else:
                # Fallback if no AI
                prospect.update({
                    "recommended_cheese_id": "smoky_alder",
                    "recommended_cheese_name": "Smoky Alder Wash Rind",
                    "cheese_subtitle": "Small-Batch, Semi-Soft",
                    "cheese_price": "$24-28/lb",
                    "match_confidence": "medium"
                })

            prospects.append(RestaurantProspect(**prospect))

        return ProspectsResponse(
            prospects=prospects,
            total=len(prospects),
            search_center={"lat": lat, "lon": lon},
            search_radius_km=round(radius / 1000, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/pitch")
async def get_full_pitch(
    name: str = Query(..., description="Restaurant name"),
    lat: float = Query(..., description="Restaurant latitude"),
    lon: float = Query(..., description="Restaurant longitude"),
    skip_asian_check: bool = Query(False, description="Skip Asian cuisine detection")
):
    """
    Generate full sales pitch for a specific restaurant

    Called when Hillary selects a restaurant from the list.
    This is the expensive operation (Google Places + Claude),
    so we only do it on-demand.
    """
    try:
        # Initialize clients
        google_client = GooglePlacesClient(GOOGLE_PLACES_API_KEY)
        pitch_generator = SalesPitchGenerator(ANTHROPIC_API_KEY)

        # Step 1: Get detailed restaurant data (Google Places)
        restaurant_data = google_client.enrich_restaurant_data(name, lat, lon)

        if not restaurant_data:
            raise HTTPException(status_code=404, detail=f"Restaurant '{name}' not found")

        # Step 1.5: Check if Asian cuisine (dairy-incompatible) - unless user wants to skip
        if not skip_asian_check:
            asian_detection = pitch_generator.detect_asian_cuisine(restaurant_data)

            if asian_detection['is_asian']:
                # Return warning instead of generating pitch
                return {
                    "warning": "asian_cuisine_detected",
                    "message": "⚠️ This appears to be an Asian cuisine restaurant. Cheese/dairy products typically don't pair well with Asian cuisines.",
                    "confidence": asian_detection['confidence'],
                    "reasons": asian_detection['reasons'],
                    "restaurant": {
                        "name": restaurant_data.get('name'),
                        "address": restaurant_data.get('address'),
                        "types": restaurant_data.get('types', [])
                    },
                    "suggestion": "Consider skipping this restaurant or manually verify the menu has cheese-friendly dishes."
                }

        # Step 2: Determine cheese match
        cheese_match = pitch_generator.determine_cheese_match(restaurant_data)

        # Step 3: Generate pitch
        pitch = pitch_generator.generate_sales_pitch(restaurant_data, cheese_match)

        return pitch

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
