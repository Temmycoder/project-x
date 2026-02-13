#!/bin/bash

# X-Share Setup Script for macOS/Linux

echo ""
echo "╔════════════════════════════════════╗"
echo "║       X-Share Setup Wizard          ║"
echo "║   Professional Screen Sharing       ║"
echo "╚════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Setup Backend
echo "📦 Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Python setup failed"
    exit 1
fi
cd ..

# Setup Frontend
echo "📦 Installing Node dependencies..."
cd electron-app
npm install
if [ $? -ne 0 ]; then
    echo "❌ Node setup failed"
    exit 1
fi
cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Python Server (Terminal 1):"
echo "   cd backend"
echo "   python3 server.py"
echo ""
echo "2. Start Electron App (Terminal 2):"
echo "   cd electron-app"
echo "   npm run dev"
echo ""
echo "Happy streaming! 🚀"
echo ""
