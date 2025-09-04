"""
Enhanced Vzoel Assistant Loader - Premium Bot Framework Management
Enhanced with premium assets integration for superior user experience
Created by: Vzoel Fox's
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from core.client import VzoelClient
from .loader_plugins import PremiumPluginLoader
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class VzoelAssistant:
    """
    Premium Vzoel Assistant Loader dengan enhanced features:
    - Premium client management dengan asset integration
    - Enhanced plugin loading dengan emoji feedback
    - Comprehensive error handling dengan premium styling
    - Real-time status reporting dengan branding
    """
    
    def __init__(self, client: Optional[VzoelClient] = None):
        """
        Initialize Premium Vzoel Assistant
        
        Args:
            client: VzoelClient instance, akan dibuat otomatis jika None
        """
        # Initialize premium assets
        self.assets = VzoelAssets()
        
        # Setup client
        if client:
            self.bot = client
        else:
            self.bot = VzoelClient()
        
        # Initialize premium plugin loader
        self.plugin_loader = PremiumPluginLoader(self.assets)
        
        # Setup enhanced logging
        self._setup_premium_logging()
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self):
        """Setup enhanced logging dengan premium styling"""
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("aktif")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        signature = self.assets.vzoel_signature()
        init_msg = [
            "",
            signature,
            f"{emoji('centang')} VzoelAssistant Loader initialized",
            f"{emoji('petir')} Client type: {bold(self.bot.__class__.__name__)}",
            f"{emoji('loading')} Plugin loader: {bold('Premium System')}",
            f"{emoji('utama')} Assets: {bold('Enhanced Collection')}",
            ""
        ]
        
        for line in init_msg:
            if line:
                self.logger.info(line)
            else:
                print()
    
    async def start(self):
        """
        Premium startup sequence dengan enhanced feedback
        """
        try:
            self.logger.info(f"{emoji('loading')} {italic('Memulai prosedur penyalaan Premium Assistant...')}")
            
            # Start premium client
            await self._start_premium_client()
            
            # Load premium plugins
            await self._load_premium_plugins()
            
            # Get bot information
            me = await self.bot.get_me()
            
            # Generate premium success message
            success_msg = self._generate_success_message(me)
            
            # Display success message
            print(success_msg)
            self.logger.info(f"{emoji('centang')} VzoelAssistant started successfully")
            
            # Send startup notification if configured
            await self._send_startup_notification(success_msg)
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Failed to start VzoelAssistant: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            raise
    
    async def _start_premium_client(self):
        """Start premium client dengan enhanced feedback"""
        startup_emojis = self.assets.get_usage_pattern("alive")
        if startup_emojis:
            self.logger.info(f"{startup_emojis[0]} {italic('Starting premium client connection...')}")
        
        await self.bot.start()
        
        if startup_emojis:
            self.logger.info(f"{startup_emojis[1]} {bold('Client connection established')}")
    
    async def _load_premium_plugins(self):
        """Load plugins dengan premium feedback system"""
        loading_emojis = self.assets.get_status_emojis("loading")
        if loading_emojis:
            self.logger.info(f"{loading_emojis[0]} {italic('Loading premium plugin system...')}")
        
        # Load plugins using premium loader
        plugin_stats = await self.plugin_loader.load_all_plugins_async()
        
        # Report loading statistics dengan premium styling
        success_emojis = self.assets.get_status_emojis("success")
        if success_emojis:
            stats_msg = self._format_plugin_stats(plugin_stats)
            self.logger.info(f"{success_emojis[0]} Plugin loading completed: {stats_msg}")
    
    def _format_plugin_stats(self, stats: Dict[str, int]) -> str:
        """Format plugin statistics dengan premium styling"""
        total = stats.get('total', 0)
        loaded = stats.get('loaded', 0)
        failed = stats.get('failed', 0)
        
        if failed > 0:
            return f"{bold(str(loaded))}/{total} loaded, {bold(str(failed))} failed"
        else:
            return f"{bold(str(loaded))}/{total} loaded successfully"
    
    def _generate_success_message(self, me) -> str:
        """Generate premium success message dengan full branding"""
        client_info = self.bot.get_premium_info() if hasattr(self.bot, 'get_premium_info') else {}
        project_info = client_info.get('project_info', {})
        asset_info = client_info.get('asset_info', {})
        
        success_lines = [
            "",
            "╔" + "═" * 56 + "╗",
            "║" + f"{'🤩 VZOEL ASSISTANT PREMIUM - ONLINE 🤩':^56}" + "║",
            "║" + f"{'Enhanced Bot Framework Successfully Started':^56}" + "║",
            "╚" + "═" * 56 + "╝",
            "",
            f"{self.assets.vzoel_signature()}",
            "",
            f"{emoji('centang')} **Assistant Information:**",
            f"  • Name: {bold(me.first_name)}",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            "",
            f"{emoji('petir')} **Framework Information:**",
            f"  • Project: {bold(project_info.get('project_name', 'VZOEL ASSISTANT'))}",
            f"  • Version: `{project_info.get('version', '1.0.0')}`",
            f"  • Client: {bold(self.bot.__class__.__name__)}",
            "",
            f"{emoji('utama')} **Premium Features Status:**",
            f"  • Enhanced Client: {bold('✓ ACTIVE')}",
            f"  • Premium Assets: {bold('✓ LOADED')}",
            f"  • Plugin System: {bold('✓ OPERATIONAL')}",
            f"  • Error Handling: {bold('✓ ENHANCED')}",
            "",
            f"{emoji('aktif')} **Asset Information:**"
        ]
        
        # Add asset information if available
        if asset_info:
            fonts_info = asset_info.get('fonts', {})
            emojis_info = asset_info.get('emojis', {})
            
            success_lines.extend([
                f"  • Font Styles: {bold(str(fonts_info.get('total_styles', 0)))}",
                f"  • Premium Emojis: {bold(str(emojis_info.get('total_emojis', 0)))}",
                f"  • Emoji Categories: {bold(str(emojis_info.get('total_categories', 0)))}"
            ])
        
        success_lines.extend([
            "",
            f"{emoji('loading')} **Status: {bold('READY TO SERVE')}**",
            f"{emoji('telegram')} **All systems operational!**",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}",
            ""
        ])
        
        return "\n".join(success_lines)
    
    async def _send_startup_notification(self, message: str):
        """Send startup notification dengan premium styling"""
        try:
            if hasattr(self.bot, 'config_data'):
                log_group_id = self.bot.config_data.get("logging", {}).get("log_group_id")
                if log_group_id:
                    await self.bot.send_message(
                        chat_id=log_group_id,
                        text=message
                    )
                    self.logger.info(f"{emoji('telegram')} Startup notification sent to log group")
        except Exception as e:
            self.logger.warning(f"{emoji('loading')} Could not send startup notification: {e}")
    
    async def stop(self):
        """Premium shutdown sequence"""
        try:
            shutdown_emojis = self.assets.get_status_emojis("loading")
            if shutdown_emojis:
                self.logger.info(f"{shutdown_emojis[0]} {italic('Shutting down Premium Assistant...')}")
            
            # Stop client
            await self.bot.stop()
            
            # Final success message
            success_emojis = self.assets.get_status_emojis("success")
            if success_emojis:
                final_msg = f"{success_emojis[0]} {bold('VzoelAssistant stopped gracefully')}"
                print(final_msg)
                self.logger.info(final_msg)
                
        except Exception as e:
            error_msg = f"{emoji('merah')} Error during shutdown: {e}"
            print(error_msg)
            self.logger.error(error_msg)
    
    def run(self):
        """
        Premium run method dengan enhanced error handling
        """
        try:
            # Display premium banner
            self._display_premium_banner()
            
            # Run with premium features
            self.bot.run()
            
        except KeyboardInterrupt:
            self.logger.info(f"{emoji('loading')} {italic('Shutdown requested by user')}")
        except Exception as e:
            error_msg = f"{emoji('merah')} Critical error in run: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            raise
    
    def _display_premium_banner(self):
        """Display premium startup banner"""
        banner = [
            "",
            "╔" + "═" * 60 + "╗",
            "║" + f"{'VZOEL ASSISTANT PREMIUM v2':^60}" + "║",
            "║" + f"{'Enhanced Bot Framework with Premium Assets':^60}" + "║",
            "║" + f"{'Created by: Vzoel Fox':^60}" + "║",
            "╚" + "═" * 60 + "╝",
            "",
            f"{self.assets.vzoel_signature()}",
            f"{emoji('loading')} {italic('Initializing premium systems...')}",
            ""
        ]
        
        for line in banner:
            print(line)
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive assistant status dengan premium info"""
        return {
            "assistant_class": self.__class__.__name__,
            "client_info": self.bot.get_premium_info() if hasattr(self.bot, 'get_premium_info') else {},
            "is_connected": self.bot.is_connected if hasattr(self.bot, 'is_connected') else False,
            "assets_info": self.assets.get_asset_info(),
            "features": {
                "premium_client": True,
                "enhanced_plugins": True,
                "premium_assets": True,
                "enhanced_logging": True
            }
        }