#!/bin/bash
# Package Happy Pastures Creamery Demo for Distribution
# Creates a portable zip file with all code and configuration

set -e  # Exit on error

echo "🧀 Packaging Happy Pastures Creamery Demo"
echo "=========================================="
echo ""

# Configuration
DEMO_NAME="happy_pastures_demo"
OUTPUT_FILE="${DEMO_NAME}.zip"
TEMP_DIR="/tmp/${DEMO_NAME}_$$"  # Use process ID for temp uniqueness

# Create temporary directory
echo "📁 Creating temporary package directory..."
mkdir -p "$TEMP_DIR"

# Copy all necessary files
echo "📋 Copying project files..."

# Core application files
cp -r backend "$TEMP_DIR/"
cp -r frontend "$TEMP_DIR/"
# Scripts and configuration
cp requirements.txt "$TEMP_DIR/"

# Create venv-aware start script (don't use the original)
cat > "$TEMP_DIR/start_app.sh" << 'STARTSCRIPT'
#!/bin/bash
# Start the Happy Pastures Creamery App with Virtual Environment

echo "🧀 Happy Pastures Creamery - Starting Application"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please run ./setup_demo.sh first to create the virtual environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting FastAPI backend server..."
echo "API will be available at: http://localhost:8000"
echo "Web app will be available at: http://localhost:8000/app"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python api.py

# Deactivate when done
deactivate
STARTSCRIPT

# Documentation
cp README.md "$TEMP_DIR/" 2>/dev/null || true
cp ARCHITECTURE.md "$TEMP_DIR/" 2>/dev/null || true
cp FILTERING_SYSTEM.md "$TEMP_DIR/" 2>/dev/null || true
cp GOOGLE_PLACES_SETUP.md "$TEMP_DIR/" 2>/dev/null || true

# IMPORTANT: Copy .env file (contains API keys)
if [ -f .env ]; then
    echo "🔑 Including .env file with API keys..."
    cp .env "$TEMP_DIR/"
else
    echo "⚠️  WARNING: No .env file found! You'll need to create one manually."
    echo "   Creating template .env file..."
    cat > "$TEMP_DIR/.env" << 'ENVFILE'
# Happy Pastures Creamery API Keys
# Fill in your actual API keys here

GEOAPIFY_API_KEY=your_geoapify_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_PLACES_API_KEY=your_google_places_key_here
ENVFILE
fi

# Create setup instructions
echo "📝 Creating setup instructions..."
cat > "$TEMP_DIR/SETUP_INSTRUCTIONS.md" << 'SETUPDOC'
# Happy Pastures Creamery - Quick Setup Guide

## 🚀 Quick Start (2 Steps!)

### Step 1: Run Automated Setup
```bash
./setup_demo.sh
```

This will:
- ✅ Create a virtual environment (`venv/`)
- ✅ Install all Python dependencies
- ✅ Verify your API keys

### Step 2: Start the Application
```bash
./start_app.sh
```

Then open: **http://localhost:8000/app**

---

## 📦 What is a Virtual Environment?

A **virtual environment** (venv) is an isolated Python environment that:
- Keeps dependencies separate from your system Python
- Prevents conflicts with other Python projects
- Makes the app portable and reproducible

The setup script automatically creates `venv/` directory - you don't need to do anything manually!

---

## 🔍 Manual Setup (Advanced)

If you prefer manual setup or `setup_demo.sh` fails:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify API keys
cat .env

# 5. Start app
./start_app.sh
```

---

## ✅ System Requirements

- **Python:** 3.9 or higher
- **Operating System:** macOS, Linux, or Windows
- **Internet:** Required for API calls

---

## 📦 What's Included

```
happy_pastures_demo/
├── backend/              # FastAPI backend server
│   ├── api.py           # REST API endpoints
│   ├── geoapify_client.py
│   ├── google_places_client.py
│   ├── sales_pitch_generator.py
│   └── cheese_products.py
├── frontend/            # Web interface
│   ├── index.html       # HTML structure
│   ├── style.css        # All CSS styles
│   └── app.js           # All JavaScript
├── venv/                # Virtual environment (created by setup_demo.sh)
├── .env                 # API keys (KEEP SECURE!)
├── requirements.txt     # Python dependencies
├── setup_demo.sh        # Setup script (creates venv, installs deps)
├── start_app.sh         # Startup script (activates venv, starts server)
└── Documentation files
```

---

## 🔧 Troubleshooting

### "Virtual environment not found" Error
```bash
# Run setup script first
./setup_demo.sh
```

### Port 8000 Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
./start_app.sh
```

### Missing Dependencies
```bash
# Make sure you ran setup first
./setup_demo.sh

# Or manually:
source venv/bin/activate
pip install -r requirements.txt
```

### Python Not Found
```bash
# Install Python (macOS)
brew install python3

# Verify version (need 3.9+)
python3 --version
```

### API Key Issues
- Geoapify: https://www.geoapify.com/ (Free tier: 3,000 requests/day)
- Anthropic: https://console.anthropic.com/ (Claude API)
- Google Places: https://console.cloud.google.com/ (Enable Places API)

---

## 🧪 Test the System

1. **GPS Search:** Click "Use My Current Location"
2. **Address Search:** Enter "Evanston, IL"
3. **View Pitch:** Click any restaurant to see AI-generated pitch
4. **Reject Restaurant:** Click "❌ Not Interested" to add to memory
5. **Get Directions:** Click "🗺️ Directions" for walking route

---

## 📚 Documentation

- **README.md** - Project overview
- **ARCHITECTURE.md** - Technical design decisions
- **FILTERING_SYSTEM.md** - Smart filtering explained
- **GOOGLE_PLACES_SETUP.md** - Google Places API setup

---

## 🔒 Security Note

**The .env file contains sensitive API keys!**
- Do NOT commit to git
- Do NOT share publicly
- Keep secure like passwords

---

## 💡 Features

✅ Mobile-first GPS location detection
✅ Smart Asian cuisine filtering (saves time + cost)
✅ Rejection learning system (remembers preferences)
✅ Walking directions integration
✅ AI-powered sales pitch generation
✅ Address history (last 5 searches)

---

## 📞 Support

For issues, check the console logs:
- Backend logs: Terminal where you ran `./start_app.sh`
- Frontend logs: Browser Console (F12)

Good luck with your demo! 🧀
SETUPDOC

# Create automated setup script
echo "🔧 Creating automated setup script..."
cat > "$TEMP_DIR/setup_demo.sh" << 'SETUPSCRIPT'
#!/bin/bash
# Automated Setup Script for Happy Pastures Creamery Demo

echo "🧀 Happy Pastures Creamery - Automated Setup"
echo "============================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if python3 -m venv venv; then
    echo "✅ Virtual environment created: ./venv"
else
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment and install requirements
echo ""
echo "Installing Python dependencies into virtual environment..."
source venv/bin/activate

if pip install --upgrade pip > /dev/null 2>&1; then
    echo "✅ pip upgraded"
fi

if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    deactivate
    exit 1
fi

deactivate

# Check .env file
echo ""
echo "Checking API configuration..."
if [ -f .env ]; then
    if grep -q "your_.*_key_here" .env; then
        echo "⚠️  WARNING: .env file contains placeholder keys"
        echo "   Please edit .env and add your real API keys"
    else
        echo "✅ .env file configured"
    fi
else
    echo "❌ No .env file found!"
    exit 1
fi

# Make start script executable
chmod +x start_app.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "📦 Virtual environment created at: ./venv"
echo "📋 All dependencies installed in isolated environment"
echo ""
echo "To start the application, run:"
echo "  ./start_app.sh"
echo ""
echo "Then open: http://localhost:8000/app"
SETUPSCRIPT

chmod +x "$TEMP_DIR/setup_demo.sh"
chmod +x "$TEMP_DIR/start_app.sh"

# Clean up Python cache files
echo "🧹 Cleaning up unnecessary files..."
find "$TEMP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$TEMP_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$TEMP_DIR" -type f -name ".DS_Store" -delete 2>/dev/null || true

# Rename temp directory to final name
echo "📦 Creating zip archive..."
cd /tmp
mv "$TEMP_DIR" "$DEMO_NAME"

# Create the zip file
zip -r "$OUTPUT_FILE" "$DEMO_NAME" > /dev/null 2>&1

# Move to original directory
mv "$OUTPUT_FILE" "$OLDPWD/"

# Use the renamed directory for cleanup
TEMP_DIR="/tmp/$DEMO_NAME"

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Get file size (in current directory now)
cd "$OLDPWD"
FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)

echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Output file: $OUTPUT_FILE"
echo "📏 Size: $FILE_SIZE"
echo ""
echo "📋 To deploy on another Mac:"
echo "   1. Copy $OUTPUT_FILE to the new machine"
echo "   2. unzip $OUTPUT_FILE"
echo "   3. cd $DEMO_NAME"
echo "   4. ./setup_demo.sh"
echo "   5. ./start_app.sh"
echo ""
echo "🔒 Security reminder: This package contains your API keys!"
echo "   Previous $OUTPUT_FILE has been overwritten."
echo ""
