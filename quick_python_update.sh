#!/bin/bash
# Quick Python Update for Ubuntu - VzoelV2 Compatible

set -e  # Exit on any error

echo "🚀 QUICK PYTHON UPDATE FOR UBUNTU"
echo "================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Don't run this script as root (remove sudo)"
   exit 1
fi

echo "📋 Current Python version:"
python3 --version 2>/dev/null || echo "Python3 not found"

echo ""
echo "🔄 Updating system packages..."
sudo apt update

echo ""  
echo "🐍 Installing Python 3.12 (latest stable)..."
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12 with all needed packages
sudo apt install python3.12 python3.12-venv python3.12-pip python3.12-dev python3.12-distutils -y

echo ""
echo "🔧 Setting up Python alternatives..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
sudo update-alternatives --install /usr/bin/python3 python3 $(which python3) 1

echo ""
echo "🔗 Creating symlinks..."
sudo ln -sf /usr/bin/python3.12 /usr/local/bin/python3
sudo ln -sf /usr/lib/python3/dist-packages/pip /usr/local/bin/pip3

echo ""
echo "⬆️  Upgrading pip..."
python3 -m pip install --upgrade pip --user

echo ""
echo "✅ Python update completed!"
echo "📋 New Python version:"
python3 --version
python3 -m pip --version

echo ""
echo "🎯 Next steps for VzoelV2:"
echo "1. cd /home/ubuntu/vzoelv2" 
echo "2. bash install.sh"
echo "3. python3 main.py"

echo ""
echo "💡 Or use virtual environment (recommended):"
echo "python3 -m venv ~/vzoelv2_env"
echo "source ~/vzoelv2_env/bin/activate" 
echo "pip install -r requirements.txt"