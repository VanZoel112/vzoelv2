"""
Logger Commands Plugin - Premium Logging Management
Interactive commands untuk managing logging system dengan premium UI
Created by: Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from logger import (
    vzoel_logger, 
    user_logger, 
    get_user_report, 
    get_daily_report,
    get_logging_system_status,
    health_check
)
from helpers.display_helper import DisplayHelper
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
from datetime import datetime, timedelta
import json

# Initialize premium components
display_helper = DisplayHelper()
assets = VzoelAssets()

@Client.on_message(filters.command("logs"))
async def logger_menu_command(client: Client, message: Message):
    """
    Main logging management menu dengan interactive navigation
    """
    
    try:
        # Get system status
        system_status = get_logging_system_status()
        health_status = health_check()
        
        # Create main menu display
        menu_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('utama')} **VZOEL LOGGING SYSTEM**",
            "",
            f"{emoji('centang')} **System Status:**",
            f"• Version: {bold(system_status['version'])}",
            f"• Health: {bold(health_status['overall_health'].title())}",
            f"• Premium Assets: {bold('✓' if system_status['premium_assets'] else '✗')}",
            f"• Telegram Logging: {bold('✓' if system_status['telegram_logging'] else '✗')}",
            f"• Config Loaded: {bold('✓' if system_status['config_loaded'] else '✗')}",
            "",
            f"{emoji('loading')} **Session Statistics:**",
            f"• Total Logs: {bold(str(system_status['session_stats']['total_logs']))}",
            f"• Uptime: {bold(system_status['session_stats']['uptime_formatted'])}",
            f"• Users Tracked: {bold(str(len(user_logger.user_activities)))}",
            "",
            f"{emoji('aktif')} **Available Commands:**",
            f"• Use buttons below untuk navigate",
            f"• `/logs status` - Quick status check", 
            f"• `/logs report` - Generate system report",
            f"• `/logs user <id>` - User activity report",
            "",
            f"{italic('Select an option to continue')}"
        ]
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('loading')} System Status", callback_data="logs_status"),
                InlineKeyboardButton(f"{emoji('centang')} Health Check", callback_data="logs_health")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} Daily Report", callback_data="logs_daily"),
                InlineKeyboardButton(f"{emoji('utama')} User Stats", callback_data="logs_users")
            ],
            [
                InlineKeyboardButton(f"{emoji('loading')} Live Monitor", callback_data="logs_monitor"),
                InlineKeyboardButton(f"{emoji('centang')} Settings", callback_data="logs_settings")
            ],
            [
                InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="logs_close")
            ]
        ])
        
        await message.reply_text("\n".join(menu_lines), reply_markup=keyboard)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to load logging menu: {str(e)}",
            ["Check system permissions", "Verify logger initialization", "Contact administrator"]
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("logs") & filters.text)
async def logger_subcommand(client: Client, message: Message):
    """
    Handle logger subcommands
    """
    
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            return  # Will be handled by main logs command
        
        subcommand = command_parts[1].lower()
        
        if subcommand == "status":
            await show_system_status(client, message)
        elif subcommand == "report":
            await show_system_report(client, message)
        elif subcommand == "user":
            if len(command_parts) >= 3:
                user_id = command_parts[2]
                await show_user_report(client, message, user_id)
            else:
                await message.reply_text(f"{emoji('merah')} Usage: /logs user <user_id>")
        elif subcommand == "daily":
            date = command_parts[2] if len(command_parts) >= 3 else None
            await show_daily_report(client, message, date)
        else:
            await message.reply_text(
                f"{emoji('merah')} Unknown subcommand: {subcommand}\n"
                f"Available: status, report, user, daily"
            )
            
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Subcommand failed: {str(e)}"
        )
        await message.reply_text(error_msg)

async def show_system_status(client: Client, message: Message):
    """Show quick system status"""
    
    try:
        system_status = get_logging_system_status()
        health_status = health_check()
        
        # Format uptime
        uptime = system_status['session_stats']['uptime_formatted']
        
        status_lines = [
            f"{emoji('loading')} **SYSTEM STATUS CHECK**",
            "",
            f"{emoji('centang' if health_status['overall_health'] == 'excellent' else 'loading')} **Overall Health:** {bold(health_status['overall_health'].title())}",
            "",
            f"{emoji('utama')} **Component Status:**",
            f"• Assistant Logger: {bold('✓ Healthy' if health_status['assistant_logger'] == 'healthy' else '✗ Error')}",
            f"• User Logger: {bold('✓ Healthy' if health_status['user_logger'] == 'healthy' else '✗ Error')}",
            f"• Config System: {bold('✓ Loaded' if health_status['config_status'] == 'loaded' else '✗ Missing')}",
            f"• Telegram Link: {bold('✓ Connected' if health_status['telegram_status'] == 'connected' else '✗ Disconnected')}",
            "",
            f"{emoji('aktif')} **Live Statistics:**",
            f"• Session Uptime: {bold(uptime)}",
            f"• Total Logs: {bold(str(system_status['session_stats']['total_logs']))}",
            f"• Error Rate: {bold(f'{(system_status['session_stats']['error_logs'] / max(system_status['session_stats']['total_logs'], 1) * 100):.1f}%')}",
            f"• Users Tracked: {bold(str(len(user_logger.user_activities)))}",
        ]
        
        if health_status['issues']:
            status_lines.extend([
                "",
                f"{emoji('merah')} **Issues Detected:**"
            ])
            for issue in health_status['issues']:
                status_lines.append(f"• {issue}")
        
        status_lines.extend([
            "",
            f"{italic('Status updated in real-time')}"
        ])
        
        await message.reply_text("\n".join(status_lines))
        
    except Exception as e:
        await message.reply_text(f"{emoji('merah')} Status check failed: {str(e)}")

async def show_system_report(client: Client, message: Message):
    """Show comprehensive system report"""
    
    try:
        # Show loading message
        loading_msg = display_helper.create_loading_message(
            "Generating System Report",
            ["Collecting system statistics", "Processing user data", "Formatting report"]
        )
        loading_message = await message.reply_text(loading_msg)
        
        # Generate comprehensive report
        report = await vzoel_logger.create_log_report()
        
        await loading_message.edit_text(report)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Report generation failed: {str(e)}"
        )
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

async def show_user_report(client: Client, message: Message, user_id: str):
    """Show user activity report"""
    
    try:
        # Validate user_id
        try:
            user_id_int = int(user_id)
        except ValueError:
            await message.reply_text(f"{emoji('merah')} Invalid user ID format")
            return
        
        # Show loading
        loading_msg = display_helper.create_loading_message(
            f"Generating User Report",
            [f"Fetching data for user {user_id}", "Processing activity history", "Creating report"]
        )
        loading_message = await message.reply_text(loading_msg)
        
        # Generate user report
        report = get_user_report(user_id)
        
        await loading_message.edit_text(report)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"User report failed: {str(e)}"
        )
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

async def show_daily_report(client: Client, message: Message, date: str = None):
    """Show daily activity report"""
    
    try:
        if date:
            # Validate date format
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                await message.reply_text(f"{emoji('merah')} Invalid date format. Use YYYY-MM-DD")
                return
        
        # Show loading
        loading_msg = display_helper.create_loading_message(
            "Generating Daily Report",
            ["Processing daily statistics", "Calculating metrics", "Formatting display"]
        )
        loading_message = await message.reply_text(loading_msg)
        
        # Generate daily report
        report = get_daily_report(date)
        
        await loading_message.edit_text(report)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Daily report failed: {str(e)}"
        )
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

# Callback query handlers
@Client.on_callback_query(filters.regex("logs_status"))
async def logs_status_callback(client: Client, callback_query: CallbackQuery):
    """Handle status callback"""
    
    try:
        system_status = get_logging_system_status()
        health_status = health_check()
        
        status_summary = [
            f"{emoji('loading')} **Quick Status Summary**",
            "",
            f"Health: {bold(health_status['overall_health'].title())}",
            f"Uptime: {bold(system_status['session_stats']['uptime_formatted'])}",
            f"Total Logs: {bold(str(system_status['session_stats']['total_logs']))}",
            f"Users Tracked: {bold(str(len(user_logger.user_activities)))}",
            "",
            f"{italic('Use /logs status for detailed view')}"
        ]
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="logs_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(status_summary), reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("logs_health"))
async def logs_health_callback(client: Client, callback_query: CallbackQuery):
    """Handle health check callback"""
    
    try:
        health_status = health_check()
        
        health_lines = [
            f"{emoji('centang')} **Health Check Results**",
            "",
            f"Overall: {bold(health_status['overall_health'].title())}",
            f"Assistant Logger: {bold('✓' if health_status['assistant_logger'] == 'healthy' else '✗')}",
            f"User Logger: {bold('✓' if health_status['user_logger'] == 'healthy' else '✗')}",
            f"Config: {bold('✓' if health_status['config_status'] == 'loaded' else '✗')}",
            f"Telegram: {bold('✓' if health_status['telegram_status'] == 'connected' else '✗')}",
        ]
        
        if health_status['issues']:
            health_lines.extend(["", f"{emoji('merah')} **Issues:**"])
            for issue in health_status['issues'][:3]:  # Show max 3 issues
                health_lines.append(f"• {issue}")
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="logs_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(health_lines), reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("logs_daily"))
async def logs_daily_callback(client: Client, callback_query: CallbackQuery):
    """Handle daily report callback"""
    
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        report = get_daily_report(today)
        
        # Add quick navigation
        nav_lines = [
            "",
            f"{emoji('loading')} **Quick Actions:**",
            f"• `/logs daily` - Today's full report",
            f"• `/logs daily YYYY-MM-DD` - Specific date",
        ]
        
        full_report = report + "\n".join(nav_lines)
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="logs_main")]
        ])
        
        await callback_query.edit_message_text(full_report, reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("logs_users"))
async def logs_users_callback(client: Client, callback_query: CallbackQuery):
    """Handle user stats callback"""
    
    try:
        top_users = user_logger.get_top_users(limit=5)
        
        if not top_users:
            user_summary = [
                f"{emoji('merah')} **No User Data Available**",
                "",
                f"Start using bot commands to generate user statistics"
            ]
        else:
            user_summary = [
                f"{emoji('aktif')} **Top 5 Active Users**",
                ""
            ]
            
            for i, user_data in enumerate(top_users, 1):
                user_info = user_data['user_info']
                name = user_info.get('first_name', 'Unknown')
                commands = user_data['total_commands']
                success_rate = user_data['success_rate']
                
                user_summary.append(f"{i}. {bold(name)} - {commands} commands ({success_rate:.1f}% success)")
        
        user_summary.extend([
            "",
            f"{emoji('loading')} **Commands:**",
            f"• `/logs user <id>` - Detailed user report",
            f"• Total users tracked: {bold(str(len(user_logger.user_activities)))}"
        ])
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="logs_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(user_summary), reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("logs_main"))
async def logs_main_callback(client: Client, callback_query: CallbackQuery):
    """Return to main logs menu"""
    
    try:
        # Recreate main menu (simplified version for callback)
        system_status = get_logging_system_status()
        
        menu_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('utama')} **VZOEL LOGGING SYSTEM**",
            "",
            f"System Health: {bold('Active')}",
            f"Total Logs: {bold(str(system_status['session_stats']['total_logs']))}",
            f"Users Tracked: {bold(str(len(user_logger.user_activities)))}",
            "",
            f"{italic('Select an option to continue')}"
        ]
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('loading')} System Status", callback_data="logs_status"),
                InlineKeyboardButton(f"{emoji('centang')} Health Check", callback_data="logs_health")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} Daily Report", callback_data="logs_daily"),
                InlineKeyboardButton(f"{emoji('utama')} User Stats", callback_data="logs_users")
            ],
            [
                InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="logs_close")
            ]
        ])
        
        await callback_query.edit_message_text("\n".join(menu_lines), reply_markup=keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("logs_close"))
async def logs_close_callback(client: Client, callback_query: CallbackQuery):
    """Close logs menu"""
    
    try:
        close_message = [
            f"{emoji('centang')} **Logging Menu Closed**",
            "",
            f"Vzoel Logging System tetap active di background",
            f"Type `/logs` anytime untuk reopen menu",
            "",
            f"{italic('Enhanced by Vzoel Premium Logging')}"
        ]
        
        await callback_query.edit_message_text("\n".join(close_message))
        await callback_query.answer("Logging menu closed")
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)