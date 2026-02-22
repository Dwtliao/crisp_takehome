# Happy Pastures Creamery - Restaurant Prospecting System

A mobile-first web application that helps Hillary find and sell to high-quality restaurant prospects using AI-powered insights.

## Quick Start

```bash
./start_app.sh
# Then open: http://localhost:8000/app
```

---

## Demo

👉 **[Video Walkthrough](link-to-video)** (5-10 minutes)

---

## What This Solves

Hillary sells artisan cheese door-to-door to restaurants. She needs to:
1. Find compatible restaurants (not fast food!)
2. Know what's on their menu before walking in
3. Have a compelling pitch ready
4. **NEW:** Listen to pitches hands-free while walking
5. **NEW:** Capture visit notes without typing in winter cold

This system does all five automatically.

---

## 🎤 Key Features: Voice Notes & TTS

### Text-to-Speech Pitch Playback
- Listen to AI-generated pitches via earbuds while walking
- Memorize key talking points hands-free
- Play/pause/replay with speed controls (0.75x - 1.5x)
- **Zero API cost** - Uses browser's built-in speech synthesis

### Voice Notes for Visit Tracking
- Dictate outcomes after each restaurant visit
- **Permanently saved** in browser localStorage (survives restarts)
- Track follow-ups: "Manager away, try next Tuesday"
- Record successes: "Loved the sample, send invoice Monday"
- **Hands-free operation** - No typing in winter weather

**Browser requirement:** Chrome or Edge (for voice notes)

---

## 📦 Location Caching: Instant Repeat Searches

**NEW Feature:** Smart caching for frequently visited locations

### How It Works
- **First search:** Results cached automatically with timestamp (address-based or GPS-based key)
- **Repeat search:** Instant load from cache (<100ms vs 3 seconds)
- **7-day TTL:** Cache auto-expires after 7 days for fresh data
- **Two manual controls:** "Clear Cache + Refresh" fetches fresh data; "Clear Cache Only" removes entry without re-fetching

### Visual Indicators
**Cached Results:**
```
📦 This restaurant list was loaded from cache (2 days ago)
[Clear Cache + Refresh]  [Clear Cache Only]
```

**Fresh Results:**
```
✨ Fresh results  (shown in search info line)
```

### Benefits
- ⚡ **Speed:** Instant repeat searches (Hillary's time matters in winter!)
- 💰 **Cost:** Free repeat searches within 7 days (~$0.001 saved per search)
- 🗺️ **Workflow:** Hillary walks same neighborhoods multiple times
- 🔄 **Control:** Manual refresh button when she wants fresh data

**Example:** Search "Evanston, IL" on Monday → Returns Tuesday → Instant load!

---

## 🔄 Pitch Refinement: Persona-Based Adaptation

### Multiple Pitch Versions for Different Audiences
After generating the initial pitch, refine it for specific situations:

**🚶 For Walking & Memorizing (NEW!)**
- Ultra-short 20-second version
- Natural, conversational flow
- Easy to memorize while walking
- Perfect for practicing en route
- ~20 seconds spoken

**🧑‍🍳 For Chef/Kitchen Staff**
- Technical, culinary-focused language
- Cooking techniques, melt points, flavor chemistry
- Peer-to-peer professional tone
- ~60 seconds spoken

**👔 For Owner/Manager**
- Business ROI and margin focus
- Menu differentiation and competitive advantage
- Local sourcing story
- ~90 seconds with concrete numbers

**🎯 For Host/Front Desk**
- Ultra-brief elevator pitch (~30 seconds)
- Get past gatekeeper to reach decision maker
- Respectful, quick credibility-building
- Simple ask with alternative

### Micro-Refinements: Polish Your Pitch
After persona refinement, fine-tune with one-click adjustments:

- **📏 Shorten** - Condense to 20-30 seconds
- **📖 Expand** - Add detail and examples
- **💬 More Casual** - Conversational tone
- **🎩 More Formal** - Professional polish
- **⚡ Strong Opener** - Attention-grabbing first line

**Cost:** ~$0.01 per micro-refinement

### Save & Reuse Pitches
- **💾 Save perfected pitches** to localStorage
- **Return visits:** Load saved pitch instantly (zero API cost!)
- **Page 1 indicator:** Shows when saved pitches exist
- **Multiple saves:** Save different personas per restaurant

### 2-Page Mobile-First Architecture
- **Page 1:** Original pitch with TTS and voice notes
  - Shows saved pitch indicator if exists
  - "Refine This Pitch" button navigates to Page 2
- **Page 2:** Refinement screen with persona selection
  - Load saved pitches or generate new
  - Micro-refine and save
- Clean navigation, no endless scrolling
- Each page has focused purpose

**Cost Breakdown:**
- Initial pitch: ~$0.05 (Google Places + Claude)
- Persona refinement: ~$0.02 (Claude only)
- Micro-refinement: ~$0.01 each
- Load saved pitch: $0 (localStorage)

---

## How to Run

See GOOGLE_PLACES_SETUP.md for complete setup instructions.

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add API keys to .env
GEOAPIFY_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_PLACES_API_KEY=...

# 3. Start the app
./start_app.sh
```

---

## Project Structure

```
backend/
  api.py                    # REST API (FastAPI)
  *_client.py              # API integrations
  sales_pitch_generator.py # AI pitch generation
  cheese_products.py       # Product catalog

frontend/
  index.html              # HTML structure only
  style.css               # All CSS styles
  app.js                  # All JavaScript

tests/
  test_*.py              # Test scripts
```

---

## Architecture & Design Decisions

**See full documentation in ARCHITECTURE.md**

Quick summary:
- FastAPI backend with 2 endpoints
- Vanilla HTML/JS frontend (mobile-first)
- 3-layer AI system (search → filter → pitch)
- Cost-optimized (~$0.05 per prospect)

---

## Technology Stack

- Python 3.9, FastAPI
- HTML5, Vanilla JS
- Claude AI (Haiku + Sonnet 4.5)
- Geoapify, Google Places APIs

---

## Technology Choices & Tradeoffs

**What worked:**
- ✅ **Google Places API** - Worked first try ($0.032/lookup, worth it)
- ✅ **Geoapify** - Free tier perfect for MVP (3K requests/day)
- ✅ **Vanilla HTML/JS** - Zero build time, instant deployment
- ✅ **Claude AI** - Haiku for filtering ($0.001), Sonnet for pitches ($0.02)

**What didn't work (time wasted):**
- ❌ **Yelp Fusion API** - $299/month required (2 hours wasted)
- ❌ **Foursquare Places** - Authentication failures, confusing docs (3 hours wasted)

**Key tradeoffs:**
- **Speed over polish** - Shipped in time constraints, vanilla JS/CSS not React (split into index.html + style.css + app.js for maintainability)
- **Cost over "free"** - Google Places costs money but works reliably
- **localStorage over database** - No infrastructure, 200-item rejection memory
- **Business focus** - Every filter optimizes for high-probability customers ($20+ entrees, cheese-friendly cuisines)

**Proactive features added:**
- 🗺️ Walking directions (Google Maps integration)
- ❌ Rejection memory (learns preferences, persists in localStorage)
- ⚠️ Asian cuisine detection (saves $0.05/restaurant)
- 🔄 Override option (respects Hillary's judgment)
- 🎯 Pre-set business rules (fine dining, $40/lb cheese compatible)
- 🔊 Text-to-speech (listen to pitches hands-free via earbuds)
- 🎤 Voice notes (dictate visit outcomes, saved permanently in localStorage)
- 🔄 Pitch refinement (5 personas: Original, Walking, Chef, Manager, Host with separate TTS)
- ✨ Micro-refinements (5 polish options: Shorten, Expand, Casual, Formal, Strong Opener)
- 💾 Save & reuse pitches (zero cost on return visits, loads from localStorage)
- 📦 Location caching (instant repeat searches, 7-day auto-expire, prominent refresh button)

