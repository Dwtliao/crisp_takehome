"""
Geoapify API Client for Restaurant Prospecting
"""
import requests
import json
from typing import Optional, List, Dict, Any

class GeoapifyClient:
    """Client for interacting with Geoapify Places API"""

    BASE_URL = "https://api.geoapify.com/v2/places"

    # Exclusion lists for post-processing
    EXCLUDED_CATEGORIES = {
        'catering.restaurant.asian',
        'catering.restaurant.chinese',
        'catering.restaurant.japanese',
        'catering.restaurant.thai',
        'catering.restaurant.korean',
        'catering.restaurant.vietnamese',
        'catering.restaurant.indian',
        'catering.restaurant.pizza',
        'catering.fast_food',
        'catering.cafe',
        'catering.ice_cream'
    }

    EXCLUDED_NAME_KEYWORDS = {
        # Coffee/Cafe
        'coffee', 'cafe', 'espresso', 'latte',

        # Pizza
        'pizza', 'pizzeria', 'pie',

        # Fast Food - Burgers/Tacos
        'taco', 'tacos', 'burger', 'burgers',

        # Asian (name-based) - EXPANDED
        'ramen', 'thai', 'sushi', 'noodle', 'noodles',
        'pho', 'teriyaki', 'wok', 'asian', 'china', 'chinese',
        'japan', 'japanese', 'korea', 'korean', 'vietnam', 'vietnamese',
        'india', 'indian', 'curry', 'tikka', 'tandoor', 'biryani',
        'dim sum', 'dumpling', 'bao', 'szechuan', 'hunan', 'cantonese',
        'hibachi', 'yakitori', 'izakaya', 'udon', 'soba', 'tempura',
        'pad thai', 'kimchi', 'bulgogi', 'bibimbap', 'tofu', 'miso',
        'siam', 'shinsen', 'todoroki', 'kansaku', 'soban',
        'paragon', 'samosa', 'panang', 'massaman', 'laksa',

        # Middle Eastern Fast Casual
        'kabob', 'kebab', 'shawarma', 'falafel', 'gyro',

        # Mexican Fast Casual
        'burrito', 'taco', 'tacos', 'taqueria', 'mexican',
        'tipico', 'taquito',

        # Casual/Fast Food
        'bagel', 'bagels', 'deli', 'buffalo', 'wings',
        'sandwich', 'sandwiches', 'hoagie', 'sub',
        'donut', 'donuts', 'diner',
        'grill', 'inn', 'tavern', 'tap', 'pita',
        'kitchen', 'eats', 'eatery',

        # Fast Food Chains
        "chili's", 'chipotle', 'starbucks', 'dunkin',
        'mcdonald', "mcdonald's", 'subway', 'panera',
        'taco bell', 'panda express', 'olive garden',
        'applebee', 'buffalo wild wings', 'red lobster',
        "wendy's", 'arbys', "arby's", 'kfc', 'popeyes',
        'five guys', 'shake shack', 'jimmy john',
        'potbelly', 'qdoba', "moe's", 'del taco',
        'ihop', 'dennys', "denny's", 'waffle house',
        'cracker barrel', 'golden corral', 'cici', 'pizza hut',
        'domino', 'papa john', 'little caesar'
    }

    def __init__(self, api_key: str, anthropic_api_key: Optional[str] = None):
        """
        Initialize Geoapify client

        Args:
            api_key: Your Geoapify API key
            anthropic_api_key: Optional Anthropic API key for LLM-based filtering
        """
        self.api_key = api_key
        self.anthropic_api_key = anthropic_api_key

    def filter_results(self, results: Dict[str, Any], target_type: str = 'all') -> Dict[str, Any]:
        """
        Post-process API results to exclude incompatible restaurants

        Args:
            results: Raw API response
            target_type: 'fine_dining', 'gastropub', or 'all'

        Returns:
            Filtered results with incompatible places removed
        """
        if not results or 'features' not in results:
            return results

        filtered_features = []

        for feature in results.get('features', []):
            props = feature.get('properties', {})
            name = props.get('name', '').lower()
            categories = props.get('categories', [])

            # Skip if no name or name is empty
            if not name or name.strip() == '':
                continue

            # Check if any excluded category matches
            has_excluded_category = any(
                cat in self.EXCLUDED_CATEGORIES for cat in categories
            )

            # Check if name contains excluded keywords
            has_excluded_keyword = any(
                keyword in name for keyword in self.EXCLUDED_NAME_KEYWORDS
            )

            # Skip if excluded
            if has_excluded_category or has_excluded_keyword:
                continue

            # Type-specific filtering
            if target_type == 'fine_dining':
                # Look for fine dining signals
                if self._is_fine_dining_candidate(name, categories, props):
                    filtered_features.append(feature)
            elif target_type == 'gastropub':
                # Look for gastropub signals
                if self._is_gastropub_candidate(name, categories, props):
                    filtered_features.append(feature)
            else:
                # Keep all non-excluded restaurants
                filtered_features.append(feature)

        # Update results with filtered features
        filtered_results = results.copy()
        filtered_results['features'] = filtered_features

        return filtered_results

    def _is_fine_dining_candidate(self, name: str, categories: List[str], props: Dict) -> bool:
        """Check if restaurant is a fine dining candidate"""

        # Fine dining category indicators
        fine_dining_categories = {
            'catering.restaurant.fine_dining',
            'catering.restaurant.french',
            'catering.restaurant.italian',
            'catering.restaurant.european',
            'catering.restaurant.steak_house',
            'catering.restaurant.seafood',
            'catering.restaurant.mediterranean'
        }

        # Check if has explicit fine dining category
        if any(cat in fine_dining_categories for cat in categories):
            return True

        # Name-based signals for Italian restaurants
        italian_signals = ['trattoria', 'osteria', 'ristorante', 'italian', 'tuscany', 'venice', 'sicily', 'roma', 'florence']
        if any(signal in name for signal in italian_signals):
            return True

        # Name-based signals for French restaurants
        # Be careful with "cafe" - only count it if there are other French signals
        french_signals_strong = ['le ', 'la ', 'bistro', 'brasserie', 'chez', 'maison', 'french', 'paris', 'provence']
        if any(signal in name for signal in french_signals_strong):
            return True

        # "Cafe" only counts as French if combined with other signals
        if 'cafe' in name and not any(excl in name for excl in ['coffee', 'espresso', 'bagel', 'corner']):
            # Check if it has French article or other French words
            if any(signal in name for signal in ['le ', 'la ', 'du ', 'des ', 'au ']):
                return True

        # Name-based signals for steakhouses
        steakhouse_signals = ['steakhouse', 'steak house', 'chophouse', 'chop house', 'prime', 'butcher']
        if any(signal in name for signal in steakhouse_signals):
            return True

        # High price level is a good signal
        if props.get('price_level', 0) >= 3:
            return True

        # Otherwise not a match
        return False

    def _is_gastropub_candidate(self, name: str, categories: List[str], props: Dict) -> bool:
        """Check if restaurant is a gastropub candidate"""

        # Gastropub category indicators
        gastropub_categories = {
            'catering.pub',
            'catering.bar',
            'catering.restaurant.american'
        }

        # Check if has gastropub category
        if any(cat in gastropub_categories for cat in categories):
            return True

        # Name-based signals
        gastropub_signals = ['pub', 'tavern', 'tap', 'brewing', 'brewery', 'grill', 'ale house']
        if any(signal in name for signal in gastropub_signals):
            return True

        return False

    def classify_with_llm(self, name: str, categories: List[str], props: Dict, target_type: str) -> bool:
        """
        Use LLM to classify if restaurant is suitable for artisan cheese sales

        Args:
            name: Restaurant name
            categories: List of categories
            props: Restaurant properties
            target_type: 'fine_dining' or 'all'

        Returns:
            True if suitable, False if should be excluded
        """
        if not self.anthropic_api_key:
            return True  # Fall back to keyword filtering if no API key

        # Build context about the restaurant
        context = {
            'name': name,
            'categories': categories[:5],  # Limit to first 5
            'price_level': props.get('price_level', 'unknown'),
        }

        if target_type == 'fine_dining':
            prompt = f"""Analyze this restaurant and determine if it's suitable for selling high-end artisan cheese (Pasture Bloom Triple Crème - a delicate, expensive triple crème cheese for fine dining).

Restaurant: {json.dumps(context, indent=2)}

Exclude if:
- Fast food or chain restaurant (IHOP, McDonald's, Chipotle, etc.)
- Casual dining (grills, diners, taverns, inns)
- Pizza places, Asian restaurants, Mexican fast-casual
- Coffee shops, cafes, bagel shops, delis
- Any place with casual indicators in name (kitchen, eats, eatery, grill)

Include if:
- Fine dining (French, Italian, European, steakhouse, upscale seafood)
- Name suggests upscale (Trattoria, Bistro, Le/La/Chez, etc.)
- High price level

Answer with just "SUITABLE" or "EXCLUDE" and brief reason."""
        else:
            prompt = f"""Analyze this restaurant and determine if it's suitable for selling artisan cheese (any upscale restaurant).

Restaurant: {json.dumps(context, indent=2)}

Exclude if:
- Fast food or chain restaurant
- Pizza, Asian, Mexican fast-casual
- Coffee shops, delis, bagel shops

Include if:
- Any upscale restaurant, any cuisine
- Creative menu, quality focus

Answer with just "SUITABLE" or "EXCLUDE" and brief reason."""

        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': self.anthropic_api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json={
                    'model': 'claude-3-haiku-20240307',  # Fast, cheap model
                    'max_tokens': 100,
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ]
                },
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                answer = result['content'][0]['text'].strip().upper()
                return 'SUITABLE' in answer
            else:
                # Fall back to keyword filtering on error
                return True

        except Exception as e:
            # Fall back to keyword filtering on error
            print(f"LLM classification error: {e}")
            return True

    def classify_batch_with_llm(self, restaurants: List[Dict], target_type: str) -> List[bool]:
        """
        Classify multiple restaurants in a single LLM call (much faster!)

        Args:
            restaurants: List of restaurant dicts with 'name', 'categories', 'props'
            target_type: 'upscale' or 'fine_dining' or 'all'

        Returns:
            List of booleans (True = keep, False = exclude)
        """
        if not self.anthropic_api_key or not restaurants:
            return [True] * len(restaurants)

        # Build batch prompt
        restaurant_list = []
        for i, r in enumerate(restaurants):
            restaurant_list.append(f"{i+1}. {r['name']} - Categories: {', '.join(r['categories'][:3])}")

        restaurants_text = "\n".join(restaurant_list)

        # Single unified prompt for high-quality restaurants
        prompt = f"""Hillary sells premium artisan cheeses ($30-50/lb) and needs high-quality restaurant prospects.

CRITICAL: Cheese/dairy does NOT pair well with Asian cuisines. We must filter out ALL Asian restaurants.

Restaurants to evaluate:
{restaurants_text}

KEEP if restaurant is:
✓ Fine dining: French (Bistro, Brasserie), Italian (Trattoria, Osteria), European
✓ Upscale steakhouses, upscale seafood (like Oceanique)
✓ Quality casual: Tapas bars (like Tapas Barcelona), upscale cafes (Bluestone Cafe)
✓ Chef-driven, creative menus, would use artisan ingredients
✓ Mediterranean, Middle Eastern (if cheese-friendly)
✓ Likely $20+ entrees, quality-focused

EXCLUDE if:
✗ No name or "Unknown" - cannot prospect without a proper restaurant name
✗ Fast food or chains (IHOP, Applebee's, Chipotle, Olive Garden, etc.)
✗ Obvious casual: diners, "grill", "kitchen", "eats", taverns, sports bars
✗ Pizza places (unless upscale wood-fired)
✗ **ANY Asian cuisine**: Chinese, Japanese, Thai, Korean, Vietnamese, Indian, Malaysian, Indonesian, Filipino
✗ Asian restaurants (even if upscale): Sushi, ramen, pho, curry, dim sum, hibachi, izakaya, yakitori
✗ Asian-sounding names: Siam, Paragon, Shinsen, Todoroki, Kansaku, Soban, any Japanese/Thai/Chinese/Korean/Indian names
✗ Mexican fast-casual (burrito, taco shops)
✗ Coffee shops (unless clearly upscale cafe with food menu)
✗ Delis, bagel shops, sandwich shops

**IMPORTANT**: Be very strict with Asian cuisine. Even if it looks upscale, if the name sounds Asian or the cuisine is Asian, EXCLUDE it. Cheese does not pair well with Asian food.

When in doubt: Would this restaurant appreciate and USE a $40/lb artisan cheese in their dishes? If yes, KEEP. If no or unsure, EXCLUDE.

For each number: "1. KEEP" or "1. EXCLUDE". One per line."""

        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': self.anthropic_api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json={
                    'model': 'claude-3-haiku-20240307',
                    'max_tokens': 500,
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ]
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                answer = result['content'][0]['text'].strip()

                # Parse the response
                decisions = []
                for line in answer.split('\n'):
                    line = line.strip().upper()
                    if 'KEEP' in line:
                        decisions.append(True)
                    elif 'EXCLUDE' in line:
                        decisions.append(False)

                # Make sure we have enough decisions
                while len(decisions) < len(restaurants):
                    decisions.append(True)  # Default to keeping if parsing fails

                return decisions[:len(restaurants)]
            else:
                print(f"⚠️  LLM API error: {response.status_code}, falling back to keyword filtering")
                return [True] * len(restaurants)

        except Exception as e:
            print(f"⚠️  LLM error: {e}, falling back to keyword filtering")
            return [True] * len(restaurants)

    def filter_results_with_llm(self, results: Dict[str, Any], target_type: str = 'all') -> Dict[str, Any]:
        """
        Post-process results using LLM classification (BATCH MODE - much faster!)

        Args:
            results: Raw API response
            target_type: 'fine_dining' or 'all'

        Returns:
            Filtered results
        """
        if not results or 'features' not in results:
            return results

        if not self.anthropic_api_key:
            print("⚠️  No Anthropic API key provided, using keyword filtering")
            return self.filter_results(results, target_type)

        features = results.get('features', [])
        print(f"🤖 Using LLM to classify {len(features)} restaurants in batches...")

        # Process in batches of 20 for better performance
        BATCH_SIZE = 20
        filtered_features = []

        for i in range(0, len(features), BATCH_SIZE):
            batch = features[i:i+BATCH_SIZE]

            # Prepare batch data
            batch_data = []
            for feature in batch:
                props = feature.get('properties', {})
                batch_data.append({
                    'name': props.get('name', ''),
                    'categories': props.get('categories', []),
                    'props': props
                })

            # Classify batch
            print(f"   Processing batch {i//BATCH_SIZE + 1}/{(len(features)-1)//BATCH_SIZE + 1}...")
            decisions = self.classify_batch_with_llm(batch_data, target_type)

            # Keep restaurants that passed
            for feature, keep in zip(batch, decisions):
                if keep:
                    filtered_features.append(feature)

        print(f"✅ LLM kept {len(filtered_features)}/{len(features)} restaurants after filtering\n")

        # Update results with filtered features
        filtered_results = results.copy()
        filtered_results['features'] = filtered_features

        return filtered_results

    def search_places(
        self,
        lat: float,
        lon: float,
        radius: int = 1000,
        categories: Optional[List[str]] = None,
        cuisines: Optional[List[str]] = None,
        price_level: Optional[int] = None,
        stars: Optional[int] = None,
        dress_code: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search for places near a location

        Args:
            lat: Latitude of search center
            lon: Longitude of search center
            radius: Search radius in meters (default: 1000m = 1km)
            categories: List of place categories (e.g., ['catering.restaurant', 'catering.cafe'])
            cuisines: List of cuisine types (e.g., ['french', 'italian', 'steak'])
            price_level: Price level filter (1=budget, 2=moderate, 3=expensive, 4=very expensive)
            stars: Minimum star rating (1-5)
            dress_code: Dress code filter (e.g., 'formal', 'casual')
            filters: Additional attribute filters (e.g., {'wifi': True, 'wheelchair': 'yes'})
            limit: Maximum number of results (default: 20, max: 500)

        Returns:
            API response as dictionary
        """
        params = {
            'apiKey': self.api_key,
            'lat': lat,
            'lon': lon,
            'radius': radius,
            'limit': limit
        }

        # Add categories filter
        if categories:
            params['categories'] = ','.join(categories)

        # Build conditions (filter parameter)
        conditions = []

        # Add cuisine filters (can be multiple)
        if cuisines:
            for cuisine in cuisines:
                conditions.append(f"cuisine:{cuisine}")

        # Add upscale signals
        if price_level:
            conditions.append(f"price_level:{price_level}")

        if stars:
            conditions.append(f"stars:{stars}")

        if dress_code:
            conditions.append(f"dress_code:{dress_code}")

        # Add other attribute filters
        if filters:
            for key, value in filters.items():
                if isinstance(value, bool):
                    conditions.append(f"{key}:{str(value).lower()}")
                else:
                    conditions.append(f"{key}:{value}")

        # Combine all conditions with comma separator
        if conditions:
            params['conditions'] = ','.join(conditions)

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return {}

    def print_results(self, results: Dict[str, Any]) -> None:
        """Pretty print search results"""
        if not results or 'features' not in results:
            print("No results found or error occurred")
            return

        features = results.get('features', [])
        print(f"\nFound {len(features)} places:\n")
        print("=" * 80)

        for idx, feature in enumerate(features, 1):
            props = feature.get('properties', {})

            # Basic info
            name = props.get('name', 'Unnamed')
            address = props.get('address_line2', 'No address')
            categories = props.get('categories', [])

            # Distance
            distance = props.get('distance', 0)
            distance_km = distance / 1000 if distance else 0

            print(f"{idx}. {name}")
            print(f"   Address: {address}")
            print(f"   Distance: {distance_km:.2f} km")
            print(f"   Categories: {', '.join(categories[:3])}")

            # Show upscale signals
            upscale_signals = []
            if props.get('price_level'):
                price_symbols = '$' * props.get('price_level')
                upscale_signals.append(f"Price: {price_symbols}")
            if props.get('stars'):
                upscale_signals.append(f"Stars: {'⭐' * int(props.get('stars'))}")
            if props.get('dress_code'):
                upscale_signals.append(f"Dress: {props.get('dress_code')}")

            if upscale_signals:
                print(f"   🎯 {', '.join(upscale_signals)}")

            # Show available amenities
            amenities = []
            if props.get('wifi'):
                amenities.append('Wi-Fi')
            if props.get('wheelchair') == 'yes':
                amenities.append('Wheelchair accessible')
            if props.get('outdoor_seating'):
                amenities.append('Outdoor seating')
            if props.get('takeaway'):
                amenities.append('Takeaway')
            if props.get('delivery'):
                amenities.append('Delivery')

            if amenities:
                print(f"   Amenities: {', '.join(amenities)}")

            print()

