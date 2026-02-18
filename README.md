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

## 🔄 Pitch Refinement: Persona-Based Adaptation

### Multiple Pitch Versions for Different Audiences
After generating the initial pitch, refine it for specific situations:

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

### 2-Page Mobile-First Architecture
- **Page 1:** Original pitch with TTS and voice notes
- **Page 2:** Refinement screen with persona selection
- Clean navigation, no endless scrolling
- Each page has focused purpose

**Cost:** ~$0.02 per refinement (Claude only, no new data lookup)

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
  index.html              # Mobile-first web app

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
- **Speed over polish** - Shipped in time constraints, vanilla JS not React
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
- 🔄 Pitch refinement (3 personas: Chef, Manager, Gatekeeper with separate TTS)

