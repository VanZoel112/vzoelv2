"""
Premium Core Loader System - Enhanced Module Management
Enhanced with premium emoji and font system for superior logging experience
Created by: Vzoel Fox's
"""

from .loader_assistant import VzoelAssistant
from .loader_plugins import PremiumPluginLoader, load_all_plugins
from utils.assets import emoji, bold, italic

# Premium initialization message
print(f"{emoji('petir')} {bold('Premium Core Loader')} - {italic('Ruang Mesin Siap Digunakan')}")

__all__ = ["VzoelAssistant", "PremiumPluginLoader", "load_all_plugins"]