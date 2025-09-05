"""
Helper module for configuration management
Provides config access for plugins
"""

import json
import os

CONFIG_JSON_PATH = os.path.join("vzoel", "config.json")

class ConfigHelper:
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        try:
            with open(CONFIG_JSON_PATH, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = self._get_default_config()
    
    def _get_default_config(self):
        return {
            "blacklist": {
                "groups": []
            }
        }
    
    @property
    def blacklist(self):
        """Access blacklist configuration"""
        return BlacklistConfig(self.data.get("blacklist", {"groups": []}))

class BlacklistConfig:
    def __init__(self, blacklist_data):
        self.groups = blacklist_data.get("groups", [])

# Global config instance
CONFIG = ConfigHelper()