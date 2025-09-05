#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Plugin Updater System
Auto-update system untuk plugins dengan GitHub integration
Created by: VZLfxs @Lutpan Assistant
"""

import os
import json
import shutil
import requests
import asyncio
import hashlib
import importlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ParseMode

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, vzoel_signature

class PluginUpdater:
    """System untuk update plugins otomatis dari GitHub"""
    
    def __init__(self):
        self.repo_url = "https://api.github.com/repos/VanZoel112/vzoelv2"
        self.plugins_dir = "plugins"
        self.backup_dir = "plugins_backup"
        self.update_cache = {}
        self.update_history = []
        
    async def check_updates(self) -> Dict[str, Dict]:
        """Check available updates dari GitHub"""
        LOGGER.info("🔍 Checking for plugin updates...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get latest commit info
                async with session.get(f"{self.repo_url}/commits/main") as response:
                    if response.status != 200:
                        raise Exception(f"GitHub API error: {response.status}")
                    
                    commit_data = await response.json()
                    latest_sha = commit_data["sha"][:8]
                    latest_date = commit_data["commit"]["committer"]["date"]
                
                # Get current plugin files
                async with session.get(f"{self.repo_url}/contents/plugins") as response:
                    if response.status != 200:
                        raise Exception(f"Failed to get plugins list: {response.status}")
                    
                    remote_files = await response.json()
                
                # Compare dengan local files
                updates_available = {}
                for remote_file in remote_files:
                    if remote_file["type"] == "file" and remote_file["name"].endswith(".py"):
                        file_name = remote_file["name"]
                        remote_sha = remote_file["sha"][:8]
                        
                        local_file_path = os.path.join(self.plugins_dir, file_name)
                        local_sha = await self._get_local_file_hash(local_file_path)
                        
                        if local_sha != remote_sha:
                            updates_available[file_name] = {
                                "local_sha": local_sha,
                                "remote_sha": remote_sha,
                                "download_url": remote_file["download_url"],
                                "size": remote_file["size"],
                                "is_new": not os.path.exists(local_file_path)
                            }
                
                self.update_cache = {
                    "last_check": datetime.now().isoformat(),
                    "latest_commit": latest_sha,
                    "latest_date": latest_date,
                    "updates": updates_available
                }
                
                LOGGER.info(f"✅ Found {len(updates_available)} plugin updates")
                return updates_available
                
        except Exception as e:
            LOGGER.error(f"Failed to check updates: {e}")
            return {}
    
    async def _get_local_file_hash(self, file_path: str) -> str:
        """Get hash dari local file"""
        if not os.path.exists(file_path):
            return "new_file"
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.sha1(content).hexdigest()[:8]
        except Exception:
            return "error"
    
    async def download_plugin(self, file_name: str, download_url: str) -> Tuple[bool, str]:
        """Download single plugin file"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as response:
                    if response.status != 200:
                        return False, f"Download failed: HTTP {response.status}"
                    
                    content = await response.text()
                    
                    # Create backup jika file exists
                    local_file_path = os.path.join(self.plugins_dir, file_name)
                    if os.path.exists(local_file_path):
                        await self._create_backup(local_file_path)
                    
                    # Write new file
                    with open(local_file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    return True, "Downloaded successfully"
                    
        except Exception as e:
            return False, str(e)
    
    async def _create_backup(self, file_path: str):
        """Create backup dari existing file"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        file_name = os.path.basename(file_path)
        backup_name = f"{file_name}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        shutil.copy2(file_path, backup_path)
        LOGGER.info(f"📋 Created backup: {backup_name}")
    
    async def update_plugin(self, file_name: str) -> Tuple[bool, str]:
        """Update specific plugin"""
        if file_name not in self.update_cache.get("updates", {}):
            return False, "No update available for this plugin"
        
        update_info = self.update_cache["updates"][file_name]
        success, message = await self.download_plugin(file_name, update_info["download_url"])
        
        if success:
            # Record update history
            self.update_history.append({
                "file": file_name,
                "timestamp": datetime.now().isoformat(),
                "from_sha": update_info["local_sha"],
                "to_sha": update_info["remote_sha"],
                "is_new": update_info["is_new"]
            })
            
            # Try to reload plugin
            try:
                await self._reload_plugin(file_name)
                return True, f"Plugin {file_name} updated and reloaded successfully"
            except Exception as e:
                return True, f"Plugin updated but reload failed: {e}"
        
        return success, message
    
    async def _reload_plugin(self, file_name: str):
        """Reload plugin module"""
        module_name = f"plugins.{file_name[:-3]}"  # Remove .py extension
        
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            importlib.import_module(module_name)
        
        LOGGER.info(f"🔄 Reloaded plugin: {file_name}")
    
    async def update_all_plugins(self) -> Dict[str, Tuple[bool, str]]:
        """Update semua available plugins"""
        results = {}
        
        if not self.update_cache.get("updates"):
            await self.check_updates()
        
        for file_name in self.update_cache.get("updates", {}):
            results[file_name] = await self.update_plugin(file_name)
            await asyncio.sleep(1)  # Rate limiting
        
        return results
    
    def create_update_keyboard(self, user_id: int) -> InlineKeyboardMarkup:
        """Create keyboard untuk update interface"""
        buttons = []
        updates = self.update_cache.get("updates", {})
        
        if not updates:
            # No updates available
            refresh_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
            buttons.append([InlineKeyboardButton(
                f"{refresh_emoji} Check for Updates",
                callback_data=f"update_check_{user_id}"
            )])
        else:
            # Individual update buttons
            for file_name in list(updates.keys())[:8]:  # Max 8 files
                is_new = updates[file_name]["is_new"]
                status_emoji = "🆕" if is_new else "⬆️"
                
                buttons.append([InlineKeyboardButton(
                    f"{status_emoji} {file_name}",
                    callback_data=f"update_single_{file_name.replace('.', '_')}_{user_id}"
                )])
            
            # Batch operations
            if len(updates) > 1:
                batch_row = []
                all_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
                batch_row.append(InlineKeyboardButton(
                    f"{all_emoji} Update All ({len(updates)})",
                    callback_data=f"update_all_{user_id}"
                ))
                buttons.append(batch_row)
        
        # Utility buttons
        util_row = []
        history_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
        util_row.append(InlineKeyboardButton(
            f"{history_emoji} History",
            callback_data=f"update_history_{user_id}"
        ))
        
        refresh_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
        util_row.append(InlineKeyboardButton(
            f"{refresh_emoji} Refresh",
            callback_data=f"update_check_{user_id}"
        ))
        
        buttons.append(util_row)
        
        return InlineKeyboardMarkup(buttons)
    
    def format_update_message(self) -> str:
        """Format update status message"""
        signature = vzoel_signature(premium_format=True)
        updates = self.update_cache.get("updates", {})
        last_check = self.update_cache.get("last_check", "Never")
        latest_commit = self.update_cache.get("latest_commit", "Unknown")
        
        aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
        centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
        
        if not updates:
            message = f"""{signature}

{centang_emoji} **All Plugins Up to Date!**

**📊 Update Status:**
• **Last Check:** `{last_check[:19] if last_check != 'Never' else 'Never'}`
• **Latest Commit:** `{latest_commit}`
• **Updates Available:** `0`

**✅ Your plugins are current with the latest version.**"""
        else:
            new_count = sum(1 for u in updates.values() if u["is_new"])
            update_count = len(updates) - new_count
            
            message = f"""{signature}

{aktif_emoji} **Plugin Updates Available!**

**📊 Update Summary:**
• **Last Check:** `{last_check[:19]}`
• **Latest Commit:** `{latest_commit}`
• **New Plugins:** `{new_count}`
• **Updated Plugins:** `{update_count}`

**📋 Available Updates:**"""
            
            for file_name, info in list(updates.items())[:5]:
                status = "🆕 NEW" if info["is_new"] else "⬆️ UPDATE"
                size_kb = info["size"] / 1024
                message += f"\n• **{file_name}** - {status} ({size_kb:.1f} KB)"
            
            if len(updates) > 5:
                message += f"\n• ... and `{len(updates) - 5}` more updates"
        
        return message

# Initialize updater
plugin_updater = PluginUpdater()

@VzoelClient.on_message(CMD_HANDLER)
async def updater_router(client: VzoelClient, message: Message):
    """Router untuk updater commands"""
    command = get_command(message)
    
    if command == "update":
        await update_command_handler(client, message)
    elif command == "checkupdates":
        await check_updates_handler(client, message)

async def update_command_handler(client: VzoelClient, message: Message):
    """Main update command dengan interactive interface"""
    user_id = message.from_user.id
    
    # Check for updates first
    loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
    status_msg = await message.reply_text(f"{loading_emoji} Checking for plugin updates...")
    
    await plugin_updater.check_updates()
    
    # Show update interface
    text = plugin_updater.format_update_message()
    keyboard = plugin_updater.create_update_keyboard(user_id)
    
    await status_msg.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def check_updates_handler(client: VzoelClient, message: Message):
    """Simple check updates command"""
    loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
    status_msg = await message.reply_text(f"{loading_emoji} Checking for updates...")
    
    updates = await plugin_updater.check_updates()
    
    if not updates:
        centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
        await status_msg.edit_text(f"{centang_emoji} **All plugins are up to date!**")
    else:
        aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
        new_count = sum(1 for u in updates.values() if u["is_new"])
        update_count = len(updates) - new_count
        
        text = f"""{aktif_emoji} **Updates Available!**

**📋 Summary:**
• **New Plugins:** `{new_count}`
• **Updated Plugins:** `{update_count}`

Use `.update` untuk interactive update interface."""
        
        await status_msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)

@VzoelClient.on_callback_query()
async def update_callback_handler(client: VzoelClient, callback_query: CallbackQuery):
    """Handle update callback queries"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if not data.endswith(f"_{user_id}") or not data.startswith("update_"):
        return
    
    try:
        if data.startswith("update_check_"):
            # Check for updates
            loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
            await callback_query.answer(f"{loading_emoji} Checking for updates...")
            
            await plugin_updater.check_updates()
            
            text = plugin_updater.format_update_message()
            keyboard = plugin_updater.create_update_keyboard(user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("update_single_"):
            # Update single plugin
            file_name_encoded = data.split("_")[2]
            file_name = file_name_encoded.replace('_', '.') + ".py" if not file_name_encoded.endswith("py") else file_name_encoded.replace('_', '.')
            
            loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
            await callback_query.answer(f"{loading_emoji} Updating {file_name}...")
            
            success, message = await plugin_updater.update_plugin(file_name)
            
            if success:
                centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
                await callback_query.answer(f"{centang_emoji} {message}", show_alert=True)
            else:
                merah_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
                await callback_query.answer(f"{merah_emoji} {message}", show_alert=True)
            
            # Refresh interface
            await plugin_updater.check_updates()
            text = plugin_updater.format_update_message()
            keyboard = plugin_updater.create_update_keyboard(user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("update_all_"):
            # Update all plugins
            loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
            await callback_query.answer(f"{loading_emoji} Updating all plugins...")
            
            results = await plugin_updater.update_all_plugins()
            
            success_count = sum(1 for success, _ in results.values() if success)
            total_count = len(results)
            
            if success_count == total_count:
                centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
                await callback_query.answer(
                    f"{centang_emoji} All {total_count} plugins updated successfully!",
                    show_alert=True
                )
            else:
                kuning_emoji = vzoel_assets.get_emoji('kuning', premium_format=True)
                await callback_query.answer(
                    f"{kuning_emoji} {success_count}/{total_count} plugins updated successfully",
                    show_alert=True
                )
            
            # Refresh interface
            await plugin_updater.check_updates()
            text = plugin_updater.format_update_message()
            keyboard = plugin_updater.create_update_keyboard(user_id)
            
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
            
        elif data.startswith("update_history_"):
            # Show update history
            history = plugin_updater.update_history
            
            if not history:
                centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
                history_text = f"{centang_emoji} **No Update History**\n\nNo plugins have been updated in this session."
            else:
                utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
                history_text = f"{utama_emoji} **Update History**\n\n"
                
                for update in history[-10:]:  # Show last 10 updates
                    timestamp = update["timestamp"][:19]
                    file_name = update["file"]
                    status = "🆕 NEW" if update["is_new"] else "⬆️ UPDATE"
                    
                    history_text += f"• **{file_name}** {status}\n  └ `{timestamp}`\n\n"
            
            # Create back button
            back_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(f"{back_emoji} Back to Updates", callback_data=f"update_check_{user_id}")
            ]])
            
            await callback_query.edit_message_text(
                text=history_text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        
    except Exception as e:
        LOGGER.error(f"Error in update callback: {e}")
        error_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
        await callback_query.answer(f"{error_emoji} Update error: {str(e)}", show_alert=True)