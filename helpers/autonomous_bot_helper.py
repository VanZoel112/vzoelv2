"""
Autonomous Bot Helper - Automated Bot Creation dan Management
Otomatis membuat bot dari BotFather dan handle premium emoji mapping
Created by: Vzoel Fox's
"""

import asyncio
import re
import json
import os
import random
import string
from typing import Dict, Any, Optional, List, Tuple
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, PeerFlood
from datetime import datetime
import time

try:
    from utils.assets import VzoelAssets, bold, italic, emoji, premium_emoji, vzoel_signature
    from logger import log_info, log_error, log_warning, log_success
    VZOEL_ASSETS_AVAILABLE = True
except ImportError:
    def bold(text): return f"**{text}**"
    def italic(text): return f"_{text}_"
    def emoji(key): return ""
    def premium_emoji(key): return ""
    def vzoel_signature(): return "Vzoel Assistant"
    def log_info(msg): print(f"INFO: {msg}")
    def log_error(msg): print(f"ERROR: {msg}")
    def log_warning(msg): print(f"WARNING: {msg}")
    def log_success(msg): print(f"SUCCESS: {msg}")
    VZOEL_ASSETS_AVAILABLE = False

class AutonomousBotCreator:
    """
    Helper untuk otomatis membuat bot dari BotFather menggunakan userbot
    """
    
    def __init__(self, user_client: Client, config_path: str = "vzoel/config.json"):
        self.user_client = user_client
        self.config_path = config_path
        self.config = self.load_config()
        self.botfather_id = 93372553  # @BotFather ID
        
        # Bot creation templates
        self.bot_name_templates = [
            "VzoelBot",
            "SmartAssistant",
            "PremiumHelper",
            "AutoBot",
            "IntelliBot"
        ]
        
        # Created bots storage
        self.created_bots_file = "autonomous_bots.json"
        self.created_bots = self.load_created_bots()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration dari file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            log_error(f"Failed to load config: {e}")
            return {}
    
    def load_created_bots(self) -> Dict[str, Any]:
        """Load list created bots"""
        try:
            if os.path.exists(self.created_bots_file):
                with open(self.created_bots_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"bots": [], "total_created": 0, "last_created": None}
        except Exception as e:
            log_error(f"Failed to load created bots: {e}")
            return {"bots": [], "total_created": 0, "last_created": None}
    
    def save_created_bots(self):
        """Save created bots data"""
        try:
            with open(self.created_bots_file, 'w', encoding='utf-8') as f:
                json.dump(self.created_bots, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Failed to save created bots: {e}")
    
    def generate_bot_name(self, prefix: Optional[str] = None) -> str:
        """Generate unique bot name"""
        if prefix:
            base_name = prefix
        else:
            base_name = random.choice(self.bot_name_templates)
        
        # Add random suffix
        suffix = ''.join(random.choices(string.digits, k=4))
        return f"{base_name}{suffix}"
    
    def generate_bot_username(self, name: str) -> str:
        """Generate unique bot username"""
        # Remove spaces and special chars
        username_base = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
        
        # Add random suffix to ensure uniqueness
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        username = f"{username_base}_{suffix}_bot"
        
        # Ensure it ends with 'bot'
        if not username.endswith('bot'):
            username += 'bot'
        
        return username[:32]  # Telegram username limit
    
    async def wait_for_response(self, timeout: int = 30) -> Optional[Message]:
        """Wait for BotFather response"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Get recent messages from BotFather
                async for message in self.user_client.get_chat_history(self.botfather_id, limit=10):
                    if message.date.timestamp() > start_time - 5:  # Recent message
                        return message
                
                await asyncio.sleep(1)
            except Exception as e:
                log_error(f"Error waiting for response: {e}")
                await asyncio.sleep(2)
        
        return None
    
    async def create_bot_automatically(self, 
                                     bot_name: Optional[str] = None,
                                     bot_username: Optional[str] = None,
                                     bot_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Otomatis create bot via BotFather
        """
        
        try:
            log_info("Starting automatic bot creation process...")
            
            # Generate names if not provided
            if not bot_name:
                bot_name = self.generate_bot_name()
            
            if not bot_username:
                bot_username = self.generate_bot_username(bot_name)
            
            if not bot_description:
                bot_description = f"Autonomous bot created by Vzoel Assistant - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Step 1: Start bot creation process
            log_info(f"Sending /newbot command to BotFather...")
            await self.user_client.send_message(self.botfather_id, "/newbot")
            await asyncio.sleep(2)
            
            # Wait for response
            response = await self.wait_for_response()
            if not response or "Alright, a new bot" not in response.text:
                log_error("Failed to start bot creation process")
                return {"success": False, "error": "Failed to start bot creation"}
            
            # Step 2: Send bot name
            log_info(f"Sending bot name: {bot_name}")
            await self.user_client.send_message(self.botfather_id, bot_name)
            await asyncio.sleep(2)
            
            # Step 3: Send bot username
            log_info(f"Sending bot username: {bot_username}")
            await self.user_client.send_message(self.botfather_id, bot_username)
            await asyncio.sleep(3)
            
            # Wait for final response with token
            response = await self.wait_for_response(timeout=45)
            if not response:
                log_error("No response received from BotFather")
                return {"success": False, "error": "No response from BotFather"}
            
            # Extract token from response
            token_match = re.search(r'(\d+:[A-Za-z0-9_-]+)', response.text)
            if not token_match:
                log_error("Failed to extract bot token from response")
                log_error(f"BotFather response: {response.text}")
                return {"success": False, "error": "Failed to extract token", "response": response.text}
            
            bot_token = token_match.group(1)
            
            # Step 4: Set bot description (optional)
            try:
                await self.user_client.send_message(self.botfather_id, "/setdescription")
                await asyncio.sleep(2)
                await self.user_client.send_message(self.botfather_id, f"@{bot_username}")
                await asyncio.sleep(2)
                await self.user_client.send_message(self.botfather_id, bot_description)
                await asyncio.sleep(2)
            except Exception as e:
                log_warning(f"Failed to set bot description: {e}")
            
            # Save bot information
            bot_info = {
                "name": bot_name,
                "username": bot_username,
                "token": bot_token,
                "description": bot_description,
                "created_at": datetime.now().isoformat(),
                "creator_id": self.config.get("owner_info", {}).get("founder_id"),
                "status": "active"
            }
            
            self.created_bots["bots"].append(bot_info)
            self.created_bots["total_created"] += 1
            self.created_bots["last_created"] = datetime.now().isoformat()
            self.save_created_bots()
            
            log_success(f"Successfully created bot: @{bot_username}")
            log_success(f"Bot token: {bot_token}")
            
            return {
                "success": True,
                "bot_info": bot_info,
                "token": bot_token,
                "username": bot_username,
                "name": bot_name
            }
            
        except FloodWait as e:
            log_error(f"Flood wait: {e.value} seconds")
            return {"success": False, "error": f"Flood wait: {e.value} seconds"}
            
        except Exception as e:
            log_error(f"Error creating bot: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_multiple_bots(self, count: int = 3, delay: int = 60) -> List[Dict[str, Any]]:
        """Create multiple bots with delay"""
        
        results = []
        
        for i in range(count):
            log_info(f"Creating bot {i+1}/{count}...")
            
            result = await self.create_bot_automatically()
            results.append(result)
            
            if result["success"]:
                log_success(f"Bot {i+1} created successfully: @{result['username']}")
            else:
                log_error(f"Failed to create bot {i+1}: {result.get('error', 'Unknown error')}")
            
            # Delay between creations to avoid flood
            if i < count - 1:  # Don't wait after last bot
                log_info(f"Waiting {delay} seconds before next bot creation...")
                await asyncio.sleep(delay)
        
        return results
    
    async def test_bot_token(self, token: str) -> Dict[str, Any]:
        """Test if bot token is valid"""
        
        try:
            # Create temporary client to test token
            test_client = Client(
                name="test_bot",
                api_id=self.config.get("telegram_api", {}).get("api_id"),
                api_hash=self.config.get("telegram_api", {}).get("api_hash"),
                bot_token=token
            )
            
            await test_client.start()
            me = await test_client.get_me()
            await test_client.stop()
            
            return {
                "valid": True,
                "bot_id": me.id,
                "bot_username": me.username,
                "bot_name": me.first_name
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def get_created_bots_report(self, premium_format: bool = False) -> str:
        """Generate report of created bots dengan premium emoji support"""
        
        if not self.created_bots["bots"]:
            error_emoji = premium_emoji('merah') if premium_format and VZOEL_ASSETS_AVAILABLE else emoji('merah')
            return f"{error_emoji} No bots created yet"
        
        # Use premium emojis jika available
        if premium_format and VZOEL_ASSETS_AVAILABLE:
            utama_emoji = premium_emoji('utama')
            centang_emoji = premium_emoji('centang')
            loading_emoji = premium_emoji('loading')
            merah_emoji = premium_emoji('merah')
        else:
            utama_emoji = emoji('utama')
            centang_emoji = emoji('centang')
            loading_emoji = emoji('loading')
            merah_emoji = emoji('merah')
        
        report_lines = [
            f"{utama_emoji} {bold('AUTONOMOUS BOTS REPORT')}",
            "",
            f"{centang_emoji} {bold('Summary:')}",
            f"• Total Created: {bold(str(self.created_bots['total_created']))}",
            f"• Last Created: {bold(self.created_bots.get('last_created', 'Never')[:19] if self.created_bots.get('last_created') else 'Never')}",
            "",
            f"{loading_emoji} {bold('Created Bots:')}"
        ]
        
        for i, bot in enumerate(self.created_bots["bots"][-10:], 1):  # Show last 10
            status_emoji = centang_emoji if bot.get('status') == 'active' else merah_emoji
            report_lines.append(f"{status_emoji} {i}. {bold(bot['name'])}")
            report_lines.append(f"   • Username: @{bot['username']}")
            report_lines.append(f"   • Created: {bot['created_at'][:19]}")
            report_lines.append("")
        
        signature = vzoel_signature(premium_format) if VZOEL_ASSETS_AVAILABLE else "Vzoel Autonomous Bot Creator"
        report_lines.append(f"{italic(f'Generated by {signature}')}")
        
        return "\n".join(report_lines)


class PremiumEmojiMapper:
    """
    Premium Emoji Mapper untuk handling custom emojis
    """
    
    def __init__(self, user_client: Client):
        self.user_client = user_client
        self.premium_emojis_file = "premium_emojis.json"
        
        # Try to use VzoelAssets if available, fallback to default
        if VZOEL_ASSETS_AVAILABLE:
            try:
                self.vzoel_assets = VzoelAssets()
                # Merge vzoel assets dengan autonomous system
                self.use_vzoel_assets = True
                log_info("Using VzoelAssets for premium emoji mapping")
            except:
                self.use_vzoel_assets = False
                self.init_default_emojis()
        else:
            self.use_vzoel_assets = False
            self.init_default_emojis()
        
        self.emoji_mapping = self.load_emoji_mapping()
    
    def init_default_emojis(self):
        """Initialize default premium emoji mapping"""
        self.default_premium_emojis = {
            # Vzoel Premium Collection
            "vzoel_fire": {"id": "5789953583373907162", "alt": "🔥", "premium": True},
            "vzoel_star": {"id": "5309970928025167875", "alt": "⭐", "premium": True},
            "vzoel_check": {"id": "5310129635848103696", "alt": "✅", "premium": True},
            "vzoel_heart": {"id": "5789738050059005422", "alt": "❤️", "premium": True},
            "vzoel_crown": {"id": "5789628129962543864", "alt": "👑", "premium": True},
            "vzoel_diamond": {"id": "5789420829468971067", "alt": "💎", "premium": True},
            "vzoel_rocket": {"id": "5789332346398226405", "alt": "🚀", "premium": True},
            "vzoel_lightning": {"id": "5789265431654298655", "alt": "⚡", "premium": True},
            "vzoel_magic": {"id": "5789183579064340771", "alt": "✨", "premium": True},
            "vzoel_celebration": {"id": "5789098746342916355", "alt": "🎉", "premium": True}
        }
    
    def load_emoji_mapping(self) -> Dict[str, Any]:
        """Load emoji mapping dari file"""
        try:
            if os.path.exists(self.premium_emojis_file):
                with open(self.premium_emojis_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            # Initialize with default emojis
            self.init_default_emojis()
            return {"emojis": self.default_premium_emojis, "last_updated": None}
        except Exception as e:
            log_error(f"Failed to load emoji mapping: {e}")
            # Initialize default emojis on error
            self.init_default_emojis()
            return {"emojis": self.default_premium_emojis, "last_updated": None}
    
    def save_emoji_mapping(self):
        """Save emoji mapping to file"""
        try:
            self.emoji_mapping["last_updated"] = datetime.now().isoformat()
            with open(self.premium_emojis_file, 'w', encoding='utf-8') as f:
                json.dump(self.emoji_mapping, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Failed to save emoji mapping: {e}")
    
    async def check_user_premium_status(self, user_id: int) -> bool:
        """Check if user has Telegram Premium"""
        try:
            user = await self.user_client.get_users(user_id)
            return user.is_premium if hasattr(user, 'is_premium') else False
        except Exception as e:
            log_error(f"Error checking premium status: {e}")
            return False
    
    def get_premium_emoji(self, emoji_key: str, fallback: bool = True) -> str:
        """Get premium emoji by key dengan VzoelAssets integration"""
        
        # Try VzoelAssets first jika available
        if self.use_vzoel_assets:
            try:
                vzoel_emoji = self.vzoel_assets.get_premium_emoji(emoji_key)
                if vzoel_emoji:
                    return vzoel_emoji
            except:
                pass
        
        # Fallback to autonomous system
        emoji_data = self.emoji_mapping["emojis"].get(emoji_key)
        if not emoji_data:
            if fallback and hasattr(self, 'default_premium_emojis'):
                return self.default_premium_emojis.get(emoji_key, {}).get("alt", "")
            return ""
        
        # Return HTML formatted custom emoji
        return f'<emoji id="{emoji_data["id"]}">{emoji_data["alt"]}</emoji>'
    
    def create_premium_message(self, text: str, emoji_mapping: Dict[str, str] = None) -> str:
        """Create message dengan premium emojis"""
        
        if not emoji_mapping:
            emoji_mapping = {}
        
        # Replace emoji placeholders dengan premium emojis
        for key, replacement in emoji_mapping.items():
            premium_emoji = self.get_premium_emoji(replacement)
            text = text.replace(f"{{{key}}}", premium_emoji)
        
        return text
    
    async def send_premium_message(self, chat_id: int, text: str, 
                                 emoji_mapping: Dict[str, str] = None) -> Optional[Message]:
        """Send message dengan premium emojis"""
        
        try:
            premium_text = self.create_premium_message(text, emoji_mapping)
            return await self.user_client.send_message(chat_id, premium_text, parse_mode="html")
        except Exception as e:
            log_error(f"Error sending premium message: {e}")
            return None
    
    def add_custom_emoji(self, key: str, emoji_id: str, alt: str, premium: bool = True):
        """Add custom emoji to mapping"""
        
        self.emoji_mapping["emojis"][key] = {
            "id": emoji_id,
            "alt": alt,
            "premium": premium
        }
        self.save_emoji_mapping()
        log_success(f"Added custom emoji: {key}")
    
    def get_emoji_report(self, premium_format: bool = False) -> str:
        """Generate emoji mapping report dengan premium support"""
        
        # Get emoji counts
        if self.use_vzoel_assets:
            vzoel_emojis = len(self.vzoel_assets.emojis.get("emojis", {}))
            autonomous_emojis = len(self.emoji_mapping["emojis"])
            total_emojis = vzoel_emojis + autonomous_emojis
        else:
            total_emojis = len(self.emoji_mapping["emojis"])
            vzoel_emojis = 0
            autonomous_emojis = total_emojis
        
        premium_emojis = sum(1 for e in self.emoji_mapping["emojis"].values() if e.get("premium", True))
        
        # Use premium emojis jika available
        if premium_format and VZOEL_ASSETS_AVAILABLE:
            utama_emoji = premium_emoji('utama')
            centang_emoji = premium_emoji('centang')
            loading_emoji = premium_emoji('loading')
            aktif_emoji = premium_emoji('aktif')
        else:
            utama_emoji = emoji('utama')
            centang_emoji = emoji('centang')
            loading_emoji = emoji('loading')
            aktif_emoji = emoji('aktif')
        
        report_lines = [
            f"{utama_emoji} {bold('PREMIUM EMOJI MAPPING REPORT')}",
            "",
            f"{centang_emoji} {bold('Summary:')}",
            f"• Total Emojis: {bold(str(total_emojis))}",
            f"• Vzoel Assets: {bold(str(vzoel_emojis))}",
            f"• Autonomous: {bold(str(autonomous_emojis))}",
            f"• Premium Support: {bold('✓' if self.use_vzoel_assets else '✗')}",
            f"• Last Updated: {bold(self.emoji_mapping.get('last_updated', 'Never')[:19] if self.emoji_mapping.get('last_updated') else 'Never')}",
            ""
        ]
        
        # Show vzoel emojis jika available
        if self.use_vzoel_assets:
            report_lines.append(f"{loading_emoji} {bold('Vzoel Assets Emojis:')}")
            vzoel_emoji_data = self.vzoel_assets.emojis.get("emojis", {})
            for key, data in list(vzoel_emoji_data.items())[:5]:  # Show first 5
                emoji_char = data.get("emoji_char", "")
                report_lines.append(f"• {bold(key)}: {emoji_char} (Vzoel Premium)")
            
            if len(vzoel_emoji_data) > 5:
                report_lines.append(f"... and {bold(str(len(vzoel_emoji_data) - 5))} more vzoel emojis")
            report_lines.append("")
        
        # Show autonomous emojis
        report_lines.append(f"{loading_emoji} {bold('Autonomous Emojis:')}")
        for key, data in list(self.emoji_mapping["emojis"].items())[:5]:  # Show first 5
            status = "Premium" if data.get("premium", True) else "Standard"
            alt_char = data.get('alt', '')
            report_lines.append(f"• {bold(key)}: {alt_char} ({status})")
        
        if autonomous_emojis > 5:
            report_lines.append(f"... and {bold(str(autonomous_emojis - 5))} more autonomous emojis")
        
        report_lines.extend([
            "",
            f"{aktif_emoji} {bold('Integration Status:')}",
            f"• VzoelAssets: {bold('✓ Active' if self.use_vzoel_assets else '✗ Not Available')}",
            f"• HTML Formatting: {bold('✓ Supported')}",
            f"• Fallback System: {bold('✓ Active')}",
            "",
            f"{aktif_emoji} {bold('Usage Example:')}",
            f"```python",
            f"# Using integrated system",
            f"mapper = PremiumEmojiMapper(client)",
            f"premium_text = mapper.create_premium_message(",
            f"    text=\"Hello {{fire}} World {{star}}!\",",
            f"    emoji_mapping={{\"fire\": \"utama\", \"star\": \"centang\"}}",
            f")```",
            ""
        ])
        
        signature = vzoel_signature(premium_format) if VZOEL_ASSETS_AVAILABLE else "Vzoel Premium Emoji Mapper"
        report_lines.append(f"{italic(f'Generated by {signature}')}")
        
        return "\n".join(report_lines)


# Convenience functions
async def create_autonomous_bot(user_client: Client, 
                              bot_name: Optional[str] = None,
                              bot_username: Optional[str] = None) -> Dict[str, Any]:
    """Quick function untuk create autonomous bot"""
    
    creator = AutonomousBotCreator(user_client)
    return await creator.create_bot_automatically(bot_name, bot_username)

def setup_premium_emoji_mapper(user_client: Client) -> PremiumEmojiMapper:
    """Quick setup untuk premium emoji mapper"""
    
    return PremiumEmojiMapper(user_client)

async def send_premium_emoji_message(user_client: Client, chat_id: int, text: str) -> Optional[Message]:
    """Quick function untuk send premium emoji message"""
    
    mapper = PremiumEmojiMapper(user_client)
    return await mapper.send_premium_message(chat_id, text)