"""
Premium Display Helper - Enhanced UI Display for Bot Assistant
Enhanced with premium emoji and font system for superior visual presentation
Created by: Vzoel Fox's
"""

import logging
from typing import Optional, Dict, Any, List
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class DisplayHelper:
    """
    Premium Display Helper dengan enhanced features:
    - Premium banner generation dengan branding
    - Interactive menu creation dengan buttons
    - Status dashboard formatting
    - Error message styling dengan emoji
    - Loading animation text generation
    """
    
    def __init__(self, assets: Optional[VzoelAssets] = None):
        """
        Initialize Premium Display Helper
        
        Args:
            assets: VzoelAssets instance untuk premium styling
        """
        self.assets = assets or VzoelAssets()
        self.logger = self._setup_premium_logging()
        
        # Display settings
        self.banner_width = 50
        self.menu_width = 40
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self) -> logging.Logger:
        """Setup enhanced logging dengan premium styling"""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("adder2")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        init_msg = [
            f"{emoji('petir')} {bold('Premium Display Helper')} initialized",
            f"{emoji('centang')} Banner width: {bold(str(self.banner_width))}",
            f"{emoji('loading')} Menu width: {bold(str(self.menu_width))}",
            f"{emoji('utama')} Premium styling: {bold('ACTIVE')}"
        ]
        
        for line in init_msg:
            self.logger.info(line)
    
    def create_banner(self, title: str, subtitle: str = "", width: int = None) -> str:
        """
        Create premium banner dengan branding
        
        Args:
            title: Main title
            subtitle: Optional subtitle
            width: Banner width (default: self.banner_width)
            
        Returns:
            Formatted banner string
        """
        width = width or self.banner_width
        
        banner_lines = [
            "",
            "╔" + "═" * width + "╗"
        ]
        
        # Title line
        title_line = f"║{title:^{width}}║"
        banner_lines.append(title_line)
        
        # Subtitle line if provided
        if subtitle:
            subtitle_line = f"║{subtitle:^{width}}║"
            banner_lines.append(subtitle_line)
        
        banner_lines.extend([
            "╚" + "═" * width + "╝",
            ""
        ])
        
        return "\n".join(banner_lines)
    
    def create_vzoel_banner(self, status: str = "ONLINE") -> str:
        """
        Create special Vzoel branded banner
        
        Args:
            status: Bot status
            
        Returns:
            Vzoel branded banner
        """
        signature = self.assets.vzoel_signature()
        
        banner_lines = [
            "",
            "╔" + "═" * 56 + "╗",
            "║" + f"{'🤩 VZOEL ASSISTANT PREMIUM 🤩':^56}" + "║",
            "║" + f"{'Enhanced Bot Framework':^56}" + "║",
            "║" + f"{'Status: ' + status:^56}" + "║",
            "╚" + "═" * 56 + "╝",
            "",
            signature,
            ""
        ]
        
        return "\n".join(banner_lines)
    
    def create_loading_message(self, action: str, steps: List[str] = None) -> str:
        """
        Create animated loading message
        
        Args:
            action: Current action
            steps: List of steps being performed
            
        Returns:
            Formatted loading message
        """
        loading_emojis = self.assets.get_status_emojis("loading")
        loading_emoji = loading_emojis[0] if loading_emojis else "⏳"
        
        loading_lines = [
            f"{loading_emoji} {bold(action)}",
            ""
        ]
        
        if steps:
            loading_lines.append(f"{emoji('aktif')} **Progress:**")
            for i, step in enumerate(steps, 1):
                loading_lines.append(f"  {i}. {step}")
            loading_lines.append("")
        
        loading_lines.extend([
            f"{italic('Please wait...')}",
            ""
        ])
        
        return "\n".join(loading_lines)
    
    def create_success_message(self, message: str, details: List[str] = None) -> str:
        """
        Create success message dengan premium styling
        
        Args:
            message: Success message
            details: Optional success details
            
        Returns:
            Formatted success message
        """
        success_emojis = self.assets.get_status_emojis("success")
        success_emoji = success_emojis[0] if success_emojis else "✅"
        
        success_lines = [
            f"{success_emoji} {bold(message)}",
            ""
        ]
        
        if details:
            for detail in details:
                success_lines.append(f"{emoji('centang')} {detail}")
            success_lines.append("")
        
        return "\n".join(success_lines)
    
    def create_error_message(self, error: str, suggestions: List[str] = None) -> str:
        """
        Create error message dengan premium styling
        
        Args:
            error: Error message
            suggestions: Optional suggestions
            
        Returns:
            Formatted error message
        """
        error_emojis = self.assets.get_status_emojis("error")
        error_emoji = error_emojis[0] if error_emojis else "❌"
        
        error_lines = [
            f"{error_emoji} {bold('Error Occurred')}",
            "",
            f"{italic(error)}",
            ""
        ]
        
        if suggestions:
            error_lines.append(f"{emoji('loading')} **Suggestions:**")
            for suggestion in suggestions:
                error_lines.append(f"  • {suggestion}")
            error_lines.append("")
        
        return "\n".join(error_lines)
    
    def create_status_dashboard(self, title: str, stats: Dict[str, Any]) -> str:
        """
        Create comprehensive status dashboard
        
        Args:
            title: Dashboard title
            stats: Statistics dictionary
            
        Returns:
            Formatted dashboard
        """
        dashboard_lines = [
            "",
            self.create_banner(title, "System Status", 48).strip(),
            "",
            f"{self.assets.vzoel_signature()}",
            ""
        ]
        
        # Group stats by category
        categories = {}
        for key, value in stats.items():
            if isinstance(value, dict) and 'category' in value:
                category = value['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append((key, value))
            else:
                if 'general' not in categories:
                    categories['general'] = []
                categories['general'].append((key, {'value': value, 'status': 'info'}))
        
        # Display categories
        for category, items in categories.items():
            dashboard_lines.append(f"{emoji('utama')} **{category.title()}:**")
            
            for key, data in items:
                if isinstance(data, dict):
                    value = data.get('value', 'N/A')
                    status = data.get('status', 'info')
                    
                    status_emoji = {
                        'success': emoji('centang'),
                        'warning': emoji('kuning'),
                        'error': emoji('merah'),
                        'info': emoji('loading')
                    }.get(status, emoji('loading'))
                    
                    dashboard_lines.append(f"  {status_emoji} {key.replace('_', ' ').title()}: {bold(str(value))}")
                else:
                    dashboard_lines.append(f"  {emoji('loading')} {key.replace('_', ' ').title()}: {bold(str(data))}")
            
            dashboard_lines.append("")
        
        dashboard_lines.extend([
            f"{italic('Dashboard updated in real-time')}",
            ""
        ])
        
        return "\n".join(dashboard_lines)
    
    def create_menu(self, title: str, options: List[Dict[str, str]], 
                   show_numbers: bool = True) -> str:
        """
        Create interactive menu
        
        Args:
            title: Menu title
            options: List of options dengan 'text' dan optional 'description'
            show_numbers: Whether to show option numbers
            
        Returns:
            Formatted menu
        """
        menu_lines = [
            "",
            f"{emoji('centang')} **{title}**",
            ""
        ]
        
        for i, option in enumerate(options, 1):
            text = option.get('text', f'Option {i}')
            description = option.get('description', '')
            
            if show_numbers:
                if description:
                    menu_lines.append(f"{emoji('aktif')} **{i}.** {bold(text)}")
                    menu_lines.append(f"     {italic(description)}")
                else:
                    menu_lines.append(f"{emoji('aktif')} **{i}.** {text}")
            else:
                if description:
                    menu_lines.append(f"{emoji('aktif')} {bold(text)}")
                    menu_lines.append(f"     {italic(description)}")
                else:
                    menu_lines.append(f"{emoji('aktif')} {text}")
        
        menu_lines.extend([
            "",
            f"{italic('Select an option to continue')}",
            ""
        ])
        
        return "\n".join(menu_lines)
    
    def create_help_section(self, section_title: str, commands: List[Dict[str, str]]) -> str:
        """
        Create help section untuk commands
        
        Args:
            section_title: Section title
            commands: List of commands dengan 'command', 'description'
            
        Returns:
            Formatted help section
        """
        help_lines = [
            "",
            f"{emoji('petir')} **{section_title}**",
            ""
        ]
        
        for cmd in commands:
            command = cmd.get('command', '')
            description = cmd.get('description', '')
            usage = cmd.get('usage', '')
            
            help_lines.append(f"{emoji('centang')} {bold(command)}")
            
            if description:
                help_lines.append(f"     {italic(description)}")
            
            if usage:
                help_lines.append(f"     Usage: {self.assets.monospace(usage)}")
            
            help_lines.append("")
        
        return "\n".join(help_lines)
    
    def create_feature_showcase(self, features: List[Dict[str, Any]]) -> str:
        """
        Create feature showcase display
        
        Args:
            features: List of features dengan details
            
        Returns:
            Formatted feature showcase
        """
        showcase_lines = [
            "",
            f"{emoji('utama')} **Premium Features Showcase**",
            ""
        ]
        
        for feature in features:
            name = feature.get('name', 'Feature')
            description = feature.get('description', '')
            status = feature.get('status', 'active')
            
            status_emoji = {
                'active': emoji('centang'),
                'inactive': emoji('loading'),
                'premium': emoji('utama'),
                'new': emoji('petir')
            }.get(status, emoji('loading'))
            
            showcase_lines.append(f"{status_emoji} {bold(name)}")
            
            if description:
                showcase_lines.append(f"     {italic(description)}")
            
            showcase_lines.append("")
        
        return "\n".join(showcase_lines)
    
    def get_helper_info(self) -> Dict[str, Any]:
        """Get comprehensive display helper information"""
        return {
            "helper_class": self.__class__.__name__,
            "banner_width": self.banner_width,
            "menu_width": self.menu_width,
            "features": {
                "premium_banners": True,
                "loading_messages": True,
                "success_messages": True,
                "error_messages": True,
                "status_dashboards": True,
                "interactive_menus": True,
                "help_sections": True,
                "feature_showcases": True
            },
            "supported_elements": [
                "banners", "menus", "dashboards", "messages", 
                "loading_screens", "help_sections", "showcases"
            ]
        }

# Convenience functions
def create_premium_display(display_type: str, **kwargs) -> str:
    """
    Quick premium display creation function
    
    Args:
        display_type: Type of display to create
        **kwargs: Display-specific arguments
        
    Returns:
        Formatted display string
    """
    helper = DisplayHelper()
    
    if display_type == "banner":
        title = kwargs.get('title', 'Premium Bot')
        subtitle = kwargs.get('subtitle', '')
        return helper.create_banner(title, subtitle)
    
    elif display_type == "vzoel_banner":
        status = kwargs.get('status', 'ONLINE')
        return helper.create_vzoel_banner(status)
    
    elif display_type == "loading":
        action = kwargs.get('action', 'Processing')
        steps = kwargs.get('steps', [])
        return helper.create_loading_message(action, steps)
    
    elif display_type == "success":
        message = kwargs.get('message', 'Operation completed')
        details = kwargs.get('details', [])
        return helper.create_success_message(message, details)
    
    elif display_type == "error":
        error = kwargs.get('error', 'An error occurred')
        suggestions = kwargs.get('suggestions', [])
        return helper.create_error_message(error, suggestions)
    
    else:
        return helper.create_banner("Premium Display", "Unknown Type")