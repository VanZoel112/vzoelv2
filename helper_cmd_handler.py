"""
Helper module for command handling
Enhanced with multiple prefixes support
Provides command parsing utilities for plugins
"""

import os
from pyrogram import filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get command prefixes from environment
COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "/,!,.").split(",")
COMMAND_PREFIXES = [prefix.strip() for prefix in COMMAND_PREFIXES]

# Enhanced command handler for plugins with multiple prefixes
CMD_HANDLER = filters.command("", prefixes=COMMAND_PREFIXES)

def get_command(message):
    """Extract command from message with multiple prefix support"""
    if not message.text:
        return None
        
    text = message.text
    for prefix in COMMAND_PREFIXES:
        if text.startswith(prefix):
            parts = text.split()
            if parts:
                return parts[0][len(prefix):]  # Remove the prefix
    return None

def get_arguments(message):
    """Extract arguments from message"""
    if not message.text:
        return ""
        
    text = message.text
    for prefix in COMMAND_PREFIXES:
        if text.startswith(prefix):
            parts = text.split(maxsplit=1)
            if len(parts) > 1:
                return parts[1]
            break
    return ""

def is_command(message, cmd):
    """Check if message is a specific command with any supported prefix"""
    if not message.text:
        return False
        
    text = message.text
    for prefix in COMMAND_PREFIXES:
        if text.startswith(prefix + cmd):
            # Make sure it's the exact command (not just starts with it)
            after_cmd = text[len(prefix + cmd):]
            return after_cmd == "" or after_cmd.startswith(" ")
    return False