# Setup Guide - Secure API Key Management

## ✅ Your code is now secure for GitHub!

All API keys have been removed from the code and moved to environment variables.

## How to Set Up Your Environment

### Option 1: Using .env file (Recommended for Development)

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env and add your actual keys:**
   ```bash
   # .env file
   GEOAPIFY_API_KEY=your_actual_geoapify_key_here
   ANTHROPIC_API_KEY=your_actual_anthropic_key_here
   ```

3. **Load environment variables:**
   ```bash
   # For bash/zsh
   export $(cat .env | xargs)

   # Or use python-dotenv (install: pip install python-dotenv)
   # Add to your scripts:
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Option 2: Export Directly (Temporary)

```bash
export GEOAPIFY_API_KEY="your_actual_geoapify_key_here"
export ANTHROPIC_API_KEY="your_actual_anthropic_key_here"
```

**Note:** These exports only last for your current terminal session.

### Option 3: Add to Shell Profile (Permanent)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export GEOAPIFY_API_KEY="your_actual_geoapify_key_here"
export ANTHROPIC_API_KEY="your_actual_anthropic_key_here"
```

Then reload: `source ~/.bashrc` or `source ~/.zshrc`

## Verify It's Working

```bash
# Check environment variables are set
echo $GEOAPIFY_API_KEY
echo $ANTHROPIC_API_KEY

# Run the test script
python tests/geoapify_test.py --use-llm

# Run the backend API
cd backend && python api.py
```

## Before Committing to GitHub

**✅ Checklist:**
- [ ] No API keys in any .py files
- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` has placeholder values only
- [ ] Test that code works with environment variables

**Check for accidentally committed secrets:**
```bash
git status
git diff
```

If you see any API keys in the diff, **DO NOT COMMIT**.

## What if I Already Committed Keys?

If you've already committed keys to GitHub (even if you delete them in a new commit, they're still in git history):

1. **Rotate your API keys immediately:**
   - Geoapify: https://www.geoapify.com/ → Delete old key, create new
   - Anthropic: https://console.anthropic.com/ → Delete old key, create new

2. **Clean git history (advanced):**
   ```bash
   # WARNING: This rewrites history!
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/config.py tests/geoapify_test.py" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (careful!)
   git push origin --force --all
   ```

## Production Deployment

For production (e.g., Heroku, AWS, Render):
- Set environment variables in your hosting platform's dashboard
- Never hardcode keys, even in "production config" files
- Use secrets managers (AWS Secrets Manager, etc.) for enterprise apps
