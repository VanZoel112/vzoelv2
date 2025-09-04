#!/usr/bin/env python3
"""
Test script untuk Vzoel Assets Manager
Menguji kelengkapan font dan emoji premium
"""

import sys
import os
sys.path.append('.')

from utils.assets import VzoelAssets, bold, italic, emoji, vzoel_msg

def test_fonts():
    """Test font styling capabilities"""
    print("=" * 50)
    print("🎨 TESTING FONT STYLING")
    print("=" * 50)
    
    assets = VzoelAssets()
    test_text = "VzoelFox Assistant"
    
    print(f"Original: {test_text}")
    print(f"Bold: {assets.bold(test_text)}")
    print(f"Italic: {assets.italic(test_text)}")
    print(f"Bold+Italic: {assets.bold_italic(test_text)}")
    print(f"Monospace: {assets.monospace(test_text)}")
    
    # Test with numbers and mixed characters
    mixed_text = "Vzoel123 Fox's!"
    print(f"\nMixed text: {mixed_text}")
    print(f"Bold mixed: {assets.bold(mixed_text)}")
    
    # Test shortcut functions
    print(f"\nShortcut bold: {bold('Quick Test')}")
    print(f"Shortcut italic: {italic('Quick Test')}")

def test_emojis():
    """Test emoji mapping capabilities"""
    print("\n" + "=" * 50)
    print("😀 TESTING EMOJI MAPPING")
    print("=" * 50)
    
    assets = VzoelAssets()
    
    # Test individual emojis
    emoji_keys = ["utama", "centang", "petir", "loading", "kuning", "biru", "merah"]
    print("Individual Emojis:")
    for key in emoji_keys:
        emoji_char = assets.get_emoji(key)
        emoji_id = assets.get_emoji_id(key)
        print(f"  {key}: {emoji_char} (ID: {emoji_id})")
    
    # Test categories
    print("\nEmojis by Category:")
    categories = ["primary", "system", "fun", "special"]
    for category in categories:
        emojis = assets.get_emojis_by_category(category)
        print(f"  {category}: {' '.join(emojis)}")
    
    # Test usage patterns
    print("\nCommand Patterns:")
    commands = ["ping", "alive", "gcast"]
    for cmd in commands:
        emojis = assets.get_usage_pattern(cmd)
        print(f"  /{cmd}: {' '.join(emojis)}")
    
    # Test status indicators
    print("\nStatus Indicators:")
    statuses = ["success", "loading", "error", "active"]
    for status in statuses:
        emojis = assets.get_status_emojis(status)
        print(f"  {status}: {' '.join(emojis)}")

def test_themes():
    """Test theme combinations"""
    print("\n" + "=" * 50)
    print("🎨 TESTING THEME COMBINATIONS")
    print("=" * 50)
    
    assets = VzoelAssets()
    
    themes = ["vzoel_primary", "vzoel_fun", "vzoel_system", "vzoel_special"]
    for theme in themes:
        emojis = assets.get_theme_emojis(theme)
        print(f"{theme}: {' '.join(emojis)}")

def test_signature():
    """Test Vzoel signature"""
    print("\n" + "=" * 50)
    print("✨ TESTING VZOEL SIGNATURE")
    print("=" * 50)
    
    assets = VzoelAssets()
    signature = assets.vzoel_signature()
    print(f"Signature: {signature}")

def test_message_formatting():
    """Test complete message formatting"""
    print("\n" + "=" * 50)
    print("💬 TESTING MESSAGE FORMATTING")
    print("=" * 50)
    
    # Test various message formats
    messages = [
        ("Bot Aktif!", "bold", "alive"),
        ("Sedang memproses...", "italic", "ping"),
        ("Pesan berhasil dikirim", "bold_italic", "gcast"),
        ("Error detected", "monospace", None)
    ]
    
    for text, style, pattern in messages:
        formatted = vzoel_msg(text, style, pattern)
        print(f"{style} + {pattern}: {formatted}")

def test_asset_info():
    """Test asset information"""
    print("\n" + "=" * 50)
    print("📊 ASSET INFORMATION")
    print("=" * 50)
    
    assets = VzoelAssets()
    info = assets.get_asset_info()
    
    print("Font Information:")
    print(f"  Available styles: {info['fonts']['available_styles']}")
    print(f"  Total styles: {info['fonts']['total_styles']}")
    
    print("\nEmoji Information:")
    print(f"  Total emojis: {info['emojis']['total_emojis']}")
    print(f"  Categories: {info['emojis']['categories']}")
    print(f"  Total categories: {info['emojis']['total_categories']}")
    
    print("\nBranding:")
    branding = info.get('branding', {})
    for key, value in branding.items():
        print(f"  {key}: {value}")
    
    print(f"\nVersion: {info['version']}")

def main():
    """Main test function"""
    print("🚀 VZOEL ASSETS TEST SUITE")
    print("Testing font and emoji premium capabilities\n")
    
    try:
        test_fonts()
        test_emojis()
        test_themes()
        test_signature()
        test_message_formatting()
        test_asset_info()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("Asset sistem siap digunakan untuk produksi")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)