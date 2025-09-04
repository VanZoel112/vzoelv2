"""
Premium Plugin Loader System - Enhanced Dynamic Module Management
Enhanced with premium emoji and font system for superior feedback
Created by: Vzoel Fox's
"""

import os
import importlib
import asyncio
import logging
from typing import Dict, List, Any, Optional
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class PremiumPluginLoader:
    """
    Premium Plugin Loader dengan enhanced features:
    - Real-time loading feedback dengan emoji
    - Comprehensive error handling dengan premium styling
    - Plugin statistics dan reporting
    - Asynchronous loading support
    """
    
    def __init__(self, assets: Optional[VzoelAssets] = None):
        """
        Initialize Premium Plugin Loader
        
        Args:
            assets: VzoelAssets instance untuk premium styling
        """
        self.assets = assets or VzoelAssets()
        self.logger = self._setup_premium_logging()
        self.plugins_dir = "plugins"
        self.loaded_plugins = []
        self.failed_plugins = []
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self) -> logging.Logger:
        """Setup enhanced logging dengan premium styling"""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("loading")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        init_msg = [
            f"{emoji('petir')} {bold('Premium Plugin Loader')} initialized",
            f"{emoji('centang')} Target directory: {bold(self.plugins_dir)}",
            f"{emoji('utama')} Enhanced features: {bold('ACTIVE')}"
        ]
        
        for line in init_msg:
            self.logger.info(line)
    
    def discover_plugins(self) -> List[str]:
        """
        Discover semua plugin files dengan premium feedback
        
        Returns:
            List of plugin module paths
        """
        plugin_modules = []
        
        if not os.path.exists(self.plugins_dir):
            self.logger.warning(f"{emoji('loading')} Plugins directory '{self.plugins_dir}' not found")
            return plugin_modules
        
        self.logger.info(f"{emoji('loading')} {italic('Discovering plugins in')} {bold(self.plugins_dir)}")
        
        # Scan for Python files
        for root, _, files in os.walk(self.plugins_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    # Convert file path to module path
                    plugin_path = os.path.join(root, file)
                    module_path = plugin_path.replace(os.sep, ".")[:-3]
                    plugin_modules.append(module_path)
        
        discovery_msg = f"{emoji('centang')} Discovered {bold(str(len(plugin_modules)))} plugin files"
        self.logger.info(discovery_msg)
        
        return plugin_modules
    
    def load_plugin(self, module_path: str) -> bool:
        """
        Load single plugin dengan enhanced error handling
        
        Args:
            module_path: Python module path (e.g., 'plugins.help')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Show loading message
            loading_emojis = self.assets.get_status_emojis("loading")
            loading_msg = f"{loading_emojis[0] if loading_emojis else '⏳'} Loading {italic(module_path)}"
            self.logger.info(loading_msg)
            
            # Import the module
            importlib.import_module(module_path)
            
            # Success message
            success_emojis = self.assets.get_status_emojis("success")
            success_msg = f"{success_emojis[0] if success_emojis else '✅'} Plugin {bold(module_path)} loaded successfully"
            self.logger.info(success_msg)
            
            self.loaded_plugins.append(module_path)
            return True
            
        except Exception as e:
            # Error message
            error_emojis = self.assets.get_status_emojis("error")
            error_msg = f"{error_emojis[0] if error_emojis else '❌'} Failed to load {bold(module_path)}: {e}"
            self.logger.error(error_msg)
            
            self.failed_plugins.append({
                'module': module_path,
                'error': str(e)
            })
            return False
    
    async def load_plugin_async(self, module_path: str) -> bool:
        """
        Asynchronous plugin loading untuk better performance
        
        Args:
            module_path: Python module path
            
        Returns:
            True if successful, False otherwise
        """
        # Run dalam thread pool untuk avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_plugin, module_path)
    
    def load_all_plugins(self) -> Dict[str, int]:
        """
        Load semua plugins dengan comprehensive reporting
        
        Returns:
            Dictionary dengan loading statistics
        """
        # Reset statistics
        self.loaded_plugins.clear()
        self.failed_plugins.clear()
        
        # Start loading process
        start_emojis = self.assets.get_usage_pattern("vzoel")
        if start_emojis:
            start_msg = f"{start_emojis[0]} {bold('Premium Plugin Loading Started')}"
            self.logger.info(start_msg)
            print(start_msg)
        
        # Discover and load plugins
        plugin_modules = self.discover_plugins()
        
        if not plugin_modules:
            self.logger.warning(f"{emoji('loading')} No plugins found to load")
            return {'total': 0, 'loaded': 0, 'failed': 0}
        
        # Load each plugin
        for module_path in plugin_modules:
            self.load_plugin(module_path)
        
        # Generate statistics
        stats = {
            'total': len(plugin_modules),
            'loaded': len(self.loaded_plugins),
            'failed': len(self.failed_plugins)
        }
        
        # Display completion report
        self._display_loading_report(stats)
        
        return stats
    
    async def load_all_plugins_async(self) -> Dict[str, int]:
        """
        Asynchronous loading semua plugins untuk better performance
        
        Returns:
            Dictionary dengan loading statistics
        """
        # Reset statistics
        self.loaded_plugins.clear()
        self.failed_plugins.clear()
        
        # Start loading process
        start_emojis = self.assets.get_usage_pattern("vzoel")
        if start_emojis:
            start_msg = f"{start_emojis[0]} {bold('Premium Plugin Loading Started (Async)')}"
            self.logger.info(start_msg)
        
        # Discover plugins
        plugin_modules = self.discover_plugins()
        
        if not plugin_modules:
            self.logger.warning(f"{emoji('loading')} No plugins found to load")
            return {'total': 0, 'loaded': 0, 'failed': 0}
        
        # Load plugins concurrently
        tasks = [self.load_plugin_async(module_path) for module_path in plugin_modules]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Generate statistics
        stats = {
            'total': len(plugin_modules),
            'loaded': len(self.loaded_plugins),
            'failed': len(self.failed_plugins)
        }
        
        # Display completion report
        self._display_loading_report(stats)
        
        return stats
    
    def _display_loading_report(self, stats: Dict[str, int]):
        """Display comprehensive loading report dengan premium styling"""
        total = stats['total']
        loaded = stats['loaded']
        failed = stats['failed']
        
        # Create report header
        report_lines = [
            "",
            "╔" + "═" * 48 + "╗",
            "║" + f"{'PLUGIN LOADING REPORT':^48}" + "║",
            "╚" + "═" * 48 + "╝",
            ""
        ]
        
        # Add statistics
        if failed == 0:
            # Perfect loading
            success_emojis = self.assets.get_status_emojis("success")
            report_lines.extend([
                f"{success_emojis[0] if success_emojis else '🎉'} {bold('Perfect Loading!')}",
                f"{emoji('centang')} Total plugins: {bold(str(total))}",
                f"{emoji('utama')} Successfully loaded: {bold(str(loaded))}",
                f"{emoji('petir')} Failed: {bold('0')}",
                "",
                f"{italic('All plugins loaded successfully!')}"
            ])
        else:
            # Mixed results
            report_lines.extend([
                f"{emoji('loading')} {bold('Loading Completed with Issues')}",
                f"{emoji('centang')} Total plugins: {bold(str(total))}",
                f"{emoji('utama')} Successfully loaded: {bold(str(loaded))}",
                f"{emoji('merah')} Failed: {bold(str(failed))}",
                ""
            ])
            
            # List failed plugins
            if self.failed_plugins:
                report_lines.append(f"{emoji('merah')} {bold('Failed Plugins:')}")
                for failed in self.failed_plugins[:3]:  # Show max 3 failed
                    report_lines.append(f"  • {failed['module']}: {failed['error'][:50]}...")
                
                if len(self.failed_plugins) > 3:
                    report_lines.append(f"  • ... and {len(self.failed_plugins) - 3} more")
            
            report_lines.append("")
            report_lines.append(f"{italic('Check logs for detailed error information')}")
        
        report_lines.append("")
        
        # Display report
        report_text = "\n".join(report_lines)
        print(report_text)
        self.logger.info("Plugin loading report displayed")
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get comprehensive plugin loading information"""
        return {
            "loader_class": self.__class__.__name__,
            "plugins_directory": self.plugins_dir,
            "loaded_plugins": self.loaded_plugins.copy(),
            "failed_plugins": self.failed_plugins.copy(),
            "statistics": {
                "total_loaded": len(self.loaded_plugins),
                "total_failed": len(self.failed_plugins),
                "success_rate": (len(self.loaded_plugins) / max(len(self.loaded_plugins) + len(self.failed_plugins), 1)) * 100
            },
            "features": {
                "async_loading": True,
                "premium_feedback": True,
                "error_reporting": True,
                "statistics_tracking": True
            }
        }
    
    def reload_plugin(self, module_path: str) -> bool:
        """
        Reload specific plugin dengan premium feedback
        
        Args:
            module_path: Python module path to reload
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"{emoji('loading')} {italic('Reloading plugin')} {bold(module_path)}")
            
            # Remove from loaded list if present
            if module_path in self.loaded_plugins:
                self.loaded_plugins.remove(module_path)
            
            # Remove from failed list if present
            self.failed_plugins = [f for f in self.failed_plugins if f['module'] != module_path]
            
            # Reload the module
            if module_path in importlib.sys.modules:
                importlib.reload(importlib.sys.modules[module_path])
            else:
                importlib.import_module(module_path)
            
            success_msg = f"{emoji('centang')} Plugin {bold(module_path)} reloaded successfully"
            self.logger.info(success_msg)
            
            self.loaded_plugins.append(module_path)
            return True
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Failed to reload {bold(module_path)}: {e}"
            self.logger.error(error_msg)
            
            self.failed_plugins.append({
                'module': module_path,
                'error': str(e)
            })
            return False

# Convenience function untuk backward compatibility
def load_all_plugins() -> Dict[str, int]:
    """
    Legacy function untuk load semua plugins
    Sekarang menggunakan PremiumPluginLoader
    
    Returns:
        Dictionary dengan loading statistics
    """
    loader = PremiumPluginLoader()
    return loader.load_all_plugins()