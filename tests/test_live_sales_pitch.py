"""
Test Live Sales Pitch Generation Workflow

This script demonstrates the complete end-to-end flow:
1. Fetch LIVE restaurant data from Google Places API
2. Analyze the restaurant and determine cheese match
3. Generate customized sales pitch using AI
4. Display the complete pitch Hillary would see

This is exactly what Hillary would use when prospecting.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.google_places_client import GooglePlacesClient
from backend.sales_pitch_generator import SalesPitchGenerator
from backend.config import GOOGLE_PLACES_API_KEY, ANTHROPIC_API_KEY


def test_live_pitch_generation(restaurant_name: str, latitude: float, longitude: float):
    """
    Test complete workflow with live data

    Args:
        restaurant_name: Name of the restaurant
        latitude: Restaurant latitude
        longitude: Restaurant longitude
    """
    print("\n" + "="*80)
    print("🧀 HAPPY PASTURES CREAMERY - Live Sales Pitch Generator")
    print("="*80)

    # Validate API keys
    if not GOOGLE_PLACES_API_KEY:
        print("❌ GOOGLE_PLACES_API_KEY not set")
        return False

    if not ANTHROPIC_API_KEY:
        print("❌ ANTHROPIC_API_KEY not set")
        return False

    # Initialize clients
    print("\n1️⃣  Initializing API clients...")
    google_client = GooglePlacesClient(GOOGLE_PLACES_API_KEY)
    pitch_generator = SalesPitchGenerator(ANTHROPIC_API_KEY)
    print("   ✅ Clients ready")

    # Step 1: Fetch LIVE restaurant data from Google Places
    print(f"\n2️⃣  Fetching LIVE data for '{restaurant_name}' from Google Places API...")
    print(f"   Location: ({latitude}, {longitude})")
    print(f"   💰 Cost: ~$0.032")

    restaurant_data = google_client.enrich_restaurant_data(
        restaurant_name,
        latitude,
        longitude
    )

    if not restaurant_data:
        print(f"   ❌ Could not find '{restaurant_name}' on Google Places")
        return False

    print(f"   ✅ Found: {restaurant_data['name']}")
    print(f"   📍 {restaurant_data.get('address', 'N/A')}")
    print(f"   ⭐ Rating: {restaurant_data.get('rating', 'N/A')}/5")
    print(f"   💰 Price: {restaurant_data.get('price', 'N/A')}")
    print(f"   📝 Reviews: {len(restaurant_data.get('reviews', []))}")

    # Show what data we have
    print("\n   📊 Data Retrieved:")
    print(f"      - Restaurant name, address, phone")
    print(f"      - Rating and review count")
    print(f"      - Price level")
    print(f"      - {len(restaurant_data.get('types', []))} category tags")
    print(f"      - {len(restaurant_data.get('reviews', []))} customer reviews with menu mentions")

    # Step 2: Analyze restaurant and determine cheese match
    print("\n3️⃣  Analyzing restaurant to determine cheese match...")
    cheese_match = pitch_generator.determine_cheese_match(restaurant_data)

    print(f"   🎯 Best Match: {cheese_match['primary_cheese']}")
    print(f"   📊 Confidence: {cheese_match['confidence'].upper()}")
    print(f"   🔢 Scores: Pasture Bloom={cheese_match['scores']['pasture_bloom']}, Smoky Alder={cheese_match['scores']['smoky_alder']}")

    if cheese_match['secondary_cheese']:
        print(f"   💡 Secondary option: {cheese_match['secondary_cheese']}")

    # Step 3: Generate AI sales pitch
    print("\n4️⃣  Generating customized sales pitch with Claude AI...")
    print("   🤖 Analyzing menu items, cuisine style, and customer preferences...")
    print("   💰 Cost: ~$0.02")

    pitch = pitch_generator.generate_sales_pitch(restaurant_data, cheese_match)

    print("   ✅ Pitch generated!")

    # Step 4: Display the complete pitch (what Hillary sees)
    print("\n" + "="*80)
    print("📱 HILLARY'S PHONE SCREEN - READY TO WALK IN")
    print("="*80)

    print(f"\n🏪 {pitch['restaurant']['name']}")
    print(f"📍 {pitch['restaurant']['address']}")
    print(f"📞 {pitch['restaurant']['phone']}")

    print(f"\n" + "-"*80)
    print(f"🧀 RECOMMENDED PRODUCT")
    print("-"*80)
    print(f"{pitch['cheese']['name']}")
    print(f"{pitch['cheese']['subtitle']}")
    print(f"💰 Wholesale: {pitch['cheese']['price_lb']}/lb")
    print(f"🎯 Match Confidence: {pitch['confidence'].upper()}")

    print(f"\n" + "-"*80)
    print("💬 YOUR OPENING LINE")
    print("-"*80)
    print(f'"{pitch["opening_hook"]}"')

    print(f"\n" + "-"*80)
    print("🍽️  MENU PAIRING IDEAS")
    print("-"*80)
    for i, pairing in enumerate(pitch['menu_pairings'], 1):
        print(f"\n{i}. {pairing['dish']}")
        print(f"   💡 {pairing['why_it_works']}")

    print(f"\n" + "-"*80)
    print("✨ KEY TALKING POINTS")
    print("-"*80)
    for i, point in enumerate(pitch['selling_points'], 1):
        print(f"{i}. {point}")

    print(f"\n" + "-"*80)
    print("🏆 WHY US VS. COMMODITY CHEESE")
    print("-"*80)
    print(pitch['competitive_advantage'])

    print(f"\n" + "-"*80)
    print("📞 CLOSE THE DEAL")
    print("-"*80)
    print(pitch['call_to_action'])

    print("\n" + "="*80)
    print("✅ READY TO KNOCK ON THE DOOR!")
    print("="*80)

    # Cost summary
    print(f"\n💰 Total API Costs for this lookup:")
    print(f"   Google Places API: ~$0.032")
    print(f"   Claude AI: ~$0.02")
    print(f"   TOTAL: ~$0.052 per restaurant prospect")

    return True


def main():
    """Run test with example restaurants"""

    print("\n🧪 Testing Live Sales Pitch Generation")
    print("="*80)
    print("This demonstrates the complete workflow Hillary uses:")
    print("1. Find a restaurant (already done with Geoapify)")
    print("2. Get detailed data (Google Places API)")
    print("3. Generate customized pitch (Claude AI)")
    print("4. Walk in with confidence!")
    print("="*80)

    # Test with known restaurants
    test_cases = [
        {
            "name": "Oceanique",
            "lat": 42.0451,
            "lon": -87.6877,
            "description": "Fine dining French/Seafood"
        },
        {
            "name": "Found Kitchen & Social House",
            "lat": 42.0451,
            "lon": -87.6877,
            "description": "Upscale American Gastropub"
        }
    ]

    # Run first test
    test = test_cases[0]
    print(f"\n🎯 TEST CASE: {test['name']} ({test['description']})")

    success = test_live_pitch_generation(
        test['name'],
        test['lat'],
        test['lon']
    )

    if success:
        print("\n\n" + "="*80)
        print("🎉 SUCCESS! The complete workflow is operational!")
        print("="*80)
        print("\nThis is exactly what Hillary experiences:")
        print("1. She selects a restaurant from her filtered list")
        print("2. The system fetches live menu data from Google")
        print("3. AI analyzes the restaurant and creates a custom pitch")
        print("4. She reads the pitch on her phone before walking in")
        print("5. She has specific talking points and menu ideas ready")
        print("\n💪 Hillary is ready to sell artisan cheese!")
    else:
        print("\n❌ Test failed - check API keys and connectivity")

    # Offer to test another restaurant
    print("\n" + "-"*80)
    print("Want to test another restaurant? Try:")
    print("  python test_live_sales_pitch.py")
    print("\nOr integrate into the full selector:")
    print("  python backend/restaurant_selector_google.py")
    print("-"*80)


if __name__ == "__main__":
    main()
