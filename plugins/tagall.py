#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium TagAll System
Advanced group tagging with animated premium emoji rotation and batched mentions
Created by: VZLfxs @Lutpan
"""

import asyncio
from typing import List, Optional, Dict, Any
from pyrogram.types import Message, User
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import MessageNotModified, FloodWait, ChatAdminRequired

# Import sistem terintegrasi premium
from helper_client import VzoelClient, is_user_mode, get_client_type
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumTagAllSystem:
    """Premium TagAll System dengan emoji rotation dan batched mentions"""
    
    def __init__(self):
        # Premium emoji rotation frames untuk tagall
        self.tagall_emoji_frames = [
            emoji("utama"),      # 🤩 - Primary
            emoji("centang"),    # 👍 - Check
            emoji("aktif"),      # ⚡ - Active  
            emoji("telegram"),   # ℹ️ - Telegram
            emoji("adder2"),     # 💟 - Premium
            emoji("petir"),      # ⛈ - Lightning
            emoji("kuning"),     # 🌟 - Star
            emoji("loading"),    # ⚙️ - Loading
            emoji("proses"),     # 🔄 - Process
            emoji("merah")       # 🔥 - Fire
        ]
        
        # Font styles untuk rotation
        self.font_styles = [
            {"name": "bold", "func": bold},
            {"name": "italic", "func": italic},
            {"name": "monospace", "func": monospace},
            {"name": "normal", "func": lambda x: x}
        ]
        
        # Active tagall sessions
        self.active_sessions = {}
        
        # Member collection settings
        self.batch_size = 5  # 5 mentions per message
        self.edit_interval = 4.0  # 4 seconds between edits
        
    async def collect_group_members(self, client: VzoelClient, chat_id: int) -> List[User]:
        """Collect all group members yang bisa ditag - works for both user and bot mode"""
        members = []
        
        try:
            client_type = get_client_type(client)
            LOGGER.info(f"Collecting members for chat {chat_id} using {client_type} mode")
            
            # Get chat members - works without admin for user mode
            async for member in client.get_chat_members(chat_id):
                # Skip bots, deleted accounts, dan restricted users
                if (member.user and 
                    not member.user.is_bot and 
                    not member.user.is_deleted and
                    member.status not in [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]):
                    
                    members.append(member.user)
            
            LOGGER.info(f"Collected {len(members)} taggable members with {client_type} mode")
            return members
            
        except ChatAdminRequired:
            # User mode can still work in many cases without admin
            if is_user_mode(client):
                LOGGER.info("Continuing with user mode - admin not required")
                try:
                    # Alternative method for user accounts
                    chat = await client.get_chat(chat_id)
                    # Use basic member list if available
                    return members  # Return what we have so far
                except:
                    pass
            else:
                LOGGER.warning("Admin privileges required for bot mode")
            return []
        except Exception as e:
            LOGGER.error(f"Error collecting members: {e}")
            return []
    
    def create_member_batches(self, members: List[User]) -> List[List[User]]:
        """Split members into batches of 5"""
        batches = []
        
        for i in range(0, len(members), self.batch_size):
            batch = members[i:i + self.batch_size]
            batches.append(batch)
        
        return batches
    
    def format_tagall_message(self, base_message: str, members: List[User], 
                            emoji_frame: str, font_style: Dict[str, Any]) -> str:
        """Format tagall message dengan premium styling"""
        
        # Apply font style to base message
        styled_message = font_style["func"](base_message)
        
        # Create member mentions
        mentions = []
        for member in members:
            # Create mention dengan premium styling
            mention_name = member.first_name or "User"
            mention_text = f"@{member.username}" if member.username else mention_name
            styled_mention = font_style["func"](mention_text)
            mentions.append(f"[{styled_mention}](tg://user?id={member.id})")
        
        # Format complete message
        tagall_lines = [
            f"{emoji_frame} {bold('VZOEL TAGALL SYSTEM')}",
            "",
            f"{emoji('telegram')} **Message:** {styled_message}",
            "",
            f"{emoji('centang')} **Tagged Members:**"
        ]
        
        # Add mentions
        for mention in mentions:
            tagall_lines.append(f"  • {mention}")
        
        tagall_lines.extend([
            "",
            f"{emoji('aktif')} **Style:** {font_style['name'].title()}",
            f"{emoji('loading')} **Auto-updating every {self.edit_interval}s**",
            "",
            f"{italic('Premium TagAll by Vzoel VZLfxs @Lutpan')}"
        ])
        
        return "\n".join(tagall_lines)
    
    async def start_tagall_session(self, client: VzoelClient, message: Message, 
                                 base_message: str, members: List[User]) -> None:
        """Start premium tagall session dengan emoji rotation"""
        
        # Create session ID
        session_id = f"tagall_{message.chat.id}_{message.id}"
        
        # Create member batches
        member_batches = self.create_member_batches(members)
        
        if not member_batches:
            await message.reply_text(
                f"{emoji('merah')} {bold('No members to tag!')}\\n\\n"
                f"{emoji('kuning')} Possible reasons:\\n"
                f"• Group has no active members\\n"
                f"• Bot lacks permission to view members\\n"
                f"• All members are bots or deleted accounts",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Mark session as active
        self.active_sessions[session_id] = True
        
        try:
            # Process each batch
            for batch_index, member_batch in enumerate(member_batches):
                
                # Check if session is still active
                if not self.active_sessions.get(session_id, False):
                    break
                
                # Send initial message untuk batch ini
                initial_emoji = self.tagall_emoji_frames[0]
                initial_style = self.font_styles[0]
                
                initial_message = self.format_tagall_message(
                    base_message, member_batch, initial_emoji, initial_style
                )
                
                batch_msg = await message.reply_text(
                    initial_message,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Start emoji rotation untuk batch ini
                asyncio.create_task(
                    self.rotate_batch_message(
                        batch_msg, base_message, member_batch, session_id
                    )
                )
                
                # Wait before next batch (if not last batch)
                if batch_index < len(member_batches) - 1:
                    await asyncio.sleep(2.0)
            
            # Log completion
            LOGGER.info(f"TagAll session started: {len(member_batches)} batches, {len(members)} total members")
            
            # Send completion notification
            completion_msg = [
                f"{emoji('centang')} {bold('TagAll Session Active!')}",
                "",
                f"{emoji('utama')} **Total Batches:** {len(member_batches)}",
                f"{emoji('aktif')} **Total Members:** {len(members)}",
                f"{emoji('loading')} **Update Interval:** {self.edit_interval}s",
                "",
                f"{emoji('merah')} **Stop:** Use {monospace('.stop')} command",
                "",
                f"{italic('Premium rotation activated!')}"
            ]
            
            await message.reply_text(
                "\\n".join(completion_msg),
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            LOGGER.error(f"Error in tagall session: {e}")
            self.active_sessions[session_id] = False
    
    async def rotate_batch_message(self, message: Message, base_message: str, 
                                 members: List[User], session_id: str) -> None:
        """Rotate emoji dan font style untuk satu batch message"""
        
        emoji_index = 0
        style_index = 0
        
        try:
            while self.active_sessions.get(session_id, False):
                
                # Get current emoji dan style
                current_emoji = self.tagall_emoji_frames[emoji_index % len(self.tagall_emoji_frames)]
                current_style = self.font_styles[style_index % len(self.font_styles)]
                
                # Format message dengan current styling
                rotated_message = self.format_tagall_message(
                    base_message, members, current_emoji, current_style
                )
                
                try:
                    await message.edit_text(
                        rotated_message,
                        parse_mode=ParseMode.MARKDOWN
                    )
                except MessageNotModified:
                    pass
                except Exception as e:
                    LOGGER.warning(f"Error editing tagall message: {e}")
                    break
                
                # Wait for next rotation
                await asyncio.sleep(self.edit_interval)
                
                # Advance indices
                emoji_index += 1
                if emoji_index % len(self.tagall_emoji_frames) == 0:
                    style_index += 1
                    
        except Exception as e:
            LOGGER.error(f"Error in message rotation: {e}")
        finally:
            # Ensure session cleanup
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    def stop_all_sessions(self) -> int:
        """Stop all active tagall sessions"""
        stopped_count = len(self.active_sessions)
        
        # Stop all sessions
        for session_id in list(self.active_sessions.keys()):
            self.active_sessions[session_id] = False
            del self.active_sessions[session_id]
        
        return stopped_count

# Initialize premium tagall system
tagall_system = PremiumTagAllSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def tagall_router(client: VzoelClient, message: Message):
    """Router untuk tagall commands"""
    command = get_command(message)
    
    if command == "tagall":
        await tagall_handler(client, message)
    elif command == "stop":
        await stop_tagall_handler(client, message)

async def tagall_handler(client: VzoelClient, message: Message):
    """
    Premium TagAll Handler
    Usage: .tagall (message) atau .tagall dengan reply
    Features: 5 mentions per batch, 4s rotation, premium emoji mapping
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{emoji('merah')} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} TagAll only works in groups and supergroups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get message content
    args = get_arguments(message)
    reply_message = message.reply_to_message
    base_message = ""
    
    if args:
        # Use provided message
        base_message = args
    elif reply_message:
        # Use replied message
        if reply_message.text:
            base_message = reply_message.text
        elif reply_message.caption:
            base_message = reply_message.caption
        else:
            base_message = "📱 Media message"
    else:
        # No message provided
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{emoji('telegram')} {bold('PREMIUM TAGALL SYSTEM')}",
            "",
            f"{emoji('merah')} **No message specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.tagall your message here')}",
            f"  • Reply to message + {monospace('.tagall')}",
            "",
            f"{emoji('centang')} **Features:**",
            f"  • 5 mentions per batch message",
            f"  • 4-second emoji rotation",
            f"  • Premium font styling",
            f"  • Auto member collection",
            "",
            f"{emoji('loading')} **Stop:** {monospace('.stop')}",
            "",
            f"{italic('Enhanced TagAll by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show collection progress
    collection_msg = await message.reply_text(
        f"{emoji('loading')} {bold('Collecting group members...')}\\n"
        f"{emoji('proses')} Please wait...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Collect group members
    members = await tagall_system.collect_group_members(client, message.chat.id)
    
    if not members:
        await collection_msg.edit_text(
            f"{emoji('merah')} {bold('Member Collection Failed!')}\\n\\n"
            f"{emoji('kuning')} Unable to collect group members.\\n"
            f"Make sure bot has admin permissions.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Update collection status
    await collection_msg.edit_text(
        f"{emoji('centang')} {bold('Members Collected!')}\\n"
        f"{emoji('aktif')} Found {bold(str(len(members)))} taggable members\\n"
        f"{emoji('loading')} Starting TagAll session...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Start tagall session
    await tagall_system.start_tagall_session(client, message, base_message, members)
    
    # Clean up collection message
    await collection_msg.delete()

async def stop_tagall_handler(client: VzoelClient, message: Message):
    """Stop all active tagall sessions"""
    
    stopped_count = tagall_system.stop_all_sessions()
    
    if stopped_count > 0:
        stop_message = [
            f"{emoji('centang')} {bold('TagAll Sessions Stopped!')}",
            "",
            f"{emoji('merah')} **Stopped:** {stopped_count} active sessions",
            f"{emoji('aktif')} **Status:** All rotations terminated",
            "",
            f"{emoji('telegram')} **Restart:** Use {monospace('.tagall message')}",
            "",
            f"{italic('TagAll system halted by Vzoel VZLfxs @Lutpan')}"
        ]
    else:
        stop_message = [
            f"{emoji('kuning')} {bold('No Active Sessions')}",
            "",
            f"{emoji('proses')} **Status:** No TagAll sessions running",
            f"{emoji('telegram')} **Start:** Use {monospace('.tagall message')}",
            "",
            f"{italic('TagAll system ready by Vzoel VZLfxs @Lutpan')}"
        ]
    
    await message.reply_text(
        "\n".join(stop_message),
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info(f"Stopped {stopped_count} TagAll sessions")

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium TagAll System initialized")