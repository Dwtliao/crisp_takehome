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

**Location:** `frontend/app.js` (localStorage)

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

**Location:** `frontend/app.js` (localStorage)

**Features:**
- Automatically saves after successful geocoding
- Shows as clickable buttons below address input
- Example: "Recent addresses: Evanston IL | 4705 N Campbell Ave"
- Click to instantly search that location again

---

## 📦 Location Caching: Speed for Repeated Searches

**NEW Feature:** Smart caching for frequently visited locations

**Location:** Frontend localStorage, search flow optimization

### What It Does
Caches restaurant search results for each location, enabling instant repeat searches within 7 days.

### How It Works

**Cache Key Generation:**
- Format: `loc_{lat}_{lon}` (rounded to 2 decimals)
- Example: Search at 42.048, -87.683 → key: `loc_42.05_-87.68`
- Handles minor GPS drift (same cache for nearby coordinates)

**Cache Lifecycle:**
1. **First search:** Fetch from API → Save to cache with timestamp
2. **Repeat search (<7 days):** Load from cache instantly (<100ms)
3. **Stale cache (>7 days):** Auto-delete, fetch fresh data
4. **Manual refresh:** User clicks "🔄 Refresh" → Bypass cache, fetch fresh

### Visual Indicators

**Cached Results (Blue Box):**
```
┌──────────────────────────────────────────┐
│ 📦 Cached results from 2 days ago       │
│                         [🔄 Refresh]     │
└──────────────────────────────────────────┘
```
- Shows cache age dynamically ("just now", "3 hours ago", "2 days ago")
- Prominent refresh button for manual override

**Fresh Results (Green Box):**
```
┌──────────────────────────────────────────┐
│ ✨ Fresh results just now                 │
└──────────────────────────────────────────┘
```
- Confirms data just fetched from API

### Storage Details

**localStorage Key:** `happy_pastures_location_cache`

**Data Structure:**
```javascript
{
  "loc_42.05_-87.68": {
    timestamp: "2026-02-18T10:00:00Z",
    lat: 42.05,
    lon: -87.68,
    data: {
      prospects: [...], // Full restaurant list
      total: 18,
      search_center: {lat: 42.05, lon: -87.68},
      search_radius_km: 2.5
    }
  }
}
```

### Business Value

**Speed Improvement:**
- Cached: <100ms (instant)
- Fresh API: 2-3 seconds
- **Time saved per repeat search:** 2-3 seconds (matters in winter!)

**Cost Savings:**
- First search: ~$0.001 (Geoapify + Claude Haiku)
- Repeat search (cached): $0
- **Example:** 5 searches of Evanston per week = 4 × $0.001 saved

**Hillary's Workflow:**
- Monday: Search Evanston (3 sec, $0.001) → Cached
- Tuesday: Search Evanston (instant, $0) → From cache
- Wednesday: Search Evanston (instant, $0) → From cache
- Thursday: Click refresh (3 sec, $0.001) → Fresh data
- **Result:** 4 searches = 2 API calls instead of 4

### Why 7-Day TTL?

**Business Rationale:**
- Restaurant turnover is slow (new restaurants don't open daily)
- Hillary revisits neighborhoods weekly/bi-weekly
- Balance between data freshness and speed
- Manual refresh always available for critical updates

**Cache Hit Rate Estimate:**
- Assuming Hillary walks 3 neighborhoods, revisits each 2×/week
- Week 1: 3 locations × 2 visits = 6 searches, 3 cached (50% hit rate)
- Month 1: ~24 searches, ~15 cached (62% hit rate)
- **Cumulative time saved:** ~45 seconds/month of not standing in cold

### Implementation Notes

**Cache Expiration Logic:**
```javascript
const cacheDate = new Date(cached.timestamp);
const now = new Date();
const daysSinceCached = (now - cacheDate) / (1000 * 60 * 60 * 24);

if (daysSinceCached > 7) {
  // Auto-delete expired cache
  // Fetch fresh data
}
```

**Age Display Logic:**
- < 1 hour: "just now"
- 1-23 hours: "3 hours ago"
- 1+ days: "2 days ago"

**Force Refresh:**
```javascript
searchRestaurants(lat, lon, forceRefresh = true)
```
- Bypasses cache check
- Fetches fresh from API
- Updates cache with new data

---

## 🎤 Voice Notes & Text-to-Speech

**NEW Feature:** Hands-free pitch listening and visit notes

**Location:** `frontend/app.js` (localStorage + Web Speech API)

### Text-to-Speech (TTS)
**What it does:** Converts sales pitches to audio so Hillary can listen while walking

**Features:**
- 🔊 **Play/Pause/Stop controls** - Full audio playback control
- 🔁 **Replay button** - Review pitch multiple times
- **Speed adjustment** - 0.75x, 1x, 1.25x, 1.5x playback speeds
- **Hands-free operation** - Listen via earbuds while walking to next restaurant
- **Zero cost** - Uses browser's built-in Web Speech API (no API charges)

**Browser support:** Chrome, Edge, Safari (limited), Firefox (not supported)

### Voice Notes
**What it does:** Capture visit outcomes hands-free using speech-to-text

**Features:**
- 🎤 **Voice recording** - Dictate notes after visiting restaurant
- 📝 **Live transcription** - See words appear in real-time
- 💾 **Persistent storage** - Notes saved in localStorage (survives browser/server restarts)
- 📅 **Timestamped entries** - Each note includes date/time
- 🔄 **Multiple notes per restaurant** - Track multiple visits/follow-ups
- 🗂️ **Restaurant-keyed storage** - Notes organized by `name_latitude_longitude`

**Example use cases:**
- "Manager wasn't available, follow up next Tuesday"
- "They loved the Smoky Alder sample, send invoice"
- "Already using a competitor, try again in 3 months"
- "Kitchen prefers softer cheeses, skip this one"

**Storage details:**
- Stored in: `localStorage['happy_pastures_voice_notes']`
- **Persists across:** Browser restarts, server restarts, computer restarts
- **Does NOT sync:** Each browser/device has separate notes
- **Clear data:** Browser console → `localStorage.removeItem('happy_pastures_voice_notes')`

**Browser support:** Chrome, Edge (requires microphone permissions)

**Why this matters:** Hillary can record visit outcomes immediately while details are fresh, without stopping to type on her phone in winter cold. Notes persist forever for long-term follow-up tracking.

---

## 🔄 Pitch Refinement: Adaptive Messaging

**NEW Feature:** Transform pitches for different audiences with one click

**Location:** 2-page architecture (Page 1: Original → Page 2: Refinement)

### How It Works
After viewing the original pitch, Hillary can refine it for specific audiences:

**🧑‍🍳 Chef/Kitchen Staff Refinement**
- **Tone:** Technical, peer-to-peer, culinary-focused
- **Content:** Cooking techniques, melt points, flavor chemistry
- **Length:** ~60 seconds
- **Example:** "Hey Chef, our Pasture Bloom melts at 90°F and emulsifies beautifully into beurre blanc..."

**👔 Owner/Manager Refinement**
- **Tone:** Business-focused, ROI-driven
- **Content:** Margins, menu differentiation, local sourcing value
- **Length:** ~90 seconds
- **Example:** "Local sourcing, $40/lb wholesale, high perceived value, upsell potential..."

**🎯 Host/Front Desk Refinement**
- **Tone:** Ultra-brief, respectful
- **Content:** Quick credibility, simple ask
- **Length:** ~30 seconds
- **Example:** "Hi, I work with Chef Sarah at [nearby restaurant]. When's good to drop off a sample?"

### 2-Page Mobile Architecture
**Page 1: Original Pitch**
- Full AI-generated pitch
- TTS controls at top
- Voice notes section
- "Refine This Pitch" button at bottom

**Page 2: Refinement Screen**
- Restaurant summary
- 4 persona buttons (Walking, Chef, Manager, Host)
- Refined pitch with TTS at top
- "Try Different Persona" and "Back to Original" navigation

### Refinement Prompt Templates
Each persona button applies a "style filter" to reshape the existing pitch:
- **Not regenerating from scratch** - Transforms existing content
- **Preset instructions** - Proven refinement strategies
- **One-click operation** - No complex UI
- **Reversible** - Easy to try different personas

---

## ✨ Micro-Refinements: Polishing the Pitch

**NEW Feature:** Fine-tune refined pitches with one-click adjustments

**Location:** Page 2 (Refinement Screen), appears after persona refinement

### The 5 Micro-Refinements

**📏 Shorten**
- **Goal:** Condense to 20-30 seconds spoken
- **Use case:** Time-limited situation, quick introduction
- **Prompt:** "Keep only most impactful points, remove fluff"

**📖 Expand**
- **Goal:** Add detail and concrete examples
- **Use case:** Engaged listener, time to elaborate
- **Prompt:** "Add 1-2 stories, statistics, sensory details"

**💬 More Casual**
- **Goal:** Conversational, friendly tone
- **Use case:** Informal setting, peer conversation
- **Prompt:** "Talk like a friend, use contractions, simpler words"

**🎩 More Formal**
- **Goal:** Professional, polished tone
- **Use case:** Business meeting, formal presentation
- **Prompt:** "Elevate language without stuffiness, authoritative"

**⚡ Strong Opener**
- **Goal:** Attention-grabbing first sentence
- **Use case:** Need to hook immediately
- **Prompt:** "Unexpected fact, bold statement, or compelling question"

### How It Works
1. Hillary selects persona (Chef, Manager, or Gatekeeper)
2. Refined pitch generates
3. She clicks micro-refinement button (e.g., "Shorten")
4. Claude applies focused transformation
5. Result replaces current pitch
6. Can apply multiple micro-refinements sequentially

### Cost
- **Initial pitch:** ~$0.05 (Google Places + Claude)
- **Each persona refinement:** +$0.02 (Claude only)
- **Each micro-refinement:** +$0.01 (focused prompt)
- **Load saved pitch:** $0 (localStorage)
- **Typical usage:** Generate → Refine → 1-2 micro-adjustments → Save

---

## 💾 Save & Reuse Pitches: Zero-Cost Return Visits

**NEW Feature:** Save perfected pitches to localStorage for instant reuse

**Location:** Page 2 (Refinement Screen), after generating/refining pitch

### How It Works

**Saving a Pitch:**
1. Hillary generates original pitch ($0.05)
2. Refines for persona ($0.02)
3. Applies 1-2 micro-refinements ($0.01 each)
4. Clicks **"💾 Save This Version"**
5. Pitch stored in localStorage with unique key

**Loading a Saved Pitch:**
1. Hillary returns to same restaurant later (got turned away, follow-up visit)
2. **Page 1 indicator:** "💾 Saved Pitches Available! You have saved pitches for: Chef, Manager"
3. Clicks "Refine This Pitch" to go to Page 2
4. **Saved pitch cards appear** showing each saved persona with timestamp
5. Clicks **"📖 Load This Pitch"** on desired persona
6. Pitch loads instantly ($0 API cost!)
7. Can still apply micro-refinements if situation changed

### Storage Structure

**localStorage Key:**
```javascript
localStorage['happy_pastures_saved_pitches'] = {
  "oceanique_42.05_-87.68_chef": {
    restaurant_name: "Oceanique",
    latitude: 42.05,
    longitude: 87.68,
    persona: "chef",
    persona_label: "🧑‍🍳 Chef/Kitchen Staff",
    refined_text: "Hey Chef, I've been working...",
    saved_at: "2026-02-18T09:45:00Z",
    cheese_name: "Pasture Bloom"
  }
}
```

**Key Format:** `{restaurant_name}_{lat}_{lon}_{persona}`

**Why This Format:**
- Prevents false positives (same name, different location)
- Allows multiple personas per restaurant
- Includes coordinates for precise matching
- Each persona saved separately

### Benefits

**Cost Savings:**
- First visit: $0.05 (generate) + $0.02 (refine) + $0.01-0.02 (micro-adjustments) = ~$0.08
- Return visit: $0 (load saved pitch)
- If Hillary visits 5 times before success: Saves $0.40 in API costs

**Time Savings:**
- Load saved pitch: <100ms (localStorage read)
- Generate new pitch: 3-5 seconds (API calls)
- No re-thinking, no re-polishing

**Long-Term Memory:**
- Survives browser restarts
- Survives server restarts
- Persists indefinitely unless browser data cleared
- Perfect for follow-up visits weeks/months later

**Multiple Personas Per Restaurant:**
- Save "Chef" version on first visit
- Save "Manager" version when chef refers Hillary to owner
- Save "Gatekeeper" version for front desk at large restaurants
- Each loads independently

### UI Indicators

**Page 1 (Original Pitch Screen):**
- If saved pitches exist: "💾 Saved Pitches Available! You have saved pitches for: Chef, Manager"
- Appears prominently near top of pitch
- Encourages Hillary to view saved work

**Page 2 (Refinement Screen):**
- **Saved pitch cards** appear at top before persona buttons
- Each card shows:
  - Persona icon and label (🧑‍🍳 Chef/Kitchen Staff)
  - Saved timestamp (Feb 18, 2026 9:45 AM)
  - "📖 Load This Pitch" button
- Can load any saved persona or generate new one

### Workflow Example

**First Visit (Manager wasn't available):**
1. Generate pitch ($0.05)
2. Refine for Chef ($0.02)
3. Shorten it ($0.01)
4. Save ($0)
5. **Total cost: $0.08**

**Return Visit (Caught manager this time):**
1. View saved pitch indicator on Page 1
2. Go to refinement screen
3. Generate NEW pitch for Manager persona ($0.02)
4. Save manager version ($0)
5. **Now has 2 saved pitches for same restaurant**

**Third Visit (Need to get past host first):**
1. Load saved Chef pitch ($0)
2. Review it
3. Also generate Gatekeeper pitch for front desk ($0.02)
4. Save gatekeeper version ($0)
5. **Now has 3 saved pitches**

### Technical Details
- **Storage limit:** ~5-10MB per origin (browser-dependent)
- **Estimated capacity:** 100-200 saved pitches before hitting limit
- **Performance:** O(1) lookup by key (<1ms)
- **Persistence:** Until browser data cleared or localStorage.removeItem() called
- **Multi-device:** Not synced (each browser has separate storage)

### Why This Matters
**Situational Adaptability:**
- Talking to host first? Use gatekeeper pitch
- Meeting with chef? Use technical version
- Pitching to owner? Use business-focused version

**Time Efficiency:**
- No manual rewriting needed
- Instant adaptation to situation
- TTS for both original and refined versions

**Mobile-First UX:**
- No endless scrolling
- Clear navigation between pages
- Each screen has focused purpose

---

## 💡 Why This Matters - Business Value

### Time Saved = Money Earned
- **No standing in winter cold** reading Asian restaurant menus
- **No wasted pitches** on fast food chains that won't buy $40/lb cheese
- **No repeat visits** - rejection memory learns from Hillary's decisions
- **Walking directions** optimize route planning block-by-block

### Cost Saved = Higher Margins
- Layer 3 Asian detection prevents ~$0.05/restaurant in unnecessary API calls
- If Hillary checks 20 restaurants/day and 4 are Asian: **$0.20/day saved**
- Over a month: **$6/month saved** (10% of Geoapify paid tier)
- **ROI matters** when bootstrapping a cheese business

### Business-Focused Intelligence
- **Pre-set rules filter for affordability** - Targets $20+ entrees, upscale signals
- **Dairy-compatibility first** - Excludes Asian cuisine (cheese doesn't pair)
- **High-probability customers only** - Fine dining, European, steakhouses
- **Learns preferences** - Rejection memory builds personalized prospect list

### Tradeoffs We Made
**Chose: Business value over technical elegance**
- Simple keyword filtering + LLM (fast, works)
- Not: Semantic embeddings, neural networks (slower, overkill for MVP)

**Chose: Proactive features over perfect UI**
- Walking directions, rejection memory, override options
- Not: Beautiful animations, React components

**Chose: Hillary's time over API costs**
- Google Places ($0.032) works reliably
- Not: "Free" APIs (Yelp, Foursquare) that wasted 5 hours debugging

### Learning Over Time
- System gets smarter as Hillary uses it
- Rejection memory builds a personalized blacklist
- Works even if restaurant names change slightly
- **Data compounds** - 200 rejections = never seeing those restaurants again

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
Edit `frontend/app.js`:
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

## 📈 What We'd Improve Next

### Immediate Wins (Week 1)
1. **Route optimization** - Sort by walking distance from *current* location (not search center)
2. **Success tracking** - Mark which pitches converted to sales
3. **Batch overnight** - Pre-generate pitches for tomorrow's planned route
4. **Export to CSV** - Share prospect list with team

### Short-term (Month 1)
1. **Semantic filtering** - Use embeddings to detect Asian cuisine by menu similarity (beyond keywords)
2. **Collaborative learning** - Share rejection data across Hillary + future sales reps
3. **Visit notes** - "Called 2/15, follow up next week"
4. **Offline mode** - Cache prospects for areas without cell coverage

### Long-term (Quarter 1)
1. **Success-based learning** - Fine-tune LLM prompts based on which pitches actually closed
2. **Multi-cheese bundles** - "Pasture Bloom for appetizers, Smoky Alder for mains"
3. **Predictive scoring** - ML model predicts conversion probability
4. **Analytics dashboard** - "You've saved $147 in wasted visits this month"
5. **CRM integration** - Sync with Salesforce/HubSpot for enterprise sales teams

### What We Won't Build (And Why)
- ❌ **Perfect UI** - Business value > aesthetics
- ❌ **Real-time sync** - localStorage sufficient for solo operation
- ❌ **Advanced reporting** - Excel export handles MVP analytics
- ❌ **Mobile native app** - Web app works on phone browsers

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
