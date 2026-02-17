"""
Example client for testing the Happy Pastures Creamery API
Demonstrates how a mobile app would interact with the backend
"""
import requests
import json


def find_prospects(latitude, longitude, radius=2500, use_llm=True):
    """
    Find restaurant prospects near a location

    Args:
        latitude: Latitude of search center
        longitude: Longitude of search center
        radius: Search radius in meters (default: 2500m = 2.5km)
        use_llm: Use LLM-based filtering (default: True)

    Returns:
        Dictionary with prospects data
    """
    url = "http://localhost:8000/api/prospects"

    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "use_llm": use_llm
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None


def main():
    """Example usage of the API"""

    print("=" * 80)
    print("Happy Pastures Creamery - API Client Example")
    print("=" * 80)

    # Hillary's location in Evanston, IL
    latitude = 42.0451
    longitude = -87.6877

    print(f"\nSearching for prospects near: {latitude}, {longitude}")
    print("Using LLM-based filtering...\n")

    # Call the API
    data = find_prospects(latitude, longitude, radius=2500, use_llm=True)

    if not data:
        print("Failed to get prospects")
        return

    # Display results
    print(f"Found {data['total_found']} high-quality prospects")
    print(f"Search radius: {data['search_radius_km']}km")
    print(f"Filtering method: {data['filtering_method']}")
    print("\n" + "=" * 80)
    print("RESTAURANT PROSPECTS:")
    print("=" * 80)

    for i, restaurant in enumerate(data['prospects'][:15], 1):  # Show top 15
        print(f"\n{i}. {restaurant['name']}")
        print(f"   Address: {restaurant['address']}")
        print(f"   Distance: {restaurant['distance']:.2f} km")

        if restaurant['categories']:
            print(f"   Categories: {', '.join(restaurant['categories'][:3])}")

        if restaurant['price_level']:
            price_symbols = '$' * restaurant['price_level']
            print(f"   Price Level: {price_symbols}")

    print("\n" + "=" * 80)
    print(f"\nTotal prospects to visit: {data['total_found']}")
    print("Hillary can now plan her walking route!")


if __name__ == "__main__":
    main()
