#!/bin/bash
# VZOEL Assistant v2 - Startup Script
# Created by: Vzoel Fox's

echo "🚀 Starting VZOEL Assistant v2..."
echo "📁 Current directory: $(pwd)"
echo "🐍 Python version: $(python3 --version)"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found!"
    echo "📋 Please run: cp .env.example .env"
    echo "✏️ Then edit .env with your credentials"
    exit 1
fi

# Check if session string exists
if grep -q "SESSION_STRING=" .env && ! grep -q "SESSION_STRING=$" .env; then
    echo "✅ Session string found"
else
    echo "⚠️ No session string found"
    echo "🔑 Please run: python3 generate_session.py"
    echo "📝 Or add SESSION_STRING to .env file"
fi

echo "🤖 Starting bot..."
echo "🛑 Press Ctrl+C to stop"
echo ""

# Start the bot
python3 main.py