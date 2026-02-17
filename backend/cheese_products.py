"""
Happy Pastures Creamery - Product Catalog

Contains full descriptions of artisan cheese products for:
- Sales pitch generation
- Semantic matching with restaurant menus
- Text embeddings for recommendation systems
"""

# Product catalog
CHEESE_PRODUCTS = {
    "pasture_bloom": {
        "name": "Pasture Bloom Triple Crème",
        "subtitle": "Seasonal, Bloomy-Rind",
        "full_description": "A decadent, high-fat, triple-crème cheese infused with a touch of cultured cream and aged just long enough to develop a delicate, edible white rind. Its texture is almost custard-like at room temp, making it ideal for fine-dining dishes like savory pastries, cheese-forward sauces, or composed appetizers. Too rich and delicate for retail, it works beautifully on tasting menus where plating precision and immediate table service keep it at peak quality.",

        # Target customers
        "target_restaurants": [
            "fine dining",
            "French cuisine",
            "Italian restaurants",
            "European bistros",
            "tasting menu restaurants",
            "upscale seafood"
        ],

        # Ideal menu applications
        "ideal_uses": [
            "Savory pastries",
            "Cheese-forward sauces",
            "Composed appetizers",
            "Tasting menus",
            "Cheese plates",
            "Amuse-bouche",
            "Paired with champagne/white wine"
        ],

        # Key selling points
        "selling_points": [
            "Luxurious custard-like texture",
            "Delicate bloomy rind",
            "High-fat triple crème (perfect for rich dishes)",
            "Peak quality when served at room temp",
            "Locally sourced and sustainably crafted",
            "Small-batch seasonal production",
            "Ideal for plated presentations"
        ],

        # Pairing suggestions
        "pairings": {
            "proteins": ["Duck", "Scallops", "Lobster", "Prosciutto"],
            "produce": ["Figs", "Apples", "Pears", "Truffle", "Mushrooms"],
            "wines": ["Champagne", "Chardonnay", "Sauvignon Blanc"],
            "flavors": ["Honey", "Herbs", "Light citrus", "Toasted nuts"]
        },

        # Price tier (for B2B sales)
        "price_tier": "premium",
        "typical_price_lb": "$32-38",

        # Production details
        "production": {
            "batch_size": "Small-batch",
            "availability": "Seasonal",
            "lead_time_days": 7,
            "minimum_order_lbs": 3
        }
    },

    "smoky_alder": {
        "name": "Smoky Alder Wash Rind",
        "subtitle": "Small-Batch, Semi-Soft",
        "full_description": "A pungent, washed-rind cheese matured with a house brine and cold-smoked over locally sourced alder wood. It delivers deep umami and subtle smoke that pairs perfectly with elevated tavern menus, gastropub burgers, charcuterie programs, and wood-fired dishes. Its assertive aroma makes it unsuitable for grocery shelves but highly prized by chefs who want a bold, signature flavor component.",

        # Target customers
        "target_restaurants": [
            "gastropubs",
            "taverns",
            "upscale American",
            "wood-fired restaurants",
            "craft beer bars",
            "burger joints (elevated)",
            "charcuterie-focused"
        ],

        # Ideal menu applications
        "ideal_uses": [
            "Gastropub burgers",
            "Charcuterie boards",
            "Wood-fired pizzas",
            "Mac and cheese",
            "Grilled cheese sandwiches",
            "Beer pairing menus",
            "Smoked meat dishes"
        ],

        # Key selling points
        "selling_points": [
            "Bold, assertive flavor profile",
            "Locally sourced alder wood smoking",
            "Deep umami character",
            "Washed-rind complexity",
            "Perfect for elevated pub fare",
            "Pairs beautifully with craft beer",
            "Signature ingredient for menu differentiation"
        ],

        # Pairing suggestions
        "pairings": {
            "proteins": ["Bacon", "Brisket", "Short rib", "Pulled pork", "Sausage"],
            "produce": ["Caramelized onions", "Roasted peppers", "Pickles", "Arugula"],
            "beverages": ["IPA", "Stout", "Porter", "Rye whiskey", "Red wine"],
            "flavors": ["Smoke", "Mustard", "BBQ sauce", "Pickled vegetables"]
        },

        # Price tier (for B2B sales)
        "price_tier": "mid-premium",
        "typical_price_lb": "$24-28",

        # Production details
        "production": {
            "batch_size": "Small-batch",
            "availability": "Year-round",
            "lead_time_days": 5,
            "minimum_order_lbs": 5
        }
    }
}


def get_cheese_by_id(cheese_id: str) -> dict:
    """Get cheese product details by ID"""
    return CHEESE_PRODUCTS.get(cheese_id)


def get_all_cheeses() -> dict:
    """Get all cheese products"""
    return CHEESE_PRODUCTS


def get_cheese_for_embedding(cheese_id: str) -> str:
    """
    Get concatenated text for semantic embedding

    Returns a comprehensive text description suitable for:
    - Text embeddings (OpenAI, Cohere, etc.)
    - Semantic search
    - Vector similarity matching
    """
    cheese = CHEESE_PRODUCTS.get(cheese_id)
    if not cheese:
        return ""

    # Concatenate all relevant text
    embedding_text = f"""
    {cheese['name']} ({cheese['subtitle']})

    Description: {cheese['full_description']}

    Target Restaurants: {', '.join(cheese['target_restaurants'])}

    Ideal Uses: {', '.join(cheese['ideal_uses'])}

    Key Selling Points: {', '.join(cheese['selling_points'])}

    Pairs Well With:
    - Proteins: {', '.join(cheese['pairings']['proteins'])}
    - Produce: {', '.join(cheese['pairings']['produce'])}
    - Beverages: {', '.join(cheese['pairings']['beverages'])}
    - Flavors: {', '.join(cheese['pairings']['flavors'])}
    """

    return embedding_text.strip()


# Helper for quick access
PASTURE_BLOOM = CHEESE_PRODUCTS["pasture_bloom"]
SMOKY_ALDER = CHEESE_PRODUCTS["smoky_alder"]
