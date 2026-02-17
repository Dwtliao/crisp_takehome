## Google Places API Setup Guide

**The Reliable Choice** - Comprehensive data, excellent documentation, actually works!

---

## Step 1: Create Google Cloud Project (5 minutes)

### 1. Go to Google Cloud Console
Visit: **https://console.cloud.google.com/**

### 2. Create a New Project
- Click **"Select a project"** dropdown at the top
- Click **"New Project"**
- Project name: `Happy Pastures Prospecting`
- Click **"Create"**
- Wait for the project to be created (~30 seconds)

---

## Step 2: Enable Places API (2 minutes)

### 1. Go to API Library
Visit: **https://console.cloud.google.com/apis/library**

Make sure your new project is selected!

### 2. Search for "Places API"
- Type "Places API" in the search box
- Look for **"Places API (New)"** (NOT the old "Places API")
- Click on it

### 3. Enable the API
- Click the blue **"Enable"** button
- Wait for it to activate (~30 seconds)

---

## Step 3: Create API Key (2 minutes)

### 1. Go to Credentials
Visit: **https://console.cloud.google.com/apis/credentials**

### 2. Create API Key
- Click **"Create Credentials"** button
- Select **"API Key"**
- A popup will show your new API key
- Click the **Copy** button
- **SAVE THIS KEY!** (you can view it again later though)

### 3. (Optional) Restrict the Key
For security, you can restrict to specific APIs:
- Click **"Edit API key"** (or the pencil icon)
- Under "API restrictions", select "Restrict key"
- Select **"Places API (New)"**
- Click **"Save"**

---

## Step 4: Enable Billing (Required!) (3 minutes)

**Even with $200 free credit, you MUST enable billing.**

### 1. Go to Billing
Visit: **https://console.cloud.google.com/billing**

### 2. Link Billing Account
- Click **"Link a billing account"**
- If you're new: Click **"Create billing account"**
  - Enter your details
  - Add credit card (won't be charged until you exceed $200)
- If you have an existing account: Select it

### 3. Confirm Free Credit
- New accounts get **$200 free credit** automatically
- This lasts 90 days or until spent
- You'll get email notifications before running out

---

## Step 5: Add to Your .env (1 minute)

Open `/Users/davidliao/git_repos/crisp_takehome/.env` and add:

```bash
# Google Places API Key (reliable, paid option)
GOOGLE_PLACES_API_KEY=your_key_here
```

Your complete `.env`:
```bash
GEOAPIFY_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_PLACES_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

---

## Step 6: Test It! (1 minute)

### Quick Test:
```bash
cd /Users/davidliao/git_repos/crisp_takehome
python test_google_places.py
```

### Run the Restaurant Selector:
```bash
python backend/restaurant_selector_google.py
```

---

## 💰 Pricing & Cost Management

### Costs per Request:
- **Text Search**: $0.032 per request
  - This gets you: name, address, rating, reviews, phone, website
- **Place Details**: $0.017 per request (not needed for our use case)

### For Your Demo:
- **Testing**: 10-20 restaurants = ~$0.50
- **Interview Demo**: 5-10 restaurants = ~$0.25
- **Total for 1-week project**: ~$1-2

### Your $200 Free Credit:
- Can look up **~6,200 restaurants**
- More than enough for the demo!

### Set a Budget Alert:
1. Go to: https://console.cloud.google.com/billing/budgets
2. Click "Create Budget"
3. Set amount: $10
4. Add email alerts at 50%, 90%, 100%

---

## 🎯 What You Get with Google Places

✅ **Comprehensive Data:**
- Restaurant name and address
- Phone number and website
- Rating (out of 5) and review count
- Price level ($, $$, $$$, $$$$)
- 5 recent customer reviews (with full text!)
- Menu hints from review analysis
- Opening hours
- Google Maps link

✅ **Reliability:**
- 99.9% uptime SLA
- Fast response times (~200ms)
- No sandbox mode BS
- No "talk to sales" requirements

✅ **Coverage:**
- Global database
- Regularly updated
- Best restaurant coverage in US

---

## Troubleshooting

### "API key not valid"
- Wait 5 minutes after creating key (propagation time)
- Check that Places API (New) is enabled
- Make sure you copied the full key

### "This API project is not authorized"
- Enable billing (required even with free credit)
- Check that Places API (New) is enabled
- Make sure you're using the right project

### "Billing must be enabled"
- Go to console.cloud.google.com/billing
- Link a billing account
- Add credit card

### API calls failing with 403
- Billing not enabled
- API not enabled
- API key restrictions too strict

---

## For Your Interview

**What to say:**
> "I integrated Google Places API for menu data enrichment. While it's a paid service, it provides reliable, comprehensive restaurant data including customer reviews that mention menu items. The $200 free credit covers all development and demo needs, and in production, the cost would be ~$0.03 per restaurant lookup, which is reasonable for a B2B sales tool."

This shows:
- ✅ You can integrate production-grade APIs
- ✅ You understand cost trade-offs
- ✅ You make pragmatic technical decisions
- ✅ You deliver working features

---

## Next Steps

Once the test passes:
1. ✅ Run `python backend/restaurant_selector_google.py`
2. ✅ Test with a few restaurants
3. ✅ Integrate into your main app if needed
4. ✅ Polish your demo
5. ✅ Ace your interview! 🎉

Good luck! 🧀
