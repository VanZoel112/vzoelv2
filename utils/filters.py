#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Custom Filters
Enhanced command filters with multiple prefixes support
Created by: VZLfxs @Lutpan
"""

import os
from pyrogram import filters
from pyrogram.types import Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get command prefixes from environment
COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "/,!,.").split(",")
COMMAND_PREFIXES = [prefix.strip() for prefix in COMMAND_PREFIXES]

def vzoel_command(commands):
    """
    Custom command filter that supports multiple prefixes
    Usage: @app.on_message(vzoel_command("ping"))
    """
    if isinstance(commands, str):
        commands = [commands]
    
    def func(flt, client, message: Message):
        if not message.text:
            return False
            
        text = message.text
        
        # Check each prefix
        for prefix in COMMAND_PREFIXES:
            if text.startswith(prefix):
                # Extract command without prefix
                command_text = text[len(prefix):].split()[0].lower()
                
                # Check if it matches any of our commands
                for cmd in commands:
                    if command_text == cmd.lower():
                        return True
        
        return False
    
    return filters.create(func, name="VzoelCommand")

def is_sudo_user(user_id: int) -> bool:
    """Check if user is sudo/admin"""
    sudo_users = os.getenv("SUDO_USER_IDS", "").split(",")
    developer_ids = os.getenv("DEVELOPER_IDS", "").split(",")
    founder_id = os.getenv("FOUNDER_ID", "0")
    
    # Clean and convert to int
    sudo_users = [int(uid.strip()) for uid in sudo_users if uid.strip().isdigit()]
    developer_ids = [int(uid.strip()) for uid in developer_ids if uid.strip().isdigit()]
    founder_id = int(founder_id) if founder_id.isdigit() else 0
    
    return user_id in sudo_users or user_id in developer_ids or user_id == founder_id

def sudo_only():
    """Filter for sudo users only"""
    def func(flt, client, message: Message):
        if not message.from_user:
            return False
        return is_sudo_user(message.from_user.id)
    
    return filters.create(func, name="SudoOnly")

def get_command_from_message(message: Message) -> str:
    """Extract command from message with custom prefixes"""
    if not message.text:
        return ""
    
    text = message.text
    
    for prefix in COMMAND_PREFIXES:
        if text.startswith(prefix):
            # Return command without prefix
            return text[len(prefix):].split()[0].lower()
    
    return ""

def get_args_from_message(message: Message) -> list:
    """Extract arguments from message"""
    if not message.text:
        return []
    
    text = message.text
    
    for prefix in COMMAND_PREFIXES:
        if text.startswith(prefix):
            # Split and remove command, return args
            parts = text[len(prefix):].split()
            return parts[1:] if len(parts) > 1 else []
    
    return []

# Export commonly used filters
__all__ = [
    'vzoel_command',
    'sudo_only', 
    'is_sudo_user',
    'get_command_from_message',
    'get_args_from_message',
    'COMMAND_PREFIXES'
]