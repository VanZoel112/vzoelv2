"""
Premium Core Module - Enhanced Bot Framework Components
Enhanced with premium asset integration and superior performance
Created by: Vzoel Fox's
"""

from .client import VzoelClient, VzoelClientInstance
from .loader import VzoelAssistant, PremiumPluginLoader, load_all_plugins
from utils.assets import emoji, bold, italic

# Premium core initialization message
print(f"{emoji('utama')} {bold('Premium Core Module')} - {italic('Enhanced Framework Loaded')}")

# Export all premium components
__all__ = [
    "VzoelClient",
    "VzoelClientInstance", 
    "VzoelAssistant",
    "PremiumPluginLoader",
    "load_all_plugins"
]

# Version and metadata
__version__ = "2.0.0-premium"
__author__ = "Vzoel Fox"
__description__ = "Premium Bot Framework with Enhanced Assets"