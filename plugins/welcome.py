#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Welcome/Leave System
Advanced welcome and leave message management with premium emoji mapping
Created by: VZLfxs @Lutpan
"""

import json
import os
from typing import Optional, Dict, Any
from pyrogram.types import Message, ChatMemberUpdated
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import MessageNotModified

# Import sistem terintegrasi premium
from helper_client import VzoelClient, is_user_mode, get_client_type
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumWelcomeSystem:
    """Premium Welcome/Leave System dengan custom message management"""
    
    def __init__(self):
        self.welcome_file = "welcome_data.json"
        
        # Load existing welcome data
        self.welcome_data = self.load_welcome_data()
        
        # Premium emoji hanya dari mapping
        self.welcome_emoji = {
            "welcome": emoji("utama"),      # 🤩 - Welcome
            "leave": emoji("merah"),        # 🔥 - Leave
            "join": emoji("centang"),       # 👍 - Join
            "set": emoji("aktif"),          # ⚡ - Set
            "remove": emoji("kuning"),      # 🌟 - Remove
            "admin": emoji("loading"),      # ⚙️ - Admin
            "error": emoji("petir"),        # ⛈ - Error
            "list": emoji("telegram"),      # ℹ️ - List
            "greeting": emoji("adder2")     # 💟 - Greeting
        }
        
        # Default welcome message template
        self.default_welcome = f"{self.welcome_emoji['welcome']} {bold('Welcome to the group!')}\\n\\n{self.welcome_emoji['greeting']} {bold('{user_mention}')}\\n{emoji('telegram')} Enjoy your stay!"
        
        # Default leave message template  
        self.default_leave = f"{self.welcome_emoji['leave']} {bold('{user_name} has left the group')}\\n\\n{emoji('kuning')} Goodbye and take care!"
    
    def load_welcome_data(self) -> Dict:
        """Load welcome data dari file"""
        try:
            if os.path.exists(self.welcome_file):
                with open(self.welcome_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"welcome_messages": {}, "leave_messages": {}, "settings": {}}
        except Exception as e:
            LOGGER.error(f"Error loading welcome data: {e}")
            return {"welcome_messages": {}, "leave_messages": {}, "settings": {}}
    
    def save_welcome_data(self) -> bool:
        """Save welcome data ke file"""
        try:
            with open(self.welcome_file, 'w', encoding='utf-8') as f:
                json.dump(self.welcome_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            LOGGER.error(f"Error saving welcome data: {e}")
            return False
    
    def set_welcome_message(self, chat_id: int, message: str) -> bool:
        """Set custom welcome message untuk chat"""
        chat_key = str(chat_id)
        self.welcome_data["welcome_messages"][chat_key] = message
        return self.save_welcome_data()
    
    def set_leave_message(self, chat_id: int, message: str) -> bool:
        """Set custom leave message untuk chat"""
        chat_key = str(chat_id)
        self.welcome_data["leave_messages"][chat_key] = message
        return self.save_welcome_data()
    
    def get_welcome_message(self, chat_id: int) -> str:
        """Get welcome message untuk chat"""
        chat_key = str(chat_id)
        return self.welcome_data["welcome_messages"].get(chat_key, self.default_welcome)
    
    def get_leave_message(self, chat_id: int) -> str:
        """Get leave message untuk chat"""
        chat_key = str(chat_id)
        return self.welcome_data["leave_messages"].get(chat_key, self.default_leave)
    
    def remove_welcome_message(self, chat_id: int) -> bool:
        """Remove custom welcome message (reset to default)"""
        chat_key = str(chat_id)
        if chat_key in self.welcome_data["welcome_messages"]:
            del self.welcome_data["welcome_messages"][chat_key]
            return self.save_welcome_data()
        return False
    
    def remove_leave_message(self, chat_id: int) -> bool:
        """Remove custom leave message (reset to default)"""
        chat_key = str(chat_id)
        if chat_key in self.welcome_data["leave_messages"]:
            del self.welcome_data["leave_messages"][chat_key]
            return self.save_welcome_data()
        return False
    
    def format_welcome_message(self, message_template: str, user_name: str, 
                             user_mention: str, user_id: int) -> str:
        """Format welcome message dengan placeholders"""
        try:
            formatted_message = message_template
            formatted_message = formatted_message.replace("{user_name}", user_name)
            formatted_message = formatted_message.replace("{user_mention}", user_mention)
            formatted_message = formatted_message.replace("{user_id}", str(user_id))
            formatted_message = formatted_message.replace("\\n", "\n")
            return formatted_message
        except Exception as e:
            LOGGER.error(f"Error formatting message: {e}")
            return message_template
    
    async def check_admin_permissions(self, client: VzoelClient, chat_id: int, 
                                    user_id: int) -> bool:
        """Check if user has admin permissions"""
        try:
            member = await client.get_chat_member(chat_id, user_id)
            return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
        except Exception as e:
            LOGGER.error(f"Error checking admin permissions: {e}")
            return False

# Initialize premium welcome system
welcome_system = PremiumWelcomeSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def welcome_router(client: VzoelClient, message: Message):
    """Router untuk welcome commands"""
    command = get_command(message)
    
    if command == "setwelcome":
        await setwelcome_handler(client, message)
    elif command == "setleave":
        await setleave_handler(client, message)
    elif command == "welcome":
        await welcome_info_handler(client, message)
    elif command == "rmwelcome":
        await rmwelcome_handler(client, message)
    elif command == "rmleave":
        await rmleave_handler(client, message)

@VzoelClient.on_chat_member_updated()
async def handle_member_updates(client: VzoelClient, update: ChatMemberUpdated):
    """Handle member join/leave events"""
    
    # Skip if not in group or supergroup
    if update.chat.type not in ["group", "supergroup"]:
        return
    
    # Skip if no user info
    if not update.new_chat_member or not update.new_chat_member.user:
        return
    
    user = update.new_chat_member.user
    old_status = update.old_chat_member.status if update.old_chat_member else None
    new_status = update.new_chat_member.status
    
    # Skip bots
    if user.is_bot:
        return
    
    try:
        # User joined (was not member, now is member/admin)
        if (old_status in [None, ChatMemberStatus.LEFT, ChatMemberStatus.BANNED] and
            new_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]):
            
            # Send welcome message
            await send_welcome_message(client, update.chat, user)
            
        # User left (was member/admin, now left/banned)
        elif (old_status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR] and
              new_status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]):
            
            # Send leave message
            await send_leave_message(client, update.chat, user)
            
    except Exception as e:
        LOGGER.error(f"Error handling member update: {e}")

async def send_welcome_message(client: VzoelClient, chat, user):
    """Send welcome message untuk new member"""
    try:
        # Get welcome message template
        welcome_template = welcome_system.get_welcome_message(chat.id)
        
        # Create user mention
        user_name = user.first_name or "User"
        user_mention = f"[{user_name}](tg://user?id={user.id})"
        
        # Format message
        formatted_message = welcome_system.format_welcome_message(
            welcome_template, user_name, user_mention, user.id
        )
        
        # Send welcome message
        await client.send_message(
            chat_id=chat.id,
            text=formatted_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Sent welcome message for {user.id} in {chat.id}")
        
    except Exception as e:
        LOGGER.error(f"Error sending welcome message: {e}")

async def send_leave_message(client: VzoelClient, chat, user):
    """Send leave message untuk member yang keluar"""
    try:
        # Get leave message template
        leave_template = welcome_system.get_leave_message(chat.id)
        
        # Create user info (no mention for left users)
        user_name = user.first_name or "User"
        user_mention = user_name  # Plain name for left users
        
        # Format message
        formatted_message = welcome_system.format_welcome_message(
            leave_template, user_name, user_mention, user.id
        )
        
        # Send leave message
        await client.send_message(
            chat_id=chat.id,
            text=formatted_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Sent leave message for {user.id} in {chat.id}")
        
    except Exception as e:
        LOGGER.error(f"Error sending leave message: {e}")

async def setwelcome_handler(client: VzoelClient, message: Message):
    """
    Set custom welcome message handler
    Usage: .setwelcome (custom_message) atau .setwelcome dengan reply
    Requires: Admin privileges
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Welcome commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check admin permissions
    if not await welcome_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Admin Required!')}\\n\\n"
            f"{emoji('kuning')} You need admin privileges to set welcome messages.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    reply_message = message.reply_to_message
    welcome_text = ""
    
    if args:
        welcome_text = args
    elif reply_message and reply_message.text:
        welcome_text = reply_message.text
    else:
        # Show usage dengan placeholders
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{welcome_system.welcome_emoji['list']} {bold('SET WELCOME MESSAGE')}",
            "",
            f"{welcome_system.welcome_emoji['error']} **No message specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.setwelcome your welcome message')}",
            f"  • Reply to message + {monospace('.setwelcome')}",
            "",
            f"{emoji('centang')} **Placeholders:**",
            f"  • {monospace('{user_name}')} - User's first name",
            f"  • {monospace('{user_mention}')} - Clickable mention",
            f"  • {monospace('{user_id}')} - User's ID",
            "",
            f"{emoji('telegram')} **Example:**",
            f"  {monospace('.setwelcome Welcome {user_mention} to our group!')}",
            "",
            f"{italic('Premium Welcome by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Set welcome message
    success = welcome_system.set_welcome_message(message.chat.id, welcome_text)
    
    if success:
        # Preview dengan dummy user
        preview_message = welcome_system.format_welcome_message(
            welcome_text, "John Doe", "[John Doe](tg://user?id=12345)", 12345
        )
        
        success_text = [
            f"{welcome_system.welcome_emoji['set']} {bold('Welcome Message Set!')}",
            "",
            f"{welcome_system.welcome_emoji['welcome']} **Preview:**",
            preview_message,
            "",
            f"{emoji('centang')} **Status:** Active for new members",
            f"{emoji('telegram')} **Remove:** {monospace('.rmwelcome')}",
            "",
            f"{italic('Premium Welcome by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Set welcome message for chat {message.chat.id}")
        
    else:
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Failed to Set Welcome!')}\\n\\n"
            f"{emoji('kuning')} Unable to save welcome message.",
            parse_mode=ParseMode.MARKDOWN
        )

async def setleave_handler(client: VzoelClient, message: Message):
    """
    Set custom leave message handler
    Usage: .setleave (custom_message) atau .setleave dengan reply
    Requires: Admin privileges
    """
    
    # Check admin permissions
    if not await welcome_system.check_admin_permissions(
        client, message.chat.id, message.from_user.id):
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Admin Required!')}",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    reply_message = message.reply_to_message
    leave_text = ""
    
    if args:
        leave_text = args
    elif reply_message and reply_message.text:
        leave_text = reply_message.text
    else:
        # Show usage
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{welcome_system.welcome_emoji['list']} {bold('SET LEAVE MESSAGE')}",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.setleave your leave message')}",
            f"  • Reply to message + {monospace('.setleave')}",
            "",
            f"{emoji('centang')} **Placeholders:**",
            f"  • {monospace('{user_name}')} - User's name",
            f"  • {monospace('{user_id}')} - User's ID",
            "",
            f"{emoji('telegram')} **Example:**",
            f"  {monospace('.setleave Goodbye {user_name}! Take care.')}",
            "",
            f"{italic('Premium Welcome by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Set leave message
    success = welcome_system.set_leave_message(message.chat.id, leave_text)
    
    if success:
        # Preview dengan dummy user
        preview_message = welcome_system.format_welcome_message(
            leave_text, "John Doe", "John Doe", 12345
        )
        
        success_text = [
            f"{welcome_system.welcome_emoji['set']} {bold('Leave Message Set!')}",
            "",
            f"{welcome_system.welcome_emoji['leave']} **Preview:**",
            preview_message,
            "",
            f"{emoji('centang')} **Status:** Active for leaving members",
            f"{emoji('telegram')} **Remove:** {monospace('.rmleave')}",
            "",
            f"{italic('Premium Welcome by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Set leave message for chat {message.chat.id}")
        
    else:
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Failed to Set Leave!')}",
            parse_mode=ParseMode.MARKDOWN
        )

async def welcome_info_handler(client: VzoelClient, message: Message):
    """Show current welcome and leave message settings"""
    
    chat_key = str(message.chat.id)
    has_custom_welcome = chat_key in welcome_system.welcome_data["welcome_messages"]
    has_custom_leave = chat_key in welcome_system.welcome_data["leave_messages"]
    
    info_lines = [
        f"{welcome_system.welcome_emoji['list']} {bold('WELCOME SETTINGS')}",
        "",
        f"{welcome_system.welcome_emoji['welcome']} **Welcome:** {'Custom' if has_custom_welcome else 'Default'}",
        f"{welcome_system.welcome_emoji['leave']} **Leave:** {'Custom' if has_custom_leave else 'Default'}",
        "",
        f"{emoji('utama')} **Commands:**",
        f"  • {monospace('.setwelcome message')} - Set welcome",
        f"  • {monospace('.setleave message')} - Set leave",
        f"  • {monospace('.rmwelcome')} - Reset welcome",
        f"  • {monospace('.rmleave')} - Reset leave",
        "",
        f"{italic('Premium Welcome by Vzoel VZLfxs @Lutpan')}"
    ]
    
    await message.reply_text(
        "\n".join(info_lines),
        parse_mode=ParseMode.MARKDOWN
    )

async def rmwelcome_handler(client: VzoelClient, message: Message):
    """Remove custom welcome message (reset to default)"""
    
    if await welcome_system.check_admin_permissions(client, message.chat.id, message.from_user.id):
        if welcome_system.remove_welcome_message(message.chat.id):
            await message.reply_text(
                f"{welcome_system.welcome_emoji['remove']} {bold('Welcome Reset!')}\\n\\n"
                f"{emoji('centang')} Using default welcome message now.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                f"{welcome_system.welcome_emoji['error']} {bold('No Custom Welcome!')}",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Admin Required!')}",
            parse_mode=ParseMode.MARKDOWN
        )

async def rmleave_handler(client: VzoelClient, message: Message):
    """Remove custom leave message (reset to default)"""
    
    if await welcome_system.check_admin_permissions(client, message.chat.id, message.from_user.id):
        if welcome_system.remove_leave_message(message.chat.id):
            await message.reply_text(
                f"{welcome_system.welcome_emoji['remove']} {bold('Leave Message Reset!')}\\n\\n"
                f"{emoji('centang')} Using default leave message now.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                f"{welcome_system.welcome_emoji['error']} {bold('No Custom Leave Message!')}",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        await message.reply_text(
            f"{welcome_system.welcome_emoji['error']} {bold('Admin Required!')}",
            parse_mode=ParseMode.MARKDOWN
        )

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Welcome/Leave System initialized")