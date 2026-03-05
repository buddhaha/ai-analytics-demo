#!/bin/bash
# Complete setup script for AI Analytics Demo (Backend + Frontend)

echo "🚀 AI Analytics Demo - Complete Setup"
echo "======================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 is not installed. Please install Python 3.11."
    echo "   On macOS: brew install python@3.11"
    echo "   On Ubuntu: sudo apt install python3.11"
    exit 1
fi

python_version=$(python3.11 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi
node_version=$(node --version)
echo "✓ Node.js version: $node_version"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
npm_version=$(npm --version)
echo "✓ npm version: $npm_version"

echo ""
echo "======================================"
echo "📦 BACKEND SETUP"
echo "======================================"
echo ""

# Backend setup
cd backend

echo "🔧 Creating Python virtual environment..."
python3.11 -m venv venv

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo "⚙️  Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "⚠️  IMPORTANT: You need to add your ANTHROPIC_API_KEY to backend/.env"
else
    echo "✓ .env file already exists"
fi

echo "🗄️  Creating and seeding database..."
python3.11 scripts/seed_data.py

echo ""
echo "======================================"
echo "🎨 FRONTEND SETUP"
echo "======================================"
echo ""

cd ../frontend

echo "📥 Installing Node.js dependencies..."
npm install

echo "⚙️  Setting up frontend environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created frontend .env file"
else
    echo "✓ Frontend .env file already exists"
fi

cd ..

echo ""
echo "======================================"
echo "✅ SETUP COMPLETE!"
echo "======================================"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Add your Anthropic API key:"
echo "   Edit backend/.env and set ANTHROPIC_API_KEY=your-key-here"
echo ""
echo "2. Start the backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python -m app.main"
echo ""
echo "3. Start the frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open your browser:"
echo "   http://localhost:5173"
echo ""
echo "📚 For detailed instructions, see START_HERE.md"
echo ""

# Made with Bob
