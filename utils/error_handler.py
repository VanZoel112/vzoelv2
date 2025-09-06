#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Error Handler
Enhanced error handling for Pyrogram peer ID issues
Created by: VZLfxs @Lutpan
"""

import logging
import asyncio
from typing import Any, Callable
from functools import wraps

logger = logging.getLogger(__name__)

def handle_peer_errors(func: Callable) -> Callable:
    """Decorator to handle peer ID invalid errors gracefully"""
    
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            if "Peer id invalid" in str(e):
                logger.warning(f"Peer ID invalid in {func.__name__}: {e}")
                return None
            raise
        except KeyError as e:
            if "ID not found" in str(e):
                logger.warning(f"Peer ID not found in {func.__name__}: {e}")
                return None
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise
    
    return wrapper

class ErrorHandler:
    """Global error handler for Vzoel Assistant"""
    
    def __init__(self):
        self.setup_exception_handler()
    
    def setup_exception_handler(self):
        """Setup global exception handler"""
        def exception_handler(loop, context):
            """Handle uncaught exceptions in asyncio tasks"""
            exception = context.get('exception')
            
            if exception:
                if isinstance(exception, ValueError) and "Peer id invalid" in str(exception):
                    # Suppress peer ID invalid errors - they're not critical
                    logger.debug(f"Suppressed peer ID error: {exception}")
                    return
                
                if isinstance(exception, KeyError) and "ID not found" in str(exception):
                    # Suppress peer not found errors - they're not critical
                    logger.debug(f"Suppressed peer not found error: {exception}")
                    return
            
            # Log other exceptions normally
            logger.error(f"Unhandled exception: {context}")
        
        # Set the exception handler for the current event loop
        try:
            loop = asyncio.get_event_loop()
            loop.set_exception_handler(exception_handler)
        except RuntimeError:
            # No event loop running yet
            pass

# Global error handler instance
error_handler = ErrorHandler()

async def safe_send_message(client, chat_id: int, text: str, **kwargs):
    """Safely send message with peer ID error handling"""
    try:
        return await client.send_message(chat_id=chat_id, text=text, **kwargs)
    except (ValueError, KeyError) as e:
        if "Peer id invalid" in str(e) or "ID not found" in str(e):
            logger.warning(f"Cannot send message to {chat_id}: Peer not accessible")
            return None
        raise

async def safe_get_chat(client, chat_id: int):
    """Safely get chat with peer ID error handling"""
    try:
        return await client.get_chat(chat_id)
    except (ValueError, KeyError) as e:
        if "Peer id invalid" in str(e) or "ID not found" in str(e):
            logger.warning(f"Cannot access chat {chat_id}: Peer not found")
            return None
        raise

def suppress_peer_errors():
    """Suppress peer ID related errors globally"""
    # Override the default exception handler
    original_handler = logging.getLogger().handlers[0] if logging.getLogger().handlers else None
    
    class PeerErrorFilter(logging.Filter):
        def filter(self, record):
            # Filter out peer ID related errors
            if "Peer id invalid" in record.getMessage():
                return False
            if "ID not found" in record.getMessage():
                return False
            return True
    
    if original_handler:
        original_handler.addFilter(PeerErrorFilter())