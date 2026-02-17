"""
Quick test script for Google Places API
Run this to verify your Google Places API key works
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.google_places_client import GooglePlacesClient, estimate_cost
from backend.config import GOOGLE_PLACES_API_KEY


def test_google_places_connection():
    """Test Google Places API connection"""

    print("\n🧪 Testing Google Places API Connection...")
    print("="*80)

    # Check API key
    if not GOOGLE_PLACES_API_KEY:
        print("❌ GOOGLE_PLACES_API_KEY not found in .env file")
        print("\n📝 To fix:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project")
        print("3. Enable 'Places API (New)' in API Library")
        print("4. Go to Credentials → Create API Key")
        print("5. Enable billing (get $200 free credit)")
        print("6. Add to .env: GOOGLE_PLACES_API_KEY=your_key_here")
        return False

    print(f"✅ API Key found: {GOOGLE_PLACES_API_KEY[:20]}...")

    # Show cost estimate
    print("\n💰 Cost Estimate:")
    costs = estimate_cost(1)
    print(f"   • Cost per restaurant: {costs['cost_per_restaurant']}")
    print(f"   • Free credit: {costs['free_credit']}")
    print(f"   • Restaurants with free credit: ~{costs['restaurants_with_free_credit']}")

    # Test search
    print("\n🔍 Testing search for 'Oceanique' in Evanston...")
    print("   (This will cost approximately $0.032)")

    client = GooglePlacesClient(GOOGLE_PLACES_API_KEY)

    # Search for a known restaurant
    result = client.search_by_name_and_location(
        name="Oceanique",
        latitude=42.0451,
        longitude=-87.6877,
        radius=200
    )

    if result:
        name = result.get('displayName', {}).get('text', 'Unknown')
        address = result.get('formattedAddress', 'No address')
        rating = result.get('rating')
        review_count = result.get('userRatingCount', 0)

        print(f"✅ Found: {name}")
        print(f"   Address: {address}")
        if rating:
            print(f"   Rating: {'⭐' * int(rating)} {rating}/5 ({review_count:,} reviews)")

        # Test enrichment
        print("\n📊 Testing full enrichment...")
        enriched = client.enrich_restaurant_data(
            "Oceanique",
            42.0451,
            -87.6877
        )

        if enriched:
            print(f"✅ Successfully enriched data")
            print(f"   Name: {enriched.get('name')}")
            print(f"   Price: {enriched.get('price')}")
            print(f"   Reviews: {len(enriched.get('reviews', []))}")
            print(f"   Phone: {enriched.get('phone', 'N/A')}")

            # Show a sample review
            reviews = enriched.get('reviews', [])
            if reviews:
                print(f"\n   First review excerpt:")
                first_review = reviews[0]['text'][:150]
                print(f"   \"{first_review}...\"")

        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("\n💰 Total cost for this test: ~$0.032")
        print("\nYou're ready to use the restaurant selector:")
        print("   python backend/restaurant_selector_google.py")
        print("="*80)
        return True

    else:
        print("❌ Search failed")
        print("\nPossible issues:")
        print("1. API key not activated - wait a few minutes")
        print("2. Places API (New) not enabled - check Cloud Console")
        print("3. Billing not enabled - required even with free credit")
        print("4. Incorrect API key format")
        return False


if __name__ == "__main__":
    try:
        success = test_google_places_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
