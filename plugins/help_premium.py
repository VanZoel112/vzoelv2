#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Help System
Enhanced help dengan auto-discovery plugins, premium mapping, dan markdown support
Created by: VZLfxs @Lutpan Assistant
"""

import os
import json
import inspect
import importlib
import asyncio
from typing import Dict, List, Any, Optional
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, vzoel_signature

class PluginDiscovery:
    """Auto-discovery system untuk detect plugins dan commands"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.discovered_plugins: Dict[str, Dict] = {}
        self.commands_map: Dict[str, Dict] = {}
        
    async def scan_plugins(self) -> Dict[str, Dict]:
        """Scan semua plugins dan extract command info"""
        LOGGER.info("🔍 Scanning plugins directory...")
        
        plugin_files = []
        if os.path.exists(self.plugins_dir):
            for file in os.listdir(self.plugins_dir):
                if file.endswith('.py') and not file.startswith('_'):
                    plugin_files.append(file[:-3])  # Remove .py extension
        
        for plugin_name in plugin_files:
            try:
                await self._analyze_plugin(plugin_name)
            except Exception as e:
                LOGGER.error(f"Error analyzing plugin {plugin_name}: {e}")
        
        LOGGER.info(f"✅ Discovered {len(self.discovered_plugins)} plugins with {len(self.commands_map)} commands")
        return self.discovered_plugins
    
    async def _analyze_plugin(self, plugin_name: str):
        """Analyze single plugin file untuk extract commands"""
        try:
            plugin_path = f"{self.plugins_dir}/{plugin_name}.py"
            
            # Read file untuk extract docstring dan commands
            with open(plugin_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract plugin info
            plugin_info = {
                "name": plugin_name,
                "file": plugin_path,
                "description": self._extract_description(content),
                "commands": self._extract_commands(content),
                "category": self._determine_category(plugin_name, content),
                "requires_premium": "premium" in content.lower() or "vzoel_assets" in content,
                "version": self._extract_version(content)
            }
            
            self.discovered_plugins[plugin_name] = plugin_info
            
            # Map commands untuk quick lookup
            for cmd in plugin_info["commands"]:
                self.commands_map[cmd["command"]] = {
                    "plugin": plugin_name,
                    **cmd
                }
                
        except Exception as e:
            LOGGER.error(f"Failed to analyze {plugin_name}: {e}")
    
    def _extract_description(self, content: str) -> str:
        """Extract plugin description dari docstring"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '"""' in line and i < 10:  # Look in first 10 lines
                desc_lines = []
                for j in range(i+1, min(i+10, len(lines))):
                    if '"""' in lines[j]:
                        break
                    desc_lines.append(lines[j].strip())
                return ' '.join(desc_lines) if desc_lines else "No description"
        return "No description available"
    
    def _extract_commands(self, content: str) -> List[Dict]:
        """Extract commands dari file content"""
        commands = []
        lines = content.split('\n')
        
        # Look for command patterns
        command_patterns = [
            'CMD_HANDLER',
            '@VzoelClient.on_message',
            'filters.command',
            'get_command(message)'
        ]
        
        current_function = None
        for i, line in enumerate(lines):
            # Detect function definitions
            if line.strip().startswith('async def ') and '_handler' in line:
                current_function = line.strip().split('(')[0].replace('async def ', '')
            
            # Look for command registrations
            if any(pattern in line for pattern in command_patterns):
                # Try to extract command name
                cmd_name = self._extract_command_name(lines, i, current_function)
                if cmd_name:
                    commands.append({
                        "command": cmd_name,
                        "function": current_function or "unknown",
                        "description": self._extract_command_description(lines, i),
                        "usage": f".{cmd_name} [arguments]"
                    })
        
        return commands
    
    def _extract_command_name(self, lines: List[str], line_index: int, function_name: str) -> str:
        """Extract actual command name dari context"""
        # Check surrounding lines untuk command references
        search_range = range(max(0, line_index-5), min(len(lines), line_index+5))
        
        for i in search_range:
            line = lines[i].lower()
            # Look for command == patterns
            if 'command ==' in line and '"' in line:
                start = line.find('"') + 1
                end = line.find('"', start)
                if start > 0 and end > start:
                    return line[start:end]
        
        # Fallback: derive dari function name
        if function_name and '_handler' in function_name:
            return function_name.replace('_handler', '').replace('async ', '')
        
        return None
    
    def _extract_command_description(self, lines: List[str], line_index: int) -> str:
        """Extract command description dari nearby comments"""
        # Look for docstring or comments near command
        search_range = range(max(0, line_index-3), min(len(lines), line_index+10))
        
        for i in search_range:
            line = lines[i].strip()
            if line.startswith('"""') and 'handler' in line.lower():
                return line.replace('"""', '').strip()
            elif line.startswith('#') and len(line) > 5:
                return line[1:].strip()
        
        return "No description available"
    
    def _determine_category(self, plugin_name: str, content: str) -> str:
        """Determine plugin category based on name and content"""
        name_lower = plugin_name.lower()
        content_lower = content.lower()
        
        if any(word in name_lower for word in ['gcast', 'broadcast', 'blacklist']):
            return "broadcast"
        elif any(word in name_lower for word in ['help', 'alive', 'ping']):
            return "basic"  
        elif any(word in name_lower for word in ['log', 'system', 'monitor']):
            return "system"
        elif any(word in name_lower for word in ['demo', 'test', 'example']):
            return "demo"
        elif 'premium' in content_lower or 'vzoel_assets' in content_lower:
            return "premium"
        else:
            return "misc"
    
    def _extract_version(self, content: str) -> str:
        """Extract version info dari file"""
        lines = content.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            if 'version' in line.lower() and ('=' in line or ':' in line):
                # Extract version number
                for char in line:
                    if char.isdigit():
                        return line[line.index(char):].split()[0]
        return "1.0.0"

class PremiumHelpSystem:
    """Premium help system dengan inline keyboard dan markdown support"""
    
    def __init__(self):
        self.plugin_discovery = PluginDiscovery()
        self.plugins_data: Dict[str, Dict] = {}
        self.categories: Dict[str, List] = {}
        self.current_sessions: Dict[int, Dict] = {}  # Track user sessions
        
    async def initialize(self):
        """Initialize help system dan discover plugins"""
        LOGGER.info("🚀 Initializing Premium Help System...")
        
        self.plugins_data = await self.plugin_discovery.scan_plugins()
        self._categorize_plugins()
        
        # Load additional metadata jika ada
        await self._load_help_metadata()
        
        LOGGER.info(f"✅ Help system ready dengan {len(self.categories)} categories")
    
    def _categorize_plugins(self):
        """Group plugins by category"""
        self.categories = {}
        
        for plugin_name, plugin_info in self.plugins_data.items():
            category = plugin_info.get("category", "misc")
            
            if category not in self.categories:
                self.categories[category] = []
            
            self.categories[category].append(plugin_info)
    
    async def _load_help_metadata(self):
        """Load additional help metadata jika ada file"""
        metadata_file = "help_metadata.json"
        if os.path.exists(metadata_file):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Merge dengan discovered data
                for plugin_name, extra_info in metadata.items():
                    if plugin_name in self.plugins_data:
                        self.plugins_data[plugin_name].update(extra_info)
                        
                LOGGER.info("📋 Loaded additional help metadata")
            except Exception as e:
                LOGGER.error(f"Failed to load help metadata: {e}")
    
    def create_main_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Create main help keyboard dengan categories"""
        buttons = []
        
        # Category buttons (2 per row)
        category_names = list(self.categories.keys())
        for i in range(0, len(category_names), 2):
            row = []
            for j in range(2):
                if i + j < len(category_names):
                    cat = category_names[i + j]
                    emoji_key = self._get_category_emoji(cat)
                    emoji_char = vzoel_assets.get_emoji(emoji_key, premium_format=True)
                    
                    row.append(InlineKeyboardButton(
                        f"{emoji_char} {cat.title()}",
                        callback_data=f"help_cat_{cat}_{user_id}"
                    ))
            buttons.append(row)
        
        # Add utility buttons
        util_row = []
        refresh_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
        info_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
        
        util_row.append(InlineKeyboardButton(
            f"{refresh_emoji} Refresh", 
            callback_data=f"help_refresh_{user_id}"
        ))
        util_row.append(InlineKeyboardButton(
            f"{info_emoji} About",
            callback_data=f"help_about_{user_id}"
        ))
        
        buttons.append(util_row)
        
        return InlineKeyboardMarkup(buttons)
    
    def create_category_keyboard(self, category: str, user_id: int) -> InlineKeyboardMarkup:
        """Create keyboard untuk specific category"""
        buttons = []
        plugins = self.categories.get(category, [])
        
        # Plugin buttons
        for plugin in plugins[:8]:  # Max 8 plugins per page
            plugin_name = plugin["name"]
            commands_count = len(plugin.get("commands", []))
            
            premium_indicator = ""
            if plugin.get("requires_premium"):
                premium_emoji = vzoel_assets.get_emoji('adder2', premium_format=True)
                premium_indicator = f" {premium_emoji}"
            
            buttons.append([InlineKeyboardButton(
                f"📄 {plugin_name.replace('_', ' ').title()} ({commands_count}){premium_indicator}",
                callback_data=f"help_plugin_{plugin_name}_{user_id}"
            )])
        
        # Navigation buttons
        nav_row = []
        back_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
        nav_row.append(InlineKeyboardButton(
            f"{back_emoji} Back to Main",
            callback_data=f"help_main_{user_id}"
        ))
        
        if len(plugins) > 8:
            next_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
            nav_row.append(InlineKeyboardButton(
                f"{next_emoji} More...",
                callback_data=f"help_cat_more_{category}_{user_id}"
            ))
        
        buttons.append(nav_row)
        
        return InlineKeyboardMarkup(buttons)
    
    def create_plugin_keyboard(self, plugin_name: str, user_id: int) -> InlineKeyboardMarkup:
        """Create keyboard untuk specific plugin details"""
        buttons = []
        plugin = self.plugins_data.get(plugin_name, {})
        commands = plugin.get("commands", [])
        
        # Command buttons (1 per row for readability)
        for cmd in commands[:6]:  # Max 6 commands shown
            cmd_name = cmd["command"]
            buttons.append([InlineKeyboardButton(
                f"⚡ {cmd_name} - {cmd.get('description', 'No description')[:30]}...",
                callback_data=f"help_cmd_{cmd_name}_{plugin_name}_{user_id}"
            )])
        
        # Navigation
        nav_row = []
        back_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
        category = plugin.get("category", "misc")
        
        nav_row.append(InlineKeyboardButton(
            f"{back_emoji} Back to {category.title()}",
            callback_data=f"help_cat_{category}_{user_id}"
        ))
        
        buttons.append(nav_row)
        
        return InlineKeyboardMarkup(buttons)
    
    def _get_category_emoji(self, category: str) -> str:
        """Get appropriate emoji untuk category"""
        emoji_map = {
            "basic": "centang",
            "broadcast": "telegram", 
            "system": "loading",
            "premium": "adder2",
            "demo": "aktif",
            "misc": "utama"
        }
        return emoji_map.get(category, "utama")
    
    def format_main_help_message(self) -> str:
        """Format main help message dengan premium styling"""
        signature = vzoel_signature(premium_format=True)
        utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
        aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
        
        total_plugins = len(self.plugins_data)
        total_commands = sum(len(p.get("commands", [])) for p in self.plugins_data.values())
        
        message = f"""{signature}

{utama_emoji} **Premium Help System**

{aktif_emoji} **Statistics:**
• **Plugins Loaded:** `{total_plugins}`
• **Commands Available:** `{total_commands}`
• **Categories:** `{len(self.categories)}`

**🎯 Select a category below to explore available commands:**"""

        return message
    
    def format_category_message(self, category: str) -> str:
        """Format category help message"""
        plugins = self.categories.get(category, [])
        category_emoji = vzoel_assets.get_emoji(self._get_category_emoji(category), premium_format=True)
        
        message = f"""{category_emoji} **{category.title()} Commands**

**📊 Category Overview:**
• **Plugins:** `{len(plugins)}`
• **Total Commands:** `{sum(len(p.get('commands', [])) for p in plugins)}`

**📝 Available Plugins:**"""
        
        for plugin in plugins[:5]:  # Show first 5
            plugin_name = plugin["name"].replace('_', ' ').title()
            commands_count = len(plugin.get("commands", []))
            premium_mark = "⭐" if plugin.get("requires_premium") else ""
            
            message += f"\n• **{plugin_name}** {premium_mark} - `{commands_count} commands`"
        
        if len(plugins) > 5:
            message += f"\n• ... and `{len(plugins) - 5}` more plugins"
        
        message += "\n\n**💡 Click on a plugin below untuk detailed commands.**"
        
        return message
    
    def format_plugin_message(self, plugin_name: str) -> str:
        """Format specific plugin help message"""
        plugin = self.plugins_data.get(plugin_name, {})
        
        name_formatted = plugin_name.replace('_', ' ').title()
        description = plugin.get("description", "No description available")
        commands = plugin.get("commands", [])
        version = plugin.get("version", "1.0.0")
        premium_mark = "⭐ Premium" if plugin.get("requires_premium") else ""
        
        aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
        centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
        
        message = f"""{aktif_emoji} **{name_formatted}** {premium_mark}

**📝 Description:**
{description}

**ℹ️ Plugin Info:**
• **Version:** `{version}`
• **Commands:** `{len(commands)}`
• **Category:** `{plugin.get('category', 'misc').title()}`

{centang_emoji} **Available Commands:**"""
        
        for cmd in commands:
            cmd_name = cmd["command"]
            cmd_desc = cmd.get("description", "No description")
            usage = cmd.get("usage", f".{cmd_name}")
            
            message += f"\n\n**⚡ {cmd_name}**"
            message += f"\n└ {cmd_desc}"
            message += f"\n└ Usage: `{usage}`"
        
        return message

# Initialize global help system
help_system = PremiumHelpSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def help_router(client: VzoelClient, message: Message):
    """Router untuk help commands"""
    command = get_command(message)
    
    if command == "help":
        await help_command_handler(client, message)
    elif command == "plugins":
        await plugins_list_handler(client, message)
    elif command == "refresh":
        await refresh_plugins_handler(client, message)

async def help_command_handler(client: VzoelClient, message: Message):
    """Main help command handler dengan premium interface"""
    # Initialize help system jika belum
    if not help_system.plugins_data:
        loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
        status_msg = await message.reply_text(f"{loading_emoji} Loading help system...")
        
        await help_system.initialize()
        await status_msg.delete()
    
    user_id = message.from_user.id
    help_system.current_sessions[user_id] = {
        "current_view": "main",
        "last_message_id": None
    }
    
    # Send main help message
    text = help_system.format_main_help_message()
    keyboard = help_system.create_main_keyboard(user_id)
    
    sent_message = await message.reply_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    
    help_system.current_sessions[user_id]["last_message_id"] = sent_message.id

async def plugins_list_handler(client: VzoelClient, message: Message):
    """List all plugins dalam format sederhana"""
    if not help_system.plugins_data:
        await help_system.initialize()
    
    utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
    aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
    
    text = f"""{utama_emoji} **Loaded Plugins**

{aktif_emoji} **Plugin List:**"""
    
    for category, plugins in help_system.categories.items():
        cat_emoji = vzoel_assets.get_emoji(help_system._get_category_emoji(category), premium_format=True)
        text += f"\n\n{cat_emoji} **{category.title()}:**"
        
        for plugin in plugins:
            name = plugin["name"].replace('_', ' ').title()
            commands_count = len(plugin.get("commands", []))
            premium_mark = "⭐" if plugin.get("requires_premium") else ""
            
            text += f"\n• {name} {premium_mark} (`{commands_count}` commands)"
    
    await message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

async def refresh_plugins_handler(client: VzoelClient, message: Message):
    """Refresh plugins discovery"""
    loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
    status_msg = await message.reply_text(f"{loading_emoji} Refreshing plugins...")
    
    await help_system.initialize()
    
    centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
    await status_msg.edit_text(
        f"{centang_emoji} **Plugins Refreshed!**\n\n"
        f"• **Plugins:** `{len(help_system.plugins_data)}`\n"
        f"• **Commands:** `{sum(len(p.get('commands', [])) for p in help_system.plugins_data.values())}`\n"
        f"• **Categories:** `{len(help_system.categories)}`"
    )

@VzoelClient.on_callback_query()
async def help_callback_handler(client: VzoelClient, callback_query: CallbackQuery):
    """Handle semua help callback queries"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    # Verify user session
    if not data.endswith(f"_{user_id}"):
        warning_emoji = vzoel_assets.get_emoji('kuning', premium_format=True)
        await callback_query.answer(f"{warning_emoji} This help session is not for you!", show_alert=True)
        return
    
    try:
        if data.startswith("help_main_"):
            # Back to main menu
            text = help_system.format_main_help_message()
            keyboard = help_system.create_main_keyboard(user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("help_cat_"):
            # Show category
            category = data.split("_")[2]
            text = help_system.format_category_message(category)
            keyboard = help_system.create_category_keyboard(category, user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("help_plugin_"):
            # Show plugin details
            plugin_name = data.split("_")[2]
            text = help_system.format_plugin_message(plugin_name)
            keyboard = help_system.create_plugin_keyboard(plugin_name, user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("help_refresh_"):
            # Refresh plugins
            loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
            await callback_query.answer(f"{loading_emoji} Refreshing plugins...")
            
            await help_system.initialize()
            
            text = help_system.format_main_help_message()
            keyboard = help_system.create_main_keyboard(user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("help_about_"):
            # Show about info
            signature = vzoel_signature(premium_format=True)
            about_text = f"""{signature}

**🎯 About VzoelV2 Help System**

• **Auto-Discovery:** Automatically detects all plugins
• **Premium Interface:** Enhanced with emoji mapping
• **Interactive Navigation:** Easy-to-use inline keyboards
• **Markdown Support:** Rich text formatting
• **Real-time Updates:** Dynamic plugin refresh

**💡 Created by VZLfxs @Lutpan Assistant**"""
            
            # Create back button
            back_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(f"{back_emoji} Back to Main", callback_data=f"help_main_{user_id}")
            ]])
            
            await callback_query.edit_message_text(
                text=about_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        
        await callback_query.answer()
        
    except Exception as e:
        LOGGER.error(f"Error handling help callback: {e}")
        error_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
        await callback_query.answer(f"{error_emoji} Error processing request", show_alert=True)

# Initialize help system on import
asyncio.create_task(help_system.initialize())