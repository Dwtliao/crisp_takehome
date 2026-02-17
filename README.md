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

This system does all three automatically.

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

## Time & Tradeoffs

**Time spent**: ~8 hours

**Key tradeoffs**:
- Simple HTML/JS over React (no build step)
- On-demand pitch generation (cost savings)
- Stateless API (faster to build)

