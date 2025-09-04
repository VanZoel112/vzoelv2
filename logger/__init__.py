"""
Vzoel Logger Package - Premium Logging System
Comprehensive logging solution dengan config integration dan user tracking
Created by: Vzoel Fox's
"""

from .log_assistant import (
    VzoelLogger,
    vzoel_logger,
    log_info,
    log_warning, 
    log_error,
    log_success,
    set_telegram_client,
    get_logger
)

from .log_user import (
    UserActivityLogger,
    user_logger,
    log_user_command,
    get_user_report,
    get_daily_report,
    get_user_activity_logger
)

# Package information
__version__ = "1.0.0"
__author__ = "Vzoel Fox's"
__description__ = "Premium logging system dengan config integration dan user activity tracking"

# Export all main classes dan functions
__all__ = [
    # Main classes
    "VzoelLogger",
    "UserActivityLogger",
    
    # Global instances
    "vzoel_logger",
    "user_logger",
    
    # Assistant logging functions
    "log_info",
    "log_warning",
    "log_error",
    "log_success",
    "set_telegram_client",
    "get_logger",
    
    # User logging functions
    "log_user_command",
    "get_user_report",
    "get_daily_report",
    "get_user_activity_logger"
]

# Initialize logging system
def initialize_logging_system(telegram_client=None):
    """
    Initialize complete logging system dengan Telegram client
    
    Args:
        telegram_client: Pyrogram Client instance untuk Telegram logging
    """
    if telegram_client:
        set_telegram_client(telegram_client)
        log_info("Vzoel Logging System initialized with Telegram integration")
    else:
        log_info("Vzoel Logging System initialized (local only)")

# Quick setup function
def setup_premium_logging(config_path="vzoel/config.json", telegram_client=None):
    """
    Quick setup untuk premium logging system
    
    Args:
        config_path: Path ke configuration file
        telegram_client: Pyrogram Client instance
    
    Returns:
        tuple: (vzoel_logger, user_logger)
    """
    
    # Initialize dengan custom config jika diperlukan
    if config_path != "vzoel/config.json":
        global vzoel_logger, user_logger
        vzoel_logger = VzoelLogger(config_path)
        user_logger = UserActivityLogger(config_path)
    
    # Setup Telegram client
    if telegram_client:
        set_telegram_client(telegram_client)
    
    # Log setup completion
    log_success("Premium logging system setup completed")
    
    return vzoel_logger, user_logger

# System status check
def get_logging_system_status():
    """
    Get comprehensive status dari logging system
    
    Returns:
        dict: System status information
    """
    
    try:
        from utils.assets import VzoelAssets
        premium_assets_available = True
    except ImportError:
        premium_assets_available = False
    
    status = {
        "version": __version__,
        "author": __author__,
        "premium_assets": premium_assets_available,
        "telegram_logging": vzoel_logger.telegram_client is not None,
        "config_loaded": len(vzoel_logger.config) > 0,
        "user_tracking": True,
        "local_logging": True,
        "session_stats": vzoel_logger.get_session_stats()
    }
    
    return status

# Emergency logging function
def emergency_log(message: str, extra_data=None):
    """
    Emergency logging function yang selalu berhasil
    Fallback logging jika system logging gagal
    """
    try:
        log_error(f"EMERGENCY: {message}", extra_data, send_to_telegram=True)
    except Exception as e:
        # Ultimate fallback - print to console
        print(f"EMERGENCY LOG FAILED: {message} | Error: {e}")
        if extra_data:
            print(f"Extra data: {extra_data}")

# Health check function
def health_check():
    """
    Perform health check pada logging system
    
    Returns:
        dict: Health check results
    """
    
    results = {
        "overall_health": "unknown",
        "assistant_logger": "unknown",
        "user_logger": "unknown",
        "config_status": "unknown",
        "telegram_status": "unknown",
        "issues": []
    }
    
    try:
        # Test assistant logger
        test_message = f"Health check at {vzoel_logger.stats['session_start']}"
        log_info(test_message)
        results["assistant_logger"] = "healthy"
    except Exception as e:
        results["assistant_logger"] = "error"
        results["issues"].append(f"Assistant logger: {str(e)}")
    
    try:
        # Test user logger
        user_count = len(user_logger.user_activities)
        results["user_logger"] = "healthy"
        results["user_count"] = user_count
    except Exception as e:
        results["user_logger"] = "error"
        results["issues"].append(f"User logger: {str(e)}")
    
    # Check config
    if len(vzoel_logger.config) > 0:
        results["config_status"] = "loaded"
    else:
        results["config_status"] = "missing"
        results["issues"].append("Config not loaded")
    
    # Check Telegram
    if vzoel_logger.telegram_client:
        results["telegram_status"] = "connected"
    else:
        results["telegram_status"] = "disconnected"
        results["issues"].append("Telegram client not set")
    
    # Overall health
    if len(results["issues"]) == 0:
        results["overall_health"] = "excellent"
    elif len(results["issues"]) <= 2:
        results["overall_health"] = "good"
    else:
        results["overall_health"] = "needs_attention"
    
    return results