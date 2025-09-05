"""
Autonomous Bot Commands - Interactive Bot Creation dan Premium Emoji Management
Commands untuk mengelola autonomous bot creation dan premium emoji mapping
Created by: Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.autonomous_bot_helper import AutonomousBotCreator, PremiumEmojiMapper
from helpers.display_helper import DisplayHelper
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
from logger import log_info, log_error, log_success, log_user_command
import asyncio
import json

# Initialize premium components
display_helper = DisplayHelper()
assets = VzoelAssets()

@Client.on_message(filters.command("autobot"))
async def autonomous_bot_menu(client: Client, message: Message):
    """
    Main autonomous bot management menu
    """
    
    try:
        # Log command usage
        log_user_command(message.from_user, message.chat, "/autobot", True)
        
        # Initialize bot creator
        bot_creator = AutonomousBotCreator(client)
        
        # Get current stats
        created_count = bot_creator.created_bots.get("total_created", 0)
        last_created = bot_creator.created_bots.get("last_created")
        last_created_display = last_created[:19] if last_created else "Never"
        
        # Create main menu
        menu_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('utama')} **AUTONOMOUS BOT CREATOR**",
            "",
            f"{emoji('centang')} **System Status:**",
            f"• Bots Created: {bold(str(created_count))}",
            f"• Last Created: {bold(last_created_display)}",
            f"• Creator Status: {bold('✓ Active')}",
            "",
            f"{emoji('loading')} **Features:**",
            f"• Automatic bot creation via @BotFather",
            f"• Premium emoji mapping support",
            f"• Bulk bot creation dengan delays",
            f"• Token validation dan testing",
            f"• Comprehensive bot management",
            "",
            f"{emoji('aktif')} **Available Actions:**",
            f"• Use buttons below untuk navigate",
            f"• `/autobot create` - Quick bot creation",
            f"• `/autobot report` - View created bots report",
            f"• `/emojipremium` - Premium emoji management",
            "",
            f"{italic('Select an option to continue')}"
        ]
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('centang')} Create Single Bot", callback_data="autobot_create_single"),
                InlineKeyboardButton(f"{emoji('loading')} Create Multiple", callback_data="autobot_create_multiple")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} View Reports", callback_data="autobot_reports"),
                InlineKeyboardButton(f"{emoji('utama')} Test Token", callback_data="autobot_test_token")
            ],
            [
                InlineKeyboardButton(f"{emoji('loading')} Premium Emojis", callback_data="premium_emoji_menu"),
                InlineKeyboardButton(f"{emoji('centang')} Bot Settings", callback_data="autobot_settings")
            ],
            [
                InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="autobot_close")
            ]
        ])
        
        await message.reply_text("\n".join(menu_lines), reply_markup=keyboard)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to load autonomous bot menu: {str(e)}",
            ["Check user permissions", "Verify bot configuration", "Contact administrator"]
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("autobot") & filters.regex(r"create"))
async def create_single_bot_command(client: Client, message: Message):
    """
    Quick command untuk create single bot
    """
    
    try:
        # Show loading message
        loading_msg = display_helper.create_loading_message(
            "Creating Autonomous Bot",
            ["Contacting @BotFather", "Generating bot credentials", "Setting up bot profile"]
        )
        loading_message = await message.reply_text(loading_msg)
        
        # Create bot
        bot_creator = AutonomousBotCreator(client)
        result = await bot_creator.create_bot_automatically()
        
        if result["success"]:
            bot_info = result["bot_info"]
            success_msg = display_helper.create_success_message(
                f"Bot created successfully: @{bot_info['username']}",
                [
                    f"Name: {bot_info['name']}",
                    f"Username: @{bot_info['username']}",
                    f"Token: `{bot_info['token']}`",
                    f"Description: {bot_info['description'][:50]}..."
                ]
            )
            await loading_message.edit_text(success_msg)
            log_success(f"Bot @{bot_info['username']} created via command")
        else:
            error_msg = display_helper.create_error_message(
                f"Failed to create bot: {result.get('error', 'Unknown error')}",
                ["Try again later", "Check @BotFather availability", "Contact support"]
            )
            await loading_message.edit_text(error_msg)
            
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Bot creation failed: {str(e)}"
        )
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

@Client.on_message(filters.command("autobot") & filters.regex(r"report"))
async def show_bot_report_command(client: Client, message: Message):
    """
    Show autonomous bots report
    """
    
    try:
        bot_creator = AutonomousBotCreator(client)
        report = bot_creator.get_created_bots_report()
        await message.reply_text(report)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to generate report: {str(e)}"
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("emojipremium"))
async def premium_emoji_menu(client: Client, message: Message):
    """
    Premium emoji management menu
    """
    
    try:
        # Log command usage
        log_user_command(message.from_user, message.chat, "/emojipremium", True)
        
        # Initialize emoji mapper
        emoji_mapper = PremiumEmojiMapper(client)
        
        # Check user premium status
        user_premium = await emoji_mapper.check_user_premium_status(message.from_user.id)
        
        # Get emoji stats
        total_emojis = len(emoji_mapper.emoji_mapping["emojis"])
        premium_count = sum(1 for e in emoji_mapper.emoji_mapping["emojis"].values() if e.get("premium", True))
        
        menu_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('utama')} **PREMIUM EMOJI SYSTEM**",
            "",
            f"{emoji('centang')} **Your Status:**",
            f"• Telegram Premium: {bold('✓ Active' if user_premium else '✗ Not Active')}",
            f"• Premium Emojis Available: {bold(str(premium_count))}",
            f"• Total Emojis: {bold(str(total_emojis))}",
            "",
            f"{emoji('loading')} **Features:**",
            f"• Custom emoji mapping system",
            f"• HTML formatted emoji support", 
            f"• Automatic premium detection",
            f"• Fallback untuk non-premium users",
            "",
            f"{emoji('aktif')} **Available Actions:**",
            f"• View available premium emojis",
            f"• Test premium emoji sending",
            f"• Add custom emoji mappings",
            f"• Generate emoji reports",
            "",
            f"{italic('Premium features require Telegram Premium subscription')}"
        ]
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('centang')} View Emojis", callback_data="emoji_view_list"),
                InlineKeyboardButton(f"{emoji('loading')} Test Send", callback_data="emoji_test_send")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} Emoji Report", callback_data="emoji_report"),
                InlineKeyboardButton(f"{emoji('utama')} Add Custom", callback_data="emoji_add_custom")
            ],
            [
                InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="emoji_close")
            ]
        ])
        
        await message.reply_text("\n".join(menu_lines), reply_markup=keyboard)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to load premium emoji menu: {str(e)}"
        )
        await message.reply_text(error_msg)

# Callback query handlers
@Client.on_callback_query(filters.regex("autobot_create_single"))
async def create_single_bot_callback(client: Client, callback_query: CallbackQuery):
    """Handle single bot creation"""
    
    try:
        await callback_query.answer("Creating bot...")
        
        loading_msg = display_helper.create_loading_message(
            "Creating Single Autonomous Bot",
            ["Contacting @BotFather", "Generating unique credentials", "Setting up bot profile"]
        )
        await callback_query.edit_message_text(loading_msg)
        
        # Create bot
        bot_creator = AutonomousBotCreator(client)
        result = await bot_creator.create_bot_automatically()
        
        if result["success"]:
            bot_info = result["bot_info"]
            success_lines = [
                f"{emoji('utama')} **Bot Created Successfully!**",
                "",
                f"{emoji('centang')} **Bot Information:**",
                f"• Name: {bold(bot_info['name'])}",
                f"• Username: {bold('@' + bot_info['username'])}",
                f"• Token: `{bot_info['token']}`",
                f"• Created: {bold(bot_info['created_at'][:19])}",
                "",
                f"{emoji('loading')} **Next Steps:**",
                f"• Save the token securely",
                f"• Configure bot settings if needed",
                f"• Test bot functionality",
                "",
                f"{italic('Bot is now ready for use!')}"
            ]
            
            back_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")]
            ])
            
            await callback_query.edit_message_text("\n".join(success_lines), reply_markup=back_keyboard)
        else:
            error_lines = [
                f"{emoji('merah')} **Bot Creation Failed**",
                "",
                f"Error: {result.get('error', 'Unknown error')}",
                "",
                f"{emoji('loading')} **Possible Solutions:**",
                f"• Wait a few minutes and try again",
                f"• Check @BotFather availability",
                f"• Ensure account has bot creation permissions",
                "",
                f"{italic('Contact support if problem persists')}"
            ]
            
            back_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")]
            ])
            
            await callback_query.edit_message_text("\n".join(error_lines), reply_markup=back_keyboard)
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("autobot_create_multiple"))
async def create_multiple_bots_callback(client: Client, callback_query: CallbackQuery):
    """Handle multiple bot creation"""
    
    try:
        await callback_query.answer("Creating multiple bots...")
        
        # Create selection menu
        selection_lines = [
            f"{emoji('utama')} **Create Multiple Bots**",
            "",
            f"{emoji('centang')} **Select Quantity:**",
            f"Choose how many bots to create simultaneously",
            "",
            f"{emoji('loading')} **Important Notes:**",
            f"• Each bot creation takes ~60 seconds",
            f"• Delays prevent @BotFather rate limits",
            f"• Process cannot be cancelled once started",
            f"• All tokens will be saved automatically",
            "",
            f"{italic('Select quantity below:')}"
        ]
        
        quantity_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("2 Bots", callback_data="autobot_bulk_2"),
                InlineKeyboardButton("3 Bots", callback_data="autobot_bulk_3"),
                InlineKeyboardButton("5 Bots", callback_data="autobot_bulk_5")
            ],
            [
                InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")
            ]
        ])
        
        await callback_query.edit_message_text("\n".join(selection_lines), reply_markup=quantity_keyboard)
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("autobot_bulk_([0-9]+)"))
async def create_bulk_bots_callback(client: Client, callback_query: CallbackQuery):
    """Handle bulk bot creation"""
    
    try:
        count = int(callback_query.matches[0].group(1))
        await callback_query.answer(f"Creating {count} bots...")
        
        loading_msg = display_helper.create_loading_message(
            f"Creating {count} Autonomous Bots",
            ["This process will take several minutes", "Please wait patiently", "Do not close this message"]
        )
        await callback_query.edit_message_text(loading_msg)
        
        # Create multiple bots
        bot_creator = AutonomousBotCreator(client)
        results = await bot_creator.create_multiple_bots(count=count, delay=60)
        
        # Process results
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        
        result_lines = [
            f"{emoji('utama')} **Bulk Bot Creation Complete**",
            "",
            f"{emoji('centang')} **Results Summary:**",
            f"• Successful: {bold(str(len(successful)))}/{count}",
            f"• Failed: {bold(str(len(failed)))}/{count}",
            f"• Success Rate: {bold(f'{len(successful)/count*100:.1f}%')}",
            ""
        ]
        
        if successful:
            result_lines.append(f"{emoji('loading')} **Successfully Created:**")
            for bot in successful[:3]:  # Show first 3
                result_lines.append(f"• {bold(bot['name'])} (@{bot['username']})")
            
            if len(successful) > 3:
                result_lines.append(f"... and {len(successful)-3} more bots")
            result_lines.append("")
        
        if failed:
            result_lines.append(f"{emoji('merah')} **Failed Creations:**")
            for bot in failed[:2]:  # Show first 2 errors
                result_lines.append(f"• Error: {bot.get('error', 'Unknown')}")
            result_lines.append("")
        
        result_lines.extend([
            f"{emoji('aktif')} **All bot tokens saved to autonomous_bots.json**",
            "",
            f"{italic('Use /autobot report to view detailed information')}"
        ])
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(result_lines), reply_markup=back_keyboard)
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("autobot_reports"))
async def show_reports_callback(client: Client, callback_query: CallbackQuery):
    """Show autonomous bots report"""
    
    try:
        bot_creator = AutonomousBotCreator(client)
        report = bot_creator.get_created_bots_report()
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")]
        ])
        
        await callback_query.edit_message_text(report, reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("premium_emoji_menu"))
async def premium_emoji_menu_callback(client: Client, callback_query: CallbackQuery):
    """Show premium emoji menu"""
    
    try:
        emoji_mapper = PremiumEmojiMapper(client)
        
        # Check user premium status
        user_premium = await emoji_mapper.check_user_premium_status(callback_query.from_user.id)
        
        menu_lines = [
            f"{emoji('utama')} **Premium Emoji Manager**",
            "",
            f"Premium Status: {bold('✓ Active' if user_premium else '✗ Not Active')}",
            f"Available Emojis: {bold(str(len(emoji_mapper.emoji_mapping['emojis'])))}",
            "",
            f"{italic('Select an action below:')}"
        ]
        
        emoji_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('centang')} View List", callback_data="emoji_view_list"),
                InlineKeyboardButton(f"{emoji('loading')} Test Send", callback_data="emoji_test_send")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} Generate Report", callback_data="emoji_report")
            ],
            [
                InlineKeyboardButton(f"{emoji('loading')} ← Back to Menu", callback_data="autobot_main")
            ]
        ])
        
        await callback_query.edit_message_text("\n".join(menu_lines), reply_markup=emoji_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("emoji_test_send"))
async def test_premium_emoji_callback(client: Client, callback_query: CallbackQuery):
    """Test sending premium emoji"""
    
    try:
        await callback_query.answer("Testing premium emoji...")
        
        emoji_mapper = PremiumEmojiMapper(client)
        
        # Test message dengan premium emojis
        test_text = "Testing Premium Emojis: {fire} {star} {check} {heart} {crown}"
        emoji_mapping = {
            "fire": "vzoel_fire",
            "star": "vzoel_star", 
            "check": "vzoel_check",
            "heart": "vzoel_heart",
            "crown": "vzoel_crown"
        }
        
        result = await emoji_mapper.send_premium_message(
            callback_query.message.chat.id, 
            test_text, 
            emoji_mapping
        )
        
        if result:
            success_msg = [
                f"{emoji('centang')} **Premium Emoji Test Successful!**",
                "",
                f"Message sent with premium emojis.",
                f"Check the message above to see the result.",
                "",
                f"{italic('Premium emojis working correctly!')}"
            ]
        else:
            success_msg = [
                f"{emoji('merah')} **Premium Emoji Test Failed**",
                "",
                f"Could not send message with premium emojis.",
                f"This might be due to:",
                f"• Account lacks Telegram Premium",
                f"• Invalid emoji IDs",
                f"• Message formatting errors"
            ]
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Emoji Menu", callback_data="premium_emoji_menu")]
        ])
        
        await callback_query.edit_message_text("\n".join(success_msg), reply_markup=back_keyboard)
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("emoji_report"))
async def emoji_report_callback(client: Client, callback_query: CallbackQuery):
    """Show emoji report"""
    
    try:
        emoji_mapper = PremiumEmojiMapper(client)
        report = emoji_mapper.get_emoji_report()
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Emoji Menu", callback_data="premium_emoji_menu")]
        ])
        
        await callback_query.edit_message_text(report, reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("autobot_main"))
async def return_to_main_menu(client: Client, callback_query: CallbackQuery):
    """Return to main autonomous bot menu"""
    
    try:
        # Recreate main menu (simplified for callback)
        bot_creator = AutonomousBotCreator(client)
        created_count = bot_creator.created_bots.get("total_created", 0)
        
        menu_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('utama')} **AUTONOMOUS BOT CREATOR**",
            "",
            f"Bots Created: {bold(str(created_count))}",
            f"Status: {bold('✓ Active')}",
            "",
            f"{italic('Select an option to continue')}"
        ]
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('centang')} Create Single", callback_data="autobot_create_single"),
                InlineKeyboardButton(f"{emoji('loading')} Create Multiple", callback_data="autobot_create_multiple")
            ],
            [
                InlineKeyboardButton(f"{emoji('aktif')} View Reports", callback_data="autobot_reports"),
                InlineKeyboardButton(f"{emoji('utama')} Premium Emojis", callback_data="premium_emoji_menu")
            ],
            [
                InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="autobot_close")
            ]
        ])
        
        await callback_query.edit_message_text("\n".join(menu_lines), reply_markup=keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("autobot_close|emoji_close"))
async def close_autonomous_menu(client: Client, callback_query: CallbackQuery):
    """Close autonomous bot menu"""
    
    try:
        close_message = [
            f"{emoji('centang')} **Menu Closed**",
            "",
            f"Autonomous Bot Creator & Premium Emoji System",
            f"Use `/autobot` or `/emojipremium` anytime to reopen",
            "",
            f"{italic('Enhanced by Vzoel Autonomous Systems')}"
        ]
        
        await callback_query.edit_message_text("\n".join(close_message))
        await callback_query.answer("Menu closed")
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)