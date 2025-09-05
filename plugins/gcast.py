#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Gcast System
Enhanced broadcast system with premium emoji mapping, animated progress, and unlimited features
Created by: Vzoel Fox's
"""

import asyncio
import aiosqlite
import time
import re
from typing import List, Optional, Tuple
from pyrogram.types import Message
from pyrogram.enums import ChatType, ParseMode
from pyrogram.errors import (
    FloodWait, UserIsBlocked, ChatAdminRequired, MessageNotModified,
    ChatWriteForbidden, PeerIdInvalid, MessageEmpty
)

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

# Database path for broadcast chats
DB_PATH = "broadcast_chats.db"

class PremiumGcastSystem:
    """Premium Gcast System dengan fitur lengkap"""
    
    def __init__(self):
        self.animation_frames = [
            "⚡", "🔥", "💫", "✨", "⭐", "🌟", "💥", "🚀"
        ]
        self.progress_chars = ["▱", "▰"]
        
    async def init_db(self):
        """Initialize broadcast database dengan premium structure"""
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY,
                    chat_type TEXT,
                    chat_title TEXT,
                    member_count INTEGER,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            await db.commit()
            LOGGER.info(f"{emoji('centang')} Gcast database initialized")
    
    def process_premium_message(self, text: str, enable_premium_emoji: bool = True) -> str:
        """
        Premium message processor dengan unlimited emoji support
        Supports:
        - Font styling (-bold, -italic, -monospace)
        - Premium emoji mapping (:emoji_key:)
        - Unlimited custom emojis
        - Bug-free text formatting
        """
        if not text:
            return ""
        
        processed_text = text
        style_applied = None
        
        # 1. FONT STYLING DETECTION & APPLICATION
        font_patterns = {
            "-bold": "bold",
            "-italic": "italic", 
            "-monospace": "monospace"
        }
        
        for pattern, style in font_patterns.items():
            if pattern in processed_text:
                processed_text = processed_text.replace(pattern, "").strip()
                style_applied = style
                break
        
        # Apply font styling using premium assets (bug-free)
        if style_applied:
            if style_applied == "bold":
                processed_text = bold(processed_text)
            elif style_applied == "italic":
                processed_text = italic(processed_text)
            elif style_applied == "monospace":
                processed_text = monospace(processed_text)
        
        # 2. PREMIUM EMOJI MAPPING
        if enable_premium_emoji:
            # Process mapped emojis first (:emoji_key:)
            available_emojis = vzoel_assets.emojis.get("emojis", {})
            for emoji_key, emoji_data in available_emojis.items():
                shortcode = f":{emoji_key}:"
                if shortcode in processed_text:
                    premium_emoji_char = premium_emoji(emoji_key)
                    if premium_emoji_char:
                        processed_text = processed_text.replace(shortcode, premium_emoji_char)
                    else:
                        # Fallback to standard emoji
                        standard_emoji_char = vzoel_assets.get_emoji(emoji_key)
                        processed_text = processed_text.replace(shortcode, standard_emoji_char)
            
            # 3. UNLIMITED EMOJI SUPPORT
            # Support for any emoji format including Unicode, custom, etc.
            # This preserves all emojis that are not in the mapping
            # No processing needed - just pass through
        
        return processed_text
    
    async def get_active_chats(self, exclude_blacklist: bool = True) -> List[Tuple[int, str]]:
        """Get active chats for broadcasting dengan blacklist filtering"""
        active_chats = []
        blacklist = CONFIG.blacklist.groups if exclude_blacklist else []
        
        async with aiosqlite.connect(DB_PATH) as db:
            query = "SELECT chat_id, chat_title FROM chats WHERE is_active = 1"
            async with db.execute(query) as cursor:
                async for row in cursor:
                    chat_id, chat_title = row
                    if chat_id not in blacklist:
                        active_chats.append((chat_id, chat_title or f"Group {chat_id}"))
        
        return active_chats
    
    async def animate_startup_sequence(self, message: Message) -> Message:
        """Premium animated startup sequence"""
        startup_frames = [
            f"{emoji('loading')} {bold('Initializing Premium Gcast...')}",
            f"{emoji('proses')} {bold('Loading chat database...')}",
            f"{emoji('telegram')} {bold('Checking blacklist configuration...')}",
            f"{emoji('aktif')} {bold('Preparing broadcast system...')}",
            f"{emoji('petir')} {bold('Ready to broadcast!')}"
        ]
        
        progress_msg = await message.reply_text(startup_frames[0], parse_mode=ParseMode.MARKDOWN)
        
        for frame in startup_frames[1:]:
            await asyncio.sleep(0.7)
            try:
                await progress_msg.edit_text(frame, parse_mode=ParseMode.MARKDOWN)
            except MessageNotModified:
                pass
        
        return progress_msg
    
    async def create_progress_animation(self, current: int, total: int, success: int, failed: int, 
                                      elapsed_time: int) -> str:
        """Create animated progress display dengan premium styling"""
        
        # Progress bar calculation
        if total > 0:
            progress_percentage = (current / total) * 100
            filled_chars = int((current / total) * 20)
            progress_bar = "▰" * filled_chars + "▱" * (20 - filled_chars)
        else:
            progress_percentage = 0
            progress_bar = "▱" * 20
        
        # Animation frame
        animation_char = self.animation_frames[current % len(self.animation_frames)]
        
        # Status message
        status_lines = [
            f"{animation_char} {bold('PREMIUM GCAST ACTIVE')}",
            "",
            f"**Progress:** `[{progress_bar}]` {progress_percentage:.1f}%",
            "",
            f"{emoji('centang')} **Success:** `{success}`",
            f"{emoji('merah')} **Failed:** `{failed}`", 
            f"{emoji('telegram')} **Remaining:** `{total - current}`",
            f"{emoji('aktif')} **Elapsed:** `{elapsed_time}s`",
            "",
            f"{italic('Broadcasting with premium quality...')}"
        ]
        
        return "\n".join(status_lines)
    
    async def broadcast_message(self, client: VzoelClient, chat_id: int, message_text: str = None, 
                              reply_message: Message = None) -> bool:
        """Send message to specific chat dengan error handling"""
        try:
            if reply_message:
                # Copy reply message (preserves all formatting, media, etc.)
                await reply_message.copy(chat_id)
            elif message_text:
                # Send processed text message
                await client.send_message(
                    chat_id, 
                    message_text, 
                    parse_mode=ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
            else:
                return False
            
            return True
            
        except FloodWait as e:
            LOGGER.warning(f"FloodWait for chat {chat_id}: {e.value} seconds")
            await asyncio.sleep(e.value)
            return False
            
        except (UserIsBlocked, ChatAdminRequired, ChatWriteForbidden) as e:
            LOGGER.warning(f"Permission error for chat {chat_id}: {e}")
            return False
            
        except (PeerIdInvalid, MessageEmpty) as e:
            LOGGER.error(f"Invalid chat/message for {chat_id}: {e}")
            return False
            
        except Exception as e:
            LOGGER.error(f"Unexpected error broadcasting to {chat_id}: {e}")
            return False
    
    async def create_final_report(self, success: int, failed: int, total_time: int, 
                                blacklist_count: int) -> str:
        """Create premium final broadcast report"""
        signature = vzoel_signature()
        
        # Calculate statistics
        total_sent = success + failed
        success_rate = (success / total_sent * 100) if total_sent > 0 else 0
        avg_time_per_message = (total_time / total_sent) if total_sent > 0 else 0
        
        report_lines = [
            f"{signature}",
            "",
            f"{emoji('adder2')} {bold('GCAST COMPLETED')} {emoji('adder1')}",
            "",
            f"**📊 BROADCAST STATISTICS:**",
            f"{emoji('centang')} **Successful:** `{success}` messages",
            f"{emoji('merah')} **Failed:** `{failed}` messages", 
            f"{emoji('telegram')} **Success Rate:** `{success_rate:.1f}%`",
            f"{emoji('proses')} **Blacklisted:** `{blacklist_count}` chats skipped",
            "",
            f"**⏱️ TIME ANALYSIS:**",
            f"{emoji('aktif')} **Total Time:** `{total_time}s`",
            f"{emoji('loading')} **Avg per Message:** `{avg_time_per_message:.1f}s`",
            "",
            f"{emoji('utama')} **Quality:** Premium broadcast with zero bugs",
            f"{emoji('petir')} **Features:** Unlimited emoji + Premium styling",
            "",
            f"{italic('Enhanced by Vzoel Fox\\\'s Premium Collection')}"
        ]
        
        return "\n".join(report_lines)

# Initialize premium gcast system
gcast_system = PremiumGcastSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def gcast_router(client: VzoelClient, message: Message):
    """Router untuk semua gcast commands"""
    command = get_command(message)
    
    if command == "updatechats":
        await update_chats_handler(client, message)
    elif command == "gcast":
        await gcast_handler(client, message)
    elif command == "gcastinfo":
        await gcast_info_handler(client, message)

async def update_chats_handler(client: VzoelClient, message: Message):
    """Update chat database dengan premium progress tracking"""
    
    # Initialize database
    await gcast_system.init_db()
    
    # Start update process
    loading_msg = await message.reply_text(
        f"{emoji('loading')} {bold('Updating chat database...')}\n"
        f"{emoji('proses')} Scanning all dialogs...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    count = 0
    updated = 0
    start_time = time.time()
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Clear old data
        await db.execute("UPDATE chats SET is_active = 0")
        
        # Scan all dialogs
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                chat_id = dialog.chat.id
                chat_title = dialog.chat.title or f"Group {chat_id}"
                member_count = getattr(dialog.chat, 'members_count', 0)
                
                # Insert or update
                await db.execute("""
                    INSERT OR REPLACE INTO chats 
                    (chat_id, chat_type, chat_title, member_count, is_active) 
                    VALUES (?, ?, ?, ?, 1)
                """, (chat_id, dialog.chat.type.name, chat_title, member_count))
                
                count += 1
                
                # Update progress every 10 chats
                if count % 10 == 0:
                    try:
                        await loading_msg.edit_text(
                            f"{emoji('aktif')} {bold('Scanning chats...')}\n"
                            f"{emoji('telegram')} Found: `{count}` groups\n"
                            f"{emoji('proses')} Processing...",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except MessageNotModified:
                        pass
        
        await db.commit()
    
    # Final report
    end_time = time.time()
    elapsed = int(end_time - start_time)
    
    final_message = [
        f"{emoji('centang')} {bold('Database Update Complete!')}",
        "",
        f"{emoji('telegram')} **Total Groups:** `{count}`",
        f"{emoji('aktif')} **Active Chats:** `{count}`",
        f"{emoji('loading')} **Processing Time:** `{elapsed}s`",
        "",
        f"{emoji('utama')} Ready for premium gcast!"
    ]
    
    await loading_msg.edit_text("\n".join(final_message), parse_mode=ParseMode.MARKDOWN)

async def gcast_handler(client: VzoelClient, message: Message):
    """
    Premium Gcast Handler dengan fitur lengkap:
    - Support .gcast <pesan> dan .gcast (reply)
    - Premium emoji mapping unlimited
    - Animated progress dengan premium styling
    - Blacklist checking dari config
    - Bug-free font rendering
    """
    
    args = get_arguments(message)
    reply_message = message.reply_to_message
    
    # Validation: harus ada pesan atau reply
    if not args and not reply_message:
        usage_text = [
            f"{vzoel_signature()}",
            "",
            f"{emoji('telegram')} {bold('PREMIUM GCAST SYSTEM')}",
            "",
            f"{emoji('utama')} **Usage Methods:**",
            f"  • {monospace('.gcast <message>')} - Send text message", 
            f"  • {monospace('.gcast')} - Reply to message to forward it",
            "",
            f"{emoji('petir')} **Premium Features:**",
            f"  • Font styling: {monospace('-bold')}, {monospace('-italic')}, {monospace('-monospace')}",
            f"  • Emoji mapping: {monospace(':utama:')}, {monospace(':telegram:')}, etc.",
            f"  • Unlimited emoji support (any Unicode emoji)",
            f"  • Animated progress tracking",
            f"  • Smart blacklist filtering",
            "",
            f"{emoji('centang')} **Examples:**",
            f"  • {monospace('.gcast -bold Hello World! :utama:')}",
            f"  • {monospace('.gcast Check this out! 🚀💫⭐')}", 
            f"  • Reply to any message + {monospace('.gcast')}",
            "",
            f"{italic('Enhanced with premium quality & zero bugs')}"
        ]
        
        await message.reply_text("\n".join(usage_text), parse_mode=ParseMode.MARKDOWN)
        return
    
    # Initialize database if needed
    await gcast_system.init_db()
    
    # Get active chats (excluding blacklist)
    active_chats = await gcast_system.get_active_chats(exclude_blacklist=True)
    blacklist_count = len(CONFIG.blacklist.groups)
    
    if not active_chats:
        error_msg = [
            f"{emoji('merah')} {bold('No Active Chats Found!')}",
            "",
            f"{emoji('kuning')} **Possible Reasons:**",
            f"  • Database is empty - run {monospace('.updatechats')} first",
            f"  • All chats are blacklisted",
            f"  • No group/supergroup permissions",
            "",
            f"{emoji('proses')} **Blacklisted Chats:** `{blacklist_count}`"
        ]
        
        await message.reply_text("\n".join(error_msg), parse_mode=ParseMode.MARKDOWN)
        return
    
    # Start animated sequence
    progress_msg = await gcast_system.animate_startup_sequence(message)
    await asyncio.sleep(1)
    
    # Prepare message content
    if args:
        # Process text message dengan premium features
        processed_message = gcast_system.process_premium_message(args, enable_premium_emoji=True)
        broadcast_text = processed_message
        broadcast_reply = None
    else:
        # Use reply message
        broadcast_text = None
        broadcast_reply = reply_message
    
    # Start broadcasting dengan animated progress
    success_count = 0
    failed_count = 0
    start_time = time.time()
    
    for i, (chat_id, chat_title) in enumerate(active_chats, 1):
        # Broadcast message
        success = await gcast_system.broadcast_message(
            client, chat_id, broadcast_text, broadcast_reply
        )
        
        if success:
            success_count += 1
        else:
            failed_count += 1
        
        # Update progress setiap 3 pesan
        if i % 3 == 0 or i == len(active_chats):
            current_time = int(time.time() - start_time)
            progress_text = await gcast_system.create_progress_animation(
                current=i,
                total=len(active_chats), 
                success=success_count,
                failed=failed_count,
                elapsed_time=current_time
            )
            
            try:
                await progress_msg.edit_text(progress_text, parse_mode=ParseMode.MARKDOWN)
            except MessageNotModified:
                pass
        
        # Safe delay to avoid flood limits
        await asyncio.sleep(1.2)
    
    # Final report
    total_time = int(time.time() - start_time)
    final_report = await gcast_system.create_final_report(
        success=success_count,
        failed=failed_count, 
        total_time=total_time,
        blacklist_count=blacklist_count
    )
    
    await progress_msg.edit_text(final_report, parse_mode=ParseMode.MARKDOWN)

async def gcast_info_handler(client: VzoelClient, message: Message):
    """Display gcast system information"""
    
    # Get statistics
    active_chats = await gcast_system.get_active_chats(exclude_blacklist=False)
    blacklisted_chats = CONFIG.blacklist.groups
    available_chats = len([chat for chat in active_chats if chat[0] not in blacklisted_chats])
    
    # Get emoji info
    available_emojis = vzoel_assets.emojis.get("emojis", {})
    emoji_categories = vzoel_assets.emojis.get("categories", {})
    
    info_text = [
        f"{vzoel_signature()}",
        "",
        f"{emoji('telegram')} {bold('GCAST SYSTEM INFO')}",
        "",
        f"**📊 CHAT STATISTICS:**",
        f"{emoji('centang')} **Total Groups:** `{len(active_chats)}`",
        f"{emoji('aktif')} **Available for Gcast:** `{available_chats}`", 
        f"{emoji('merah')} **Blacklisted:** `{len(blacklisted_chats)}`",
        "",
        f"**🎨 PREMIUM FEATURES:**",
        f"{emoji('utama')} **Mapped Emojis:** `{len(available_emojis)}` premium emojis",
        f"{emoji('adder2')} **Emoji Categories:** `{len(emoji_categories)}` categories",
        f"{emoji('petir')} **Font Styles:** Bold, Italic, Monospace",
        f"{emoji('proses')} **Unlimited Emojis:** Full Unicode support",
        "",
        f"**⚙️ SYSTEM STATUS:**",
        f"{emoji('loading')} **Database:** `{DB_PATH}`",
        f"{emoji('kuning')} **Animation Frames:** `{len(gcast_system.animation_frames)}`",
        f"{emoji('biru')} **Progress Tracking:** Real-time updates",
        "",
        f"{italic('Premium broadcast system by Vzoel Fox')}"
    ]
    
    await message.reply_text("\n".join(info_text), parse_mode=ParseMode.MARKDOWN)

# Initialize database on module load
# Note: Database initialization is handled in each command that needs it
LOGGER.info(f"{emoji('centang')} Premium Gcast system initialized")