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
