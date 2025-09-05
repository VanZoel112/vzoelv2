"""
Helper module for command handling
Provides command parsing utilities for plugins
"""

from pyrogram import filters

# Command handler for plugins
CMD_HANDLER = filters.command("", prefixes=".")

def get_command(message):
    """Extract command from message"""
    if message.text and message.text.startswith('.'):
        parts = message.text.split()
        if parts:
            return parts[0][1:]  # Remove the dot prefix
    return None

def get_arguments(message):
    """Extract arguments from message"""
    if message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) > 1:
            return parts[1]
    return ""