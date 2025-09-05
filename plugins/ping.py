#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Ping System
Advanced ping system with latency, color mapping, and spam reset features
Created by: Vzoel Fox's
"""

import asyncio
import time
from typing import Optional
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import MessageNotModified, FloodWait

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, emoji, vzoel_signature

class PremiumPingSystem:
    """Premium Ping System dengan 3 fitur canggih"""
    
    def __init__(self):
        # Color mapping untuk .pink command
        self.color_frames = [
            {"emoji": "🔴", "name": "Red", "style": "bold"},
            {"emoji": "🟠", "name": "Orange", "style": "italic"},
            {"emoji": "🟡", "name": "Yellow", "style": "monospace"},
            {"emoji": "🟢", "name": "Green", "style": "bold"},
            {"emoji": "🔵", "name": "Blue", "style": "italic"},
            {"emoji": "🟣", "name": "Purple", "style": "monospace"},
            {"emoji": "🟤", "name": "Brown", "style": "bold"},
            {"emoji": "⚫", "name": "Black", "style": "italic"},
            {"emoji": "⚪", "name": "White", "style": "monospace"},
            {"emoji": "🌈", "name": "Rainbow", "style": "bold"}
        ]
        
        # Animation frames untuk .pong processing
        self.pong_animation_frames = [
            f"{emoji('loading')} Initializing flood reset...",
            f"{emoji('proses')} Connecting to @spambot...",
            f"{emoji('telegram')} Sending reset request...",
            f"{emoji('aktif')} Processing response...",
            f"{emoji('petir')} Applying flood reset...",
            f"{emoji('centang')} Reset completed!"
        ]
    
    def calculate_latency(self, start_time: float, end_time: float) -> float:
        """Calculate latency in milliseconds"""
        return round((end_time - start_time) * 1000, 2)
    
    def format_latency(self, latency: float) -> str:
        """Format latency dengan premium styling"""
        if latency < 100:
            return f"{emoji('centang')} {bold(f'{latency}ms')} {emoji('kuning')}"
        elif latency < 300:
            return f"{emoji('kuning')} {bold(f'{latency}ms')} {emoji('proses')}"
        elif latency < 500:
            return f"{emoji('merah')} {bold(f'{latency}ms')} {emoji('loading')}"
        else:
            return f"{emoji('merah')} {bold(f'{latency}ms')} {emoji('petir')}"
    
    def get_premium_ping_message(self, latency: float) -> str:
        """Generate premium ping message"""
        ping_lines = [
            f"{emoji('telegram')} {bold('VZOEL ASSISTANT v2')}",
            "",
            f"{emoji('aktif')} {bold('PONG!!!')}",
            "",
            f"{emoji('loading')} **Latency:** {self.format_latency(latency)}",
            f"{emoji('centang')} **Status:** {bold('Online & Ready')}",
            f"{emoji('utama')} **Server:** {bold('Premium Performance')}",
            "",
            f"{italic('Ultra-fast response by Vzoel Fox\u0027s')}"
        ]
        
        return "\n".join(ping_lines)
    
    async def get_premium_pink_message(self) -> str:
        """Generate premium pink message dengan color mapping"""
        import random
        
        # Select random color
        color = random.choice(self.color_frames)
        
        # Apply styling based on color style
        if color["style"] == "bold":
            message_text = bold("VZOEL ASSISTANT anti delay")
        elif color["style"] == "italic":
            message_text = italic("VZOEL ASSISTANT anti delay")
        elif color["style"] == "monospace":
            message_text = monospace("VZOEL ASSISTANT anti delay")
        else:
            message_text = "VZOEL ASSISTANT anti delay"
        
        color_name = color['name'].upper()
        pink_lines = [
            f"{color['emoji']} {bold(f'COLOR: {color_name}')}",
            "",
            f"{emoji('adder2')} {message_text}",
            "",
            f"{emoji('petir')} **Performance:** {bold('Zero Delay')}",
            f"{emoji('centang')} **Anti-Lag:** {bold('Activated')}",
            f"{emoji('utama')} **Optimization:** {bold('Premium Level')}",
            "",
            f"{color['emoji']} {italic(f'Powered by {color_name} Energy')}"
        ]
        
        return "\n".join(pink_lines)
    
    async def animate_pong_process(self, message: Message) -> Message:
        """Animate pong processing sequence"""
        
        # Start animation
        progress_msg = await message.reply_text(
            self.pong_animation_frames[0],
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Animate through frames
        for frame in self.pong_animation_frames[1:]:
            await asyncio.sleep(0.6)
            
            try:
                await progress_msg.edit_text(
                    frame,
                    parse_mode=ParseMode.MARKDOWN
                )
            except MessageNotModified:
                pass
        
        return progress_msg
    
    async def send_spambot_reset(self, client: VzoelClient) -> bool:
        """Send reset message to @spambot"""
        try:
            reset_message = "/start"
            
            # Send message to spambot
            await client.send_message("@spambot", reset_message)
            
            LOGGER.info("Sent flood reset request to @spambot")
            return True
            
        except FloodWait as e:
            LOGGER.warning(f"FloodWait when sending to spambot: {e.value}s")
            return False
        except Exception as e:
            LOGGER.error(f"Error sending to spambot: {e}")
            return False
    
    async def get_final_pong_message(self, latency: float, spambot_success: bool) -> str:
        """Generate final pong message"""
        
        status_emoji = emoji('centang') if spambot_success else emoji('kuning')
        status_text = "Success" if spambot_success else "Partial"
        
        pong_lines = [
            f"{emoji('telegram')} {bold('VZOEL PONG SYSTEM')}",
            "",
            f"{emoji('aktif')} {bold('Latency Check:')} {self.format_latency(latency)}",
            f"{status_emoji} **Flood Reset:** {bold(status_text)}",
            f"{emoji('proses')} **@spambot:** {bold('Request Sent' if spambot_success else 'Rate Limited')}",
            "",
            f"{emoji('petir')} **Premium Features:**",
            f"  • Automated flood reset",
            f"  • Real-time latency monitoring", 
            f"  • Anti-delay optimization",
            "",
            f"{emoji('centang')} **Status:** {bold('All systems operational')}",
            "",
            f"{italic('Advanced ping system by Vzoel Fox\\'s')}"
        ]
        
        return "\n".join(pong_lines)

# Initialize premium ping system
ping_system = PremiumPingSystem()

@VzoelClient.on_message(CMD_HANDLER)
async def ping_router(client: VzoelClient, message: Message):
    """Router untuk ping commands"""
    command = get_command(message)
    
    if command == "ping":
        await ping_handler(client, message)
    elif command == "pink":
        await pink_handler(client, message)
    elif command == "pong":
        await pong_handler(client, message)

async def ping_handler(client: VzoelClient, message: Message):
    """
    Standard ping command handler
    Usage: .ping
    Response: PONG!!! dengan latency display
    """
    
    # Record start time
    start_time = time.time()
    
    # Send initial response untuk measure latency
    temp_msg = await message.reply_text(
        f"{emoji('loading')} {bold('Calculating latency...')}", 
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Record end time
    end_time = time.time()
    
    # Calculate latency
    latency = ping_system.calculate_latency(start_time, end_time)
    
    # Generate premium ping message
    ping_message = ping_system.get_premium_ping_message(latency)
    
    # Update message with results
    await temp_msg.edit_text(
        ping_message,
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info(f"Ping command executed with {latency}ms latency")

async def pink_handler(client: VzoelClient, message: Message):
    """
    Pink command handler dengan color mapping
    Usage: .pink  
    Response: Random color dengan VZOEL ASSISTANT anti delay message
    """
    
    # Generate premium pink message
    pink_message = await ping_system.get_premium_pink_message()
    
    # Send pink response
    await message.reply_text(
        pink_message,
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info("Pink command executed with color mapping")

async def pong_handler(client: VzoelClient, message: Message):
    """
    Advanced pong command handler
    Usage: .pong
    Features: Animated processing, latency check, @spambot reset
    """
    
    # Record start time untuk latency
    start_time = time.time()
    
    # Start animated processing
    progress_msg = await ping_system.animate_pong_process(message)
    
    # Send reset request to spambot
    spambot_success = await ping_system.send_spambot_reset(client)
    
    # Calculate latency
    end_time = time.time()
    latency = ping_system.calculate_latency(start_time, end_time)
    
    # Generate final message
    final_message = await ping_system.get_final_pong_message(latency, spambot_success)
    
    # Update dengan hasil final
    await progress_msg.edit_text(
        final_message,
        parse_mode=ParseMode.MARKDOWN
    )
    
    LOGGER.info(f"Pong command completed - Latency: {latency}ms, Spambot: {spambot_success}")

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Ping System initialized with 3 features")