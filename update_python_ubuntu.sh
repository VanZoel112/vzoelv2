#!/bin/bash
# Update Python di Ubuntu - Complete Guide
# Support Ubuntu 18.04, 20.04, 22.04, 24.04

echo "🐍 PYTHON UPDATE GUIDE FOR UBUNTU"
echo "=================================="

# Check current system
echo "🔍 Checking current system..."
ubuntu_version=$(lsb_release -rs 2>/dev/null || echo "unknown")
python_version=$(python3 --version 2>/dev/null | cut -d" " -f2 || echo "not installed")

echo "Ubuntu Version: $ubuntu_version"
echo "Current Python: $python_version"

# Function to update Python to latest version
update_python_latest() {
    echo ""
    echo "🚀 METHOD 1: Update to Latest Python (Recommended)"
    echo "================================================"
    
    echo "1️⃣ Update system packages:"
    echo "sudo apt update && sudo apt upgrade -y"
    
    echo ""
    echo "2️⃣ Install deadsnakes PPA (for latest Python versions):"
    echo "sudo apt install software-properties-common -y"
    echo "sudo add-apt-repository ppa:deadsnakes/ppa -y"
    echo "sudo apt update"
    
    echo ""
    echo "3️⃣ Install Python 3.12 (latest stable):"
    echo "sudo apt install python3.12 python3.12-venv python3.12-pip -y"
    
    echo ""
    echo "4️⃣ Install development packages:"
    echo "sudo apt install python3.12-dev python3.12-distutils -y"
    
    echo ""
    echo "5️⃣ Set Python 3.12 as default (optional):"
    echo "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1"
    
    echo ""
    echo "6️⃣ Verify installation:"
    echo "python3 --version"
    echo "python3 -m pip --version"
}

# Function to install specific Python version
install_specific_python() {
    echo ""
    echo "🎯 METHOD 2: Install Specific Python Version"
    echo "============================================"
    
    echo "Available versions via deadsnakes PPA:"
    echo "• Python 3.8:  sudo apt install python3.8 python3.8-venv python3.8-pip"
    echo "• Python 3.9:  sudo apt install python3.9 python3.9-venv python3.9-pip"
    echo "• Python 3.10: sudo apt install python3.10 python3.10-venv python3.10-pip"
    echo "• Python 3.11: sudo apt install python3.11 python3.11-venv python3.11-pip"
    echo "• Python 3.12: sudo apt install python3.12 python3.12-venv python3.12-pip"
    
    echo ""
    echo "Set specific version as default:"
    echo "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1"
    echo "sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2"
    echo ""
    echo "Switch between versions:"
    echo "sudo update-alternatives --config python3"
}

# Function to compile from source
compile_from_source() {
    echo ""
    echo "⚙️  METHOD 3: Compile from Source (Advanced)"
    echo "==========================================="
    
    echo "1️⃣ Install build dependencies:"
    echo "sudo apt install build-essential zlib1g-dev libncurses5-dev \\"
    echo "    libgdbm-dev libnss3-dev libssl-dev libreadline-dev \\"
    echo "    libffi-dev libsqlite3-dev wget libbz2-dev -y"
    
    echo ""
    echo "2️⃣ Download Python source:"
    echo "cd /tmp"
    echo "wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz"
    echo "tar -xf Python-3.12.0.tgz"
    echo "cd Python-3.12.0"
    
    echo ""
    echo "3️⃣ Configure and compile:"
    echo "./configure --enable-optimizations"
    echo "make -j \$(nproc)"
    echo "sudo make altinstall"
    
    echo ""
    echo "4️⃣ Create symlinks:"
    echo "sudo ln -sf /usr/local/bin/python3.12 /usr/bin/python3"
    echo "sudo ln -sf /usr/local/bin/pip3.12 /usr/bin/pip3"
}

# Function for virtual environment setup
setup_venv() {
    echo ""
    echo "🔒 METHOD 4: Use Virtual Environment (Safest)"
    echo "============================================="
    
    echo "1️⃣ Install latest Python (if needed):"
    echo "sudo apt install python3.12 python3.12-venv -y"
    
    echo ""
    echo "2️⃣ Create virtual environment:"
    echo "python3.12 -m venv ~/vzoelv2_env"
    
    echo ""
    echo "3️⃣ Activate virtual environment:"
    echo "source ~/vzoelv2_env/bin/activate"
    
    echo ""
    echo "4️⃣ Upgrade pip in venv:"
    echo "pip install --upgrade pip"
    
    echo ""
    echo "5️⃣ Install VzoelV2 dependencies:"
    echo "cd /path/to/vzoelv2"
    echo "pip install -r requirements.txt"
    
    echo ""
    echo "6️⃣ Run bot in venv:"
    echo "python main.py"
    
    echo ""
    echo "📝 Note: Always activate venv before running:"
    echo "source ~/vzoelv2_env/bin/activate"
}

# Quick fix for common issues
quick_fixes() {
    echo ""
    echo "🔧 QUICK FIXES FOR COMMON ISSUES"
    echo "================================"
    
    echo "❌ 'python3: command not found'"
    echo "Fix: sudo apt install python3"
    
    echo ""
    echo "❌ 'pip3: command not found'"
    echo "Fix: sudo apt install python3-pip"
    
    echo ""
    echo "❌ 'ModuleNotFoundError: No module named pip'"
    echo "Fix: python3 -m ensurepip --upgrade"
    
    echo ""
    echo "❌ Permission denied errors"
    echo "Fix: Use virtual environment or --user flag"
    echo "     pip3 install --user package_name"
    
    echo ""
    echo "❌ SSL/TLS certificate errors"
    echo "Fix: sudo apt install ca-certificates"
    echo "     pip3 install --trusted-host pypi.org --trusted-host pypi.python.org package_name"
}

# One-liner commands
one_liners() {
    echo ""
    echo "⚡ ONE-LINER COMMANDS"
    echo "==================="
    
    echo "🚀 Quick Python 3.12 install:"
    echo "sudo apt update && sudo apt install software-properties-common -y && sudo add-apt-repository ppa:deadsnakes/ppa -y && sudo apt update && sudo apt install python3.12 python3.12-pip python3.12-venv -y"
    
    echo ""
    echo "🔧 Fix pip and install VzoelV2 deps:"
    echo "python3 -m ensurepip --upgrade && python3 -m pip install --upgrade pip && pip3 install pyrogram tgcrypto aiofiles"
    
    echo ""
    echo "🐍 Create venv and install everything:"
    echo "python3 -m venv ~/vzoelv2_env && source ~/vzoelv2_env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"
}

# Check if running as script or sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    update_python_latest
    install_specific_python  
    compile_from_source
    setup_venv
    quick_fixes
    one_liners
    
    echo ""
    echo "🎯 RECOMMENDED FOR VZOELV2:"
    echo "==========================="
    echo "1. Use METHOD 1 for latest Python"
    echo "2. Use METHOD 4 (Virtual Environment) for isolation"
    echo "3. Run: bash install.sh (from VzoelV2 repo)"
    
    echo ""
    echo "📞 Need Help?"
    echo "Create issue: https://github.com/VanZoel112/vzoelv2/issues"
fi