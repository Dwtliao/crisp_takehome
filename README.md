# Happy Pastures Creamery - Restaurant Prospecting System

A complete solution for finding high-quality restaurant prospects for artisan cheese sales.

## Project Structure

```
/
├── tests/              # Test scripts and CLI tools
│   └── geoapify_test.py
├── backend/            # Production API server
│   ├── api.py         # FastAPI endpoints
│   ├── geoapify_client.py  # Geoapify API client
│   ├── config.py      # Configuration
│   ├── example_client.py   # Example usage
│   └── README.md      # Backend documentation
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Business Case

Help Hillary, owner of Happy Pastures Creamery, find restaurant prospects within walking distance (2.5km) for her two artisan cheese products:

1. **Pasture Bloom Triple Crème** - Delicate, high-fat bloomy-rind cheese
   - Target: Italian & French fine dining restaurants
   - Use: Tasting menus, savory pastries, cheese-forward sauces, composed appetizers

2. **Smoky Alder Wash Rind** - Bold, pungent washed-rind cheese with alder smoke
   - Target: Gastropubs, taverns, upscale American restaurants
   - Use: Burgers, charcuterie programs, wood-fired dishes, bold flavor components

Built using Geoapify Places API as a cost-effective alternative to Google Maps for proof of concept.

## Quick Start

### Option 1: Test CLI Tool (for testing/exploration)

```bash
# Run the test script
python tests/geoapify_test.py --use-llm
```

### Option 2: Backend API (for mobile app integration)

```bash
# Start the API server
cd backend
python api.py

# In another terminal, test it
python backend/example_client.py
```

## Detailed Setup

1. **Get your Geoapify API key**
   - Sign up at https://www.geoapify.com/
   - Go to your dashboard and copy your API key
   - Free tier: 3,000 requests/day

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   - Open `geoapify_test.py`
   - Replace `YOUR_API_KEY_HERE` with your actual API key (line 144)

4. **Run the prospecting tool**
   ```bash
   # Hillary's cheese prospecting (default mode)
   python geoapify_test.py

   # Prospect from different location
   python geoapify_test.py --lat 41.8781 --lon -87.6298  # Chicago downtown

   # Run generic test examples instead
   python geoapify_test.py --mode test

   # Get help
   python geoapify_test.py --help
   ```

## What the Tool Does

The script uses **3-LAYER PRECISION FILTERING** to find the best prospects:

### Layer 1: Categories (Broad Net)
Cast a wide net with relevant restaurant types

### Layer 2: Cuisine Filters (Refinement)
Add cuisine-specific filters for precision targeting

### Layer 3: Upscale Signals (Quality Filter)
Filter by price level, star ratings, and dress code to find high-end venues

## Two Targeted Searches:

### 1. Fine Dining (Pasture Bloom Triple Crème)
**Target**: Italian, French, European, steakhouses, seafood, Mediterranean fine dining
**Strategy**: Strict filtering for high-end establishments only
**Name Signals**: Trattoria, Bistro, Le/La, Chez, Steakhouse, etc.
**Excludes**: Asian, pizza, fast-food, cafes, grills, inns, taverns, bars
**Why**: Delicate triple crème needs refined plating, tasting menus, cheese courses

### 2. All Upscale Restaurants (Smoky Alder Wash Rind)
**Target**: Any upscale restaurant regardless of cuisine
**Strategy**: Broader filtering - catches restaurants that don't fit fine dining signals but are still upscale
**Excludes**: Asian, pizza, fast-food, cafes, grills, inns, taverns
**Why**: Bold smoky cheese has wider appeal - works with any creative upscale menu

## Each Result Shows:
- Restaurant name and address
- Walking distance from Hillary's location
- Category/cuisine type
- 🎯 **Upscale signals**: Price level ($$$), star ratings (⭐⭐⭐), dress code
- Available amenities (helpful for planning visits)

## Features Demonstrated

The test script shows how to:

- **Radius-based search**: Search within customizable radius (in meters)
- **Category filtering**: Filter by restaurant types (500+ categories available)
- **Attribute filtering**: Filter by amenities like:
  - Wi-Fi availability
  - Wheelchair accessibility
  - Outdoor seating
  - Takeaway/delivery options
- **Multiple filters**: Combine multiple filters in a single query

## Categories Used for Hillary's Prospecting

### Fine Dining (Pasture Bloom Triple Crème):
- `catering.restaurant.fine_dining` - Explicitly tagged fine dining establishments
- `catering.restaurant.french` - Classic cheese pairing traditions
- `catering.restaurant.italian` - Italian cuisine pairs naturally with artisan cheese
- `catering.restaurant.european` - Broad European cuisine category
- `catering.restaurant.steak_house` - High-end, often feature cheese courses
- `catering.restaurant.mediterranean` - Mediterranean cuisine with cheese traditions
- `catering.restaurant.seafood` - Upscale seafood restaurants with diverse menus

### Gastropubs/Taverns (Smoky Alder Wash Rind):
- `catering.pub` - Pubs and taverns with elevated menus
- `catering.restaurant.american` - American restaurants (includes gastropubs)

### Why "catering" prefix?
Geoapify uses hierarchical categories:
- `catering` = Top-level for all food/drink establishments
- `catering.restaurant` = All restaurants
- `catering.restaurant.italian` = Specifically Italian restaurants

[Full category list (500+)](https://apidocs.geoapify.com/docs/places/#categories)

## Common Attributes for Filtering

- `wifi` - Wi-Fi availability (boolean)
- `wheelchair` - Wheelchair accessibility ('yes', 'no', 'limited')
- `outdoor_seating` - Outdoor seating (boolean)
- `takeaway` - Takeaway service (boolean)
- `delivery` - Delivery service (boolean)
- `smoking` - Smoking allowed (boolean)
- `dog` - Dogs allowed (boolean)
- `air_conditioning` - Air conditioning (boolean)
- `reservation` - Accepts reservations (boolean)
- `drive_through` - Has drive-through (boolean)

## How the 3-Layer Filtering Works

### Example: Finding Fine Dining Prospects

```python
client.search_places(
    lat=42.0451,
    lon=-87.6877,
    radius=2500,

    # Layer 1: Categories - Cast wide net
    categories=[
        'catering.restaurant.fine_dining',
        'catering.restaurant.french',
        'catering.restaurant.italian'
    ],

    # Layer 2: Cuisines - Refine further
    cuisines=['french', 'italian', 'european', 'steak'],

    # Layer 3: Upscale Signals - Quality filter
    price_level=3,  # Expensive restaurants ($$$ or $$$$)
    stars=4,        # Optional: 4+ star ratings

    limit=30
)
```

**How it works**:
- Categories find the right **type** of restaurant
- Cuisines add **precision** to cuisine style
- Upscale signals ensure **quality/budget fit** for premium products

### Available Upscale Filters

| Filter | Values | Example |
|--------|--------|---------|
| `price_level` | 1-4 (budget to very expensive) | `price_level=3` for $$$ |
| `stars` | 1-5 (rating) | `stars=4` for 4+ stars |
| `dress_code` | formal, casual, etc. | `dress_code='formal'` |

**Note**: Not all restaurants have these fields, but when available, they're powerful filters.

## Official Documentation & More Filters

### Main Documentation
- **Places API Overview**: https://apidocs.geoapify.com/docs/places/
- **API Playground**: https://apidocs.geoapify.com/playground/places/

### Complete Reference
- **All Categories (500+)**: https://apidocs.geoapify.com/docs/places/#categories
  - View the full hierarchical list of categories
  - Categories are hierarchical (e.g., `catering.restaurant.pizza`)

- **All Conditions/Filters**: https://apidocs.geoapify.com/docs/places/#conditions
  - Complete list of available attribute filters
  - How to combine filters with AND/OR logic
  - Examples of complex filtering

- **Location Parameters**: https://apidocs.geoapify.com/docs/places/#location
  - Circle (radius) - what we're using
  - Rectangle (bounding box)
  - Custom polygon areas

### Advanced Features
- **Place Details API**: Get comprehensive info about a specific place
- **Autocomplete API**: For building search-as-you-type features
- **Geocoding API**: Convert addresses to coordinates

## API Response Structure

Each place includes:
- Name and address
- Coordinates (lat/lon)
- Distance from search point
- Categories
- Available amenities/attributes
- Place ID for detailed queries

## Cost Comparison

**Geoapify (Free tier)**:
- 3,000 requests/day
- $0 for POC testing

**Google Maps Places API**:
- ~$17 per 1,000 requests for Nearby Search
- ~$32 per 1,000 requests for Text Search

For a POC with ~100-500 test queries, Geoapify saves $2-15.

## Next Steps

1. Test with your actual target locations
2. Experiment with different radius values
3. Try various category combinations
4. Build backend API wrapper for mobile app
5. Consider migration path to Google Maps if needed
