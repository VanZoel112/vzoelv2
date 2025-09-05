#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Bot Framework
Enhanced with Pyrogram + uvloop + Premium Assets
Created by: Vzoel Fox's
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

# =================================================================
# 2. PREMIUM ASSET SYSTEM IMPORT
# =================================================================
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

# Initialize premium assets
assets = VzoelAssets()

# =================================================================
# 3. CONFIGURATION MANAGEMENT
# =================================================================
class VzoelConfig:
    """Enhanced configuration manager with premium features"""
    
    def __init__(self):
        # Load environment variables first
        load_dotenv()
        self._config = self._load_config()
        self._validate_config()
    
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
        """Validate essential configuration"""
        required_keys = [
            ("telegram_api", "api_id"),
            ("telegram_api", "api_hash"),
            ("bot_credentials", "bot_token")
        ]
        
        for section, key in required_keys:
            if not self._config.get(section, {}).get(key):
                raise ValueError(f"Missing required config: {section}.{key}")
    
    @property
    def api_id(self) -> int:
        return self._config["telegram_api"]["api_id"]
    
    @property
    def api_hash(self) -> str:
        return self._config["telegram_api"]["api_hash"]
    
    @property
    def bot_token(self) -> str:
        return self._config["bot_credentials"]["bot_token"]
    
    @property
    def session_name(self) -> str:
        return self._config["bot_credentials"].get("session_name", "vzoel_session")
    
    @property
    def session_string(self) -> Optional[str]:
        """Get session string from config or env"""
        # Try environment first
        env_session = os.getenv("SESSION_STRING")
        if env_session:
            return env_session
        # Fall back to config
        return self._config["bot_credentials"].get("session_string")
    
    @property
    def user_session_string(self) -> Optional[str]:
        """Get user session string from config or env"""
        # Try environment first
        env_session = os.getenv("USER_SESSION_STRING") 
        if env_session:
            return env_session
        # Fall back to config
        return self._config["bot_credentials"].get("user_session_string")
    
    @property
    def phone_number(self) -> Optional[str]:
        """Get phone number from config or env"""
        # Try environment first
        env_phone = os.getenv("PHONE_NUMBER")
        if env_phone:
            return env_phone
        # Fall back to config
        return self._config["bot_credentials"].get("phone_number")
    
    @property
    def founder_id(self) -> int:
        return self._config["owner_info"]["founder_id"]
    
    @property
    def project_info(self) -> Dict[str, Any]:
        return self._config.get("project_info", {})
    
    @property
    def branding_info(self) -> Dict[str, Any]:
        return self._config.get("branding_info", {})

# Initialize configuration
config = VzoelConfig()

# =================================================================
# 4. PREMIUM CLIENT INITIALIZATION
# =================================================================
class VzoelAssistant(Client):
    """Enhanced Pyrogram client with premium features"""
    
    def __init__(self):
        # Determine client initialization parameters
        client_params = {
            "name": config.session_name,
            "api_id": config.api_id,
            "api_hash": config.api_hash,
            "plugins": {"root": "plugins"},
            "parse_mode": ParseMode.MARKDOWN
        }
        
        # Use session string if available, otherwise use bot token
        if config.session_string:
            client_params["session_string"] = config.session_string
            print(f"{emoji('centang')} Using session string authentication")
        elif config.bot_token:
            client_params["bot_token"] = config.bot_token
            print(f"{emoji('telegram')} Using bot token authentication")
        else:
            raise ValueError("Either SESSION_STRING or BOT_TOKEN must be provided")
        
        super().__init__(**client_params)
        
        # Premium features
        self.assets = assets
        self.config_data = config
        self.start_time = None
        
        # Setup logging dengan premium styling
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup enhanced logging with premium styling"""
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s - {emoji("aktif")} %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('vzoel_assistant.log')
            ]
        )
    
    async def start(self):
        """Enhanced start method with premium welcome"""
        self.start_time = asyncio.get_event_loop().time()
        
        await super().start()
        
        # Premium startup message
        me = await self.get_me()
        startup_msg = self._get_startup_message(me)
        
        print(startup_msg)
        logging.info("Vzoel Assistant started successfully")
        
        # Send startup notification if log group configured
        try:
            log_group_id = config._config.get("logging", {}).get("log_group_id")
            if log_group_id:
                await self.send_message(
                    chat_id=log_group_id,
                    text=startup_msg
                )
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
            f"{emoji('centang')} **Bot Information:**",
            f"  • Name: {bold(me.first_name)}",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            "",
            f"{emoji('petir')} **Project Information:**",
            f"  • Name: {bold(project_info.get('project_name', 'VZOEL ASSISTANT'))}",
            f"  • Version: `{project_info.get('version', '1.0.0')}`",
            f"  • Description: {italic(project_info.get('description', 'Premium Assistant'))}",
            "",
            f"{emoji('utama')} **System Status:**",
            f"  • Performance: {bold('uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop')}",
            f"  • Assets: {bold('Premium Collection Loaded')}",
            f"  • Parse Mode: {bold('Enhanced Markdown')}",
            "",
            f"{emoji('loading')} **Ready to serve!**",
            "",
            f"{italic(branding_info.get('footer_text', 'Created by Vzoel Fox'))}"
        ]
        
        return "\n".join(startup_lines)
    
    def get_uptime(self) -> str:
        """Get formatted uptime with premium styling"""
        if not self.start_time:
            return bold("Not available")
        
        uptime_seconds = int(asyncio.get_event_loop().time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            return f"{bold(str(hours))}h {bold(str(minutes))}m {bold(str(seconds))}s"
        elif minutes > 0:
            return f"{bold(str(minutes))}m {bold(str(seconds))}s"
        else:
            return f"{bold(str(seconds))}s"

# Initialize the premium client
app = VzoelAssistant()

# =================================================================
# 5. CORE COMMAND HANDLERS WITH PREMIUM STYLING
# =================================================================

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: VzoelAssistant, message: Message):
    """Enhanced start command with premium welcome"""
    
    user = message.from_user
    signature = client.assets.vzoel_signature()
    branding = client.config_data.branding_info
    
    welcome_text = [
        f"{signature}",
        "",
        f"Halo {bold(user.first_name)}! {emoji('utama')}",
        "",
        f"Selamat datang di {bold(branding.get('assistant_display_name', 'VZOEL ASSISTANT'))}",
        f"Premium bot assistant dengan fitur-fitur canggih!",
        "",
        f"{emoji('centang')} **Fitur Utama:**",
        f"  • Premium styling & emoji",
        f"  • High-performance dengan uvloop",
        f"  • Interactive command system",
        f"  • Enhanced markdown support",
        "",
        f"Ketik /help untuk melihat semua perintah yang tersedia.",
        "",
        f"{italic(branding.get('footer_text', 'Created by Vzoel Fox'))}"
    ]
    
    await message.reply_text("\n".join(welcome_text))

@app.on_message(filters.command("ping"))
async def ping_command(client: VzoelAssistant, message: Message):
    """Enhanced ping command with premium response"""
    
    import time
    
    # Show loading first
    loading_emojis = client.assets.get_status_emojis("loading")
    loading_msg = f"{loading_emojis[0]} {italic('Checking connection...')}"
    
    sent = await message.reply_text(loading_msg)
    
    # Calculate response time
    start_time = time.time()
    await asyncio.sleep(0.1)  # Simulate processing
    ping_time = round((time.time() - start_time) * 1000, 2)
    
    # Premium response
    pong_msg = vzoel_msg(f"Pong! {ping_time}ms", "bold", "ping")
    uptime_msg = f"{emoji('aktif')} Uptime: {client.get_uptime()}"
    
    final_msg = f"{pong_msg}\n{uptime_msg}"
    
    await sent.edit_text(final_msg)

@app.on_message(filters.command("alive"))
async def alive_command(client: VzoelAssistant, message: Message):
    """Enhanced alive command showing premium status"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    
    alive_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"{emoji('centang')} **Bot Status:** {bold('ONLINE')}",
        f"{emoji('petir')} **Version:** {bold(project_info.get('version', '1.0.0'))}",
        f"{emoji('aktif')} **Uptime:** {client.get_uptime()}",
        f"{emoji('loading')} **Performance:** {bold('uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop')}",
        "",
        f"**Premium Features Active:**",
        f"{emoji('utama')} Enhanced Markdown Styling",
        f"{emoji('biru')} Premium Emoji Collection",
        f"{emoji('kuning')} Interactive Command System", 
        f"{emoji('merah')} High-Performance Framework",
        "",
        f"{italic('Ready to serve with premium quality!')}"
    ]
    
    await message.reply_text("\n".join(alive_text))

@app.on_message(filters.command("info"))
async def info_command(client: VzoelAssistant, message: Message):
    """Show comprehensive bot information"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    asset_info = client.assets.get_asset_info()
    
    info_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"{emoji('centang')} **Bot Information:**",
        f"  • Name: {bold(me.first_name)}",
        f"  • Username: @{me.username}",
        f"  • ID: `{me.id}`",
        f"  • Version: {bold(project_info.get('version', '1.0.0'))}",
        "",
        f"{emoji('petir')} **System Information:**",
        f"  • Framework: {bold('Pyrogram + uvloop')}",
        f"  • Parse Mode: {bold('Enhanced Markdown')}",
        f"  • Uptime: {client.get_uptime()}",
        "",
        f"{emoji('utama')} **Premium Assets:**",
        f"  • Font Styles: {bold(str(asset_info['fonts']['total_styles']))}",
        f"  • Premium Emojis: {bold(str(asset_info['emojis']['total_emojis']))}",
        f"  • Categories: {bold(str(asset_info['emojis']['total_categories']))}",
        f"  • Version: {bold(asset_info['version'])}",
        "",
        f"{italic('Enhanced by Vzoel Fox Premium Collection')}"
    ]
    
    await message.reply_text("\n".join(info_text))

# =================================================================
# 6. MAIN EXECUTION WITH PREMIUM ERROR HANDLING
# =================================================================

async def main():
    """Enhanced main function with premium startup"""
    
    try:
        # Premium startup sequence
        print(f"\n{emoji('loading')} Starting Vzoel Assistant...")
        print(f"{emoji('petir')} Initializing premium systems...")
        
        # Start the bot
        await app.start()
        
        # Keep running with premium status
        print(f"{emoji('centang')} All systems ready!")
        print(f"{emoji('utama')} Vzoel Assistant is now running with premium features!")
        
        # Keep alive
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print(f"\n{emoji('loading')} Shutting down Vzoel Assistant...")
        logging.info("Bot stopped by user")
        
    except Exception as e:
        error_msg = f"{emoji('merah')} Critical error: {e}"
        print(error_msg)
        logging.error(f"Critical error in main: {e}")
        raise
    
    finally:
        # Cleanup
        if app.is_connected:
            await app.stop()
        print(f"{emoji('centang')} Vzoel Assistant stopped gracefully")

# =================================================================
# 7. APPLICATION ENTRY POINT
# =================================================================

if __name__ == "__main__":
    try:
        # Print premium banner
        banner = [
            "",
            "╔" + "═" * 50 + "╗",
            "║" + f"{'VZOEL ASSISTANT v2 - PREMIUM':^50}" + "║",
            "║" + f"{'Enhanced with Pyrogram + uvloop':^50}" + "║", 
            "║" + f"{'Created by: Vzoel Fox':^50}" + "║",
            "╚" + "═" * 50 + "╝",
            ""
        ]
        
        for line in banner:
            print(line)
        
        # Run with uvloop optimization
        app.run(main())
        
    except Exception as e:
        print(f"{emoji('merah')} Failed to start: {e}")
        logging.error(f"Failed to start application: {e}")
        exit(1)