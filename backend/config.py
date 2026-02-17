"""
Configuration for Happy Pastures Creamery API
"""
import os
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, use environment variables
    pass

# ============================================================================
# API KEYS - MUST be set via environment variables!
# ============================================================================
GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
if not GEOAPIFY_API_KEY:
    raise ValueError("GEOAPIFY_API_KEY environment variable is required")

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# Anthropic key is optional - will fall back to keyword filtering if not set

# ============================================================================
# Search Configuration
# ============================================================================
DEFAULT_SEARCH_RADIUS = 2500  # meters (2.5km)
MAX_SEARCH_RADIUS = 5000      # meters (5km)
DEFAULT_RESULT_LIMIT = 100

# Use LLM filtering by default (more accurate)
USE_LLM_FILTERING = True
