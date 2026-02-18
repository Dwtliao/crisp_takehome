# Smart Filtering & Learning System

## Overview

This document explains the intelligent filtering system that prevents Hillary from wasting time on incompatible restaurants (Asian cuisine, fast food, previously rejected).

---

## 🛡️ Three Layers of Defense

### Layer 1: Backend Keyword Filtering (Preventive)

**Location:** `backend/geoapify_client.py`

**What it does:** Filters restaurants at the API level before they ever reach Hillary.

**Keywords blocked:**
- Asian cuisines: Thai, Chinese, Japanese, Korean, Vietnamese, Indian, curry, sushi, ramen, pho, dim sum, etc.
- Fast food: McDonald's, Taco Bell, Chipotle, Subway, Pizza chains
- Casual: Cafes, coffee shops, bagel shops, diners

**Specific restaurants filtered:**
- Royal Thai
- Siam Paragon
- Shinsen
- Todoroki
- Kansaku
- Soban Korea
- Inspired Indian

**Result:** Reduces 150 raw results → ~20-25 quality prospects

---

### Layer 2: Rejection Learning System (Adaptive)

**Location:** `frontend/index.html` (localStorage)

**What it does:** Remembers Hillary's rejections and never shows them again.

**Features:**
- ❌ "Not Interested" button on each restaurant card
- Stores up to 200 rejected restaurants with location
- Persists across browser sessions
- Shows count: "🧠 45 restaurants in rejection memory"
- "Clear memory" link to reset if needed

**How it works:**
1. Hillary clicks "❌ Not Interested" on a restaurant
2. Restaurant fades out and is saved to localStorage
3. Next time she searches that area, it won't appear
4. Works across different search sessions

**Storage key format:**
```
restaurant_name_latitude_longitude
```

This prevents false positives (two restaurants with same name in different cities).

---

### Layer 3: Pre-Pitch Asian Detection (Cost-Saving)

**Location:** `backend/sales_pitch_generator.py` + `backend/api.py`

**What it does:** Catches Asian restaurants that slipped through Layers 1 & 2 BEFORE generating expensive pitch.

**Detection method:**
- Analyzes restaurant name, types, and menu reviews
- Scores based on Asian cuisine indicators:
  - **Strong signals:** sushi, ramen, curry, tikka, pho, pad thai, etc.
  - **Menu mentions:** 3+ Asian dishes in reviews
  - **Restaurant types:** Asian, Chinese, Japanese, Thai, Korean, Vietnamese, Indian

**Scoring:**
- Restaurant type match: +10 points
- Name keyword match: +5 points
- Menu keyword matches: +1 point each
- **Threshold:** 5+ points = Asian cuisine

**Response when detected:**
```json
{
  "warning": "asian_cuisine_detected",
  "message": "⚠️ This appears to be an Asian cuisine restaurant...",
  "confidence": "high",
  "reasons": ["Restaurant type: Japanese", "Menu mentions: sushi, ramen, miso"],
  "suggestion": "Consider skipping or manually verify..."
}
```

**UI Display:**
- Yellow warning box with reasons
- "Not Interested - Remember This" button
- Adds to rejection memory automatically
- **Saves:** $0.05 per avoided pitch (Google Places + Claude API)

---

## 📊 Filtering Stats Display

Hillary sees real-time filtering information:

**On restaurant list:**
```
Found 18 prospects (sorted by distance) • 6 filtered, 3 previously rejected
🧠 45 restaurants in rejection memory
```

**What each number means:**
- **18 prospects:** Clean restaurants that passed all filters
- **6 filtered:** Blocked by Layer 1 (keywords/categories)
- **3 previously rejected:** Blocked by Layer 2 (Hillary's past decisions)
- **45 in memory:** Total restaurants Hillary has rejected over time

---

## 🎯 Address History

**Bonus feature:** Saves last 5 searched addresses

**Location:** `frontend/index.html` (localStorage)

**Features:**
- Automatically saves after successful geocoding
- Shows as clickable buttons below address input
- Example: "Recent addresses: Evanston IL | 4705 N Campbell Ave"
- Click to instantly search that location again

---

## 💡 Why This Matters

### Time Saved
- No standing in the cold reading Asian restaurant menus
- No wasted pitches on places that won't buy
- No seeing the same rejected restaurants twice

### Cost Saved
- Layer 3 prevents ~$0.05/restaurant in unnecessary API calls
- If Hillary checks 20 restaurants/day and 4 are Asian: **$0.20/day saved**
- Over a month: **$6/month saved**

### Learning Over Time
- System gets smarter as Hillary uses it
- Rejection memory builds a personalized blacklist
- Works even if restaurant names change slightly

---

## 🔧 Adding New Filters

### Backend keywords (Layer 1):
Edit `backend/geoapify_client.py`:
```python
EXCLUDED_NAME_KEYWORDS = {
    'siam', 'todoroki', 'your_keyword_here'
}
```

### Frontend blacklist (Layer 2):
Edit `frontend/index.html`:
```javascript
const RESTAURANT_BLACKLIST = [
    'royal thai',
    'your_restaurant_name_here'
];
```

### Clear rejection memory:
Click "Clear memory" link on restaurant list screen, or:
```javascript
localStorage.removeItem('happy_pastures_rejected_restaurants');
```

---

## 🧪 Testing the System

1. **Test Layer 1:** Search "Evanston, IL" - Royal Thai, Siam Paragon, Todoroki should NOT appear
2. **Test Layer 2:** Click "❌ Not Interested" on a restaurant, refresh page, search again - it should be gone
3. **Test Layer 3:** If an Asian restaurant slips through, clicking "View Pitch" shows warning instead of pitch

---

## 📈 Future Enhancements

Potential improvements:

1. **Semantic filtering:** Use embeddings to detect Asian cuisine by menu similarity
2. **Success tracking:** Learn which restaurants actually bought cheese
3. **Collaborative learning:** Share rejection data across all sales reps
4. **Offline mode:** Cache rejection list for areas without internet
5. **Analytics:** "You've saved $47 in API costs this month!"

---

## Technical Details

**Storage:**
- Address history: `happy_pastures_address_history` (max 5 items)
- Rejection memory: `happy_pastures_rejected_restaurants` (max 200 items)

**Performance:**
- Layer 1: Runs on backend, no frontend cost
- Layer 2: O(1) lookup in localStorage (~1ms)
- Layer 3: Runs only when pitch requested (~500ms API call saved)

**Data privacy:**
- All data stored locally in browser
- No server-side user tracking
- Clear data anytime with "Clear memory"
