"""
Interactive Restaurant Selector with Menu Data (Google Places version)
Uses Google Places API - Reliable, comprehensive, paid service
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from geoapify_client import GeoapifyClient
from google_places_client import GooglePlacesClient, estimate_cost
from sales_pitch_generator import SalesPitchGenerator
from config import GEOAPIFY_API_KEY, ANTHROPIC_API_KEY, GOOGLE_PLACES_API_KEY


def select_restaurant_interactive(restaurants: list) -> dict:
    """
    Let user select a restaurant from a list

    Args:
        restaurants: List of restaurant feature dicts from Geoapify

    Returns:
        Selected restaurant feature dict
    """
    print("\n" + "="*80)
    print("🧀 SELECT A RESTAURANT TO LEARN MORE ABOUT")
    print("="*80)

    for idx, feature in enumerate(restaurants, 1):
        props = feature.get('properties', {})
        name = props.get('name', 'Unknown')
        address = props.get('address_line2', 'No address')
        distance = props.get('distance', 0) / 1000

        print(f"\n{idx}. {name}")
        print(f"   📍 {address}")
        print(f"   📏 {distance:.2f} km away")

    print("\n" + "="*80)

    while True:
        try:
            choice = input(f"\nEnter restaurant number (1-{len(restaurants)}) or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                print("Exiting...")
                sys.exit(0)

            idx = int(choice) - 1
            if 0 <= idx < len(restaurants):
                return restaurants[idx]
            else:
                print(f"❌ Please enter a number between 1 and {len(restaurants)}")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)


def display_menu_data(restaurant_data: dict, google_client: GooglePlacesClient, pitch_generator: SalesPitchGenerator = None):
    """
    Display enriched restaurant data from Google Places + Sales Pitch

    Args:
        restaurant_data: Enriched data from Google Places
        google_client: Google Places client for menu extraction
        pitch_generator: Optional sales pitch generator
    """
    if not restaurant_data:
        print("\n❌ No Google Places data found for this restaurant")
        return

    print("\n" + "="*80)
    print(f"🍽️  {restaurant_data['name']}")
    print("="*80)

    # Basic info
    rating = restaurant_data.get('rating')
    review_count = restaurant_data.get('review_count', 0)
    if rating:
        stars = '⭐' * int(rating)
        print(f"\n📊 Rating: {stars} {rating}/5 ({review_count:,} reviews)")

    price = restaurant_data.get('price')
    if price and price != 'N/A':
        print(f"💰 Price: {price}")

    print(f"📍 Address: {restaurant_data.get('address', 'N/A')}")
    print(f"📞 Phone: {restaurant_data.get('phone', 'N/A')}")

    website = restaurant_data.get('website')
    if website:
        print(f"🌐 Website: {website}")

    # Types/Categories
    types = restaurant_data.get('types', [])
    if types:
        # Clean up type names
        clean_types = [t.replace('_', ' ').title() for t in types if 'restaurant' not in t.lower()]
        if clean_types:
            print(f"\n🏷️  Categories: {', '.join(clean_types[:5])}")

    # Reviews with menu hints
    reviews = restaurant_data.get('reviews', [])
    if reviews:
        print(f"\n📝 Recent Reviews ({len(reviews)} reviews):")
        for i, review in enumerate(reviews[:3], 1):  # Show first 3
            rating_stars = '⭐' * review.get('rating', 0)
            author = review.get('author', 'Anonymous')
            time = review.get('time', '')
            text = review.get('text', '')[:200]  # First 200 chars

            print(f"\n   {i}. {rating_stars} - {author} ({time})")
            print(f"      {text}")
            if len(review.get('text', '')) > 200:
                print("      ...")

    # Google Maps link
    maps_url = restaurant_data.get('google_maps_url', '')
    if maps_url:
        print(f"\n🗺️  Google Maps: {maps_url}")

    # Menu hints extracted from reviews
    print("\n" + "-"*80)
    print("🍴 MENU HINTS (extracted from customer reviews):")
    print("-"*80)

    menu_keywords = google_client.extract_menu_hints_from_reviews(reviews)
    if menu_keywords:
        for item in menu_keywords:
            print(f"  • {item}")
    else:
        print("  (No specific menu items mentioned in recent reviews)")

    # Generate Sales Pitch
    if pitch_generator:
        print("\n" + "="*80)
        print("🧀 SALES PITCH - Happy Pastures Creamery")
        print("="*80)
        print("Generating customized pitch...")

        # Determine cheese match
        cheese_match = pitch_generator.determine_cheese_match(restaurant_data)

        # Generate pitch
        pitch = pitch_generator.generate_sales_pitch(restaurant_data, cheese_match)

        # Display pitch
        print(f"\n🎯 RECOMMENDED CHEESE: {pitch['cheese']['name']}")
        print(f"   {pitch['cheese']['subtitle']} | {pitch['cheese']['price_lb']}/lb")
        print(f"   Match Confidence: {pitch['confidence'].upper()}")

        print(f"\n💬 OPENING HOOK:")
        print(f"   \"{pitch['opening_hook']}\"")

        print(f"\n🍽️  MENU PAIRING IDEAS:")
        for i, pairing in enumerate(pitch['menu_pairings'], 1):
            print(f"   {i}. {pairing['dish']}")
            print(f"      → {pairing['why_it_works']}")

        print(f"\n✨ KEY SELLING POINTS:")
        for point in pitch['selling_points']:
            print(f"   • {point}")

        print(f"\n🏆 COMPETITIVE ADVANTAGE:")
        print(f"   {pitch['competitive_advantage']}")

        print(f"\n📞 CALL TO ACTION:")
        print(f"   {pitch['call_to_action']}")

    print("\n" + "="*80)
    print("✅ Data from Google Places API + AI-Generated Pitch")
    print("="*80)


def main():
    """Main CLI program"""

    print("\n🧀 HAPPY PASTURES CREAMERY - Restaurant Menu Explorer (Google Places)")
    print("="*80)

    # Check for API keys
    if not GEOAPIFY_API_KEY:
        print("❌ Error: GEOAPIFY_API_KEY not set in config.py")
        sys.exit(1)

    if not GOOGLE_PLACES_API_KEY:
        print("❌ Error: GOOGLE_PLACES_API_KEY not set in config.py")
        print("\n📝 To get a Google Places API key:")
        print("   1. Go to: https://console.cloud.google.com/")
        print("   2. Create a new project")
        print("   3. Enable 'Places API (New)'")
        print("   4. Create credentials → API Key")
        print("   5. Enable billing ($200 free credit)")
        print("   6. Add to .env: GOOGLE_PLACES_API_KEY=your_key_here")
        sys.exit(1)

    # Initialize clients
    geo_client = GeoapifyClient(GEOAPIFY_API_KEY, ANTHROPIC_API_KEY)
    google_client = GooglePlacesClient(GOOGLE_PLACES_API_KEY)
    pitch_generator = SalesPitchGenerator(ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

    # Hillary's location (Evanston)
    HILLARY_LAT = 42.0451
    HILLARY_LON = -87.6877

    print(f"\n🔍 Searching for restaurants near Evanston...")

    # Search for restaurants
    results = geo_client.search_places(
        lat=HILLARY_LAT,
        lon=HILLARY_LON,
        radius=2500,  # 2.5km walking distance
        categories=['catering.restaurant'],
        limit=150  # Increased to get more results before LLM filtering
    )

    # Filter using LLM if available
    if ANTHROPIC_API_KEY:
        filtered = geo_client.filter_results_with_llm(results, target_type='upscale')
    else:
        filtered = geo_client.filter_results(results, target_type='fine_dining')

    features = filtered.get('features', [])

    if not features:
        print("❌ No restaurants found")
        sys.exit(1)

    print(f"✅ Found {len(features)} high-quality prospects")

    # Show cost estimate
    costs = estimate_cost(len(features))
    print(f"\n💰 Google Places API Cost Estimate:")
    print(f"   • {costs['cost_per_restaurant']} per restaurant")
    print(f"   • {costs['total_cost']} for all {len(features)} restaurants")
    print(f"   • {costs['note']}")

    # Let user select a restaurant
    selected = select_restaurant_interactive(features)

    # Get restaurant details
    props = selected.get('properties', {})
    name = props.get('name')
    geometry = selected.get('geometry', {})
    coords = geometry.get('coordinates', [None, None])
    lat = coords[1]
    lon = coords[0]

    print(f"\n🔍 Looking up '{name}' on Google Places...")
    print(f"💰 Cost for this lookup: ~$0.032")

    # Get Google Places data
    google_data = google_client.enrich_restaurant_data(name, lat, lon)

    if google_data:
        display_menu_data(google_data, google_client, pitch_generator)
    else:
        print(f"\n❌ Could not find '{name}' on Google Places")
        print("   (The restaurant may not be in Google's database)")

    print("\n")


if __name__ == "__main__":
    main()
