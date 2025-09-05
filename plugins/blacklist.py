#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Blacklist Chat System
Advanced chat moderation with word triggers and user locks
Created by: Vzoel Fox's
"""

import asyncio
import json
import os
from typing import List, Dict, Set, Optional
from pyrogram.types import Message, User
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired, MessageDeleteForbidden, MessageNotModified,
    UsernameNotOccupied, UsernameInvalid, PeerIdInvalid
)

# Import sistem terintegrasi premium
from helper_client import VzoelClient, is_user_mode, get_client_type
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumBlacklistSystem:
    """Premium Blacklist System dengan word triggers dan user locks"""
    
    def __init__(self):
        self.blacklist_file = "blacklist_data.json"
        
        # Load existing blacklist data
        self.blacklist_data = self.load_blacklist_data()
        
        # Premium emoji hanya dari mapping
        self.blacklist_emoji = {
            "add": emoji("centang"),        # 👍 - Added
            "remove": emoji("merah"),       # 🔥 - Removed
            "trigger": emoji("petir"),      # ⛈ - Trigger
            "locked": emoji("loading"),     # ⚙️ - Locked
            "deleted": emoji("aktif"),      # ⚡ - Deleted
            "admin": emoji("utama"),        # 🤩 - Admin
            "error": emoji("kuning"),       # 🌟 - Error
            "list": emoji("telegram"),      # ℹ️ - List
            "warning": emoji("proses")      # 🔄 - Warning
        }
        
    def load_blacklist_data(self) -> Dict:
        """Load blacklist data dari file"""
        try:
            if os.path.exists(self.blacklist_file):
                with open(self.blacklist_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"word_triggers": {}, "locked_users": {}}
        except Exception as e:
            LOGGER.error(f"Error loading blacklist data: {e}")
            return {"word_triggers": {}, "locked_users": {}}
    
    def save_blacklist_data(self) -> bool:
        """Save blacklist data ke file"""
        try:
            with open(self.blacklist_file, 'w', encoding='utf-8') as f:
                json.dump(self.blacklist_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            LOGGER.error(f"Error saving blacklist data: {e}")
            return False
    
    def add_word_trigger(self, chat_id: int, trigger_word: str) -> bool:
        """Add word trigger untuk chat"""
        chat_key = str(chat_id)
        
        if chat_key not in self.blacklist_data["word_triggers"]:
            self.blacklist_data["word_triggers"][chat_key] = []
        
        # Check if already exists
        trigger_lower = trigger_word.lower()
        existing_triggers = [t.lower() for t in self.blacklist_data["word_triggers"][chat_key]]
        
        if trigger_lower not in existing_triggers:
            self.blacklist_data["word_triggers"][chat_key].append(trigger_word)
            return self.save_blacklist_data()
        
        return False  # Already exists
    
    def remove_word_trigger(self, chat_id: int, trigger_word: str) -> bool:
        """Remove word trigger dari chat"""
        chat_key = str(chat_id)
        
        if chat_key in self.blacklist_data["word_triggers"]:
            trigger_lower = trigger_word.lower()
            original_triggers = self.blacklist_data["word_triggers"][chat_key]
            
            # Remove matching trigger (case insensitive)
            new_triggers = [t for t in original_triggers if t.lower() != trigger_lower]
            
            if len(new_triggers) != len(original_triggers):
                self.blacklist_data["word_triggers"][chat_key] = new_triggers
                return self.save_blacklist_data()
        
        return False  # Not found
    
    def add_locked_user(self, chat_id: int, user_id: int, username: str = None) -> bool:
        """Add user ke locked list"""
        chat_key = str(chat_id)
        user_key = str(user_id)
        
        if chat_key not in self.blacklist_data["locked_users"]:
            self.blacklist_data["locked_users"][chat_key] = {}
        
        self.blacklist_data["locked_users"][chat_key][user_key] = {
            "user_id": user_id,
            "username": username
        }
        
        return self.save_blacklist_data()
    
    def remove_locked_user(self, chat_id: int, user_id: int) -> bool:
        """Remove user dari locked list"""
        chat_key = str(chat_id)
        user_key = str(user_id)
        
        if (chat_key in self.blacklist_data["locked_users"] and 
            user_key in self.blacklist_data["locked_users"][chat_key]):
            
            del self.blacklist_data["locked_users"][chat_key][user_key]
            return self.save_blacklist_data()
        
        return False
    
    def check_word_triggers(self, chat_id: int, text: str) -> List[str]:
        """Check if text contains blacklisted words"""
        chat_key = str(chat_id)
        matched_triggers = []
        
        if chat_key in self.blacklist_data["word_triggers"]:
            text_lower = text.lower()
            
            for trigger in self.blacklist_data["word_triggers"][chat_key]:
                if trigger.lower() in text_lower:
                    matched_triggers.append(trigger)
        
        return matched_triggers
    
    def is_user_locked(self, chat_id: int, user_id: int) -> bool:
        """Check if user is locked"""
        chat_key = str(chat_id)
        user_key = str(user_id)
        
        return (chat_key in self.blacklist_data["locked_users"] and 
                user_key in self.blacklist_data["locked_users"][chat_key])
    
    async def check_admin_permissions(self, client: VzoelClient, chat_id: int, 
                                    user_id: int) -> bool:
        """Check if user has admin with delete message permissions"""
        try:
            member = await client.get_chat_member(chat_id, user_id)
            
            # Owner always has permission
            if member.status == ChatMemberStatus.OWNER:
                return True
            
            # Check admin with delete permission
            if (member.status == ChatMemberStatus.ADMINISTRATOR and 
                hasattr(member, 'privileges') and member.privileges and
                member.privileges.can_delete_messages):
                return True
            
            return False
            
        except Exception as e:
            LOGGER.error(f"Error checking admin permissions: {e}")
            return False
    
    async def resolve_target_user(self, client: VzoelClient, message: Message,
                                args: str) -> Optional[User]:
        """Resolve target user dari argument atau reply"""
        
        # Check reply first
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user
        
        # Check username argument
        if args:
            # Clean username
            username = args.strip().lstrip('@')
            
            try:
                user = await client.get_users(username)
                return user
            except (UsernameNotOccupied, UsernameInvalid, PeerIdInvalid):
                return None
        
        return None
    
    def get_chat_blacklist_info(self, chat_id: int) -> Dict:
        """Get blacklist info untuk chat"""
        chat_key = str(chat_id)
        
        word_triggers = self.blacklist_data["word_triggers"].get(chat_key, [])
        locked_users = self.blacklist_data["locked_users"].get(chat_key, {})
        
        return {
            "word_triggers": word_triggers,
            "locked_users": locked_users,
            "total_triggers": len(word_triggers),
            "total_locked": len(locked_users)
        }

# Initialize premium blacklist system
blacklist_system = PremiumBlacklistSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def blacklist_router(client: VzoelClient, message: Message):
    """Router untuk blacklist commands"""
    command = get_command(message)
    
    if command == "bl":
        await bl_handler(client, message)
    elif command == "rmbl":
        await rmbl_handler(client, message)
    elif command == "lock":
        await lock_handler(client, message)
    elif command == "unlock":
        await unlock_handler(client, message)
    elif command == "bllist":
        await bllist_handler(client, message)

@VzoelClient.on_message()
async def blacklist_monitor(client: VzoelClient, message: Message):
    """Monitor messages untuk blacklist triggers dan locked users"""
    
    # Skip if not in group or no text
    if (message.chat.type not in ["group", "supergroup"] or 
        not message.text or not message.from_user):
        return
    
    # Skip if from admin (to prevent deletion loops)
    if await blacklist_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        return
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    should_delete = False
    deletion_reason = ""
    
    # Check if user is locked
    if blacklist_system.is_user_locked(chat_id, user_id):
        should_delete = True
        deletion_reason = "User locked"
    
    # Check word triggers
    elif message.text:
        matched_triggers = blacklist_system.check_word_triggers(chat_id, message.text)
        if matched_triggers:
            should_delete = True
            deletion_reason = f"Triggered: {', '.join(matched_triggers[:2])}"
    
    # Delete message if needed
    if should_delete:
        try:
            await message.delete()
            LOGGER.info(f"Deleted message in {chat_id}: {deletion_reason}")
        except MessageDeleteForbidden:
            LOGGER.warning(f"Cannot delete message in {chat_id}: insufficient permissions")
        except Exception as e:
            LOGGER.error(f"Error deleting message: {e}")

async def bl_handler(client: VzoelClient, message: Message):
    """
    Blacklist word trigger handler
    Usage: .bl (trigger_word) atau .bl dengan reply message
    Requires: Admin dengan delete message permission
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Blacklist commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check admin permissions
    if not await blacklist_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Admin Required!')}\\n\\n"
            f"{emoji('kuning')} You need admin privileges with delete message permission.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    reply_message = message.reply_to_message
    trigger_word = ""
    
    if args:
        trigger_word = args.strip()
    elif reply_message and reply_message.text:
        trigger_word = reply_message.text.strip()
    else:
        # Show usage
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{blacklist_system.blacklist_emoji['list']} {bold('PREMIUM BLACKLIST SYSTEM')}",
            "",
            f"{blacklist_system.blacklist_emoji['error']} **No trigger word specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.bl trigger_word')} - Add word trigger",
            f"  • {monospace('.bl')} + reply to message - Use message as trigger",
            "",
            f"{emoji('centang')} **Examples:**",
            f"  • {monospace('.bl spam')}",
            f"  • Reply to unwanted message + {monospace('.bl')}",
            "",
            f"{emoji('telegram')} **View list:** {monospace('.bllist')}",
            "",
            f"{italic('Premium Blacklist by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Add trigger word
    success = blacklist_system.add_word_trigger(message.chat.id, trigger_word)
    
    if success:
        success_text = [
            f"{blacklist_system.blacklist_emoji['add']} {bold('Blacklist Added!')}",
            "",
            f"{blacklist_system.blacklist_emoji['trigger']} **Trigger:** {monospace(trigger_word)}",
            f"{emoji('aktif')} **Action:** Messages containing this will be deleted",
            f"{emoji('centang')} **Status:** Active immediately",
            "",
            f"{emoji('telegram')} **View all triggers:** {monospace('.bllist')}",
            "",
            f"{italic('Premium Blacklist by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Added blacklist trigger '{trigger_word}' in chat {message.chat.id}")
        
    else:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['warning']} {bold('Trigger Already Exists!')}\\n\\n"
            f"{emoji('kuning')} **Word:** {monospace(trigger_word)}\\n"
            f"{emoji('proses')} This trigger is already in the blacklist.",
            parse_mode=ParseMode.MARKDOWN
        )

async def rmbl_handler(client: VzoelClient, message: Message):
    """
    Remove blacklist trigger handler
    Usage: .rmbl (trigger_word) atau .rmbl dengan reply message
    Requires: Admin dengan delete message permission
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Blacklist commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check admin permissions
    if not await blacklist_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Admin Required!')}\\n\\n"
            f"{emoji('kuning')} You need admin privileges with delete message permission.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    reply_message = message.reply_to_message
    trigger_word = ""
    
    if args:
        trigger_word = args.strip()
    elif reply_message and reply_message.text:
        trigger_word = reply_message.text.strip()
    else:
        # Show current triggers for removal
        chat_info = blacklist_system.get_chat_blacklist_info(message.chat.id)
        
        if chat_info['total_triggers'] == 0:
            await message.reply_text(
                f"{blacklist_system.blacklist_emoji['error']} {bold('No Triggers Found!')}\\n\\n"
                f"{emoji('kuning')} No blacklist triggers to remove.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        trigger_list = "\\n".join([f"• {monospace(trigger)}" for trigger in chat_info['word_triggers'][:10]])
        
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{blacklist_system.blacklist_emoji['list']} {bold('REMOVE BLACKLIST TRIGGER')}",
            "",
            f"{blacklist_system.blacklist_emoji['error']} **No trigger word specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.rmbl trigger_word')} - Remove word trigger",
            f"  • {monospace('.rmbl')} + reply to message - Remove message trigger",
            "",
            f"{emoji('centang')} **Current Triggers ({chat_info['total_triggers']}):**",
            trigger_list,
            "",
            f"{emoji('telegram')} **View all:** {monospace('.bllist')}",
            "",
            f"{italic('Premium Blacklist by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Remove trigger word
    success = blacklist_system.remove_word_trigger(message.chat.id, trigger_word)
    
    if success:
        success_text = [
            f"{blacklist_system.blacklist_emoji['remove']} {bold('Blacklist Removed!')}",
            "",
            f"{blacklist_system.blacklist_emoji['trigger']} **Removed:** {monospace(trigger_word)}",
            f"{emoji('centang')} **Action:** This trigger is no longer active",
            f"{emoji('aktif')} **Status:** Messages with this word won't be deleted",
            "",
            f"{emoji('telegram')} **View remaining:** {monospace('.bllist')}",
            "",
            f"{italic('Premium Blacklist by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Removed blacklist trigger '{trigger_word}' from chat {message.chat.id}")
        
    else:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['warning']} {bold('Trigger Not Found!')}\\n\\n"
            f"{emoji('kuning')} **Word:** {monospace(trigger_word)}\\n"
            f"{emoji('proses')} This trigger is not in the blacklist.",
            parse_mode=ParseMode.MARKDOWN
        )

async def lock_handler(client: VzoelClient, message: Message):
    """
    Lock user handler - delete all messages from target user
    Usage: .lock @username atau .lock dengan reply
    Requires: Admin dengan delete message permission
    """
    
    # Check admin permissions
    if not await blacklist_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Admin Required!')}\\n\\n"
            f"{emoji('kuning')} You need admin privileges with delete message permission.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    
    # Resolve target user
    target_user = await blacklist_system.resolve_target_user(client, message, args)
    
    if not target_user:
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{blacklist_system.blacklist_emoji['list']} {bold('PREMIUM USER LOCK SYSTEM')}",
            "",
            f"{blacklist_system.blacklist_emoji['error']} **No target specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.lock @username')} - Lock by username",
            f"  • Reply to user + {monospace('.lock')} - Lock by reply",
            "",
            f"{emoji('centang')} **Examples:**",
            f"  • {monospace('.lock @spammer')}",
            f"  • Reply to message + {monospace('.lock')}",
            "",
            f"{emoji('merah')} **Unlock:** {monospace('.unlock @username')}",
            "",
            f"{italic('Premium Lock System by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if target is admin (prevent locking admins)
    if await blacklist_system.check_admin_permissions(
        client, message.chat.id, target_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Cannot Lock Admin!')}\\n\\n"
            f"{emoji('kuning')} Cannot lock administrators or group owners.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Lock user
    success = blacklist_system.add_locked_user(
        message.chat.id, target_user.id, target_user.username
    )
    
    if success:
        success_text = [
            f"{blacklist_system.blacklist_emoji['locked']} {bold('User Locked!')}",
            "",
            f"{emoji('utama')} **Locked User:** {bold(target_user.first_name)}",
            f"{emoji('proses')} **Username:** {monospace(f'@{target_user.username}' if target_user.username else 'No username')}",
            f"{blacklist_system.blacklist_emoji['deleted']} **Effect:** All messages from this user will be deleted",
            "",
            f"{emoji('merah')} **Unlock:** {monospace(f'.unlock @{target_user.username}' if target_user.username else f'.unlock {target_user.id}')}",
            "",
            f"{italic('Premium Lock System by Vzoel Fox\u0027s')}"
        ]
        
        await message.reply_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Locked user {target_user.username or target_user.id} in chat {message.chat.id}")
        
    else:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Lock Failed!')}\\n\\n"
            f"{emoji('kuning')} Unable to lock this user.",
            parse_mode=ParseMode.MARKDOWN
        )

async def unlock_handler(client: VzoelClient, message: Message):
    """Unlock user handler"""
    
    # Check admin permissions
    if not await blacklist_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Admin Required!')}",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    target_user = await blacklist_system.resolve_target_user(client, message, args)
    
    if target_user and blacklist_system.remove_locked_user(message.chat.id, target_user.id):
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['add']} {bold('User Unlocked!')}\\n\\n"
            f"{emoji('centang')} **{target_user.first_name}** can now send messages.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.reply_text(
            f"{blacklist_system.blacklist_emoji['error']} {bold('Unlock Failed!')}",
            parse_mode=ParseMode.MARKDOWN
        )

async def bllist_handler(client: VzoelClient, message: Message):
    """Show blacklist info for current chat"""
    
    chat_info = blacklist_system.get_chat_blacklist_info(message.chat.id)
    
    info_lines = [
        f"{blacklist_system.blacklist_emoji['list']} {bold('BLACKLIST STATUS')}",
        "",
        f"{blacklist_system.blacklist_emoji['trigger']} **Word Triggers:** {chat_info['total_triggers']}",
        f"{blacklist_system.blacklist_emoji['locked']} **Locked Users:** {chat_info['total_locked']}",
        "",
        f"{italic('Premium Blacklist by Vzoel Fox\u0027s')}"
    ]
    
    await message.reply_text(
        "\\n".join(info_lines),
        parse_mode=ParseMode.MARKDOWN
    )

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Blacklist System initialized")