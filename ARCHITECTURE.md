# System Architecture & Technology Choices

**Happy Pastures Creamery Restaurant Prospecting System**

## Overview

This system helps Hillary sell $30-50/lb artisan cheese by finding high-probability customers (fine dining restaurants) and generating AI-powered sales pitches. The architecture prioritizes **working immediately** over perfection, **cost-effectiveness** over enterprise features, and **business value** over technical sophistication.

---

## Technology Choices: What Worked, What Didn't

### API Selection - Learning from Failure

**Yelp Fusion API** - Dead End ($299/month business tier required, wasted 2 hours)
**Foursquare Places API** - Dead End (confusing v2/v3 migration, authentication failures, wasted 3 hours)
**Google Places API (New)** - ✅ **Worked first try**. Yes, it costs money ($0.032/lookup), but reliability matters when you have limited time. Sometimes "supposedly free" APIs are expensive time sinks.

**Geoapify Places** - ✅ **Perfect for MVP**. Free tier (3,000 requests/day) provides geolocation search and rich category data. Critical for bootstrapping: Hillary doesn't need to pay until the business proves itself. When she scales, upgrading is straightforward.

### Frontend: Vanilla HTML/JS - Intentional Simplicity

**No React, no Vue, no build step.** This wasn't laziness - it was pragmatism under time constraints. 500 lines of readable JavaScript that works on any browser, deploys instantly, and reviewers can run without `npm install`. Mobile-first GPS integration (Hillary's walking door-to-door) with address fallback. The UI is simple but **proactive**: walking directions button, rejection memory, override options for edge cases. We built what Hillary needs, not what looks impressive in a portfolio.

---

## Architecture: Three-Layer Intelligence

**Layer 1: Discovery (Geoapify)** - 2.5km walking radius returns 150 raw prospects. Free tier handles MVP scale.

**Layer 2: Quality Filter (Claude Haiku)** - Batch processes 20 restaurants simultaneously. **Business-focused rules**: excludes Asian cuisine (dairy-incompatible), fast food, and casual chains. Reduces 150 → 20 high-probability prospects who can afford $40/lb cheese. Cost: ~$0.001/restaurant.

**Layer 3: Sales Pitch (Claude Sonnet 4.5 + Google Places)** - **On-demand only** (critical cost optimization). When Hillary selects a restaurant, we fetch live menu data from Google Places reviews ($0.032), analyze dishes, match cheese, generate customized pitch (~$0.02). Total: $0.053 per selected prospect. She only pays for restaurants she's actually visiting.

---

## Key Tradeoffs & Design Decisions

### Tradeoff: Speed vs. Polish
**Chose:** Ship working product in constrained time
**Sacrificed:** React UI, comprehensive testing, offline mode
**Result:** Hillary can use it today, not next month

### Tradeoff: Cost vs. Reliability
**Chose:** Google Places ($0.032) over "free" alternatives
**Sacrificed:** $0 API bill
**Result:** Works reliably, no time wasted debugging flaky APIs

### Tradeoff: Database vs. Stateless
**Chose:** localStorage + stateless API
**Sacrificed:** Server-side history, analytics, multi-device sync
**Result:** Zero infrastructure, instant deployment, 200-restaurant rejection memory persists locally

### Proactive Features Despite Time Constraints
- **Walking directions** - Google Maps integration saves Hillary time in winter
- **Rejection memory** - Learns her preferences, never shows rejected restaurants again
- **Asian cuisine warning** - Pre-pitch detection saves $0.05/restaurant on incompatible prospects
- **Override option** - "Generate pitch anyway" button respects Hillary's judgment
- **Pre-set business rules** - Filters for $20+ entrees, upscale signals, cheese-friendly cuisines
- **Text-to-speech** - Listen to pitches hands-free while walking (browser built-in, $0 cost)
- **Voice notes** - Dictate visit outcomes, saved permanently in localStorage
- **Pitch refinement** - 3 persona-based adaptations (Chef, Manager, Gatekeeper)
- **Micro-refinements** - 5 polish options (Shorten, Expand, Casual, Formal, Strong Opener)
- **Save & reuse** - Store perfected pitches in localStorage for return visits

### Tradeoff: 2-Page Architecture for Mobile UX
**Chose:** Separate screens for original pitch and refinement
**Sacrificed:** Single-page "everything at once" view
**Result:** Mobile-friendly, no endless scrolling, focused purpose per screen

**Why this matters:**
- Mobile screens are small - separate pages prevent scroll fatigue
- Each page has clear purpose: view pitch vs refine pitch
- Better state management (original TTS vs refined TTS don't conflict)
- Explicit navigation creates intentional workflow
- Fixes UI glitches from trying to show everything on one page

**Complete Web Page Flows:**

```
┌──────────────────────────────────────────────────────────┐
│ PAGE 1: Original Pitch Screen                            │
├──────────────────────────────────────────────────────────┤
│ 1. Restaurant name, address, phone                       │
│ 2. 🔊 Listen to Pitch (TTS controls)                     │
│ 3. 🧀 Recommended Product                                │
│ 4. 💬 Opening Hook                                       │
│ 5. 🍽️ Menu Pairings (from real menu data)               │
│ 6. ✨ Key Talking Points                                 │
│ 7. 🏆 Competitive Advantage                              │
│ 8. 📞 Call to Action                                     │
│ 9. 📝 Voice Notes (record visit outcomes)                │
│                                                           │
│ 10. 💾 Saved Pitches Available! (if exists)             │
│     └─ Shows: "You have saved pitches for: Chef, Manager"│
│                                                           │
│ 11. [Refine This Pitch →] Button                         │
│     └─ Click → Navigate to Page 2                        │
└──────────────────────────────────────────────────────────┘

                            ↓ Click "Refine This Pitch"

┌──────────────────────────────────────────────────────────┐
│ PAGE 2: Pitch Refinement Screen                          │
├──────────────────────────────────────────────────────────┤
│ [← Back to Original Pitch]                               │
│                                                           │
│ Restaurant: Oceanique                                     │
│ 📍 Address                                                │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐  │
│ │ 💾 Your Saved Pitches: (if exists)                 │  │
│ │                                                     │  │
│ │ 🧑‍🍳 Chef/Kitchen Staff                             │  │
│ │ Saved: 2/18/2026 9:45 AM                           │  │
│ │ [📖 Load This Pitch]  ← Click to instant load      │  │
│ │                                                     │  │
│ │ 👔 Owner/Manager                                    │  │
│ │ Saved: 2/18/2026 10:12 AM                          │  │
│ │ [📖 Load This Pitch]                                │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                           │
│ 🔄 Refine For:                                            │
│ [🧑‍🍳 Chef / Kitchen Staff] ← Click to generate          │
│ [👔 Owner / Manager]                                      │
│ [🎯 Host / Front Desk]                                    │
│                                                           │
│ ─────── After clicking persona or load ──────            │
│                                                           │
│ ┌─────────────────────────────────────────────────────┐  │
│ │ 📝 Refined for: 🧑‍🍳 Chef/Kitchen Staff            │  │
│ │                                                     │  │
│ │ 🔊 Listen to Refined Pitch (TTS at top)            │  │
│ │                                                     │  │
│ │ [Refined pitch text content]                       │  │
│ │                                                     │  │
│ │ ✨ Fine-tune This Pitch:                            │  │
│ │ [📏 Shorten] [📖 Expand]                            │  │
│ │ [💬 More Casual] [🎩 More Formal]                   │  │
│ │ [⚡ Strong Opener]                                   │  │
│ │                                                     │  │
│ │ 💾 Save This Version                                │  │
│ │ └─ Stores to localStorage for return visits        │  │
│ │                                                     │  │
│ │ [← Try Different Persona]                           │  │
│ └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Implementation Details:**
- **Page 1 (Pitch Screen):**
  - Original pitch with TTS controls
  - Voice notes section
  - Saved pitch indicator (checks localStorage on load)
  - "Refine This Pitch" CTA button navigates to Page 2

- **Page 2 (Refinement Screen):**
  - Restaurant summary at top
  - Load saved pitches section (if exist)
  - 3 persona buttons for new generation
  - Refined pitch display area
  - 5 micro-refinement buttons
  - Save pitch button
  - TTS controls for refined pitch

- **Navigation:** Simple show/hide with scroll-to-top on transition
- **State Management:** Separate TTS instances for original vs refined
- **Costs:**
  - Initial pitch: ~$0.05 (Google Places + Claude)
  - Persona refinement: ~$0.02 (Claude only)
  - Micro-refinement: ~$0.01 each
  - Load saved pitch: $0 (localStorage)

### Save Pitch Architecture (localStorage)

**Storage Structure:**
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
  },
  "oceanique_42.05_-87.68_manager": {
    // Another saved pitch for same restaurant, different persona
  }
}
```

**Key Design:**
- Key format: `{restaurant_name}_{lat}_{lon}_{persona}`
- Prevents false positives (same name, different location)
- Allows multiple personas per restaurant
- Includes timestamp for "last saved" display

**Benefits:**
- **Zero API cost** on return visits (no regeneration needed)
- **Instant load** (sub-100ms from localStorage)
- **Persistent** across browser restarts, server restarts
- **Multiple saves** per restaurant (one per persona)
- **Long-term follow-ups** - Hillary's work persists indefinitely

**Workflow:**
1. First visit: Generate → Refine → Polish with micro-refinements → Save
2. Return visit (got turned away):
   - Page 1 shows "💾 Saved Pitches Available"
   - Click refine → See saved pitch cards
   - Click "Load This Pitch" → Instant display ($0 cost)
   - Can still micro-refine further if needed

---

## What We'd Improve Next

**Immediate (Week 1):** Route optimization (sort by walking distance from current location, not search center), success tracking (which pitches converted to sales?), batch overnight pitch generation for tomorrow's route.

**Short-term (Month 1):** PostgreSQL for cross-device history, visit notes/follow-ups, offline mode with cached prospects, A/B test pitch variations.

**Long-term (Quarter 1):** Fine-tune LLM prompts based on successful sales data, semantic embeddings for menu-cheese matching (beyond keywords), multi-cheese bundle recommendations, CRM integration.

---

## Why This Architecture Works

1. **Immediately Useful** - Hillary uses it today, not after "Phase 2"
2. **Cost-Conscious** - Free tier until revenue proves the model ($0.05/prospect when paying)
3. **Business-Focused** - Every filter optimizes for high-probability customers
4. **Pragmatically Sophisticated** - AI where it helps (pitch generation), rules where they work (category filtering)
5. **Production-Ready Path** - Stateless design means adding PostgreSQL doesn't require rewrite

This isn't the system we'd build with 6 months and a team. It's the system Hillary needs this winter to sell cheese profitably.
