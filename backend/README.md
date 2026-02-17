# Happy Pastures Creamery - Backend API

REST API for finding high-quality restaurant prospects and generating AI-powered sales pitches.

## Quick Start

```bash
# From project root
./start_app.sh

# Or from backend/
python api.py
```

Server runs on: **http://localhost:8000**

---

## API Endpoints

### GET /
Root endpoint - returns API info and available endpoints

### GET /health
Health check

**Response:**
```json
{
  "status": "healthy"
}
```

---

### GET /api/prospects
Find restaurant prospects near a location

**Query Parameters:**
- `lat` (required): Latitude
- `lon` (required): Longitude
- `radius` (optional): Search radius in meters (default: 2500, max: 5000)
- `limit` (optional): Max results (default: 20, max: 50)

**Example:**
```bash
curl "http://localhost:8000/api/prospects?lat=42.0451&lon=-87.6877&radius=2500&limit=20"
```

**Response:**
```json
{
  "prospects": [
    {
      "name": "Oceanique",
      "address": "505 Main St, Evanston, IL",
      "distance_km": 1.46,
      "rating": 4.6,
      "phone": "(847) 864-3435",
      "latitude": 42.045,
      "longitude": -87.688,
      "recommended_cheese_id": "pasture_bloom",
      "recommended_cheese_name": "Pasture Bloom Triple Crème",
      "cheese_subtitle": "Seasonal, Bloomy-Rind",
      "cheese_price": "$32-38/lb",
      "match_confidence": "high"
    }
  ],
  "total": 24,
  "search_center": {"lat": 42.0451, "lon": -87.6877},
  "search_radius_km": 2.5
}
```

---

### GET /api/pitch
Generate detailed sales pitch for a specific restaurant

**Query Parameters:**
- `name` (required): Restaurant name
- `lat` (required): Restaurant latitude
- `lon` (required): Restaurant longitude

**Example:**
```bash
curl "http://localhost:8000/api/pitch?name=Oceanique&lat=42.0451&lon=-87.6877"
```

**Response:**
```json
{
  "restaurant": {
    "name": "Oceanique",
    "address": "505 Main St, Evanston, IL",
    "phone": "(847) 864-3435"
  },
  "cheese": {
    "id": "pasture_bloom",
    "name": "Pasture Bloom Triple Crème",
    "subtitle": "Seasonal, Bloomy-Rind",
    "price_lb": "$32-38/lb"
  },
  "opening_hook": "Hi! I'm Hillary from Happy Pastures Creamery...",
  "menu_pairings": [
    {
      "dish": "Lobster Bisque",
      "why_it_works": "The triple crème adds rich, creamy depth..."
    }
  ],
  "selling_points": [
    "Small-batch, seasonal production",
    "Locally sourced ingredients",
    "Perfect for fine dining presentation"
  ],
  "competitive_advantage": "Unlike commodity cheese...",
  "call_to_action": "I'd love to drop off a sample...",
  "confidence": "high"
}
```

---

## Interactive API Documentation

Visit **http://localhost:8000/docs** for:
- Interactive Swagger UI
- Try endpoints directly in browser
- Full request/response schemas

---

## Testing the API

### Python:
```python
import requests

# Get prospects
response = requests.get(
    'http://localhost:8000/api/prospects',
    params={'lat': 42.0451, 'lon': -87.6877, 'limit': 20}
)
prospects = response.json()['prospects']

# Get pitch for first restaurant
restaurant = prospects[0]
pitch_response = requests.get(
    'http://localhost:8000/api/pitch',
    params={
        'name': restaurant['name'],
        'lat': restaurant['latitude'],
        'lon': restaurant['longitude']
    }
)
pitch = pitch_response.json()
print(pitch['opening_hook'])
```

### JavaScript (Frontend):
```javascript
// Get prospects near current location
const response = await fetch(
  `http://localhost:8000/api/prospects?lat=${lat}&lon=${lon}&limit=20`
);
const data = await response.json();
const prospects = data.prospects;

// Get pitch for selected restaurant
const pitchResponse = await fetch(
  `http://localhost:8000/api/pitch?name=${restaurant.name}&lat=${restaurant.latitude}&lon=${restaurant.longitude}`
);
const pitch = await pitchResponse.json();
```

---

## Configuration

Edit `config.py` to customize:
- `DEFAULT_SEARCH_RADIUS`: 2500m (2.5km walking distance)
- `MAX_SEARCH_RADIUS`: 5000m (5km)
- `DEFAULT_RESULT_LIMIT`: 100 raw results before filtering
- `USE_LLM_FILTERING`: True (use AI for quality filtering)

---

## Cost Analysis

Per restaurant prospect:
- Geoapify search: Free tier
- LLM filtering: ~$0.001 per restaurant
- Google Places lookup: $0.032 (only when selected)
- Sales pitch generation: $0.020 (only when selected)

**Total cost per complete pitch: ~$0.053**

---

## Deployment

### Production with Gunicorn:
```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ backend/
COPY frontend/ frontend/
WORKDIR /app/backend
CMD ["python", "api.py"]
```

---

## Security Notes

- 🔒 Never commit API keys (use .env)
- 🔒 Restrict CORS in production
- 🔒 Add rate limiting for public APIs
- 🔒 Use HTTPS in production
