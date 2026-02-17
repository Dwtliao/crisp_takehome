"""
Quick test of the Sales Pitch Generator
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.sales_pitch_generator import SalesPitchGenerator
from backend.config import ANTHROPIC_API_KEY

# Mock restaurant data (as if from Google Places)
mock_restaurant = {
    "name": "Oceanique",
    "types": ["seafood_restaurant", "french_restaurant", "fine_dining"],
    "price": "$$$",
    "rating": 4.5,
    "address": "505 Main St, Evanston, IL",
    "phone": "+18478643435",
    "reviews": [
        {
            "text": "The lobster bisque was incredible, rich and creamy. The scallops were perfectly seared. Every dish felt like fine dining at its best.",
            "rating": 5
        },
        {
            "text": "We had the duck confit and the Chilean sea bass. Both were excellent. The wine list is impressive with great French selections.",
            "rating": 5
        },
        {
            "text": "Their cheese plate is phenomenal! They clearly value quality ingredients. The foie gras appetizer was divine.",
            "rating": 5
        }
    ]
}

print("\n🧪 Testing Sales Pitch Generator...")
print("="*80)

if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set")
    sys.exit(1)

pitch_gen = SalesPitchGenerator(ANTHROPIC_API_KEY)

# Step 1: Determine cheese match
print("\n1️⃣  Determining cheese match...")
cheese_match = pitch_gen.determine_cheese_match(mock_restaurant)

print(f"   Primary: {cheese_match['primary_cheese']}")
print(f"   Secondary: {cheese_match['secondary_cheese']}")
print(f"   Confidence: {cheese_match['confidence']}")
print(f"   Scores: {cheese_match['scores']}")

# Step 2: Generate sales pitch
print("\n2️⃣  Generating sales pitch with Claude...")
pitch = pitch_gen.generate_sales_pitch(mock_restaurant, cheese_match)

# Step 3: Display pitch
print("\n" + "="*80)
print(f"🧀 SALES PITCH for {pitch['restaurant']['name']}")
print("="*80)

print(f"\n🎯 RECOMMENDED: {pitch['cheese']['name']}")
print(f"   {pitch['cheese']['subtitle']} | {pitch['cheese']['price_lb']}/lb")

print(f"\n💬 OPENING HOOK:")
print(f"   \"{pitch['opening_hook']}\"")

print(f"\n🍽️  MENU PAIRINGS:")
for i, pairing in enumerate(pitch['menu_pairings'], 1):
    print(f"   {i}. {pairing['dish']}")
    print(f"      → {pairing['why_it_works']}")

print(f"\n✨ SELLING POINTS:")
for point in pitch['selling_points']:
    print(f"   • {point}")

print(f"\n🏆 COMPETITIVE ADVANTAGE:")
print(f"   {pitch['competitive_advantage']}")

print(f"\n📞 CALL TO ACTION:")
print(f"   {pitch['call_to_action']}")

print("\n" + "="*80)
print("✅ TEST PASSED!")
print("="*80)
