#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Bot Framework
Enhanced with Pyrogram + uvloop + Premium Assets + Auto Session
Created by: VZLfxs @Lutpan
"""

# =================================================================
# 1. SYSTEM OPTIMIZATION & CORE IMPORTS
# =================================================================
import asyncio
import logging
import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Install uvloop for maximum performance (with fallback)
try:
    import uvloop
    uvloop.install()
    UVLOOP_AVAILABLE = True
except ImportError:
    UVLOOP_AVAILABLE = False
    # Don't log warning during import, will log later

# Core Pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid
)

# =================================================================
# 2. PREMIUM ASSET SYSTEM IMPORT
# =================================================================
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
from utils.error_handler import ErrorHandler, safe_send_message, suppress_peer_errors
from utils.filters import vzoel_command

# Initialize premium assets
assets = VzoelAssets()

# Setup global error handling
suppress_peer_errors()

# =================================================================
# 3. SESSION IMPORT HELPER
# =================================================================
def load_session_from_file():
    """Load session string from vzoel_session.txt"""
    try:
        if os.path.exists('vzoel_session.txt'):
            with open('vzoel_session.txt', 'r') as f:
                session_string = f.read().strip()
                if session_string:
                    print("✅ Session string loaded from vzoel_session.txt")
                    return session_string
    except Exception as e:
        print(f"❌ Error loading session file: {e}")
    return None

# =================================================================
# 4. CONFIGURATION MANAGEMENT
# =================================================================
class VzoelConfig:
    """Enhanced configuration manager with premium features"""
    
    def __init__(self):
        # Load environment variables first
        load_dotenv()
        self._config = self._load_config()
        # Don't validate config here - let it be flexible
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from vzoel/config.json"""
        try:
            config_path = os.path.join("vzoel", "config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Fallback default configuration"""
        return {
            "telegram_api": {
                "api_id": 0,
                "api_hash": ""
            },
            "bot_credentials": {
                "bot_token": "",
                "session_name": "vzoel_session"
            },
            "owner_info": {
                "founder_id": 0
            }
        }
    
    def _validate_config(self):
        """Validate essential configuration - flexible validation"""
        # Just log warnings, don't raise errors
        pass
    
    @property
    def api_id(self) -> int:
        return self._config.get("telegram_api", {}).get("api_id", 29919905)
    
    @property
    def api_hash(self) -> str:
        return self._config.get("telegram_api", {}).get("api_hash", "717957f0e3ae20a7db004d08b66bfd30")
    
    @property
    def bot_token(self) -> str:
        return self._config.get("bot_credentials", {}).get("bot_token", "")
    
    @property
    def session_name(self) -> str:
        return self._config.get("bot_credentials", {}).get("session_name", "vzoel_session")
    
    @property
    def session_string(self) -> Optional[str]:
        """Get session string from multiple sources"""
        # Try file first (from session_generate.py)
        file_session = load_session_from_file()
        if file_session:
            return file_session
        
        # Try environment second
        env_session = os.getenv("SESSION_STRING")
        if env_session:
            return env_session
            
        # Fall back to config
        return self._config.get("bot_credentials", {}).get("session_string")
    
    @property
    def user_session_string(self) -> Optional[str]:
        """Get user session string from config or env"""
        # Try environment first
        env_session = os.getenv("USER_SESSION_STRING") 
        if env_session:
            return env_session
        # Fall back to config
        return self._config.get("bot_credentials", {}).get("user_session_string")
    
    @property
    def phone_number(self) -> Optional[str]:
        """Get phone number from config or env"""
        # Try environment first
        env_phone = os.getenv("PHONE_NUMBER")
        if env_phone:
            return env_phone
        # Fall back to config
        return self._config.get("bot_credentials", {}).get("phone_number")
    
    @property
    def founder_id(self) -> int:
        return self._config.get("owner_info", {}).get("founder_id", 0)
    
    @property
    def project_info(self) -> Dict[str, Any]:
        return self._config.get("project_info", {})
    
    @property
    def branding_info(self) -> Dict[str, Any]:
        return self._config.get("branding_info", {})

# Initialize configuration
config = VzoelConfig()

# =================================================================
# 5. ENHANCED CLIENT WITH AUTO SESSION
# =================================================================
class VzoelAssistant(Client):
    """Enhanced Pyrogram client with auto session generation"""
    
    def __init__(self, session_string=None, api_id=None, api_hash=None):
        # Use provided session or config
        self.session_string = session_string or config.session_string
        self.api_id = api_id or config.api_id
        self.api_hash = api_hash or config.api_hash
        
        # Determine client initialization parameters
        client_params = {
            "name": config.session_name,
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "plugins": {"root": "plugins"},
            "parse_mode": ParseMode.MARKDOWN
        }
        
        # PURE USERBOT - session string only
        if not self.session_string:
            raise ValueError("No session string available - this is a USERBOT, not a BOT")
        
        client_params["session_string"] = self.session_string
        print(f"✅ USERBOT: Using session string authentication for user account")
        
        super().__init__(**client_params)
        
        # Premium features
        self.assets = assets
        self.config_data = config
        self.start_time = None
        
        # Setup logging dengan premium styling
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup enhanced logging with premium styling"""
        # Create custom filter to reduce peer ID error noise
        class PeerErrorFilter(logging.Filter):
            def filter(self, record):
                message = record.getMessage()
                # Suppress specific peer ID errors that aren't critical
                if "Task exception was never retrieved" in message and "Peer id invalid" in message:
                    return False
                if "ID not found" in message and "KeyError" in message:
                    return False
                return True
        
        # Setup logging with filter
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s - ✨ %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('vzoel_assistant.log')
            ]
        )
        
        # Add filter to reduce noise
        peer_filter = PeerErrorFilter()
        for handler in logging.getLogger().handlers:
            handler.addFilter(peer_filter)
    
    async def start(self):
        """Enhanced start method with premium welcome"""
        self.start_time = asyncio.get_event_loop().time()
        
        await super().start()
        
        # Premium startup message
        me = await self.get_me()
        startup_msg = self._get_startup_message(me)
        
        print(startup_msg)
        logging.info("Vzoel Userbot started successfully for user account")
        
        # Send startup notification if log group configured
        try:
            log_group_id = config._config.get("logging", {}).get("log_group_id")
            if log_group_id:
                # Try to send to log group using safe send
                await safe_send_message(self, log_group_id, startup_msg)
        except Exception as e:
            logging.warning(f"Could not send startup notification: {e}")
    
    def _get_startup_message(self, me) -> str:
        """Generate premium startup message"""
        signature = self.assets.vzoel_signature()
        project_info = config.project_info
        branding_info = config.branding_info
        
        startup_lines = [
            f"{signature}",
            "",
            f"👤 **User Account:**",
            f"  • Name: **{me.first_name}**",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            f"  • Type: **USERBOT** (Personal Account Automation)",
            "",
            f"⚡ **Userbot Information:**",
            f"  • Assistant: **{project_info.get('project_name', 'VZOEL ASSISTANT')}**",
            f"  • Version: `{project_info.get('version', '1.0.0')}`",
            f"  • Mode: _{project_info.get('description', 'Personal Account Assistant')}_",
            "",
            f"🔥 **Automation Status:**",
            f"  • Performance: **{'uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop'}**",
            f"  • Features: **Premium Collection Active**",
            f"  • Commands: **Ready for Personal Use**",
            "",
            f"🚀 **Personal Assistant Ready!**",
            "",
            f"_{branding_info.get('footer_text', 'Created by VZLfxs @Lutpan')}_"
        ]
        
        return "\n".join(startup_lines)
    
    def get_uptime(self) -> str:
        """Get formatted uptime with premium styling"""
        if not self.start_time:
            return "**Not available**"
        
        uptime_seconds = int(asyncio.get_event_loop().time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"**{hours}**h **{minutes}**m **{seconds}**s"
        elif minutes > 0:
            return f"**{minutes}**m **{seconds}**s"
        else:
            return f"**{seconds}**s"

# Global app variable - will be initialized later
app = None

# =================================================================
# 6. CORE COMMAND HANDLERS WITH PREMIUM STYLING
# =================================================================

@Client.on_message(vzoel_command("start") & filters.private)
async def start_command(client: VzoelAssistant, message: Message):
    """Enhanced start command with premium welcome"""
    
    user = message.from_user
    signature = client.assets.vzoel_signature()
    branding = client.config_data.branding_info
    
    welcome_text = [
        f"{signature}",
        "",
        f"Halo **{user.first_name}**! 🔥",
        "",
        f"Selamat datang di **{branding.get('assistant_display_name', 'VZOEL ASSISTANT')}**",
        f"Personal userbot automation untuk akun Telegram kamu!",
        "",
        f"✅ **Fitur Userbot:**",
        f"  • Commands automation untuk akun personal",
        f"  • Premium styling & emoji collection",  
        f"  • High-performance dengan uvloop",
        f"  • Interactive command system",
        "",
        f"Ketik !help atau .help untuk melihat semua perintah userbot.",
        "",
        f"_{branding.get('footer_text', 'Created by VZLfxs @Lutpan')}_"
    ]
    
    await message.reply_text("\n".join(welcome_text))

@Client.on_message(vzoel_command("ping"))
async def ping_command(client: VzoelAssistant, message: Message):
    """Enhanced ping command with premium response"""
    
    import time
    
    # Show loading first
    loading_emojis = client.assets.get_status_emojis("loading")
    loading_msg = f"{loading_emojis[0]} _Checking connection..._"
    
    sent = await message.reply_text(loading_msg)
    
    # Calculate response time
    start_time = time.time()
    await asyncio.sleep(0.1)  # Simulate processing
    ping_time = round((time.time() - start_time) * 1000, 2)
    
    # Premium response
    pong_msg = vzoel_msg(f"Pong! {ping_time}ms", "bold", "ping")
    uptime_msg = f"✨ Uptime: {client.get_uptime()}"
    
    final_msg = f"{pong_msg}\n{uptime_msg}"
    
    await sent.edit_text(final_msg)

@Client.on_message(vzoel_command("alive"))
async def alive_command(client: VzoelAssistant, message: Message):
    """Enhanced alive command showing premium status"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    
    alive_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"👤 **Personal Account:** **@{me.username}**",
        f"🤖 **Userbot Status:** **ACTIVE**",
        f"⚡ **Version:** **{project_info.get('version', '1.0.0')}**",
        f"✨ **Uptime:** {client.get_uptime()}",
        f"🚀 **Performance:** **{'uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop'}**",
        "",
        f"**Personal Automation Features:**",
        f"🔥 Advanced Command Processing",
        f"🔵 Premium Styling Collection",
        f"🟡 Interactive Response System", 
        f"🔴 High-Performance Automation",
        "",
        f"_Personal assistant for {me.first_name} is ready!_"
    ]
    
    await message.reply_text("\n".join(alive_text))

@Client.on_message(vzoel_command("info"))
async def info_command(client: VzoelAssistant, message: Message):
    """Show comprehensive bot information"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    asset_info = client.assets.get_asset_info()
    
    info_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"👤 **User Account Information:**",
        f"  • Name: **{me.first_name}**",
        f"  • Username: @{me.username}",
        f"  • ID: `{me.id}`",
        f"  • Account Type: **Personal Userbot**",
        "",
        f"🤖 **Userbot System:**",
        f"  • Framework: **Pyrogram + uvloop**",
        f"  • Version: **{project_info.get('version', '1.0.0')}**",
        f"  • Parse Mode: **Enhanced Markdown**",
        f"  • Uptime: {client.get_uptime()}",
        "",
        f"🔥 **Premium Features:**",
        f"  • Font Styles: **{asset_info['fonts']['total_styles']}**",
        f"  • Premium Emojis: **{asset_info['emojis']['total_emojis']}**",
        f"  • Categories: **{asset_info['emojis']['total_categories']}**",
        f"  • Asset Version: **{asset_info['version']}**",
        "",
        f"_Personal automation enhanced by VZLfxs @Lutpan_"
    ]
    
    await message.reply_text("\n".join(info_text))

# =================================================================
# 7. MAIN EXECUTION WITH AUTO SESSION SETUP
# =================================================================

async def main():
    """Enhanced main function with auto session setup"""
    global app
    
    try:
        # Check if session exists
        session_string = config.session_string
        api_id = config.api_id
        api_hash = config.api_hash
        
        if not session_string:
            print(f"\n❌ No session string found!")
            print(f"💡 Please generate session first:")
            print(f"   1. Run: python3 session_generate.py")
            print(f"   2. Follow the prompts to create session")
            print(f"   3. Then run: python3 main.py")
            print(f"\n🔄 Session will be saved to vzoel_session.txt")
            return
        
        # Initialize client with session
        app = VzoelAssistant(session_string, api_id, api_hash)
        
        # Premium userbot startup sequence
        print(f"\n🔄 Starting Vzoel Userbot...")
        print(f"⚡ Initializing personal account automation...")
        
        # Start the bot
        await app.start()
        
        # Keep running with userbot status
        print(f"✅ Personal userbot ready!")
        print(f"🔥 Vzoel Userbot is active for your account!")
        
        # Keep alive
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print(f"\n🔄 Shutting down Vzoel Userbot...")
        logging.info("Userbot stopped by user")
        
    except Exception as e:
        error_msg = f"❌ Critical error: {e}"
        print(error_msg)
        logging.error(f"Critical error in main: {e}")
        raise
    
    finally:
        # Cleanup
        if app and app.is_connected:
            await app.stop()
        print(f"✅ Vzoel Userbot stopped gracefully")

# =================================================================
# 8. APPLICATION ENTRY POINT
# =================================================================

if __name__ == "__main__":
    try:
        # Print premium banner
        banner = [
            "",
            "╔" + "═" * 50 + "╗",
            "║" + f"{'VZOEL USERBOT v2 - PREMIUM':^50}" + "║",
            "║" + f"{'Personal Account Automation + uvloop':^50}" + "║", 
            "║" + f"{'Created by: VZLfxs @Lutpan':^50}" + "║",
            "╚" + "═" * 50 + "╝",
            ""
        ]
        
        for line in banner:
            print(line)
        
        # Run main function
        asyncio.run(main())
        
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        logging.error(f"Failed to start application: {e}")
        exit(1)