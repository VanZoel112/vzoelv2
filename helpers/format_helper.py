"""
Premium Format Helper - Enhanced Text Formatting for Bot Assistant
Enhanced with premium emoji and font system for superior text styling
Created by: Vzoel Fox's
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class FormatHelper:
    """
    Premium Format Helper dengan enhanced features:
    - Advanced text formatting dengan premium styling
    - Smart time formatting dengan localization
    - File size formatting dengan units
    - Number formatting dengan separators
    - Progress bar generation dengan emoji
    """
    
    def __init__(self, assets: Optional[VzoelAssets] = None):
        """
        Initialize Premium Format Helper
        
        Args:
            assets: VzoelAssets instance untuk premium styling
        """
        self.assets = assets or VzoelAssets()
        self.logger = self._setup_premium_logging()
        
        # Formatting settings
        self.locale = "id"  # Indonesian locale
        self.timezone_offset = 7  # WIB timezone
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self) -> logging.Logger:
        """Setup enhanced logging dengan premium styling"""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("kuning")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        init_msg = [
            f"{emoji('petir')} {bold('Premium Format Helper')} initialized",
            f"{emoji('centang')} Locale: {bold(self.locale.upper())}",
            f"{emoji('loading')} Timezone: {bold(f'UTC+{self.timezone_offset}')}",
            f"{emoji('utama')} Premium styling: {bold('ACTIVE')}"
        ]
        
        for line in init_msg:
            self.logger.info(line)
    
    def format_time(self, seconds: int) -> str:
        """
        Format time duration dengan premium styling
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        if seconds < 60:
            return f"{bold(str(seconds))}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds > 0:
                return f"{bold(str(minutes))}m {bold(str(remaining_seconds))}s"
            return f"{bold(str(minutes))}m"
        elif seconds < 86400:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes > 0:
                return f"{bold(str(hours))}h {bold(str(remaining_minutes))}m"
            return f"{bold(str(hours))}h"
        else:
            days = seconds // 86400
            remaining_hours = (seconds % 86400) // 3600
            if remaining_hours > 0:
                return f"{bold(str(days))}d {bold(str(remaining_hours))}h"
            return f"{bold(str(days))}d"
    
    def format_datetime(self, dt: datetime = None, format_type: str = "full") -> str:
        """
        Format datetime dengan premium styling
        
        Args:
            dt: Datetime object (default: now)
            format_type: Format type ("full", "date", "time", "relative")
            
        Returns:
            Formatted datetime string
        """
        if dt is None:
            dt = datetime.now()
        
        # Adjust for timezone
        dt = dt + timedelta(hours=self.timezone_offset)
        
        if format_type == "full":
            return f"{bold(dt.strftime('%d %B %Y'))}, {bold(dt.strftime('%H:%M:%S'))} WIB"
        elif format_type == "date":
            return f"{bold(dt.strftime('%d %B %Y'))}"
        elif format_type == "time":
            return f"{bold(dt.strftime('%H:%M:%S'))} WIB"
        elif format_type == "relative":
            now = datetime.now() + timedelta(hours=self.timezone_offset)
            diff = now - dt
            
            if diff.days > 0:
                return f"{bold(str(diff.days))} hari yang lalu"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{bold(str(hours))} jam yang lalu"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{bold(str(minutes))} menit yang lalu"
            else:
                return f"{bold(str(diff.seconds))} detik yang lalu"
        else:
            return str(dt)
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size dengan appropriate units
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            Formatted file size string
        """
        if size_bytes == 0:
            return f"{bold('0')} B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1
        
        if unit_index == 0:
            return f"{bold(str(int(size)))} {units[unit_index]}"
        else:
            return f"{bold(f'{size:.2f}')} {units[unit_index]}"
    
    def format_number(self, number: int, separator: str = ".") -> str:
        """
        Format number dengan thousands separator
        
        Args:
            number: Number to format
            separator: Thousands separator
            
        Returns:
            Formatted number string
        """
        formatted = f"{number:,}".replace(",", separator)
        return bold(formatted)
    
    def format_percentage(self, value: float, total: float) -> str:
        """
        Format percentage dengan premium styling
        
        Args:
            value: Current value
            total: Total value
            
        Returns:
            Formatted percentage string
        """
        if total == 0:
            return f"{bold('0')}%"
        
        percentage = (value / total) * 100
        return f"{bold(f'{percentage:.1f}')}%"
    
    def create_progress_bar(self, current: int, total: int, width: int = 20) -> str:
        """
        Create progress bar dengan emoji
        
        Args:
            current: Current progress
            total: Total target
            width: Progress bar width
            
        Returns:
            Progress bar string dengan emoji
        """
        if total == 0:
            return f"{emoji('loading')} {bold('0%')}"
        
        progress = min(current / total, 1.0)
        filled_width = int(progress * width)
        empty_width = width - filled_width
        
        # Choose appropriate emoji based on progress
        if progress == 1.0:
            bar_emoji = emoji('centang')
        elif progress >= 0.8:
            bar_emoji = emoji('utama')
        elif progress >= 0.5:
            bar_emoji = emoji('loading')
        else:
            bar_emoji = emoji('aktif')
        
        bar = "█" * filled_width + "░" * empty_width
        percentage = f"{progress * 100:.1f}%"
        
        return f"{bar_emoji} {bar} {bold(percentage)}"
    
    def create_status_line(self, label: str, value: Any, status: str = "info") -> str:
        """
        Create formatted status line
        
        Args:
            label: Status label
            value: Status value
            status: Status type ("info", "success", "warning", "error")
            
        Returns:
            Formatted status line
        """
        status_emojis = {
            "info": emoji('loading'),
            "success": emoji('centang'),
            "warning": emoji('kuning'),
            "error": emoji('merah')
        }
        
        status_emoji = status_emojis.get(status, emoji('loading'))
        return f"{status_emoji} {bold(label)}: {value}"
    
    def create_info_box(self, title: str, items: List[Dict[str, Any]]) -> str:
        """
        Create formatted information box
        
        Args:
            title: Box title
            items: List of items dengan 'label' dan 'value'
            
        Returns:
            Formatted info box
        """
        box_lines = [
            "",
            f"{emoji('utama')} **{title}**"
        ]
        
        for item in items:
            label = item.get('label', 'Unknown')
            value = item.get('value', 'N/A')
            status = item.get('status', 'info')
            
            status_line = self.create_status_line(label, value, status)
            box_lines.append(f"  {status_line}")
        
        box_lines.append("")
        return "\n".join(box_lines)
    
    def create_command_list(self, commands: List[Dict[str, str]], title: str = "Available Commands") -> str:
        """
        Create formatted command list
        
        Args:
            commands: List of commands dengan 'command' dan 'description'
            title: List title
            
        Returns:
            Formatted command list
        """
        cmd_lines = [
            "",
            f"{emoji('centang')} **{title}**",
            ""
        ]
        
        for cmd in commands:
            command = cmd.get('command', '')
            description = cmd.get('description', '')
            
            cmd_lines.append(f"{emoji('aktif')} {bold(command)} - {description}")
        
        cmd_lines.append("")
        return "\n".join(cmd_lines)
    
    def create_feature_list(self, features: List[str], title: str = "Features") -> str:
        """
        Create formatted feature list
        
        Args:
            features: List of features
            title: List title
            
        Returns:
            Formatted feature list
        """
        feature_lines = [
            "",
            f"{emoji('utama')} **{title}**"
        ]
        
        for feature in features:
            feature_lines.append(f"  {emoji('centang')} {feature}")
        
        feature_lines.append("")
        return "\n".join(feature_lines)
    
    def create_separator(self, length: int = 30, char: str = "─") -> str:
        """
        Create text separator
        
        Args:
            length: Separator length
            char: Separator character
            
        Returns:
            Separator string
        """
        return char * length
    
    def get_helper_info(self) -> Dict[str, Any]:
        """Get comprehensive format helper information"""
        return {
            "helper_class": self.__class__.__name__,
            "locale": self.locale,
            "timezone_offset": self.timezone_offset,
            "features": {
                "time_formatting": True,
                "datetime_formatting": True,
                "file_size_formatting": True,
                "number_formatting": True,
                "progress_bars": True,
                "status_lines": True,
                "info_boxes": True,
                "command_lists": True,
                "feature_lists": True
            },
            "datetime_formats": ["full", "date", "time", "relative"],
            "status_types": ["info", "success", "warning", "error"]
        }

# Convenience functions
def premium_format(text: str, format_type: str = "bold") -> str:
    """
    Quick premium formatting function
    
    Args:
        text: Text to format
        format_type: Format type ("bold", "italic", "code")
        
    Returns:
        Formatted text
    """
    assets = VzoelAssets()
    
    if format_type == "bold":
        return bold(text)
    elif format_type == "italic":
        return italic(text)
    elif format_type == "code":
        return assets.monospace(text)
    else:
        return text