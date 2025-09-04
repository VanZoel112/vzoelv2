"""
Enhanced Vzoel Client - Premium Pyrogram Client with Asset Integration
Enhanced with premium emoji and font system for superior user experience
Created by: Vzoel Fox's
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pyrogram import Client
from pyrogram.enums import ParseMode
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class VzoelClient(Client):
    """
    Enhanced Pyrogram Client dengan premium features:
    - Premium emoji dan font integration
    - Configuration management from vzoel/config.json
    - Enhanced logging dengan emoji styling
    - Auto-detection environment variables dan config file
    """
    
    def __init__(self, session_name: Optional[str] = None):
        """
        Initialize enhanced Vzoel client dengan premium assets
        
        Args:
            session_name: Nama session file, default dari config
        """
        # Initialize premium assets
        self.assets = VzoelAssets()
        
        # Load configuration
        self.config_data = self._load_config()
        
        # Setup session name
        if not session_name:
            session_name = self.config_data.get("bot_credentials", {}).get("session_name", "vzoel_client_session")
        
        # Extract credentials
        api_id = self._get_api_id()
        api_hash = self._get_api_hash()
        bot_token = self._get_bot_token()
        
        # Initialize parent Client dengan premium features
        super().__init__(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins={"root": "plugins"},
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Setup enhanced logging dengan premium styling
        self._setup_premium_logging()
        
        # Log initialization success
        self._log_initialization()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration dari vzoel/config.json dengan fallback"""
        try:
            config_path = os.path.join("vzoel", "config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logging.info(f"{emoji('centang')} Configuration loaded from vzoel/config.json")
                return config
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"{emoji('loading')} Config file error: {e}, using environment variables")
            return {}
    
    def _get_api_id(self) -> int:
        """Get API ID dari config atau environment dengan premium error handling"""
        # Try config first
        api_id = self.config_data.get("telegram_api", {}).get("api_id")
        if api_id:
            return int(api_id)
        
        # Fallback to environment
        env_api_id = os.getenv("API_ID")
        if env_api_id:
            return int(env_api_id)
        
        raise ValueError(f"{emoji('merah')} API_ID not found in config or environment")
    
    def _get_api_hash(self) -> str:
        """Get API Hash dari config atau environment"""
        # Try config first  
        api_hash = self.config_data.get("telegram_api", {}).get("api_hash")
        if api_hash:
            return api_hash
        
        # Fallback to environment
        env_api_hash = os.getenv("API_HASH")
        if env_api_hash:
            return env_api_hash
            
        raise ValueError(f"{emoji('merah')} API_HASH not found in config or environment")
    
    def _get_bot_token(self) -> str:
        """Get Bot Token dari config atau environment"""
        # Try config first
        bot_token = self.config_data.get("bot_credentials", {}).get("bot_token")
        if bot_token:
            return bot_token
        
        # Fallback to environment
        env_bot_token = os.getenv("BOT_TOKEN")
        if env_bot_token:
            return env_bot_token
            
        raise ValueError(f"{emoji('merah')} BOT_TOKEN not found in config or environment")
    
    def _setup_premium_logging(self):
        """Setup enhanced logging dengan premium emoji styling"""
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s - {emoji("aktif")} %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('vzoel_client.log')
            ]
        )
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        project_info = self.config_data.get("project_info", {})
        branding_info = self.config_data.get("branding_info", {})
        
        init_msg = [
            "",
            f"{self.assets.vzoel_signature()}",
            f"{emoji('centang')} VzoelClient initialized successfully",
            f"{emoji('petir')} Project: {bold(project_info.get('project_name', 'VZOEL CLIENT'))}",
            f"{emoji('loading')} Version: {project_info.get('version', '1.0.0')}",
            f"{emoji('utama')} Premium assets: {bold('LOADED')}",
            ""
        ]
        
        for line in init_msg:
            if line:
                logging.info(line)
            else:
                print()
    
    async def start(self):
        """Enhanced start method dengan premium startup sequence"""
        try:
            # Premium startup message
            startup_emojis = self.assets.get_usage_pattern("alive")
            if startup_emojis:
                print(f"{startup_emojis[0]} {italic('Starting Vzoel Client...')}")
            
            # Start the client
            await super().start()
            
            # Get bot info
            me = await self.get_me()
            
            # Premium startup complete message
            success_msg = self._generate_startup_message(me)
            print(success_msg)
            logging.info("VzoelClient started successfully")
            
            # Send notification to log group if configured
            await self._send_startup_notification(success_msg)
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Failed to start VzoelClient: {e}"
            print(error_msg)
            logging.error(error_msg)
            raise
    
    def _generate_startup_message(self, me) -> str:
        """Generate premium startup message dengan full branding"""
        project_info = self.config_data.get("project_info", {})
        branding_info = self.config_data.get("branding_info", {})
        
        startup_lines = [
            "",
            "╔" + "═" * 52 + "╗",
            "║" + f"{branding_info.get('assistant_display_name', 'VZOEL CLIENT'):^52}" + "║",
            "║" + f"{'Premium Client Successfully Started':^52}" + "║",
            "╚" + "═" * 52 + "╝",
            "",
            f"{self.assets.vzoel_signature()}",
            "",
            f"{emoji('centang')} **Client Information:**",
            f"  • Name: {bold(me.first_name)}",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            "",
            f"{emoji('petir')} **Project Information:**",
            f"  • Name: {bold(project_info.get('project_name', 'VZOEL CLIENT'))}",
            f"  • Version: `{project_info.get('version', '1.0.0')}`",
            f"  • Description: {italic(project_info.get('description', 'Premium Client'))}",
            "",
            f"{emoji('utama')} **Premium Features:**",
            f"  • Enhanced Pyrogram Client: {bold('✓')}",
            f"  • Premium Assets System: {bold('✓')}",  
            f"  • Configuration Management: {bold('✓')}",
            f"  • Enhanced Error Handling: {bold('✓')}",
            "",
            f"{emoji('loading')} **Status: {bold('READY TO SERVE')}**",
            "",
            f"{italic(branding_info.get('footer_text', 'Enhanced by Vzoel Fox'))}",
            ""
        ]
        
        return "\n".join(startup_lines)
    
    async def _send_startup_notification(self, message: str):
        """Send startup notification ke log group jika dikonfigurasi"""
        try:
            log_group_id = self.config_data.get("logging", {}).get("log_group_id")
            if log_group_id:
                await self.send_message(
                    chat_id=log_group_id,
                    text=message
                )
                logging.info(f"{emoji('telegram')} Startup notification sent to log group")
        except Exception as e:
            logging.warning(f"{emoji('loading')} Could not send startup notification: {e}")
    
    async def stop(self):
        """Enhanced stop method dengan premium shutdown sequence"""
        try:
            # Premium shutdown message
            shutdown_emojis = self.assets.get_status_emojis("loading")
            if shutdown_emojis:
                print(f"{shutdown_emojis[0]} {italic('Shutting down Vzoel Client...')}")
            
            await super().stop()
            
            # Final shutdown message
            success_emojis = self.assets.get_status_emojis("success")
            if success_emojis:
                final_msg = f"{success_emojis[0]} {bold('VzoelClient stopped gracefully')}"
                print(final_msg)
                logging.info(final_msg)
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Error during shutdown: {e}"
            print(error_msg)
            logging.error(error_msg)
    
    def get_premium_info(self) -> Dict[str, Any]:
        """Get comprehensive premium client information"""
        asset_info = self.assets.get_asset_info()
        project_info = self.config_data.get("project_info", {})
        
        return {
            "client_type": self.__class__.__name__,
            "session_name": self.name,
            "parse_mode": self.parse_mode.name if self.parse_mode else "DEFAULT",
            "project_info": project_info,
            "asset_info": asset_info,
            "features": {
                "premium_assets": True,
                "config_management": True,
                "enhanced_logging": True,
                "auto_plugin_loading": True
            }
        }

# Create default instance untuk backward compatibility
# Tapi sekarang dengan premium features
try:
    VzoelClientInstance = VzoelClient()
    logging.info(f"{emoji('centang')} Default VzoelClient instance created successfully")
except Exception as e:
    logging.error(f"{emoji('merah')} Failed to create default VzoelClient instance: {e}")
    VzoelClientInstance = None