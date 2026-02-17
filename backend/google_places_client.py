"""
Google Places API Client for Menu Data
Reliable, comprehensive, but paid ($0.017-0.032 per request)
Free $200 credit for new accounts

Documentation: https://developers.google.com/maps/documentation/places/web-service/overview
"""
import requests
from typing import Dict, Any, Optional, List
import time


class GooglePlacesClient:
    """Client for Google Places API (New)"""

    BASE_URL = "https://places.googleapis.com/v1"

    def __init__(self, api_key: str):
        """
        Initialize Google Places client

        Args:
            api_key: Your Google Places API key
        """
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount,places.priceLevel,places.types,places.nationalPhoneNumber,places.websiteUri,places.regularOpeningHours,places.reviews'
        }

    def search_by_name_and_location(
        self,
        name: str,
        latitude: float,
        longitude: float,
        radius: int = 100
    ) -> Optional[Dict[str, Any]]:
        """
        Find a specific restaurant by name and location using Text Search

        Args:
            name: Restaurant name
            latitude: Latitude
            longitude: Longitude
            radius: Search radius in meters (default 100m)

        Returns:
            Place data or None if not found
        """
        try:
            # Use Text Search (New)
            url = f"{self.BASE_URL}/places:searchText"

            payload = {
                "textQuery": name,
                "locationBias": {
                    "circle": {
                        "center": {
                            "latitude": latitude,
                            "longitude": longitude
                        },
                        "radius": radius
                    }
                },
                "maxResultCount": 1
            }

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                places = data.get('places', [])
                if places:
                    return places[0]
            elif response.status_code == 429:
                print("⚠️  Google Places API rate limit exceeded")
            elif response.status_code == 403:
                print("⚠️  Google Places API error: Check billing is enabled")
            else:
                print(f"⚠️  Google Places API error: {response.status_code}")
                print(f"    Response: {response.text[:200]}")

            return None

        except Exception as e:
            print(f"Error searching Google Places: {e}")
            return None

    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place

        Args:
            place_id: Google Places ID

        Returns:
            Place details or None
        """
        try:
            url = f"{self.BASE_URL}/places/{place_id}"

            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️  Google Places API error: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting place details: {e}")
            return None

    def enrich_restaurant_data(
        self,
        restaurant_name: str,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive restaurant data including reviews with menu mentions

        Args:
            restaurant_name: Name of the restaurant
            latitude: Latitude
            longitude: Longitude

        Returns:
            Enriched data with Google Places info
        """
        # Search for the place
        place = self.search_by_name_and_location(
            restaurant_name,
            latitude,
            longitude,
            radius=200  # 200m radius for accuracy
        )

        if not place:
            return None

        # Extract data
        name = place.get('displayName', {}).get('text', 'Unknown')
        address = place.get('formattedAddress', 'No address')
        rating = place.get('rating')
        rating_count = place.get('userRatingCount', 0)
        price_level = place.get('priceLevel', 'PRICE_LEVEL_UNSPECIFIED')
        types = place.get('types', [])
        phone = place.get('nationalPhoneNumber')
        website = place.get('websiteUri')
        reviews = place.get('reviews', [])

        # Convert price level
        price_map = {
            'PRICE_LEVEL_UNSPECIFIED': 'N/A',
            'PRICE_LEVEL_FREE': 'Free',
            'PRICE_LEVEL_INEXPENSIVE': '$',
            'PRICE_LEVEL_MODERATE': '$$',
            'PRICE_LEVEL_EXPENSIVE': '$$$',
            'PRICE_LEVEL_VERY_EXPENSIVE': '$$$$'
        }
        price = price_map.get(price_level, 'N/A')

        # Build enriched data
        enriched = {
            'name': name,
            'address': address,
            'rating': rating,
            'review_count': rating_count,
            'price': price,
            'types': types[:5],  # Limit to 5 types
            'phone': phone,
            'website': website,
            'google_maps_url': f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}&query_place_id={place.get('id', '')}",
            'reviews': [
                {
                    'text': review.get('text', {}).get('text', ''),
                    'rating': review.get('rating', 0),
                    'time': review.get('relativePublishTimeDescription', ''),
                    'author': review.get('authorAttribution', {}).get('displayName', 'Anonymous')
                }
                for review in reviews[:5]  # Get up to 5 reviews
            ]
        }

        return enriched

    def extract_menu_hints_from_reviews(self, reviews: List[Dict[str, Any]]) -> List[str]:
        """
        Extract likely menu items mentioned in reviews

        Args:
            reviews: List of review dicts with 'text' field

        Returns:
            List of potential menu items/dishes mentioned
        """
        food_keywords = [
            'steak', 'pasta', 'salad', 'burger', 'fish', 'chicken',
            'lamb', 'pork', 'duck', 'risotto', 'soup', 'dessert',
            'wine', 'cocktail', 'cheese', 'bread', 'seafood',
            'lobster', 'crab', 'oyster', 'tuna', 'salmon', 'scallops',
            'appetizer', 'entree', 'dish', 'special'
        ]

        menu_hints = []
        for review in reviews:
            text = review.get('text', '').lower()
            # Split into sentences
            for sentence in text.replace('!', '.').replace('?', '.').split('.'):
                sentence = sentence.strip()
                # If sentence mentions food AND is reasonably short
                if any(food in sentence for food in food_keywords) and 10 < len(sentence) < 150:
                    menu_hints.append(sentence.capitalize())

        # Return unique mentions, limit to 10
        return list(dict.fromkeys(menu_hints))[:10]


# Cost estimation helper
def estimate_cost(num_restaurants: int) -> Dict[str, Any]:
    """
    Estimate Google Places API costs

    Args:
        num_restaurants: Number of restaurants to enrich

    Returns:
        Cost breakdown
    """
    # Pricing (as of 2024)
    SEARCH_COST = 0.032  # Text Search
    DETAILS_COST = 0.017  # Place Details (if needed)

    # We use Text Search with field mask (gets most data in one call)
    cost_per_restaurant = SEARCH_COST

    total_cost = num_restaurants * cost_per_restaurant

    return {
        'num_restaurants': num_restaurants,
        'cost_per_restaurant': f"${cost_per_restaurant:.3f}",
        'total_cost': f"${total_cost:.2f}",
        'free_credit': "$200.00",
        'restaurants_with_free_credit': int(200 / cost_per_restaurant),
        'note': 'New Google Cloud accounts get $200 free credit'
    }
