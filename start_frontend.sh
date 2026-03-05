#!/bin/bash

# Start Frontend Development Server
# This script starts the React development server with Vite

set -e

echo "🚀 Starting AI Analytics Frontend..."
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Error: node_modules not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Start development server
cd frontend

echo "✅ Starting Vite development server on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev

# Made with Bob
