#!/bin/bash
# VZOEL ASSISTANT v2 - Fixed Installation Script
# Guaranteed to fix "No module named 'pyrogram'" error

set -e  # Exit on error

echo "🔥 VZOEL V2 - EMERGENCY FIX INSTALLER"
echo "===================================="

# Check Python
echo "🐍 Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Install Python first:"
    echo "sudo apt install python3 python3-pip -y"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Update pip first (skip in Termux)
echo "⬆️  Updating pip..."
if [[ "$PREFIX" == *"com.termux"* ]]; then
    echo "🤖 Detected Termux, skipping pip upgrade"
else
    python3 -m pip install --upgrade pip --user
fi

# Install essential packages one by one
echo "📦 Installing CORE packages..."

essential_packages=(
    "pyrogram>=2.0.106"
    "tgcrypto>=1.2.5" 
    "aiofiles>=23.0.0"
    "aiohttp>=3.8.0"
    "PyYAML>=6.0.0"
    "python-dotenv>=1.0.0"
    "aiosqlite>=0.19.0"
    "colorama>=0.4.6"
    "requests>=2.31.0"
)

for package in "${essential_packages[@]}"; do
    echo "📦 Installing $package..."
    python3 -m pip install "$package" --user --no-warn-script-location
done

# Install performance boost
echo "⚡ Installing performance packages..."
if [[ "$OSTYPE" != "msys" ]]; then
    python3 -m pip install "uvloop>=0.19.0" --user --no-warn-script-location || echo "⚠️  uvloop failed (optional)"
fi

# Additional useful packages
echo "🔧 Installing additional utilities..."
additional_packages=(
    "motor>=3.3.0"
    "rich>=13.7.0" 
    "click>=8.1.7"
    "cryptography>=41.0.0"
    "Pillow>=10.0.0"
    "httpx>=0.27.0"
)

for package in "${additional_packages[@]}"; do
    echo "📦 Installing $package..."
    python3 -m pip install "$package" --user --no-warn-script-location || echo "⚠️  $package failed (optional)"
done

# Test critical imports
echo ""
echo "🧪 Testing critical imports..."
python3 -c "
import sys
sys.path.insert(0, '.')

try:
    import pyrogram
    print('✅ pyrogram imported successfully')
    
    import aiofiles
    print('✅ aiofiles imported successfully')
    
    import aiohttp
    print('✅ aiohttp imported successfully')
    
    import yaml
    print('✅ PyYAML imported successfully')
    
    from utils.assets import vzoel_assets
    print('✅ VzoelAssets imported successfully')
    print(f'✅ Emojis loaded: {len(vzoel_assets.emojis.get(\"emojis\", {}))}')
    
    print('')
    print('🎉 ALL IMPORTS SUCCESSFUL!')
    print('🚀 Ready to run: python3 main.py')
    
except ImportError as e:
    print(f'❌ Import failed: {e}')
    print('Try running the script again or check Python path')
    sys.exit(1)
except Exception as e:
    print(f'⚠️  VzoelAssets check failed: {e}')
    print('✅ Core packages OK, run from project directory')
"

echo ""
echo "✅ INSTALLATION COMPLETED!"
echo "=========================="
echo "🚀 Next steps:"
echo "1. cd /path/to/vzoelv2"  
echo "2. python3 main.py"
echo ""
echo "💡 If still getting errors:"
echo "export PYTHONPATH=\$PYTHONPATH:\$(pwd)"
echo "python3 main.py"