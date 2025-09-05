#!/bin/bash
# VZOEL ASSISTANT v2 - Installation Script
# Enhanced installation dengan premium features

echo "🚀 VZOEL ASSISTANT v2 - Premium Bot Installation"
echo "================================================"

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d" " -f2 | cut -d"." -f1-2)
echo "Python version: $python_version"

if [[ $(echo "$python_version 3.8" | awk '{print ($1 >= $2)}') == 1 ]]; then
    echo "✅ Python version compatible"
else
    echo "❌ Python 3.8+ required"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3-pip python3-dev build-essential libffi-dev
elif command -v pkg &> /dev/null; then
    pkg update
    pkg install -y python build-essential libffi
fi

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip3 install --upgrade pip

# Install core dependencies first
echo "🔧 Installing core framework..."
pip3 install pyrogram==2.0.106 tgcrypto==1.2.5

# Install requirements (step by step for better error handling)
echo "⚡ Installing core requirements first..."
if [ -f "requirements-minimal.txt" ]; then
    pip3 install -r requirements-minimal.txt
else
    echo "⚠️  Minimal requirements not found, installing manually..."
    pip3 install pyrogram tgcrypto aiofiles aiohttp PyYAML python-dotenv aiosqlite colorama
fi

echo "📚 Installing full requirements..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --no-deps --force-reinstall || {
        echo "⚠️  Some packages failed, trying without --no-deps..."
        pip3 install -r requirements.txt
    }
else
    echo "❌ requirements.txt not found"
    exit 1
fi

# Verify critical imports
echo "🧪 Verifying installation..."
python3 -c "
try:
    import pyrogram
    import aiofiles
    import aiohttp
    from utils.assets import vzoel_assets
    print('✅ All critical modules imported successfully')
    print(f'✅ Pyrogram version: {pyrogram.__version__}')
    print(f'✅ VzoelAssets loaded: {len(vzoel_assets.emojis.get(\"emojis\", {}))} emojis')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 INSTALLATION COMPLETED SUCCESSFULLY!"
    echo "================================================"
    echo "📋 Next steps:"
    echo "1. Configure config.json with your bot tokens"
    echo "2. Run: python3 main.py"
    echo "3. Enjoy premium features! 🚀"
    echo ""
    echo "🔗 Repository: https://github.com/VanZoel112/vzoelv2"
    echo "👨‍💻 Created by: Vzoel Fox's Assistant"
else
    echo "❌ Installation verification failed"
    exit 1
fi