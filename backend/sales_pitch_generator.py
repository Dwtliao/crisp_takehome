"""
Sales Pitch Generator for Happy Pastures Creamery

Uses AI to analyze restaurant data and generate customized sales pitches
that Hillary can use when visiting restaurants door-to-door.
"""
import requests
from typing import Dict, Any, List, Optional
from cheese_products import CHEESE_PRODUCTS, get_cheese_by_id


class SalesPitchGenerator:
    """Generates customized sales pitches using Claude AI"""

    def __init__(self, anthropic_api_key: str):
        """
        Initialize the pitch generator

        Args:
            anthropic_api_key: Anthropic API key for Claude
        """
        self.api_key = anthropic_api_key

    def determine_cheese_match(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine which cheese(s) are the best fit for this restaurant

        Args:
            restaurant_data: Restaurant info from Google Places

        Returns:
            Dict with cheese recommendations and confidence scores
        """
        # Extract restaurant characteristics
        name = restaurant_data.get('name', '')
        types = restaurant_data.get('types', [])
        reviews = restaurant_data.get('reviews', [])
        price = restaurant_data.get('price', 'N/A')

        # Get menu hints from reviews
        menu_hints = []
        for review in reviews[:5]:
            text = review.get('text', '').lower()
            menu_hints.append(text)

        menu_text = ' '.join(menu_hints)

        # Analyze restaurant type
        restaurant_types_lower = [t.lower() for t in types]

        # Simple rule-based matching
        pasture_bloom_score = 0
        smoky_alder_score = 0

        # Fine dining indicators → Pasture Bloom
        fine_dining_keywords = ['fine_dining', 'french', 'italian', 'european', 'bistro', 'upscale', 'tasting']
        for keyword in fine_dining_keywords:
            if any(keyword in t for t in restaurant_types_lower):
                pasture_bloom_score += 2

        # Menu mentions
        if any(word in menu_text for word in ['duck', 'scallop', 'lobster', 'tasting', 'amuse', 'champagne']):
            pasture_bloom_score += 1

        # Gastropub/tavern indicators → Smoky Alder
        gastropub_keywords = ['pub', 'gastropub', 'tavern', 'bar', 'american', 'burger', 'grill']
        for keyword in gastropub_keywords:
            if any(keyword in t for t in restaurant_types_lower):
                smoky_alder_score += 2

        # Menu mentions
        if any(word in menu_text for word in ['burger', 'bacon', 'bbq', 'smoke', 'beer', 'wood-fired', 'charcuterie']):
            smoky_alder_score += 1

        # Price level can indicate fine dining
        if price in ['$$$', '$$$$']:
            pasture_bloom_score += 1
        elif price in ['$$', '$$$']:
            smoky_alder_score += 1

        # Determine primary recommendation
        if pasture_bloom_score > smoky_alder_score:
            primary_cheese = "pasture_bloom"
            secondary_cheese = "smoky_alder" if smoky_alder_score > 0 else None
            confidence = "high" if pasture_bloom_score >= 3 else "medium"
        elif smoky_alder_score > pasture_bloom_score:
            primary_cheese = "smoky_alder"
            secondary_cheese = "pasture_bloom" if pasture_bloom_score > 0 else None
            confidence = "high" if smoky_alder_score >= 3 else "medium"
        else:
            # Tie or both low - default to Smoky Alder (more versatile)
            primary_cheese = "smoky_alder"
            secondary_cheese = "pasture_bloom"
            confidence = "low"

        return {
            "primary_cheese": primary_cheese,
            "secondary_cheese": secondary_cheese,
            "confidence": confidence,
            "scores": {
                "pasture_bloom": pasture_bloom_score,
                "smoky_alder": smoky_alder_score
            }
        }

    def detect_asian_cuisine(self, restaurant_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if restaurant serves Asian cuisine (dairy-incompatible)

        Args:
            restaurant_data: Restaurant info from Google Places

        Returns:
            Dict with is_asian (bool), confidence (str), and reasons (list)
        """
        name = restaurant_data.get('name', '').lower()
        types = [t.lower() for t in restaurant_data.get('types', [])]
        reviews = restaurant_data.get('reviews', [])

        # Get menu text from reviews
        menu_text = ' '.join([r.get('text', '').lower() for r in reviews[:5]])

        # Asian cuisine indicators
        asian_keywords = {
            'strong': [
                'sushi', 'ramen', 'pho', 'pad thai', 'dim sum', 'curry', 'tikka',
                'tandoor', 'bibimbap', 'bulgogi', 'teriyaki', 'tempura', 'udon',
                'soba', 'miso', 'kimchi', 'dumpling', 'bao', 'noodle', 'wok',
                'szechuan', 'hunan', 'cantonese', 'thai', 'chinese', 'japanese',
                'korean', 'vietnamese', 'indian', 'asian', 'siam', 'tofu'
            ],
            'moderate': [
                'rice bowl', 'stir fry', 'spring roll', 'edamame', 'sake',
                'wasabi', 'ginger', 'soy sauce', 'sesame'
            ]
        }

        asian_types = [
            'asian', 'chinese', 'japanese', 'thai', 'korean', 'vietnamese', 'indian'
        ]

        reasons = []
        score = 0

        # Check restaurant types (strongest signal)
        for asian_type in asian_types:
            if any(asian_type in t for t in types):
                reasons.append(f"Restaurant type: {asian_type}")
                score += 10

        # Check name for strong keywords
        for keyword in asian_keywords['strong']:
            if keyword in name:
                reasons.append(f"Name contains: {keyword}")
                score += 5
                break  # Only count once for name

        # Check menu/reviews for strong keywords
        strong_menu_matches = [kw for kw in asian_keywords['strong'] if kw in menu_text]
        if len(strong_menu_matches) >= 3:
            reasons.append(f"Menu mentions: {', '.join(strong_menu_matches[:3])}")
            score += len(strong_menu_matches)

        # Check menu for moderate keywords
        moderate_menu_matches = [kw for kw in asian_keywords['moderate'] if kw in menu_text]
        if len(moderate_menu_matches) >= 2:
            score += 1

        # Determine result
        is_asian = score >= 5
        confidence = 'high' if score >= 10 else 'medium' if score >= 5 else 'low'

        return {
            'is_asian': is_asian,
            'confidence': confidence,
            'score': score,
            'reasons': reasons
        }

    def generate_sales_pitch(
        self,
        restaurant_data: Dict[str, Any],
        cheese_match: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a customized sales pitch using Claude AI

        Args:
            restaurant_data: Restaurant info from Google Places
            cheese_match: Cheese matching results

        Returns:
            Complete sales pitch with talking points, pairings, etc.
        """
        primary_cheese_id = cheese_match['primary_cheese']
        primary_cheese = get_cheese_by_id(primary_cheese_id)

        # Build context for Claude
        restaurant_context = self._build_restaurant_context(restaurant_data)
        cheese_context = self._build_cheese_context(primary_cheese)

        # Generate pitch with Claude
        prompt = f"""You are a sales assistant helping Hillary from Happy Pastures Creamery sell artisan cheese to restaurants.

RESTAURANT PROFILE:
{restaurant_context}

CHEESE PRODUCT TO PITCH:
{cheese_context}

Generate a compelling, concise sales pitch that Hillary can use when she walks into this restaurant. The pitch should:

1. **Opening Hook** (1-2 sentences): Why this cheese is perfect for THIS specific restaurant
2. **3-4 Specific Menu Pairings**: Real dishes from their reviews/menu that would work beautifully with this cheese
3. **Key Selling Points** (2-3 bullets): What makes HPC cheese special (local, sustainable, small-batch, etc.)
4. **Competitive Advantage**: Why artisan > generic cheese for their menu
5. **Call to Action**: Simple next step (sample order, tasting, etc.)

Keep it conversational and focused on THEIR menu and THEIR customers. Hillary will read this on her phone before walking in, so keep it scannable and practical.

Format as JSON:
{{
  "opening_hook": "...",
  "menu_pairings": [
    {{"dish": "...", "why_it_works": "..."}},
    ...
  ],
  "selling_points": ["...", "...", "..."],
  "competitive_advantage": "...",
  "call_to_action": "..."
}}"""

        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': self.api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json={
                    'model': 'claude-sonnet-4-5-20250929',  # Latest Sonnet 4.5
                    'max_tokens': 1500,
                    'temperature': 0.7,
                    'messages': [
                        {'role': 'user', 'content': prompt}
                    ]
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']

                # Parse JSON from response
                import json
                # Extract JSON from markdown code blocks if present
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                pitch_data = json.loads(content)

                # Add metadata
                pitch_data['cheese'] = {
                    'id': primary_cheese_id,
                    'name': primary_cheese['name'],
                    'subtitle': primary_cheese['subtitle'],
                    'price_lb': primary_cheese['typical_price_lb']
                }
                pitch_data['restaurant'] = {
                    'name': restaurant_data.get('name'),
                    'address': restaurant_data.get('address'),
                    'phone': restaurant_data.get('phone')
                }
                pitch_data['confidence'] = cheese_match['confidence']

                return pitch_data

            else:
                print(f"⚠️  Claude API error: {response.status_code}")
                return self._generate_fallback_pitch(restaurant_data, primary_cheese)

        except Exception as e:
            print(f"⚠️  Error generating pitch: {e}")
            return self._generate_fallback_pitch(restaurant_data, primary_cheese)

    def _build_restaurant_context(self, restaurant_data: Dict[str, Any]) -> str:
        """Build restaurant context string for Claude"""
        name = restaurant_data.get('name', 'Unknown')
        types = ', '.join(restaurant_data.get('types', [])[:5])
        price = restaurant_data.get('price', 'N/A')
        rating = restaurant_data.get('rating', 'N/A')
        reviews = restaurant_data.get('reviews', [])

        context = f"Name: {name}\n"
        context += f"Type: {types}\n"
        context += f"Price Level: {price}\n"
        context += f"Rating: {rating}/5\n\n"

        context += "Menu Hints from Recent Reviews:\n"
        for i, review in enumerate(reviews[:3], 1):
            text = review.get('text', '')[:200]
            context += f"{i}. {text}...\n"

        return context

    def _build_cheese_context(self, cheese: Dict[str, Any]) -> str:
        """Build cheese context string for Claude"""
        context = f"{cheese['name']} ({cheese['subtitle']})\n\n"
        context += f"Description: {cheese['full_description']}\n\n"
        context += f"Ideal Uses: {', '.join(cheese['ideal_uses'][:5])}\n"
        context += f"Price: {cheese['typical_price_lb']} per lb\n"
        return context

    def _generate_fallback_pitch(
        self,
        restaurant_data: Dict[str, Any],
        cheese: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a simple fallback pitch if AI fails"""
        return {
            "opening_hook": f"{cheese['name']} would be a perfect addition to your menu - it's a locally-sourced, small-batch artisan cheese that brings unique flavor and story to your dishes.",
            "menu_pairings": [
                {
                    "dish": "Cheese plate or appetizer",
                    "why_it_works": "Showcases the cheese's unique characteristics"
                },
                {
                    "dish": "Featured in a signature dish",
                    "why_it_works": "Creates menu differentiation"
                }
            ],
            "selling_points": cheese['selling_points'][:3],
            "competitive_advantage": "Local, sustainable, small-batch production means better quality and a story your customers will love.",
            "call_to_action": "How about a complimentary sample to try in your kitchen?",
            "cheese": {
                "id": "unknown",
                "name": cheese['name'],
                "subtitle": cheese['subtitle'],
                "price_lb": cheese['typical_price_lb']
            },
            "restaurant": {
                "name": restaurant_data.get('name'),
                "address": restaurant_data.get('address'),
                "phone": restaurant_data.get('phone')
            },
            "confidence": "low"
        }
