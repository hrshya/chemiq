#!/bin/bash
# Quick start script for the entire application

echo "🚀 Chemical Equipment Parameter Visualizer - Quick Start"
echo "======================================================="
echo ""

# Check Python
echo "📋 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python $(python3 --version | cut -d' ' -f2) found"
echo ""

# Check Node.js
echo "📋 Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16 or higher."
    exit 1
fi
echo "✓ Node.js $(node --version | cut -d'v' -f2) found"
echo ""

# Start backend
echo "🔨 Starting Backend..."
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
pip install -q -r requirements.txt 2>/dev/null || true
python3 manage.py migrate > /dev/null 2>&1
echo "✓ Backend starting on port 8000..."
python3 manage.py runserver &
BACKEND_PID=$!
sleep 2

# Start frontend
echo "🎨 Starting Frontend..."
cd ../frontend/web
npm install -q > /dev/null 2>&1
echo "✓ Frontend starting on port 3000..."
npm run dev &
FRONTEND_PID=$!
sleep 2

echo ""
echo "✅ Application Started!"
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend API: http://localhost:8000/api"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Wait for both processes
wait
