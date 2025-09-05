#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium CheckID System
Advanced ID checker with animated processing, premium emoji mapping, and unlimited loop animations
Created by: VZLfxs @Lutpan
"""

import asyncio
import re
from typing import Optional, Dict, Any
from pyrogram.types import Message, User
from pyrogram.enums import ParseMode
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, PeerIdInvalid, MessageNotModified

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumCheckIDSystem:
    """Premium CheckID System dengan unlimited animations"""
    
    def __init__(self):
        # Animation frames untuk processing
        self.processing_frames = [
            "🔍", "🔎", "📡", "⚡", "💫", "⭐", "🌟", "✨", "💥", "🚀"
        ]
        
        # Loop animation frames untuk hasil
        self.result_loop_frames = [
            {"emoji": "🎯", "style": "bold", "color": "primary"},
            {"emoji": "📋", "style": "italic", "color": "info"},
            {"emoji": "👤", "style": "monospace", "color": "user"},
            {"emoji": "🆔", "style": "bold", "color": "accent"},
            {"emoji": "💎", "style": "italic", "color": "premium"},
            {"emoji": "⚡", "style": "bold", "color": "energy"},
            {"emoji": "🌟", "style": "monospace", "color": "star"},
            {"emoji": "🔥", "style": "italic", "color": "fire"}
        ]
        
        # Premium styling colors
        self.style_colors = {
            "primary": "🤩",    # utama
            "info": "ℹ️",       # telegram  
            "user": "👤",       # centang
            "accent": "⛈",      # petir
            "premium": "💟",    # adder2
            "energy": "⚡",     # aktif
            "star": "🌟",       # kuning
            "fire": "🔥"        # merah
        }
        
        # Control variables
        self.active_loops = {}
        
    def extract_username_from_text(self, text: str) -> Optional[str]:
        """Extract username dari text dengan berbagai format"""
        if not text:
            return None
        
        # Remove common prefixes
        text = text.strip()
        
        # Pattern untuk username
        patterns = [
            r'@([a-zA-Z0-9_]{5,32})',           # @username
            r'https?://t\.me/([a-zA-Z0-9_]{5,32})',  # t.me/username
            r'([a-zA-Z0-9_]{5,32})'             # username tanpa @
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                username = match.group(1)
                # Validasi username format
                if re.match(r'^[a-zA-Z0-9_]{5,32}$', username):
                    return username
        
        return None
    
    def format_user_info(self, user: User, frame_data: Dict[str, str]) -> str:
        """Format user information dengan premium styling"""
        
        # Get frame styling
        frame_emoji = frame_data["emoji"]
        style = frame_data["style"]
        color_key = frame_data["color"]
        
        # Apply premium font styling
        if style == "bold":
            name_formatted = bold(user.first_name or "Unknown")
            username_formatted = bold(f"@{user.username}" if user.username else "No username")
        elif style == "italic":
            name_formatted = italic(user.first_name or "Unknown")
            username_formatted = italic(f"@{user.username}" if user.username else "No username")
        elif style == "monospace":
            name_formatted = monospace(user.first_name or "Unknown")
            username_formatted = monospace(f"@{user.username}" if user.username else "No username")
        else:
            name_formatted = user.first_name or "Unknown"
            username_formatted = f"@{user.username}" if user.username else "No username"
        
        # Premium emoji mapping
        id_emoji = emoji("loading")  # ⚙️
        user_emoji = emoji("centang")  # 👍
        name_emoji = emoji("utama")   # 🤩
        
        # Format dengan premium styling
        info_lines = [
            f"{frame_emoji} {bold('USER INFORMATION')}",
            "",
            f"{id_emoji} **User ID:** `{user.id}`",
            f"{user_emoji} **Username:** {username_formatted}",
            f"{name_emoji} **Name:** {name_formatted}",
            "",
            f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
        ]
        
        return "\n".join(info_lines)
    
    async def animate_processing(self, message: Message, target_info: str) -> Message:
        """Animate processing sequence dengan premium styling"""
        
        processing_stages = [
            f"{emoji('loading')} {bold('Initializing Premium CheckID...')}",
            f"{emoji('proses')} {bold('Scanning user database...')}",
            f"{emoji('telegram')} {bold('Resolving target:')} {monospace(target_info)}",
            f"{emoji('aktif')} {bold('Processing user information...')}",
            f"{emoji('petir')} {bold('Preparing premium display...')}"
        ]
        
        # Start processing animation
        progress_msg = await message.reply_text(
            processing_stages[0], 
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Animate through processing stages
        for i, stage in enumerate(processing_stages[1:], 1):
            await asyncio.sleep(0.8)
            
            # Add processing frame animation
            frame_emoji = self.processing_frames[i % len(self.processing_frames)]
            animated_stage = f"{frame_emoji} {stage}"
            
            try:
                await progress_msg.edit_text(
                    animated_stage,
                    parse_mode=ParseMode.MARKDOWN
                )
            except MessageNotModified:
                pass
        
        return progress_msg
    
    async def start_unlimited_loop_animation(self, message: Message, user: User, 
                                           loop_id: str) -> None:
        """Start unlimited loop animation untuk hasil dengan 2 detik interval"""
        
        self.active_loops[loop_id] = True
        frame_index = 0
        
        try:
            while self.active_loops.get(loop_id, False):
                # Get current frame data
                frame_data = self.result_loop_frames[frame_index % len(self.result_loop_frames)]
                
                # Format user info dengan current frame
                formatted_info = self.format_user_info(user, frame_data)
                
                try:
                    await message.edit_text(
                        formatted_info,
                        parse_mode=ParseMode.MARKDOWN
                    )
                except MessageNotModified:
                    pass
                except Exception as e:
                    LOGGER.error(f"Error in loop animation: {e}")
                    # Stop animation jika ada error
                    self.active_loops[loop_id] = False
                    break
                
                # Wait 2 seconds before next frame
                await asyncio.sleep(2.0)
                frame_index += 1
                
        except Exception as e:
            LOGGER.error(f"Critical error in unlimited loop: {e}")
            self.active_loops[loop_id] = False
    
    def stop_loop_animation(self, loop_id: str) -> None:
        """Stop loop animation"""
        if loop_id in self.active_loops:
            self.active_loops[loop_id] = False
            del self.active_loops[loop_id]
    
    async def resolve_user_from_username(self, client: VzoelClient, username: str) -> Optional[User]:
        """Resolve user dari username"""
        try:
            # Get user info dari username
            user = await client.get_users(username)
            return user
        except (UsernameNotOccupied, UsernameInvalid, PeerIdInvalid) as e:
            LOGGER.warning(f"Username resolution failed for {username}: {e}")
            return None
        except Exception as e:
            LOGGER.error(f"Unexpected error resolving username {username}: {e}")
            return None
    
    async def resolve_user_from_reply(self, reply_message: Message) -> Optional[User]:
        """Resolve user dari reply message"""
        try:
            if reply_message and reply_message.from_user:
                return reply_message.from_user
            return None
        except Exception as e:
            LOGGER.error(f"Error resolving user from reply: {e}")
            return None

# Initialize premium checkid system
checkid_system = PremiumCheckIDSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def checkid_router(client: VzoelClient, message: Message):
    """Router untuk checkid commands"""
    command = get_command(message)
    
    if command == "id" or command == "checkid":
        await checkid_handler(client, message)
    elif command == "stopid":
        await stop_checkid_handler(client, message)

async def checkid_handler(client: VzoelClient, message: Message):
    """
    Premium CheckID Handler dengan fitur lengkap:
    - Support .id @username dan .id (reply)
    - Premium emoji mapping dengan bug-free fonts
    - Animated processing sequence
    - Unlimited loop animation untuk hasil
    - 2-second edit interval timing
    """
    
    args = get_arguments(message)
    reply_message = message.reply_to_message
    target_user = None
    target_info = ""
    
    # Determine target dari argument atau reply
    if args:
        # Extract username dari argument
        username = checkid_system.extract_username_from_text(args)
        if username:
            target_info = f"@{username}"
            # Start processing animation
            progress_msg = await checkid_system.animate_processing(message, target_info)
            
            # Resolve user dari username
            target_user = await checkid_system.resolve_user_from_username(client, username)
            
            if not target_user:
                error_text = [
                    f"{emoji('merah')} {bold('User Not Found!')}",
                    "",
                    f"{emoji('kuning')} **Searched:** {monospace(target_info)}",
                    f"{emoji('proses')} **Possible Issues:**",
                    f"  • Username doesn't exist",
                    f"  • User has privacy restrictions",
                    f"  • Invalid username format",
                    "",
                    f"{emoji('telegram')} **Try:**",
                    f"  • {monospace('.id @validusername')}",
                    f"  • Reply to user's message + {monospace('.id')}",
                    "",
                    f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
                ]
                
                await progress_msg.edit_text(
                    "\n".join(error_text),
                    parse_mode=ParseMode.MARKDOWN
                )
                return
        else:
            # Invalid argument format
            usage_text = [
                f"{vzoel_signature()}",
                "",
                f"{emoji('telegram')} {bold('PREMIUM CHECKID SYSTEM')}",
                "",
                f"{emoji('utama')} **Usage Methods:**",
                f"  • {monospace('.id @username')} - Check user by username",
                f"  • {monospace('.id')} - Reply to message to check sender",
                f"  • {monospace('.checkid @username')} - Alternative command",
                "",
                f"{emoji('petir')} **Premium Features:**",
                f"  • Animated processing sequence",
                f"  • Premium emoji mapping with bug-free fonts",
                f"  • Unlimited loop animations for results",
                f"  • 2-second edit timing for smooth experience",
                f"  • Smart username resolution",
                "",
                f"{emoji('centang')} **Examples:**",
                f"  • {monospace('.id @telegram')}",
                f"  • {monospace('.id durov')}",
                f"  • Reply to any message + {monospace('.id')}",
                "",
                f"{emoji('loading')} **Stop Animation:** {monospace('.stopid')}",
                "",
                f"{italic('Enhanced with premium quality & zero bugs')}"
            ]
            
            await message.reply_text(
                "\n".join(usage_text),
                parse_mode=ParseMode.MARKDOWN
            )
            return
    
    elif reply_message:
        # Get user dari reply message
        target_info = "replied message"
        # Start processing animation
        progress_msg = await checkid_system.animate_processing(message, target_info)
        
        target_user = await checkid_system.resolve_user_from_reply(reply_message)
        
        if not target_user:
            error_text = [
                f"{emoji('merah')} {bold('Reply Target Invalid!')}",
                "",
                f"{emoji('kuning')} **Issue:** Cannot resolve user from reply",
                f"{emoji('proses')} **Possible Causes:**",
                f"  • Message is from channel/anonymous",
                f"  • User information unavailable",
                f"  • System/service message",
                "",
                f"{emoji('telegram')} **Alternative:** Use {monospace('.id @username')}",
                "",
                f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
            ]
            
            await progress_msg.edit_text(
                "\n".join(error_text),
                parse_mode=ParseMode.MARKDOWN
            )
            return
    else:
        # No target provided
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{emoji('telegram')} {bold('PREMIUM CHECKID SYSTEM')}",
            "",
            f"{emoji('merah')} **No Target Specified!**",
            "",
            f"{emoji('utama')} **Usage:**",
            f"  • {monospace('.id @username')} - Check by username",
            f"  • {monospace('.id')} - Reply to message first",
            "",
            f"{emoji('centang')} **Examples:**",
            f"  • {monospace('.id @telegram')}",
            f"  • Reply to message + {monospace('.id')}",
            "",
            f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await message.reply_text(
            "\n".join(usage_text),
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Success! Start unlimited loop animation
    if target_user:
        # Create unique loop ID
        loop_id = f"checkid_{message.chat.id}_{message.id}"
        
        # Start unlimited loop animation (2-second intervals)
        asyncio.create_task(
            checkid_system.start_unlimited_loop_animation(
                progress_msg, target_user, loop_id
            )
        )
        
        LOGGER.info(f"Started unlimited CheckID loop animation for user {target_user.id}")

async def stop_checkid_handler(client: VzoelClient, message: Message):
    """Stop all active CheckID loop animations"""
    
    stopped_count = 0
    
    # Stop all active loops
    for loop_id in list(checkid_system.active_loops.keys()):
        checkid_system.stop_loop_animation(loop_id)
        stopped_count += 1
    
    if stopped_count > 0:
        stop_message = [
            f"{emoji('centang')} {bold('CheckID Animations Stopped!')}",
            "",
            f"{emoji('loading')} **Stopped:** `{stopped_count}` active animations",
            f"{emoji('aktif')} **Status:** All loops terminated",
            "",
            f"{emoji('telegram')} **Restart:** Use {monospace('.id @username')} again",
            "",
            f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
        ]
    else:
        stop_message = [
            f"{emoji('kuning')} {bold('No Active Animations')}",
            "",
            f"{emoji('proses')} **Status:** No CheckID loops running",
            f"{emoji('telegram')} **Start:** Use {monospace('.id @username')}",
            "",
            f"{italic('Premium CheckID by Vzoel VZLfxs @Lutpan')}"
        ]
    
    await message.reply_text(
        "\n".join(stop_message),
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info(f"Stopped {stopped_count} CheckID loop animations")

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium CheckID system initialized")