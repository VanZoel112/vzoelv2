#!/usr/bin/env python3
"""
Verify VzoelV2 Installation
Quick check untuk memastikan semua dependencies terinstall
"""

def verify_installation():
    print("🔍 VERIFYING VZOEL ASSISTANT v2 INSTALLATION")
    print("=" * 50)
    
    required_modules = [
        ("pyrogram", "Telegram bot framework"),
        ("aiofiles", "Async file operations"), 
        ("aiohttp", "HTTP client"),
        ("PIL", "Image processing"),
        ("yaml", "YAML parsing"),
        ("asyncio", "Async support")
    ]
    
    optional_modules = [
        ("cv2", "OpenCV image processing"),
        ("redis", "Redis database"),
        ("motor", "MongoDB async driver")
    ]
    
    success_count = 0
    total_required = len(required_modules)
    
    print("📋 Checking required modules:")
    for module, description in required_modules:
        try:
            if module == "PIL":
                import PIL
                version = PIL.__version__
            else:
                imported = __import__(module)
                version = getattr(imported, '__version__', 'unknown')
            
            print(f"  ✅ {module} ({description}): v{version}")
            success_count += 1
        except ImportError:
            print(f"  ❌ {module} ({description}): NOT FOUND")
    
    print(f"\n📋 Checking optional modules:")
    for module, description in optional_modules:
        try:
            imported = __import__(module)
            version = getattr(imported, '__version__', 'unknown')
            print(f"  ✅ {module} ({description}): v{version}")
        except ImportError:
            print(f"  ⚠️  {module} ({description}): Optional - not installed")
    
    print(f"\n📊 INSTALLATION STATUS:")
    print(f"Required modules: {success_count}/{total_required}")
    
    if success_count == total_required:
        print("🎉 ALL REQUIRED MODULES INSTALLED!")
        
        # Test VzoelAssets if available
        try:
            from utils.assets import vzoel_assets
            emoji_count = len(vzoel_assets.emojis.get('emojis', {}))
            print(f"🚀 VzoelAssets integration: {emoji_count} emojis loaded")
        except ImportError:
            print("⚠️  VzoelAssets not found (run from project directory)")
        
        print("\n✨ Ready to run VzoelV2!")
        return True
    else:
        print("❌ MISSING REQUIRED MODULES!")
        print("Run: pip3 install -r requirements.txt")
        return False

if __name__ == "__main__":
    verify_installation()