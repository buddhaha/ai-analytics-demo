#!/bin/bash

# Start Backend Server
# This script activates the virtual environment and starts the FastAPI server

set -e

echo "🚀 Starting AI Analytics Backend..."
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment and start server
cd backend
source venv/bin/activate

echo "✅ Virtual environment activated"
echo "✅ Starting FastAPI server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3.11 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Made with Bob
