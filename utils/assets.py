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
    def get_emoji(self, emoji_key: str, premium_format: bool = False) -> str:
        """Get emoji character by key with optional premium formatting"""
        emoji_data = self.emojis.get("emojis", {}).get(emoji_key, {})
        emoji_char = emoji_data.get("emoji_char", "")
        
        if premium_format and emoji_data.get("custom_emoji_id"):
            # Return HTML formatted premium emoji
            custom_id = emoji_data.get("custom_emoji_id")
            return f'<emoji id="{custom_id}">{emoji_char}</emoji>'
        
        return emoji_char
    
    def get_emoji_id(self, emoji_key: str) -> str:
        """Get custom emoji ID by key"""
        emoji_data = self.emojis.get("emojis", {}).get(emoji_key, {})
        return emoji_data.get("custom_emoji_id", "")
    
    def get_premium_emoji(self, emoji_key: str) -> str:
        """Get premium formatted emoji (HTML format)"""
        return self.get_emoji(emoji_key, premium_format=True)
    
    def get_emoji_data(self, emoji_key: str) -> Dict[str, Any]:
        """Get complete emoji data including metadata"""
        return self.emojis.get("emojis", {}).get(emoji_key, {})
    
    def get_emojis_by_category(self, category: str, premium_format: bool = False) -> List[str]:
        """Get all emojis in a specific category"""
        category_data = self.emojis.get("categories", {}).get(category, {})
        emoji_keys = category_data.get("emojis", [])
        return [self.get_emoji(key, premium_format) for key in emoji_keys]
    
    def get_usage_pattern(self, command: str, premium_format: bool = False) -> List[str]:
        """Get emoji pattern for specific command"""
        patterns = self.emojis.get("usage_patterns", {}).get("command_responses", {})
        emoji_keys = patterns.get(command, [])
        return [self.get_emoji(key, premium_format) for key in emoji_keys]
    
    def get_status_emojis(self, status: str, premium_format: bool = False) -> List[str]:
        """Get emojis for status indicators"""
        patterns = self.emojis.get("usage_patterns", {}).get("status_indicators", {})
        emoji_keys = patterns.get(status, [])
        return [self.get_emoji(key, premium_format) for key in emoji_keys]
    
    def get_theme_emojis(self, theme: str, premium_format: bool = False) -> List[str]:
        """Get emojis for specific theme"""
        patterns = self.emojis.get("usage_patterns", {}).get("themes", {})
        emoji_keys = patterns.get(theme, [])
        return [self.get_emoji(key, premium_format) for key in emoji_keys]
    
    # Utility Methods
    def format_message(self, text: str, style: str = "bold", 
                      emoji_pattern: Optional[str] = None, premium_format: bool = False) -> str:
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
            emojis = self.get_usage_pattern(emoji_pattern, premium_format)
            if emojis:
                return f"{emojis[0]} {formatted_text} {emojis[-1]}"
        
        return formatted_text
    
    def vzoel_signature(self, premium_format: bool = False) -> str:
        """Get Vzoel Fox's signature with emojis"""
        signature_emojis = self.emojis.get("quick_access", {}).get("vzoel_signature", [])
        emojis = []
        for emoji_id in signature_emojis:
            for key, data in self.emojis.get("emojis", {}).items():
                if data.get("custom_emoji_id") == emoji_id:
                    if premium_format:
                        emojis.append(f'<emoji id="{emoji_id}">{data.get("emoji_char", "")}</emoji>')
                    else:
                        emojis.append(data.get("emoji_char", ""))
                    break
        
        if emojis:
            return f"{emojis[0]} Vzoel Fox's Assistant {emojis[1]}{emojis[2]}"
        return "🤩 Vzoel Fox's Assistant 😈⛈"
    
    def create_premium_message(self, text: str, emoji_replacements: Dict[str, str] = None) -> str:
        """Create message dengan premium emoji replacements"""
        if not emoji_replacements:
            return text
        
        result_text = text
        for placeholder, emoji_key in emoji_replacements.items():
            premium_emoji = self.get_premium_emoji(emoji_key)
            if premium_emoji:
                result_text = result_text.replace(f"{{{placeholder}}}", premium_emoji)
        
        return result_text
    
    def get_vzoel_theme_message(self, message_type: str = "primary", premium_format: bool = False) -> str:
        """Get themed message dengan vzoel branding"""
        theme_mapping = {
            "primary": "vzoel_primary",
            "fun": "vzoel_fun", 
            "system": "vzoel_system",
            "special": "vzoel_special"
        }
        
        theme = theme_mapping.get(message_type, "vzoel_primary")
        emojis = self.get_theme_emojis(theme, premium_format)
        
        branding = self.emojis.get("vzoel_fox_branding", {})
        assistant_name = branding.get("assistant", "Vzoel Fox's Assistant")
        
        if emojis:
            return f"{emojis[0]} {assistant_name} {emojis[-1]}"
        return f"🤩 {assistant_name} ⛈"
    
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

def emoji(key: str, premium_format: bool = False) -> str:
    """Quick emoji access dengan premium support"""
    return vzoel_assets.get_emoji(key, premium_format)

def premium_emoji(key: str) -> str:
    """Quick premium emoji access (HTML format)"""
    return vzoel_assets.get_premium_emoji(key)

def vzoel_msg(text: str, style: str = "bold", pattern: str = None, premium_format: bool = False) -> str:
    """Quick message formatting dengan premium emoji support"""
    return vzoel_assets.format_message(text, style, pattern, premium_format)

def monospace(text: str) -> str:
    """Quick monospace formatting"""
    return vzoel_assets.monospace(text)

def vzoel_signature(premium_format: bool = False) -> str:
    """Quick Vzoel signature dengan premium support"""
    return vzoel_assets.vzoel_signature(premium_format)

def create_premium_message(text: str, emoji_replacements: Dict[str, str] = None) -> str:
    """Quick premium message creation"""
    return vzoel_assets.create_premium_message(text, emoji_replacements)