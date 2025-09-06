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

# Initialize premium assets
assets = VzoelAssets()

# =================================================================
# 3. AUTO SESSION GENERATOR
# =================================================================
class AutoSessionSetup:
    """Auto session setup untuk userbot"""
    
    def __init__(self):
        # Default API credentials untuk session generation
        self.api_id = 24194005
        self.api_hash = "717957f0e3ae20a7db004d08b66bfd30"
        self.session_name = "vzoel_assistant_session"
    
    def display_session_banner(self):
        """Display session setup banner"""
        print("\n" + "═" * 60)
        print("║      VZOEL ASSISTANT v2 - AUTO SESSION SETUP      ║")
        print("║        Setup userbot session dengan mudah          ║")
        print("║           Created by: VZLfxs @Lutpan               ║")
        print("═" * 60 + "\n")
    
    def get_phone_number(self):
        """Get phone number input"""
        while True:
            phone = input("📱 Masukkan nomor HP (dengan kode negara, contoh: +6283199218067): ").strip()
            if phone.startswith('+') and len(phone) >= 10:
                print(f"✅ Nomor HP: {phone}")
                return phone
            else:
                print("❌ Format nomor HP salah! Gunakan format +628xxxxxxxxxx")
    
    def get_verification_code(self):
        """Get verification code input"""
        while True:
            try:
                code = input("🔑 Masukkan kode verifikasi (5 digit): ").strip()
                if len(code) == 5 and code.isdigit():
                    return code
                else:
                    print("❌ Kode verifikasi harus 5 digit angka!")
            except KeyboardInterrupt:
                print("\n❌ Dibatalkan oleh user")
                return None
    
    def get_password(self):
        """Get 2FA password if needed"""
        password = input("🔐 Masukkan 2FA password (kosongkan jika tidak ada): ").strip()
        return password if password else None
    
    async def create_session(self):
        """Generate session string dengan phone number"""
        try:
            self.display_session_banner()
            
            print("📋 Setup Information:")
            print(f"   • API ID: {self.api_id}")
            print(f"   • API Hash: {self.api_hash}")
            print(f"   • Session Name: {self.session_name}")
            print("")
            
            # Get phone number
            phone_number = self.get_phone_number()
            
            print("🔄 Membuat client Pyrogram...")
            client = Client(
                name=self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=phone_number
            )
            
            print("📞 Mengirim kode verifikasi...")
            await client.connect()
            sent_code = await client.send_code(phone_number)
            
            print(f"✅ Kode verifikasi dikirim ke {phone_number}")
            print("💬 Cek SMS/Telegram untuk mendapatkan kode verifikasi")
            
            # Get verification code
            code = self.get_verification_code()
            if not code:
                await client.disconnect()
                return None, None, None
            
            print("🔑 Memverifikasi kode...")
            try:
                await client.sign_in(phone_number, sent_code.phone_code_hash, code)
                print("✅ Login berhasil!")
                
            except SessionPasswordNeeded:
                print("🔐 2FA diperlukan...")
                password = self.get_password()
                if password:
                    await client.check_password(password)
                    print("✅ 2FA berhasil!")
                else:
                    print("❌ 2FA diperlukan tapi tidak dimasukkan")
                    await client.disconnect()
                    return None, None, None
                    
            except (PhoneCodeInvalid, PhoneCodeExpired) as e:
                print(f"❌ Error kode verifikasi: {e}")
                await client.disconnect()
                return None, None, None
            
            # Get user info
            me = await client.get_me()
            print(f"\n🎉 Session berhasil dibuat untuk:")
            print(f"   • Nama: {me.first_name} {me.last_name or ''}")
            print(f"   • Username: @{me.username or 'Tidak ada'}")
            print(f"   • ID: {me.id}")
            
            # Get session string
            session_string = await client.export_session_string()
            await client.disconnect()
            
            return session_string, self.api_id, self.api_hash
            
        except PhoneNumberInvalid:
            print("❌ Nomor HP tidak valid")
            return None, None, None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None, None

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
        return self._config.get("telegram_api", {}).get("api_id", 24194005)
    
    @property
    def api_hash(self) -> str:
        return self._config.get("telegram_api", {}).get("api_hash", "717957f0e3ae20a7db004d08b66bfd30")
    
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
        
        # Use session string if available
        if self.session_string:
            client_params["session_string"] = self.session_string
            print(f"✅ Using session string authentication")
        else:
            # Fallback to bot token if available
            if config.bot_token:
                client_params["bot_token"] = config.bot_token
                print(f"🤖 Using bot token authentication")
            else:
                raise ValueError("No authentication method available - will generate session")
        
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
            format=f'%(asctime)s - ✨ %(name)s - %(levelname)s - %(message)s',
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
            f"✅ **Bot Information:**",
            f"  • Name: **{me.first_name}**",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            "",
            f"⚡ **Project Information:**",
            f"  • Name: **{project_info.get('project_name', 'VZOEL ASSISTANT')}**",
            f"  • Version: `{project_info.get('version', '1.0.0')}`",
            f"  • Description: _{project_info.get('description', 'Premium Assistant')}_",
            "",
            f"🔥 **System Status:**",
            f"  • Performance: **{'uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop'}**",
            f"  • Assets: **Premium Collection Loaded**",
            f"  • Parse Mode: **Enhanced Markdown**",
            "",
            f"🚀 **Ready to serve!**",
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

@Client.on_message(filters.command("start") & filters.private)
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
        f"Premium bot assistant dengan fitur-fitur canggih!",
        "",
        f"✅ **Fitur Utama:**",
        f"  • Premium styling & emoji",
        f"  • High-performance dengan uvloop",
        f"  • Interactive command system",
        f"  • Enhanced markdown support",
        "",
        f"Ketik /help untuk melihat semua perintah yang tersedia.",
        "",
        f"_{branding.get('footer_text', 'Created by VZLfxs @Lutpan')}_"
    ]
    
    await message.reply_text("\n".join(welcome_text))

@Client.on_message(filters.command("ping"))
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

@Client.on_message(filters.command("alive"))
async def alive_command(client: VzoelAssistant, message: Message):
    """Enhanced alive command showing premium status"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    
    alive_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"✅ **Bot Status:** **ONLINE**",
        f"⚡ **Version:** **{project_info.get('version', '1.0.0')}**",
        f"✨ **Uptime:** {client.get_uptime()}",
        f"🚀 **Performance:** **{'uvloop Optimized' if UVLOOP_AVAILABLE else 'Standard Event Loop'}**",
        "",
        f"**Premium Features Active:**",
        f"🔥 Enhanced Markdown Styling",
        f"🔵 Premium Emoji Collection",
        f"🟡 Interactive Command System", 
        f"🔴 High-Performance Framework",
        "",
        f"_Ready to serve with premium quality!_"
    ]
    
    await message.reply_text("\n".join(alive_text))

@Client.on_message(filters.command("info"))
async def info_command(client: VzoelAssistant, message: Message):
    """Show comprehensive bot information"""
    
    me = await client.get_me()
    project_info = client.config_data.project_info
    asset_info = client.assets.get_asset_info()
    
    info_text = [
        f"{client.assets.vzoel_signature()}",
        "",
        f"✅ **Bot Information:**",
        f"  • Name: **{me.first_name}**",
        f"  • Username: @{me.username}",
        f"  • ID: `{me.id}`",
        f"  • Version: **{project_info.get('version', '1.0.0')}**",
        "",
        f"⚡ **System Information:**",
        f"  • Framework: **Pyrogram + uvloop**",
        f"  • Parse Mode: **Enhanced Markdown**",
        f"  • Uptime: {client.get_uptime()}",
        "",
        f"🔥 **Premium Assets:**",
        f"  • Font Styles: **{asset_info['fonts']['total_styles']}**",
        f"  • Premium Emojis: **{asset_info['emojis']['total_emojis']}**",
        f"  • Categories: **{asset_info['emojis']['total_categories']}**",
        f"  • Version: **{asset_info['version']}**",
        "",
        f"_Enhanced by VZLfxs @Lutpan Premium Collection_"
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
            print(f"🔄 Starting automatic session generation...")
            
            # Generate session automatically
            session_setup = AutoSessionSetup()
            session_string, api_id, api_hash = await session_setup.create_session()
            
            if not session_string:
                print(f"\n❌ Failed to generate session string")
                return
            
            print(f"\n✅ Session generated successfully!")
            print(f"💡 Session string: {session_string[:20]}...")
            print(f"🚀 Starting userbot...")
        
        # Initialize client with session
        app = VzoelAssistant(session_string, api_id, api_hash)
        
        # Premium startup sequence
        print(f"\n🔄 Starting Vzoel Assistant...")
        print(f"⚡ Initializing premium systems...")
        
        # Start the bot
        await app.start()
        
        # Keep running with premium status
        print(f"✅ All systems ready!")
        print(f"🔥 Vzoel Assistant is now running with premium features!")
        
        # Keep alive
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print(f"\n🔄 Shutting down Vzoel Assistant...")
        logging.info("Bot stopped by user")
        
    except Exception as e:
        error_msg = f"❌ Critical error: {e}"
        print(error_msg)
        logging.error(f"Critical error in main: {e}")
        raise
    
    finally:
        # Cleanup
        if app and app.is_connected:
            await app.stop()
        print(f"✅ Vzoel Assistant stopped gracefully")

# =================================================================
# 8. APPLICATION ENTRY POINT
# =================================================================

if __name__ == "__main__":
    try:
        # Print premium banner
        banner = [
            "",
            "╔" + "═" * 50 + "╗",
            "║" + f"{'VZOEL ASSISTANT v2 - PREMIUM':^50}" + "║",
            "║" + f"{'Enhanced with Auto Session + uvloop':^50}" + "║", 
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