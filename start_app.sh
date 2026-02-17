#!/bin/bash
# Start the Happy Pastures Creamery App
# Simple script to launch the backend API server

echo "🧀 Happy Pastures Creamery - Starting Application"
echo "=================================================="
echo ""
echo "Starting FastAPI backend server..."
echo "API will be available at: http://localhost:8000"
echo "Web app will be available at: http://localhost:8000/app"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")/backend"
python api.py
