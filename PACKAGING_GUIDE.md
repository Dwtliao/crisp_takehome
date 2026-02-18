# Packaging Guide - Happy Pastures Creamery Demo

## 📦 Creating a Demo Package

### Quick Package
```bash
./package_demo.sh
```

This creates a timestamped zip file like: `happy_pastures_demo_20260217_143022.zip`

---

## 📋 What Gets Packaged

### ✅ Included:
- All backend code (`backend/`)
- All frontend code (`frontend/`)
- Test scripts (`tests/`)
- **Your .env file with API keys** 🔑
- requirements.txt
- start_app.sh
- All documentation (README, ARCHITECTURE, etc.)
- Automated setup script

### ❌ Excluded:
- .git directory
- __pycache__ folders
- .pyc files
- .DS_Store files
- Virtual environments

---

## 🚀 Using the Package on Another Mac

### Step 1: Transfer the Zip File
```bash
# Copy via USB, AirDrop, or scp
scp happy_pastures_demo_*.zip user@other-mac:~/Downloads/
```

### Step 2: On the New Mac
```bash
# Unzip
unzip happy_pastures_demo_20260217_143022.zip

# Navigate into directory
cd happy_pastures_demo_20260217_143022

# Run automated setup (installs dependencies)
./setup_demo.sh

# Start the app
./start_app.sh
```

### Step 3: Open Browser
Navigate to: **http://localhost:8000/app**

---

## 📁 Package Contents

After unzipping, you'll see:

```
happy_pastures_demo_20260217_143022/
├── backend/                      # Backend API
│   ├── api.py
│   ├── geoapify_client.py
│   ├── google_places_client.py
│   ├── sales_pitch_generator.py
│   ├── cheese_products.py
│   └── config.py
├── frontend/                     # Frontend web app
│   └── index.html
├── tests/                        # Test scripts
├── .env                          # ⚠️ API KEYS (keep secure!)
├── requirements.txt              # Python dependencies
├── start_app.sh                  # App launcher
├── setup_demo.sh                 # Automated setup
├── SETUP_INSTRUCTIONS.md         # Quick start guide
├── README.md                     # Project overview
├── ARCHITECTURE.md               # Technical details
├── FILTERING_SYSTEM.md           # Feature documentation
└── GOOGLE_PLACES_SETUP.md        # API setup guide
```

---

## 🔧 Manual Setup (if setup_demo.sh fails)

```bash
# 1. Install Python dependencies
pip3 install -r requirements.txt

# 2. Make start script executable
chmod +x start_app.sh

# 3. Verify .env file
cat .env

# 4. Start the app
./start_app.sh
```

---

## 🔒 Security Considerations

### The .env File Contains Sensitive API Keys!

**Do NOT:**
- ❌ Commit the package to public git repositories
- ❌ Share the package publicly
- ❌ Email the package to untrusted recipients
- ❌ Upload to public cloud storage

**Do:**
- ✅ Share only via secure channels (encrypted USB, private file share)
- ✅ Delete the package after transferring
- ✅ Regenerate API keys if compromised

### API Key Scopes:
- **Geoapify:** Location searches only
- **Anthropic:** Claude API access
- **Google Places:** Restaurant data lookups

If keys are compromised, regenerate them at:
- Geoapify: https://www.geoapify.com/
- Anthropic: https://console.anthropic.com/
- Google: https://console.cloud.google.com/

---

## 📊 Package Size

Typical package size: **~50-100 KB** (very small!)

The package is lightweight because:
- No dependencies bundled (installed via pip)
- No .git history
- No virtual environment
- Pure Python/HTML/JS code

---

## 🧪 Testing the Package

Before sharing, test on the same machine:

```bash
# Create package
./package_demo.sh

# Move to Desktop and test
cp happy_pastures_demo_*.zip ~/Desktop/
cd ~/Desktop
unzip happy_pastures_demo_*.zip
cd happy_pastures_demo_*
./setup_demo.sh
./start_app.sh
```

---

## 💡 Tips

### Creating Multiple Packages
Each run creates a new timestamped file, so you won't overwrite previous packages:
```bash
./package_demo.sh  # Creates happy_pastures_demo_20260217_143022.zip
./package_demo.sh  # Creates happy_pastures_demo_20260217_143045.zip
```

### Custom Package Name
Edit `package_demo.sh` and change `DEMO_NAME`:
```bash
DEMO_NAME="interview_demo"  # Creates interview_demo_TIMESTAMP.zip
```

### Packaging Without API Keys
If you want to share code WITHOUT your API keys:
```bash
# Temporarily rename .env
mv .env .env.backup

# Run packaging
./package_demo.sh

# Restore .env
mv .env.backup .env
```

The recipient will see a template .env and need to add their own keys.

---

## 🎯 Common Use Cases

### 1. Interview Demo
Package everything and bring to interview on USB drive

### 2. Team Collaboration
Share with team members who need to run the app locally

### 3. Backup
Create snapshots of working versions before major changes

### 4. Client Demo
Package for client to run on their machine (remove your API keys first!)

---

## 📞 Troubleshooting

### "Permission denied" on setup_demo.sh
```bash
chmod +x setup_demo.sh
./setup_demo.sh
```

### "Package too large to email"
50KB should email fine, but if needed:
- Use Google Drive / Dropbox (private link)
- Use AirDrop (macOS)
- Use secure file transfer: https://send.firefox.com/

### "Dependencies fail to install"
Check Python version:
```bash
python3 --version  # Should be 3.9 or higher
```

Upgrade pip:
```bash
pip3 install --upgrade pip
```

---

## ✅ Checklist Before Sharing

- [ ] Package created successfully
- [ ] Tested unzip on same machine
- [ ] Verified .env contains real API keys (or template)
- [ ] Tested `./setup_demo.sh`
- [ ] Tested `./start_app.sh`
- [ ] App loads at http://localhost:8000/app
- [ ] Can search for restaurants
- [ ] Can generate pitch
- [ ] Confirmed secure transfer method

---

Happy packaging! 🧀📦
