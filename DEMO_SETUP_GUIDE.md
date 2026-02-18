# Demo Setup Guide - Virtual Environment Included

## 🎯 Quick Answer

**Yes, the user needs to install dependencies**, but it's **automated** with virtual environment!

Just run:
```bash
./setup_demo.sh  # Creates venv + installs everything
./start_app.sh   # Activates venv + starts server
```

---

## 📦 What Happens Automatically

### Step 1: `./setup_demo.sh`
```bash
✅ Creates virtual environment (venv/)
✅ Activates the venv
✅ Upgrades pip
✅ Installs all dependencies from requirements.txt
✅ Verifies .env file exists
```

### Step 2: `./start_app.sh`
```bash
✅ Checks if venv exists
✅ Activates the venv
✅ Starts the FastAPI server
✅ Deactivates venv when done
```

---

## 🔍 Virtual Environment Benefits

### Why Use venv?
1. **Isolation** - Dependencies don't conflict with system Python
2. **Portability** - Same setup works on any machine
3. **Clean** - Easy to delete and recreate
4. **Safety** - Won't break other Python projects

### What Gets Installed?
From `requirements.txt`:
```
fastapi==0.115.6
uvicorn[standard]==0.34.0
requests==2.32.3
anthropic==0.42.0
python-dotenv==1.0.1
```

All installed **only** in `venv/` directory, not system-wide!

---

## 📋 Complete Workflow on 2nd Mac

### First Time Setup (One Time Only)
```bash
# 1. Unzip package
unzip happy_pastures_demo_20260217_181405.zip

# 2. Enter directory
cd happy_pastures_demo_20260217_181405

# 3. Run setup (creates venv, installs deps)
./setup_demo.sh

# Output:
# ✅ Virtual environment created: ./venv
# ✅ Dependencies installed successfully
# ✅ .env file configured
```

### Every Time You Start the App
```bash
# Just run start script (it handles venv automatically)
./start_app.sh

# Output:
# Activating virtual environment...
# Starting FastAPI backend server...
# API will be available at: http://localhost:8000
```

### Stopping the App
```bash
# Press Ctrl+C in terminal
# venv automatically deactivates
```

---

## 🗂️ Directory Structure After Setup

```
happy_pastures_demo_20260217_181405/
├── venv/                         # ⬅️ CREATED BY setup_demo.sh
│   ├── bin/                      # Python executable, activation scripts
│   ├── lib/                      # Installed packages (FastAPI, etc.)
│   └── pyvenv.cfg               # Virtual environment config
├── backend/
├── frontend/
├── tests/
├── .env                          # Your API keys
├── requirements.txt              # Dependency list
├── setup_demo.sh                 # Setup script (run once)
├── start_app.sh                  # Start script (run each time)
└── SETUP_INSTRUCTIONS.md
```

**Note:** The `venv/` folder is NOT in the zip file - it gets created during setup!

---

## 🆚 Old Way vs. New Way

### ❌ Old Way (Manual)
```bash
# User has to remember to:
pip3 install -r requirements.txt  # Installs system-wide
python backend/api.py             # Hope dependencies are correct
```

**Problems:**
- Dependencies installed system-wide
- Conflicts with other Python projects
- Hard to clean up

### ✅ New Way (Automated with venv)
```bash
./setup_demo.sh  # One time: creates venv + installs
./start_app.sh   # Every time: activates venv + runs
```

**Benefits:**
- Isolated environment
- Repeatable setup
- Easy to delete (just remove venv/)
- No system pollution

---

## 🔧 Manual venv Operations (Advanced)

### Activate venv manually
```bash
source venv/bin/activate
# Prompt changes to: (venv) user@machine:~$
```

### Install/update packages
```bash
source venv/bin/activate
pip install some-new-package
pip freeze > requirements.txt  # Save new deps
```

### Deactivate venv
```bash
deactivate
# Back to system Python
```

### Delete and recreate
```bash
rm -rf venv/
./setup_demo.sh  # Recreates from scratch
```

---

## 🧪 Test the New Package

On your 1st Mac, test the automated setup:

```bash
# Create temp test directory
mkdir ~/Desktop/test_package
cd ~/Desktop/test_package

# Copy and extract
cp ~/git_repos/crisp_takehome/happy_pastures_demo_20260217_181405.zip .
unzip happy_pastures_demo_20260217_181405.zip
cd happy_pastures_demo_20260217_181405

# Run setup
./setup_demo.sh

# Check venv was created
ls -la venv/

# Start app
./start_app.sh

# Visit http://localhost:8000/app
```

Should work perfectly! 🎉

---

## 💡 Package Improvements Made

### Latest Package: `happy_pastures_demo_20260217_181405.zip`

**New features:**
1. ✅ `setup_demo.sh` creates virtual environment automatically
2. ✅ `start_app.sh` activates venv before starting server
3. ✅ `SETUP_INSTRUCTIONS.md` explains venv benefits
4. ✅ Better error messages if venv missing
5. ✅ Deactivates venv cleanly when server stops

**Old packages (before this):**
- ❌ Required manual pip install
- ❌ No venv isolation
- ❌ System-wide dependency installation

---

## 📞 Common Questions

### Q: Do I need to activate venv before running start_app.sh?
**A:** No! `start_app.sh` automatically activates it.

### Q: Can I use my own venv instead?
**A:** Yes! Just skip `setup_demo.sh` and create your own:
```bash
python3 -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
```
Then edit `start_app.sh` to use `my_venv` instead.

### Q: What if setup_demo.sh fails?
**A:** Try manual setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Q: Can I delete venv/ and recreate?
**A:** Yes! It's safe to delete and recreate anytime:
```bash
rm -rf venv/
./setup_demo.sh  # Recreates everything
```

---

## ✅ Summary

**Bottom line:** The user needs to install requirements.txt, but it's fully automated!

1. **First time:** Run `./setup_demo.sh` (creates venv, installs deps)
2. **Every time:** Run `./start_app.sh` (activates venv, starts app)
3. **No manual pip commands needed!**

The virtual environment keeps everything clean and isolated. 🎯
