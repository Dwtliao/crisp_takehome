"""
Debug restaurant filtering to see why specific restaurants aren't showing up
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.geoapify_client import GeoapifyClient
from backend.config import GEOAPIFY_API_KEY, ANTHROPIC_API_KEY


def main():
    print("\n🔍 Restaurant Filtering Debugger")
    print("="*80)

    # Hillary's location (Evanston)
    HILLARY_LAT = 42.0451
    HILLARY_LON = -87.6877

    geo_client = GeoapifyClient(GEOAPIFY_API_KEY, ANTHROPIC_API_KEY)

    # Step 1: Get RAW results from Geoapify
    print("\n📍 Step 1: Getting RAW results from Geoapify...")
    print("-"*80)

    raw_results = geo_client.search_places(
        lat=HILLARY_LAT,
        lon=HILLARY_LON,
        radius=2500,  # 2.5km
        categories=['catering.restaurant'],
        limit=100  # Get more to see if Oceanique is there
    )

    raw_features = raw_results.get('features', [])
    print(f"✅ Found {len(raw_features)} total restaurants\n")

    # Search for Oceanique in raw results
    oceanique_in_raw = None
    for feature in raw_features:
        props = feature.get('properties', {})
        name = props.get('name', '').lower()
        if 'oceanique' in name:
            oceanique_in_raw = feature
            print(f"🎯 FOUND 'Oceanique' in raw results!")
            print(f"   Name: {props.get('name')}")
            print(f"   Address: {props.get('address_line2')}")
            print(f"   Categories: {props.get('categories', [])}")
            print(f"   Distance: {props.get('distance', 0) / 1000:.2f} km")
            break

    if not oceanique_in_raw:
        print("❌ 'Oceanique' NOT found in raw Geoapify results")
        print("   This means Geoapify doesn't have it or it's outside the search radius")

    # Show sample of restaurants found
    print(f"\n📋 Sample of raw results (first 10):")
    for idx, feature in enumerate(raw_features[:10], 1):
        props = feature.get('properties', {})
        name = props.get('name', '')
        categories = ', '.join(props.get('categories', [])[:3])
        print(f"   {idx}. {name}")
        print(f"      Categories: {categories}")

    # Step 2: Apply LLM filtering
    print("\n" + "="*80)
    print("🤖 Step 2: Applying LLM filtering...")
    print("-"*80)

    filtered_results = geo_client.filter_results_with_llm(raw_results, target_type='upscale')
    filtered_features = filtered_results.get('features', [])

    print(f"\n✅ After LLM filtering: {len(filtered_features)} restaurants kept\n")

    # Check if Oceanique survived filtering
    oceanique_in_filtered = None
    for feature in filtered_features:
        props = feature.get('properties', {})
        name = props.get('name', '').lower()
        if 'oceanique' in name:
            oceanique_in_filtered = feature
            print(f"🎯 'Oceanique' SURVIVED LLM filtering!")
            break

    if oceanique_in_raw and not oceanique_in_filtered:
        print("❌ 'Oceanique' was REMOVED by LLM filtering")
        print("   The LLM incorrectly classified it as unsuitable")

    # Show filtered results
    print(f"\n📋 Filtered results (all {len(filtered_features)}):")
    for idx, feature in enumerate(filtered_features, 1):
        props = feature.get('properties', {})
        name = props.get('name', '')
        distance = props.get('distance', 0) / 1000
        categories = ', '.join(props.get('categories', [])[:3])
        print(f"   {idx}. {name} ({distance:.2f} km)")
        print(f"      Categories: {categories}")

    # Step 3: Try keyword filtering instead
    print("\n" + "="*80)
    print("🔑 Step 3: Trying KEYWORD filtering (no LLM)...")
    print("-"*80)

    keyword_filtered = geo_client.filter_results(raw_results, target_type='fine_dining')
    keyword_features = keyword_filtered.get('features', [])

    print(f"✅ After keyword filtering: {len(keyword_features)} restaurants kept\n")

    # Check if Oceanique is in keyword results
    for feature in keyword_features:
        props = feature.get('properties', {})
        name = props.get('name', '').lower()
        if 'oceanique' in name:
            print(f"🎯 'Oceanique' found in keyword-filtered results!")
            break
    else:
        if oceanique_in_raw:
            print("❌ 'Oceanique' was REMOVED by keyword filtering too")

    print(f"\n📋 Keyword-filtered results (first 15):")
    for idx, feature in enumerate(keyword_features[:15], 1):
        props = feature.get('properties', {})
        name = props.get('name', '')
        distance = props.get('distance', 0) / 1000
        print(f"   {idx}. {name} ({distance:.2f} km)")

    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"Raw Geoapify results: {len(raw_features)}")
    print(f"After LLM filtering: {len(filtered_features)}")
    print(f"After keyword filtering: {len(keyword_features)}")
    print()
    print(f"Oceanique in raw results: {'✅ YES' if oceanique_in_raw else '❌ NO'}")
    print(f"Oceanique after LLM filter: {'✅ YES' if oceanique_in_filtered else '❌ NO'}")
    print()

    if not oceanique_in_raw:
        print("💡 ISSUE: Oceanique not in Geoapify results")
        print("   Solutions:")
        print("   1. Increase search radius")
        print("   2. Search specifically by name")
        print("   3. Oceanique might be categorized differently")
    elif oceanique_in_raw and not oceanique_in_filtered:
        print("💡 ISSUE: LLM filtering removed Oceanique incorrectly")
        print("   Solutions:")
        print("   1. Adjust LLM prompt to be less aggressive")
        print("   2. Use keyword filtering instead")
        print("   3. Increase result limit before filtering")


if __name__ == "__main__":
    main()
