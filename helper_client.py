"""
Helper module for Vzoel Client
Provides compatibility layer for plugins supporting both bot and user mode
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import VzoelAssistant
    # Alias for backward compatibility
    VzoelClient = VzoelAssistant
except ImportError:
    # Fallback if main module can't be imported
    from pyrogram import Client
    VzoelClient = Client

def is_user_mode(client) -> bool:
    """Check if client is running in user mode (not bot)"""
    try:
        # Check if client has bot_token (bot mode) or session_string (user mode)
        return hasattr(client, 'session_string') or not hasattr(client, 'bot_token')
    except:
        return False

def get_client_type(client) -> str:
    """Get client type for logging purposes"""
    return "USER" if is_user_mode(client) else "BOT"