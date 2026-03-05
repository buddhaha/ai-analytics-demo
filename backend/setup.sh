#!/bin/bash
# Setup script for AI Analytics Demo Backend

echo "🚀 Setting up AI Analytics Demo Backend..."

# Check Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 is not installed. Please install Python 3.11."
    echo "   On macOS: brew install python@3.11"
    echo "   On Ubuntu: sudo apt install python3.11"
    exit 1
fi

python_version=$(python3.11 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your ANTHROPIC_API_KEY"
else
    echo "✓ .env file already exists"
fi

# Create database
echo "🗄️  Creating and seeding database..."
python3.11 scripts/seed_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your ANTHROPIC_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start the server: python -m app.main"
echo "4. Visit http://localhost:8000/docs for API documentation"
echo ""

# Made with Bob
