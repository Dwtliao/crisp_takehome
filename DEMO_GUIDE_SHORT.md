# Demo Script (Short Version)
**Target: 5–8 minutes | Structure matches the 4 required video elements**

---

## Before You Hit Record

- Clear localStorage (DevTools → Application → Clear site data)
- Restart server: `./start_app.sh`
- Browser tab open at `http://localhost:8000/app`
- Volume on, microphone ready

---

## PART 1 — Problem Framing (30 sec)

**SAY:**
> “Hi, I’m David. In this demo, I’m going to walk you through the sales‑pitch assistant I built — a lightweight, browser‑based tool designed to help reps generate clearer, more contextual pitches in under a minute. I’ll show you the core workflow, the reasoning behind a few key design decisions, and how the system balances cost, reliability, and real‑world usability. Let’s jump in.”
> "Let's help Hilary sell her specialty cheeses.  You should have a zip file to unpack, run the startup_demo file to setup a virtual env for python, then run start_app for local server of a web page to be ready!"
> "Hillary sells $40/lb artisan cheese door-to-door to restaurants. The problem was deliberately vague — I interpreted it as three core needs: **find** compatible restaurants, **qualify** them before wasting a visit, and **convert** with a pitch that's actually relevant to their menu. Everything in this system maps to one of those three."

---

## PART 2 — Live Demo (2–3 min)

### Step 1: Search
- Type `Evanston, IL` → click Search
- **SAY:** "2.5km walking radius — about 20 minutes of walking territory. The system filters in real-time."
- **POINT TO** the stats line: "X prospects shown, Y filtered out, Z in rejection memory"

### Step 2: Asian Cuisine Warning (the pre-pitch filter)
- Click **Oceanique**
- **SAY:** "Name sounds French — normally a strong cheese-pairing signal. But look — the system caught this is Asian-fusion *before* spending $0.05 on API calls."
- Point to the warning box and cost-saved message
- Click **"Generate Pitch Anyway"** to override
- **SAY:** "We trust Hillary's judgment — she can always override."

### Step 3: Generate a Real Pitch
- Go back, pick a non-Asian restaurant (Prairie Moon, Found Kitchen, etc.)
- Click View Pitch — let it load
- **POINT TO** Menu Pairings: "These are real dishes from their actual menu — not generic suggestions. This is what makes the pitch credible."
- **POINT TO** Recommended Product: "Specific cheese from the catalog, matched to the cuisine."
- Click **💾 Save Original Pitch** — **SAY:** "Zero API cost. Hillary saves this before she walks in — no need to refine just to preserve it."

### Step 4: Voice Features (quick)
- Click 🔊 Listen — play 5 seconds — **SAY:** "Hands-free. Hillary memorizes this during the walk over."
- Scroll to Notes → click 🎤 → dictate: *"Manager unavailable, try Tuesday afternoon"* → stop
- **SAY:** "Gloves on, winter cold — no typing required. Saved permanently in localStorage."

### Step 5: Pitch Refinement (30 sec)
- Click **Refine This Pitch →**
- **SAY:** "Hillary might talk to the host, then the chef, then the manager — each needs a different pitch."
- Show the 2x2 persona grid: Walking / Chef / Manager / Host
- Click 🚶 Walking — show the 20-second version
- **SAY:** "Memorize this en route. Same data, completely different register."

---

## PART 3 — Architecture & Technology Choices (1.5 min)

**SAY + SHOW** (can stay on pitch screen or switch to terminal):

> "Three-layer intelligence:"

1. **Discovery:** Geoapify Places API — free tier (3K requests/day), 2.5km radius, returns ~150 raw candidates
2. **Filtering (two-stage):**
   - Stage 1: Claude Haiku batch-processes 20 at a time — context-aware, catches nuance like Oceanique. Cost: ~$0.001 each.
   - Stage 2: Keyword safety net — catches obvious fast-casual patterns (`express`, `to go`, `breakfast`) that LLM might pass. Best of both worlds.
3. **Pitch generation:** Claude Sonnet + Google Places — on-demand only, never pre-generated. $0.032 for menu data + ~$0.02 for pitch = $0.053 per prospect Hillary actually visits.

**SAY on tech choices:**
> "Yelp was $299/month. Foursquare had authentication failures — 3 hours wasted. Google Places costs money but worked first try. Sometimes the 'free' API is the expensive one."

> "Vanilla HTML/JS — no React, no build step. Ships instantly, works on any browser, Hillary can use it today."

---

## PART 4 — Tradeoffs & What I'd Improve (1 min)

**Key tradeoffs:**
- **localStorage vs database:** Zero infrastructure, instant deployment, rejection memory + pitch saves + location cache all persist locally. Sacrificed: cross-device sync, analytics. Fine for MVP.
- **On-demand vs pre-generated pitches:** Hillary only pays for restaurants she actually visits. Sacrificed: instant pitch load on first view.
- **2-page mobile UX vs single page:** Prevented TTS state conflicts, reduced scroll fatigue on mobile. Cost: slightly more navigation.
- **Rule-based cheese selection vs LLM:** `determine_cheese_match()` scores Pasture Bloom vs Smoky Alder with keyword rules — fast and free, but coarse. The cheese catalog's full pairing data (proteins, produce, beverages, selling points) is now wired into the pitch prompt so Sonnet generates pitches grounded in the actual product catalog, not just inferred from review text.

**What's next (say 2-3 of these):**
- Route optimization — sort by walking distance from current location, not search center
- Success tracking — mark which pitches converted to sales, feed that back into filtering
- Batch overnight generation — pre-generate pitches for tomorrow's planned route
- PostgreSQL when multi-device sync matters (stateless backend design means this is a drop-in)

---

## PART 5 — Code Worth Scrutiny (30 sec)

> "Per the assessment — here's where to focus code review:"

**Worth scrutiny:**
- `backend/api.py` — endpoint design, two-stage filtering pipeline, error handling
- `backend/sales_pitch_generator.py` — prompt architecture, persona templates, micro-refinement chaining; `_build_cheese_context()` specifically wires the full product catalog (selling points, protein/produce/beverage pairings) into every pitch prompt
- `backend/geoapify_client.py` — keyword filter logic, LLM batch processing
- `backend/google_places_client.py` — menu data extraction from reviews

**Not worth scrutiny:**
- `frontend/index.html` + `style.css` + `app.js` — intentionally vanilla/simple, split for maintainability, no engineering pretensions here

---

## Timing Guide

| Section | Time |
|---|---|
| Problem framing | 0:00–0:30 |
| Live demo | 0:30–3:30 |
| Architecture + tech choices | 3:30–5:00 |
| Tradeoffs + roadmap | 5:00–6:00 |
| Code scrutiny call-out | 6:00–6:30 |
| **Total** | **~6:30** |

---

## If Something Breaks

- **Pitch won't generate:** Check `.env` has all 3 API keys, server is running
- **Voice note mic denied:** Use Chrome/Edge, allow mic in browser settings
- **No restaurants appear:** Geoapify free tier may be exhausted — try a different address or check API key
- **Oceanique not showing:** It may have already been filtered by backend — try a fresh search or clear localStorage first
