"""
Helper module for Vzoel Client
Provides compatibility layer for plugins
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