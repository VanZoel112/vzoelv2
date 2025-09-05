#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Voice Chat System
Advanced voice chat controls with duration monitoring and premium emoji mapping
Created by: Vzoel Fox's
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageNotModified, FloodWait
from pyrogram.raw import functions, types

# Import sistem terintegrasi premium
from helper_client import VzoelClient, is_user_mode, get_client_type
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumVoiceChatSystem:
    """Premium Voice Chat System dengan duration monitoring"""
    
    def __init__(self):
        # VC monitoring sessions
        self.active_vc_sessions = {}
        self.vc_start_times = {}
        
        # Duration update interval (30 seconds)
        self.update_interval = 30.0
        
        # Premium emoji hanya dari mapping
        self.vc_status_emoji = {
            "joining": emoji("loading"),    # ⚙️
            "joined": emoji("centang"),     # 👍  
            "active": emoji("aktif"),       # ⚡
            "speaking": emoji("utama"),     # 🤩
            "muted": emoji("kuning"),       # 🌟
            "leaving": emoji("proses"),     # 🔄
            "left": emoji("merah"),         # 🔥
            "error": emoji("petir")         # ⛈
        }
        
    def format_duration(self, seconds: int) -> str:
        """Format duration ke human readable format"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    async def join_voice_chat(self, client: VzoelClient, chat_id: int) -> bool:
        """Join voice chat dengan proper handling"""
        try:
            # Join voice chat using raw API
            result = await client.invoke(
                functions.phone.JoinGroupCall(
                    call=types.InputGroupCall(
                        id=0,  # Will be resolved by Telegram
                        access_hash=0
                    ),
                    join_as=types.InputPeerSelf(),
                    muted=False,
                    video_stopped=True,
                    params=types.DataJSON(data="{}")
                )
            )
            
            return True
            
        except Exception as e:
            LOGGER.error(f"Error joining VC: {e}")
            return False
    
    async def leave_voice_chat(self, client: VzoelClient, chat_id: int) -> bool:
        """Leave voice chat dengan proper handling"""
        try:
            # Leave voice chat using raw API
            result = await client.invoke(
                functions.phone.LeaveGroupCall(
                    call=types.InputGroupCall(
                        id=0,
                        access_hash=0
                    ),
                    source=0
                )
            )
            
            return True
            
        except Exception as e:
            LOGGER.error(f"Error leaving VC: {e}")
            return False
    
    async def start_voice_chat(self, client: VzoelClient, chat_id: int) -> bool:
        """Start voice chat di group"""
        try:
            # Start voice chat using raw API
            result = await client.invoke(
                functions.phone.CreateGroupCall(
                    peer=await client.resolve_peer(chat_id),
                    random_id=client.rnd_id(),
                    title="VZOEL Voice Chat",
                    schedule_date=None
                )
            )
            
            return True
            
        except Exception as e:
            LOGGER.error(f"Error starting VC: {e}")
            return False
    
    async def stop_voice_chat(self, client: VzoelClient, chat_id: int) -> bool:
        """Stop voice chat di group"""
        try:
            # Discard voice chat using raw API
            result = await client.invoke(
                functions.phone.DiscardGroupCall(
                    call=types.InputGroupCall(
                        id=0,
                        access_hash=0
                    )
                )
            )
            
            return True
            
        except Exception as e:
            LOGGER.error(f"Error stopping VC: {e}")
            return False
    
    def create_vc_status_message(self, status: str, chat_title: str, 
                               duration: Optional[int] = None) -> str:
        """Create VC status message dengan premium emoji"""
        
        status_emoji = self.vc_status_emoji.get(status, emoji("loading"))
        
        # Base message lines
        status_lines = [
            f"{status_emoji} {bold('VZOEL VOICE CHAT')}",
            "",
            f"{emoji('telegram')} **Chat:** {monospace(chat_title)}",
            f"{emoji('proses')} **Status:** {bold(status.upper())}"
        ]
        
        # Add duration if available
        if duration is not None:
            duration_text = self.format_duration(duration)
            status_lines.append(f"{emoji('aktif')} **Duration:** {bold(duration_text)}")
        
        # Add timestamp
        current_time = datetime.now().strftime("%H:%M:%S")
        status_lines.extend([
            f"{emoji('kuning')} **Time:** {monospace(current_time)}",
            "",
            f"{italic('Premium VC by Vzoel VZLfxs @Lutpan')}"
        ])
        
        return "\n".join(status_lines)
    
    async def start_vc_monitoring(self, client: VzoelClient, chat_id: int, 
                                status_message: Message) -> None:
        """Start VC duration monitoring"""
        
        session_id = f"vc_monitor_{chat_id}"
        self.active_vc_sessions[session_id] = True
        self.vc_start_times[session_id] = time.time()
        
        try:
            # Get chat info
            chat = await client.get_chat(chat_id)
            chat_title = chat.title or "Unknown Chat"
            
            while self.active_vc_sessions.get(session_id, False):
                
                # Calculate duration
                current_time = time.time()
                duration = int(current_time - self.vc_start_times[session_id])
                
                # Update status message
                updated_message = self.create_vc_status_message(
                    "active", chat_title, duration
                )
                
                try:
                    await status_message.edit_text(
                        updated_message,
                        parse_mode=ParseMode.MARKDOWN
                    )
                except MessageNotModified:
                    pass
                except Exception as e:
                    LOGGER.warning(f"Error updating VC status: {e}")
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
                
        except Exception as e:
            LOGGER.error(f"Error in VC monitoring: {e}")
        finally:
            # Cleanup session
            if session_id in self.active_vc_sessions:
                del self.active_vc_sessions[session_id]
            if session_id in self.vc_start_times:
                del self.vc_start_times[session_id]
    
    def stop_vc_monitoring(self, chat_id: int) -> bool:
        """Stop VC monitoring untuk specific chat"""
        session_id = f"vc_monitor_{chat_id}"
        
        if session_id in self.active_vc_sessions:
            self.active_vc_sessions[session_id] = False
            return True
        
        return False

# Initialize premium VC system
vc_system = PremiumVoiceChatSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def vc_router(client: VzoelClient, message: Message):
    """Router untuk voice chat commands"""
    command = get_command(message)
    
    if command == "joinvc":
        await joinvc_handler(client, message)
    elif command == "leavevc":
        await leavevc_handler(client, message)
    elif command == "startvc":
        await startvc_handler(client, message)
    elif command == "stopvc":
        await stopvc_handler(client, message)

async def joinvc_handler(client: VzoelClient, message: Message):
    """
    Join voice chat handler
    Usage: .joinvc
    Works for both user and bot mode
    """
    
    # Check if in group
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply_text(
            f"{emoji('merah')} {bold('Group Only!')}\\n\\n"
            f"{emoji('kuning')} Voice chat commands only work in groups.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show joining status
    joining_msg = await message.reply_text(
        vc_system.create_vc_status_message("joining", message.chat.title or "Group"),
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Attempt to join VC
    success = await vc_system.join_voice_chat(client, message.chat.id)
    
    if success:
        # Update to joined status
        joined_message = vc_system.create_vc_status_message(
            "joined", message.chat.title or "Group"
        )
        
        await joining_msg.edit_text(
            joined_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Start monitoring
        asyncio.create_task(
            vc_system.start_vc_monitoring(client, message.chat.id, joining_msg)
        )
        
        LOGGER.info(f"Joined VC in chat {message.chat.id}")
        
    else:
        # Update to error status
        error_message = vc_system.create_vc_status_message(
            "error", message.chat.title or "Group"
        )
        
        await joining_msg.edit_text(
            error_message,
            parse_mode=ParseMode.MARKDOWN
        )

async def leavevc_handler(client: VzoelClient, message: Message):
    """
    Leave voice chat handler
    Usage: .leavevc
    """
    
    # Show leaving status
    leaving_msg = await message.reply_text(
        vc_system.create_vc_status_message("leaving", message.chat.title or "Group"),
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Stop monitoring first
    vc_system.stop_vc_monitoring(message.chat.id)
    
    # Attempt to leave VC
    success = await vc_system.leave_voice_chat(client, message.chat.id)
    
    if success:
        # Update to left status
        left_message = vc_system.create_vc_status_message(
            "left", message.chat.title or "Group"
        )
        
        await leaving_msg.edit_text(
            left_message,
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Left VC in chat {message.chat.id}")
        
    else:
        # Update to error status
        error_message = vc_system.create_vc_status_message(
            "error", message.chat.title or "Group"
        )
        
        await leaving_msg.edit_text(
            error_message,
            parse_mode=ParseMode.MARKDOWN
        )

async def startvc_handler(client: VzoelClient, message: Message):
    """
    Start voice chat handler
    Usage: .startvc
    """
    
    # Show starting status
    starting_msg = await message.reply_text(
        f"{emoji('loading')} {bold('Starting Voice Chat...')}\\n\\n"
        f"{emoji('proses')} Initializing group call...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Attempt to start VC
    success = await vc_system.start_voice_chat(client, message.chat.id)
    
    if success:
        # Update to success status
        success_message = [
            f"{emoji('centang')} {bold('Voice Chat Started!')}",
            "",
            f"{emoji('telegram')} **Chat:** {monospace(message.chat.title or 'Group')}",
            f"{emoji('aktif')} **Status:** {bold('ACTIVE')}",
            f"{emoji('utama')} **Action:** Voice chat is now available",
            "",
            f"{emoji('kuning')} **Join:** Use {monospace('.joinvc')} to participate",
            "",
            f"{italic('Premium VC by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await starting_msg.edit_text(
            "\n".join(success_message),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Started VC in chat {message.chat.id}")
        
    else:
        # Update to error status
        error_message = [
            f"{emoji('petir')} {bold('Failed to Start VC!')}",
            "",
            f"{emoji('merah')} Voice chat could not be started",
            f"{emoji('kuning')} Possible issues:",
            f"  • VC already active",
            f"  • Insufficient permissions",
            f"  • Group limitations",
            "",
            f"{italic('Premium VC by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await starting_msg.edit_text(
            "\n".join(error_message),
            parse_mode=ParseMode.MARKDOWN
        )

async def stopvc_handler(client: VzoelClient, message: Message):
    """
    Stop voice chat handler
    Usage: .stopvc
    """
    
    # Show stopping status
    stopping_msg = await message.reply_text(
        f"{emoji('proses')} {bold('Stopping Voice Chat...')}\\n\\n"
        f"{emoji('loading')} Terminating group call...",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Stop monitoring first
    vc_system.stop_vc_monitoring(message.chat.id)
    
    # Attempt to stop VC
    success = await vc_system.stop_voice_chat(client, message.chat.id)
    
    if success:
        # Update to success status
        success_message = [
            f"{emoji('centang')} {bold('Voice Chat Stopped!')}",
            "",
            f"{emoji('telegram')} **Chat:** {monospace(message.chat.title or 'Group')}",
            f"{emoji('merah')} **Status:** {bold('TERMINATED')}",
            f"{emoji('proses')} **Action:** Voice chat has been ended",
            "",
            f"{emoji('kuning')} **Restart:** Use {monospace('.startvc')} to begin new call",
            "",
            f"{italic('Premium VC by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await stopping_msg.edit_text(
            "\n".join(success_message),
            parse_mode=ParseMode.MARKDOWN
        )
        
        LOGGER.info(f"Stopped VC in chat {message.chat.id}")
        
    else:
        # Update to error status
        error_message = [
            f"{emoji('petir')} {bold('Failed to Stop VC!')}",
            "",
            f"{emoji('merah')} Voice chat could not be stopped",
            f"{emoji('kuning')} Possible issues:",
            f"  • No active VC to stop",
            f"  • Insufficient permissions",
            f"  • Connection problems",
            "",
            f"{italic('Premium VC by Vzoel VZLfxs @Lutpan')}"
        ]
        
        await stopping_msg.edit_text(
            "\n".join(error_message),
            parse_mode=ParseMode.MARKDOWN
        )

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Voice Chat System initialized")