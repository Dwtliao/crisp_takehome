# Happy Pastures Creamery - Backend API

REST API for finding high-quality restaurant prospects for artisan cheese sales.

## Setup

### 1. Install Dependencies

```bash
cd ..
pip install -r requirements.txt
```

### 2. Configure API Keys

Edit `backend/config.py` or set environment variables:

```bash
export GEOAPIFY_API_KEY="your-geoapify-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### 3. Run the Server

```bash
cd backend
python api.py
```

Server runs on: **http://localhost:8000**

## API Endpoints

### GET /
Health check - returns API info

### GET /health
Health status check

### POST /api/prospects
Find restaurant prospects near a location

**Request Body:**
```json
{
  "latitude": 42.0451,
  "longitude": -87.6877,
  "radius": 2500,
  "use_llm": true,
  "limit": 100
}
```

**Response:**
```json
{
  "prospects": [
    {
      "name": "Trattoria Demi",
      "address": "1571 Sherman Ave, Evanston, IL",
      "distance": 0.45,
      "categories": ["catering.restaurant.italian"],
      "price_level": 3,
      "latitude": 42.048,
      "longitude": -87.687
    }
  ],
  "total_found": 25,
  "search_radius_km": 2.5,
  "filtering_method": "llm"
}
```

## Testing the API

### Using curl:

```bash
curl -X POST http://localhost:8000/api/prospects \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 42.0451,
    "longitude": -87.6877,
    "radius": 2500,
    "use_llm": true
  }'
```

### Using Python:

```python
import requests

response = requests.post(
    'http://localhost:8000/api/prospects',
    json={
        'latitude': 42.0451,
        'longitude': -87.6877,
        'radius': 2500,
        'use_llm': True
    }
)

prospects = response.json()
print(f"Found {prospects['total_found']} prospects")
for restaurant in prospects['prospects'][:5]:
    print(f"  - {restaurant['name']} ({restaurant['distance']:.2f}km)")
```

### Interactive API Docs:

Visit **http://localhost:8000/docs** for interactive Swagger documentation

## Mobile App Integration

### Example React Native / Expo:

```javascript
const findProspects = async (latitude, longitude) => {
  try {
    const response = await fetch('http://localhost:8000/api/prospects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        latitude,
        longitude,
        radius: 2500,
        use_llm: true,
      }),
    });

    const data = await response.json();
    return data.prospects;
  } catch (error) {
    console.error('Error fetching prospects:', error);
    return [];
  }
};

// Usage
const prospects = await findProspects(42.0451, -87.6877);
```

### Example Flutter:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<Restaurant>> findProspects(double lat, double lon) async {
  final response = await http.post(
    Uri.parse('http://localhost:8000/api/prospects'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'latitude': lat,
      'longitude': lon,
      'radius': 2500,
      'use_llm': true,
    }),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return (data['prospects'] as List)
        .map((r) => Restaurant.fromJson(r))
        .toList();
  }
  throw Exception('Failed to load prospects');
}
```

## Configuration Options

Edit `config.py` to customize:

- `DEFAULT_SEARCH_RADIUS`: Default walking radius (meters)
- `MAX_SEARCH_RADIUS`: Maximum allowed radius (meters)
- `DEFAULT_RESULT_LIMIT`: Default result limit before filtering
- `USE_LLM_FILTERING`: Enable/disable LLM filtering by default

## Deployment

### Production Mode:

```bash
# Use gunicorn for production
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["gunicorn", "api:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## Security Notes

- 🔒 **Remove API keys before committing!**
- 🔒 Use environment variables in production
- 🔒 Restrict CORS origins to your mobile app domain
- 🔒 Add authentication/rate limiting for production
