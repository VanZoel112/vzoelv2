"""
Helper module for logging
Provides logging utilities for plugins
"""

import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Global logger instance
LOGGER = logging.getLogger('vzoel')