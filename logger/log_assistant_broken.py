"""
Vzoel Assistant Logger - Premium Logging System
Enhanced logging dengan premium assets dan config integration
Created by: Vzoel Fox's
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Union, List
from pyrogram import Client
from pyrogram.types import Message

try:
    from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
except ImportError:
    print("Warning: Could not import premium assets, using basic logging")
    def bold(text): return f"**{text}**"
    def italic(text): return f"_{text}_"
    def emoji(key): return ""
    def vzoel_msg(): return "Vzoel Assistant"

class VzoelLogger:
    """
    Premium logging system dengan config integration dan Telegram logging
    """
    
    def __init__(self, config_path: str = "vzoel/config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.assets = None
        
        # Initialize premium assets if available
        try:
            self.assets = VzoelAssets()
        except:
            pass
        
        # Setup local logging
        self.setup_local_logging()
        
        # Telegram logging setup
        self.log_group_id = self.config.get("logging", {}).get("log_group_id")
        self.telegram_client = None
        
        # Logging statistics
        self.stats = {
            "total_logs": 0,
            "info_count": 0,
            "warning_count": 0,
            "error_count": 0,
            "critical_count": 0,
            "session_start": datetime.now().isoformat()
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration dari vzoel/config.json"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Failed to load config: {e}")
            return {}
    
    def setup_local_logging(self):
        """Setup local file logging system"""
        
        # Create logs directory if not exists
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Setup formatter dengan premium styling
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        formatter = logging.Formatter(log_format)
        
        # Setup file handler
        log_file = os.path.join(logs_dir, f"vzoel_assistant_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Setup logger
        self.logger = logging.getLogger("VzoelAssistant")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def set_telegram_client(self, client: Client):
        """Set Telegram client untuk logging ke group"""
        self.telegram_client = client
    
    def get_premium_emoji(self, emoji_key: str) -> str:
        """Get premium emoji atau fallback"""
        if self.assets:
            return self.assets.get_emoji(emoji_key)
        return emoji(emoji_key) if 'emoji' in globals() else ""
    
    def format_message(self, level: str, message: str, extra_data: Dict = None) -> str:
        """Format message dengan premium styling"""
        
        level_emojis = {
            "INFO": "centang",
            "WARNING": "loading",
            "ERROR": "merah", 
            "CRITICAL": "merah",
            "DEBUG": "aktif",
            "SUCCESS": "utama"
        }
        
        emoji_char = self.get_premium_emoji(level_emojis.get(level, "centang"))
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Basic formatting
        formatted_parts = [
            f"{emoji_char} {bold(level)} [{timestamp}]",
            f"{message}"
        ]
        
        # Add extra data if provided
        if extra_data:
            for key, value in extra_data.items():
                formatted_parts.append(f"{italic(key)}: {bold(str(value))}")
        
        return "\n".join(formatted_parts)
    
    async def log_to_telegram(self, level: str, message: str, extra_data: Dict = None):
        """Send log message to Telegram group"""
        
        if not self.telegram_client or not self.log_group_id:
            return
        
        try:
            # Format untuk Telegram
            telegram_message = self.format_message(level, message, extra_data)
            
            # Add session info untuk critical logs
            if level in ["ERROR", "CRITICAL"]:
                project_info = self.config.get("project_info", {})
                session_info = [
                    "",
                    f"{self.get_premium_emoji('loading')} {bold('Session Info:')}",
                    f"• Version: {project_info.get('version', 'Unknown')}",
                    f"• Project: {project_info.get('project_name', 'Vzoel Assistant')}",
                    f"• Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                ]
                telegram_message += "\n".join(session_info)
            
            # Send to group
            await self.telegram_client.send_message(
                chat_id=self.log_group_id,
                text=telegram_message
            )
            
        except Exception as e:
            # Fallback to local logging jika Telegram gagal
            self.logger.error(f"Failed to send log to Telegram: {e}")
    
    def info(self, message: str, extra_data: Dict = None, send_to_telegram: bool = False):
        """Log info message"""
        self.logger.info(message)
        self.stats["info_count"] += 1
        self.stats["total_logs"] += 1
        
        if send_to_telegram and self.telegram_client:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.log_to_telegram("INFO", message, extra_data))
            except:
                pass
    
    def warning(self, message: str, extra_data: Dict = None, send_to_telegram: bool = False):
        """Log warning message"""
        self.logger.warning(message)
        self.stats["warning_count"] += 1
        self.stats["total_logs"] += 1
        
        if send_to_telegram and self.telegram_client:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.log_to_telegram("WARNING", message, extra_data))
            except:
                pass
    
    def error(self, message: str, extra_data: Dict = None, send_to_telegram: bool = True):
        """Log error message (auto send to Telegram)"""
        self.logger.error(message)
        self.stats["error_count"] += 1
        self.stats["total_logs"] += 1
        
        if send_to_telegram and self.telegram_client:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.log_to_telegram("ERROR", message, extra_data))
            except:
                pass
    
    def critical(self, message: str, extra_data: Dict = None, send_to_telegram: bool = True):
        """Log critical message (auto send to Telegram)"""
        self.logger.critical(message)
        self.stats["critical_count"] += 1
        self.stats["total_logs"] += 1
        
        if send_to_telegram and self.telegram_client:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.log_to_telegram("CRITICAL", message, extra_data))
            except:
                pass
    
    def success(self, message: str, extra_data: Dict = None, send_to_telegram: bool = False):
        """Log success message dengan premium styling"""
        self.logger.info(f"SUCCESS: {message}")
        self.stats["total_logs"] += 1
        
        if send_to_telegram and self.telegram_client:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                loop.create_task(self.log_to_telegram("SUCCESS", message, extra_data))
            except:
                pass
    
    def log_command_usage(self, command: str, user_id: int, chat_id: int, success: bool = True):
        """Log command usage untuk statistics"""
        
        status = "SUCCESS" if success else "FAILED"
        log_data = {
            "command": command,
            "user_id": user_id,
            "chat_id": chat_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        message = f"Command {command} executed by user {user_id} in chat {chat_id}"
        
        if success:
            self.info(message, log_data)
        else:
            self.warning(message, log_data)
    
    def log_startup(self, bot_info: Dict):
        """Log bot startup dengan system information"""
        
        startup_data = {
            "bot_id": bot_info.get("id"),
            "bot_username": bot_info.get("username"),
            "bot_name": bot_info.get("first_name"),
            "config_loaded": len(self.config) > 0,
            "premium_assets": self.assets is not None,
            "telegram_logging": self.log_group_id is not None
        }
        
        project_info = self.config.get("project_info", {})
        message = f"{project_info.get('project_name', 'Vzoel Assistant')} v{project_info.get('version', '1.0.0')} started successfully"
        
        self.success(message, startup_data, send_to_telegram=True)
    
    def log_shutdown(self, reason: str = "Normal shutdown"):
        """Log bot shutdown"""
        
        shutdown_data = {
            "reason": reason,
            "uptime_stats": self.get_session_stats(),
            "timestamp": datetime.now().isoformat()
        }
        
        message = f"Bot shutdown: {reason}"
        self.info(message, shutdown_data, send_to_telegram=True)
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        
        session_start = datetime.fromisoformat(self.stats["session_start"])
        uptime_seconds = (datetime.now() - session_start).total_seconds()
        
        return {
            "uptime_seconds": int(uptime_seconds),
            "uptime_formatted": self.format_uptime(uptime_seconds),
            "total_logs": self.stats["total_logs"],
            "info_logs": self.stats["info_count"],
            "warning_logs": self.stats["warning_count"],
            "error_logs": self.stats["error_count"],
            "critical_logs": self.stats["critical_count"]
        }
    
    def format_uptime(self, seconds: float) -> str:
        """Format uptime untuk display"""
        
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    async def create_log_report(self) -> str:
        """Create comprehensive log report dengan premium formatting"""
        
        stats = self.get_session_stats()
        project_info = self.config.get("project_info", {})
        
        report_lines = [
            f"{self.get_premium_emoji('utama')} {bold('VZOEL ASSISTANT LOG REPORT')}",
            "",
            f"{self.get_premium_emoji('centang')} {bold('Session Information:')}",
            f"• Project: {bold(project_info.get('project_name', 'Vzoel Assistant'))}",
            f"" Version: {bold(project_info.get('version', '1.0.0'))}",
            f"" Uptime: {bold(stats['uptime_formatted'])}",
            f"" Session Start: {bold(self.stats['session_start'][:19])}",
            "",
            f"{self.get_premium_emoji('loading')} {bold('Logging Statistics:')}",
            f"" Total Logs: {bold(str(stats['total_logs']))}",
            f"" Info: {bold(str(stats['info_logs']))}",
            f"" Warnings: {bold(str(stats['warning_logs']))}",
            f"" Errors: {bold(str(stats['error_logs']))}",
            f"" Critical: {bold(str(stats['critical_logs']))}",
            "",
            f"{self.get_premium_emoji('aktif')} {bold('System Status:')}",
            f"" Config Loaded: {bold('' if len(self.config) > 0 else '')}",
            f"" Premium Assets: {bold('' if self.assets else '')}",
            f"" Telegram Logging: {bold('' if self.log_group_id else '')}",
            f"" Local Logging: {bold('')}",
            "",
            f"{italic('Generated by Vzoel Assistant Logger System')}"
        ]
        
        return "\n".join(report_lines)

# Global logger instance
vzoel_logger = VzoelLogger()

# Convenience functions
def log_info(message: str, extra_data: Dict = None, send_to_telegram: bool = False):
    """Quick info logging"""
    vzoel_logger.info(message, extra_data, send_to_telegram)

def log_warning(message: str, extra_data: Dict = None, send_to_telegram: bool = False):
    """Quick warning logging"""
    vzoel_logger.warning(message, extra_data, send_to_telegram)

def log_error(message: str, extra_data: Dict = None, send_to_telegram: bool = True):
    """Quick error logging"""
    vzoel_logger.error(message, extra_data, send_to_telegram)

def log_success(message: str, extra_data: Dict = None, send_to_telegram: bool = False):
    """Quick success logging"""
    vzoel_logger.success(message, extra_data, send_to_telegram)

def set_telegram_client(client: Client):
    """Set Telegram client untuk global logger"""
    vzoel_logger.set_telegram_client(client)

def get_logger() -> VzoelLogger:
    """Get global logger instance"""
    return vzoel_logger