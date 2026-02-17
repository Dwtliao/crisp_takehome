# System Architecture & Technology Choices

**Happy Pastures Creamery Restaurant Prospecting System**

## Overview (498 words)

This system solves Hillary's core problem: finding compatible restaurants and creating effective sales pitches without standing in the cold reading menus. The architecture balances **pragmatism** with **sophistication** - using AI where it adds genuine value, simple rules where they suffice.

### Technology Choices & Rationale

**Backend: FastAPI + Python**

FastAPI provides a modern, async REST API with automatic OpenAPI documentation. Python was chosen for its rich AI/ML ecosystem and rapid development cycle. The backend exposes two endpoints: `/api/prospects` for listing nearby restaurants with quick cheese matches, and `/api/pitch` for generating detailed, AI-powered sales pitches on-demand.

**Frontend: Vanilla HTML/JavaScript**

This was a **pragmatic decision** over React or Vue. With ~400 lines of readable code, zero build steps, and instant deployment, it demonstrates time-aware engineering. The mobile-first responsive design uses HTML5 Geolocation API for GPS access (Hillary's primary use case) with address input as fallback. No framework means no dependency management, no compilation, and trivial debugging - perfect for a take-home project that reviewers need to run quickly.

**AI Architecture - Three Intelligent Layers:**

**Layer 1: Restaurant Discovery (Geoapify)**
Geolocation-based search within 2.5km walking distance returns 150+ raw prospects. The free tier handles development needs, and the API provides rich categorical data essential for filtering.

**Layer 2: Quality Filtering (Claude Haiku)**
Batch processing evaluates 20 restaurants simultaneously, dramatically reducing API calls. The LLM filters out fast food chains, casual diners, and incompatible cuisines, reducing 150 prospects to ~20-25 high-quality targets. This costs approximately $0.001 per restaurant - negligible compared to the value of Hillary's time.

**Layer 3: Sales Pitch Generation (Claude Sonnet 4.5)**
**On-demand only** - this is a critical cost optimization. Rather than generating pitches for all 20 prospects upfront, we wait until Hillary selects a specific restaurant. The system then fetches live menu data via Google Places API ($0.032), analyzes customer reviews for menu items, matches the appropriate cheese product, and generates a customized pitch (~$0.02). Total cost per selected prospect: ~$0.053.

**Data Enrichment: Google Places API**

Live menu data comes from analyzing actual customer reviews - not static menu listings. When someone mentions "the lobster bisque" or "wood-fired pizza," those become concrete pairing opportunities in the sales pitch. This human signal is far more valuable than generic menu categories.

### Key Design Decisions

**Cost Optimization Through Lazy Loading**: The expensive operations (Google Places + Claude Sonnet) happen only when Hillary selects a restaurant. This means she sees the prospect list immediately (fast + cheap), then generates the detailed pitch only for restaurants she's actually going to visit.

**Two-Tier Cheese Matching**: Fast rule-based matching (French/Italian → Pasture Bloom, Pub/American → Smoky Alder) provides instant recommendations in the list view. Sophisticated AI analysis with menu review understanding powers the detailed pitch. Best of both worlds: speed where it matters, intelligence where it counts.

**Stateless API Design**: No database, no sessions, no authentication (for v1). This kept development time to one day while maintaining a clear path to production - add PostgreSQL, implement JWT auth, deploy to cloud. The core architecture doesn't change.

### What Would Come Next

**Phase 2**: Offline mode with cached prospects, visit tracking with notes, route optimization, success metrics tracking, batch overnight pitch generation.

**Production**: PostgreSQL for history, authentication, error monitoring (Sentry), rate limiting, HTTPS with proper CORS.

**AI Enhancements**: Fine-tuned prompts based on successful sales, semantic embeddings for menu-cheese matching, multi-cheese bundle recommendations.

This architecture works because it's **immediately useful** (Hillary can use it today), **appropriately sophisticated** (AI where it helps, rules where they work), and has a **clear path to scale** (stateless design, cached data, on-demand generation).
