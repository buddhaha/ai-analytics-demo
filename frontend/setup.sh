#!/bin/bash
# Frontend setup script for AI Analytics Demo

echo "🎨 AI Analytics Frontend - Setup"
echo "================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

node_version=$(node --version)
echo "✓ Node.js version: $node_version"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi

npm_version=$(npm --version)
echo "✓ npm version: $npm_version"

echo ""
echo "📥 Installing dependencies..."
npm install

echo ""
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "To start the development server:"
echo "  npm run dev"
echo ""
echo "The app will be available at:"
echo "  http://localhost:5173"
echo ""

# Made with Bob
