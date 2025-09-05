#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Staff Management System
Advanced admin promotion and staff listing with premium emoji mapping
Created by: Vzoel Fox's
"""

import asyncio
from typing import List, Optional, Dict, Any
from pyrogram.types import Message, ChatMember, User
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired, UserAdminInvalid, RightForbidden,
    UsernameNotOccupied, UsernameInvalid, PeerIdInvalid
)

# Import sistem terintegrasi premium
from helper_client import VzoelClient, is_user_mode, get_client_type
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumStaffSystem:
    """Premium Staff Management System dengan admin promotion dan listing"""
    
    def __init__(self):
        # Admin hierarchy mapping
        self.admin_hierarchy = {
            ChatMemberStatus.OWNER: {"name": "Pendiri", "priority": 1},
            ChatMemberStatus.ADMINISTRATOR: {"name": "Admin", "priority": 3}
        }
        
        # Special admin titles detection
        self.special_titles = {
            "founder": "Pendiri",
            "co-founder": "Wakil Pendiri", 
            "co founder": "Wakil Pendiri",
            "wakil pendiri": "Wakil Pendiri",
            "deputy": "Wakil Pendiri",
            "vice": "Wakil Pendiri",
            "admin": "Admin",
            "administrator": "Admin",
            "moderator": "Admin",
            "mod": "Admin"
        }
        
        # Premium emoji hanya dari mapping
        self.staff_emoji = {
            "owner": emoji("utama"),        # 🤩 - Pendiri
            "co_founder": emoji("adder2"),  # 💟 - Wakil Pendiri  
            "admin": emoji("centang"),      # 👍 - Admin
            "promoting": emoji("loading"),  # ⚙️ - Promoting
            "success": emoji("aktif"),      # ⚡ - Success
            "error": emoji("merah"),        # 🔥 - Error
            "list": emoji("telegram"),      # ℹ️ - List
            "user": emoji("kuning")         # 🌟 - User
        }
    
    def get_admin_title(self, member: ChatMember) -> str:
        """Get admin title dengan hierarchy detection"""
        
        # Owner always gets Pendiri
        if member.status == ChatMemberStatus.OWNER:
            return "Pendiri"
        
        # Check custom title first
        if member.custom_title:
            title_lower = member.custom_title.lower()
            
            # Check for special titles
            for key, display_name in self.special_titles.items():
                if key in title_lower:
                    return display_name
            
            # Return custom title if not special
            return member.custom_title
        
        # Default admin title
        return "Admin"
    
    def format_admin_entry(self, index: int, member: ChatMember) -> str:
        """Format single admin entry untuk display"""
        
        user = member.user
        if not user:
            return ""
        
        # Get admin title dan emoji
        admin_title = self.get_admin_title(member)
        
        # Select emoji based on title
        if admin_title == "Pendiri":
            title_emoji = self.staff_emoji["owner"]
        elif admin_title == "Wakil Pendiri":
            title_emoji = self.staff_emoji["co_founder"]
        else:
            title_emoji = self.staff_emoji["admin"]
        
        # Format name
        full_name = user.first_name or "Unknown"
        if user.last_name:
            full_name += f" {user.last_name}"
        
        # Format username
        username_text = f"@{user.username}" if user.username else "No username"
        
        # Create entry lines
        entry_lines = [
            f"{bold(f'{index}.')} {title_emoji} {bold(full_name)}",
            f"   {emoji('proses')} {monospace(username_text)}",
            f"   {emoji('loading')} {italic(admin_title)}"
        ]
        
        return "\n".join(entry_lines)
    
    async def get_chat_admins(self, client: VzoelClient, chat_id: int) -> List[ChatMember]:
        """Get all chat administrators"""
        try:
            admins = []
            
            # Get chat administrators
            async for member in client.get_chat_members(chat_id, filter="administrators"):
                if member.user and not member.user.is_bot:
                    admins.append(member)
            
            # Sort by hierarchy (owner first, then admins)
            admins.sort(key=lambda x: (
                self.admin_hierarchy.get(x.status, {"priority": 99})["priority"],
                x.user.first_name or "Unknown"
            ))
            
            return admins
            
        except Exception as e:
            LOGGER.error(f"Error getting chat admins: {e}")
            return []
    
    async def promote_user_to_admin(self, client: VzoelClient, chat_id: int, 
                                  target_user: User) -> bool:
        """Promote user to administrator"""
        try:
            # Promote user dengan basic admin rights
            await client.promote_chat_member(
                chat_id=chat_id,
                user_id=target_user.id,
                privileges={
                    "can_manage_chat": True,
                    "can_delete_messages": True,
                    "can_manage_video_chats": True,
                    "can_restrict_members": True,
                    "can_promote_members": False,  # Tidak bisa promote others
                    "can_change_info": True,
                    "can_invite_users": True,
                    "can_pin_messages": True
                }
            )
            
            return True
            
        except ChatAdminRequired:
            LOGGER.error("Chat admin privileges required to promote")
            return False
        except UserAdminInvalid:
            LOGGER.error("Cannot promote this user")
            return False
        except RightForbidden:
            LOGGER.error("Insufficient rights to promote users")
            return False
        except Exception as e:
            LOGGER.error(f"Error promoting user: {e}")
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

# Initialize premium staff system
staff_system = PremiumStaffSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def staff_router(client: VzoelClient, message: Message):
    """Router untuk staff commands"""
    command = get_command(message)
    
    if command == "admin":
        await admin_handler(client, message)
    elif command == "staff":
        await staff_handler(client, message)

async def admin_handler(client: VzoelClient, message: Message):
    """
    Admin promotion handler
    Usage: .admin @username atau .admin dengan reply
    Requires: Admin privileges dengan promote rights
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{staff_system.staff_emoji['error']} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Admin commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get arguments
    args = get_arguments(message)
    
    # Resolve target user
    target_user = await staff_system.resolve_target_user(client, message, args)
    
    if not target_user:
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{staff_system.staff_emoji['list']} {bold('PREMIUM ADMIN PROMOTION')}",
            "",
            f"{staff_system.staff_emoji['error']} **No target specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.admin @username')} - Promote by username",
            f"  • Reply to user + {monospace('.admin')} - Promote by reply",
            "",
            f"{emoji('centang')} **Examples:**",
            f"  • {monospace('.admin @johndoe')}",
            f"  • Reply to message + {monospace('.admin')}",
            "",
            f"{emoji('loading')} **Requirements:** Admin with promote rights",
            "",
            f"{italic('Premium Admin System by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show promoting status
    promoting_msg = await message.reply_text(
        f"{staff_system.staff_emoji['promoting']} {bold('Promoting User...')}\\n\\n"
        f"{emoji('proses')} **Target:** {bold(target_user.first_name)}\\n"
        f"{emoji('loading')} **Username:** {monospace(f'@{target_user.username}' if target_user.username else 'No username')}\\n"
        f"{emoji('kuning')} **Processing promotion...**",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Attempt promotion
    success = await staff_system.promote_user_to_admin(client, message.chat.id, target_user)
    
    if success:
        # Success message
        success_text = [
            f"{staff_system.staff_emoji['success']} {bold('User Promoted Successfully!')}",
            "",
            f"{emoji('utama')} **New Admin:** {bold(target_user.first_name)}",
            f"{emoji('proses')} **Username:** {monospace(f'@{target_user.username}' if target_user.username else 'No username')}",
            f"{emoji('centang')} **Rank:** {bold('Administrator')}",
            f"{emoji('aktif')} **Privileges:** Standard admin rights granted",
            "",
            f"{emoji('telegram')} **View all staff:** {monospace('.staff')}",
            "",
            f"{italic(f'Promoted by {message.from_user.first_name} via Vzoel VZLfxs @Lutpan')}"
        ]
        
        await promoting_msg.edit_text(
            "\n".join(success_text),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Successfully promoted {target_user.username or target_user.id} to admin")
        
    else:
        # Error message
        error_text = [
            f"{staff_system.staff_emoji['error']} {bold('Promotion Failed!')}",
            "",
            f"{emoji('merah')} Unable to promote user to admin",
            f"{emoji('kuning')} **Possible Issues:**",
            f"  • Insufficient admin privileges",
            f"  • User is already an admin",
            f"  • Cannot promote this user type",
            f"  • Group restrictions",
            "",
            f"{emoji('telegram')} **Current staff:** {monospace('.staff')}",
            "",
            f"{italic('Premium Admin System by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await promoting_msg.edit_text(
            "\n".join(error_text),
            parse_mode=ParseMode.MARKDOWN
        )

async def staff_handler(client: VzoelClient, message: Message):
    """
    Staff listing handler  
    Usage: .staff
    Shows all admins dengan hierarchy dan titles
    No admin privileges required untuk viewing
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{staff_system.staff_emoji['error']} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Staff commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show loading message
    loading_msg = await message.reply_text(
        f"{staff_system.staff_emoji['list']} {bold('Loading Staff List...')}\\n\\n"
        f"{emoji('loading')} Collecting administrators...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Get chat admins
    admins = await staff_system.get_chat_admins(client, message.chat.id)
    
    if not admins:
        await loading_msg.edit_text(
            f"{staff_system.staff_emoji['error']} {bold('Unable to Load Staff!')}\\n\\n"
            f"{emoji('merah')} Cannot access administrator list\\n"
            f"{emoji('kuning')} This may be due to privacy settings",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Format staff list
    chat_title = message.chat.title or "Group"
    
    staff_lines = [
        f"{staff_system.staff_emoji['list']} {bold(f'STAFF LIST - {chat_title.upper()}')}",
        "",
        f"{emoji('aktif')} **Total Administrators:** {bold(str(len(admins)))}",
        ""
    ]
    
    # Add each admin
    for index, admin in enumerate(admins, 1):
        admin_entry = staff_system.format_admin_entry(index, admin)
        if admin_entry:
            staff_lines.append(admin_entry)
            staff_lines.append("")  # Empty line between entries
    
    # Add footer
    staff_lines.extend([
        f"{emoji('utama')} **Promote new admin:** {monospace('.admin @username')}",
        "",
        f"{italic('Premium Staff System by Vzoel VZLfxs @Lutpan')}"
    ])
    
    # Update message dengan staff list
    await loading_msg.edit_text(
        "\n".join(staff_lines),
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info(f"Displayed staff list for chat {message.chat.id} - {len(admins)} admins")

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Staff Management System initialized")