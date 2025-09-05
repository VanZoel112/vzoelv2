# 🚀 VzoelV2 Installation Guide

## Quick Fix untuk "ModuleNotFoundError: No module named 'pyrogram'"

### Method 1: Emergency Fix (Recommended)
```bash
cd /home/ubuntu/vzoelv2
bash install-fix.sh
```

### Method 2: Manual Install
```bash
# Update system
sudo apt update && sudo apt install python3-pip -y

# Install core packages
pip3 install pyrogram>=2.0.106 tgcrypto>=1.2.5 aiofiles aiohttp PyYAML python-dotenv aiosqlite colorama

# Run bot
python3 main.py
```

### Method 3: Virtual Environment (Safest)
```bash
# Create virtual environment
python3 -m venv ~/vzoelv2_env
source ~/vzoelv2_env/bin/activate

# Install dependencies
pip install -r requirements-minimal.txt
pip install -r requirements.txt

# Run bot
python main.py
```

## Installation Scripts Available

| Script | Purpose | Usage |
|--------|---------|-------|
| `install-fix.sh` | Emergency fix for import errors | `bash install-fix.sh` |
| `install.sh` | Full installation with all features | `bash install.sh` |
| `quick_python_update.sh` | Update Python to 3.12 | `bash quick_python_update.sh` |
| `verify_install.py` | Check installation status | `python3 verify_install.py` |

## Requirements Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `requirements-minimal.txt` | Core dependencies only | Fix import errors quickly |
| `requirements.txt` | Full feature set | Complete installation |

## Troubleshooting

### Error: "python3: command not found"
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### Error: "pip3: command not found" 
```bash
python3 -m ensurepip --upgrade
# or
sudo apt install python3-pip -y
```

### Error: Permission denied
```bash
# Use --user flag
pip3 install --user package_name

# Or use virtual environment (recommended)
python3 -m venv ~/vzoelv2_env
source ~/vzoelv2_env/bin/activate
```

### Error: "No module named 'utils.assets'"
```bash
# Make sure you're in the right directory
cd /home/ubuntu/vzoelv2

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 main.py
```

## Quick Start After Installation

1. **Configure bot:**
   ```bash
   cp config.json.example config.json
   nano config.json  # Add your bot token and API credentials
   ```

2. **Run bot:**
   ```bash
   python3 main.py
   ```

3. **Check status:**
   ```bash
   python3 verify_install.py
   ```

## System Requirements

- **OS:** Ubuntu 18.04+ / Debian 10+ / Any Linux
- **Python:** 3.8+ (3.12 recommended)
- **RAM:** 512MB minimum
- **Storage:** 1GB free space

## Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/VanZoel112/vzoelv2/issues)
- 📖 **Documentation:** Check `docs/` folder
- 💬 **Community:** Telegram @VzoelSupport

---
*Created by Vzoel Fox's Assistant with ❤️*