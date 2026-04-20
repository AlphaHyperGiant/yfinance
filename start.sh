#!/bin/bash
# Quick start script for Stock Portfolio Tracker

echo "🚀 Starting Stock Portfolio Tracker..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements-app.txt

# Start the application
echo ""
echo "✅ Starting Flask server..."
echo "📱 Open http://localhost:5000 in your browser"
echo ""
python app.py
