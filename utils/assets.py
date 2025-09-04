"""
Vzoel Assets Manager - Font & Emoji Utilities
Enhanced asset management for Vzoel Fox's Assistant
"""

import json
import os
from typing import Dict, Any, List, Optional

class VzoelAssets:
    def __init__(self, assets_path: str = "vzoel"):
        """Initialize Vzoel Assets Manager"""
        self.assets_path = assets_path
        self.fonts = self._load_fonts()
        self.emojis = self._load_emojis()
    
    def _load_fonts(self) -> Dict[str, Any]:
        """Load font mapping from vzoel_fonts.json"""
        try:
            font_path = os.path.join(self.assets_path, "vzoel_fonts.json")
            with open(font_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"style_map": {}}
    
    def _load_emojis(self) -> Dict[str, Any]:
        """Load emoji mapping from vzoel_emojis.json"""
        try:
            emoji_path = os.path.join(self.assets_path, "vzoel_emojis.json")
            with open(emoji_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"emojis": {}, "categories": {}, "usage_patterns": {}}
    
    # Font Styling Methods
    def bold(self, text: str) -> str:
        """Apply bold formatting to text"""
        return self._apply_style(text, "bold")
    
    def italic(self, text: str) -> str:
        """Apply italic formatting to text"""
        return self._apply_style(text, "italic")
    
    def bold_italic(self, text: str) -> str:
        """Apply bold+italic formatting to text"""
        return self._apply_style(text, "bold_italic")
    
    def monospace(self, text: str) -> str:
        """Apply monospace formatting to text"""
        return self._apply_style(text, "monospace")
    
    def _apply_style(self, text: str, style: str) -> str:
        """Apply specific style to text character by character"""
        style_map = self.fonts.get("style_map", {}).get(style, {})
        if not style_map:
            return text
        
        result = ""
        for char in text:
            if char in style_map:
                result += style_map[char]
            else:
                # For unsupported characters, apply simple markdown
                if style == "bold":
                    result += f"**{char}**"
                elif style == "italic":
                    result += f"*{char}*"
                elif style == "bold_italic":
                    result += f"***{char}***"
                elif style == "monospace":
                    result += f"`{char}`"
                else:
                    result += char
        return result
    
    # Emoji Methods
    def get_emoji(self, emoji_key: str) -> str:
        """Get emoji character by key"""
        emoji_data = self.emojis.get("emojis", {}).get(emoji_key, {})
        return emoji_data.get("emoji_char", "")
    
    def get_emoji_id(self, emoji_key: str) -> str:
        """Get custom emoji ID by key"""
        emoji_data = self.emojis.get("emojis", {}).get(emoji_key, {})
        return emoji_data.get("custom_emoji_id", "")
    
    def get_emojis_by_category(self, category: str) -> List[str]:
        """Get all emojis in a specific category"""
        category_data = self.emojis.get("categories", {}).get(category, {})
        emoji_keys = category_data.get("emojis", [])
        return [self.get_emoji(key) for key in emoji_keys]
    
    def get_usage_pattern(self, command: str) -> List[str]:
        """Get emoji pattern for specific command"""
        patterns = self.emojis.get("usage_patterns", {}).get("command_responses", {})
        emoji_keys = patterns.get(command, [])
        return [self.get_emoji(key) for key in emoji_keys]
    
    def get_status_emojis(self, status: str) -> List[str]:
        """Get emojis for status indicators"""
        patterns = self.emojis.get("usage_patterns", {}).get("status_indicators", {})
        emoji_keys = patterns.get(status, [])
        return [self.get_emoji(key) for key in emoji_keys]
    
    def get_theme_emojis(self, theme: str) -> List[str]:
        """Get emojis for specific theme"""
        patterns = self.emojis.get("usage_patterns", {}).get("themes", {})
        emoji_keys = patterns.get(theme, [])
        return [self.get_emoji(key) for key in emoji_keys]
    
    # Utility Methods
    def format_message(self, text: str, style: str = "bold", 
                      emoji_pattern: Optional[str] = None) -> str:
        """Format message with style and emoji"""
        # Apply text styling
        if style == "bold":
            formatted_text = self.bold(text)
        elif style == "italic":
            formatted_text = self.italic(text)
        elif style == "bold_italic":
            formatted_text = self.bold_italic(text)
        elif style == "monospace":
            formatted_text = self.monospace(text)
        else:
            formatted_text = text
        
        # Add emoji pattern if specified
        if emoji_pattern:
            emojis = self.get_usage_pattern(emoji_pattern)
            if emojis:
                return f"{emojis[0]} {formatted_text} {emojis[-1]}"
        
        return formatted_text
    
    def vzoel_signature(self) -> str:
        """Get Vzoel Fox's signature with emojis"""
        signature_emojis = self.emojis.get("quick_access", {}).get("vzoel_signature", [])
        emojis = []
        for emoji_id in signature_emojis:
            for key, data in self.emojis.get("emojis", {}).items():
                if data.get("custom_emoji_id") == emoji_id:
                    emojis.append(data.get("emoji_char", ""))
                    break
        
        if emojis:
            return f"{emojis[0]} Vzoel Fox's Assistant {emojis[1]}{emojis[2]}"
        return "🤩 Vzoel Fox's Assistant 😈⛈"
    
    # Asset Information
    def get_asset_info(self) -> Dict[str, Any]:
        """Get comprehensive asset information"""
        font_styles = list(self.fonts.get("style_map", {}).keys())
        emoji_count = len(self.emojis.get("emojis", {}))
        categories = list(self.emojis.get("categories", {}).keys())
        
        return {
            "fonts": {
                "available_styles": font_styles,
                "total_styles": len(font_styles)
            },
            "emojis": {
                "total_emojis": emoji_count,
                "categories": categories,
                "total_categories": len(categories)
            },
            "branding": self.emojis.get("vzoel_fox_branding", {}),
            "version": self.emojis.get("emoji_mapping", {}).get("version", "unknown")
        }

# Global instance untuk kemudahan penggunaan
vzoel_assets = VzoelAssets()

# Shortcut functions untuk akses cepat
def bold(text: str) -> str:
    """Quick bold formatting"""
    return vzoel_assets.bold(text)

def italic(text: str) -> str:
    """Quick italic formatting"""
    return vzoel_assets.italic(text)

def emoji(key: str) -> str:
    """Quick emoji access"""
    return vzoel_assets.get_emoji(key)

def vzoel_msg(text: str, style: str = "bold", pattern: str = None) -> str:
    """Quick message formatting"""
    return vzoel_assets.format_message(text, style, pattern)