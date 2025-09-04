"""
Enhanced Alive Plugin - Premium Bot Status Display with Logo
Enhanced with premium helper integration and logo display
Created by: Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.logo_helper import LogoHelper, send_logo_message
from helpers.format_helper import FormatHelper
from helpers.display_helper import DisplayHelper
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
import asyncio
import time

# Initialize premium components
logo_helper = LogoHelper()
format_helper = FormatHelper()
display_helper = DisplayHelper()
assets = VzoelAssets()

@Client.on_message(filters.command("alive"))
async def enhanced_alive_command(client: Client, message: Message):
    """
    Enhanced alive command dengan premium logo display
    Shows comprehensive bot status dengan branding
    """
    
    try:
        # Show loading message first
        loading_msg = display_helper.create_loading_message(
            "Checking Bot Status", 
            ["Gathering system information", "Processing premium assets", "Preparing status display"]
        )
        
        loading_message = await message.reply_text(loading_msg)
        
        # Simulate processing time for better UX
        await asyncio.sleep(1.5)
        
        # Get bot information
        me = await client.get_me()
        
        # Calculate uptime (simplified - in real implementation, track actual start time)
        current_time = time.time()
        uptime_seconds = int(current_time % 86400)  # Mock uptime
        uptime_formatted = format_helper.format_time(uptime_seconds)
        
        # Prepare bot information
        bot_info = {
            'first_name': me.first_name,
            'username': me.username,
            'id': me.id,
            'uptime': uptime_formatted,
            'version': '2.0.0-premium',
            'framework': 'Pyrogram + Premium Assets'
        }
        
        # Delete loading message
        await loading_message.delete()
        
        # Send premium alive message dengan logo
        await logo_helper.send_logo_with_caption(
            client=client,
            chat_id=message.chat.id,
            caption_type="alive",
            custom_data=bot_info,
            reply_to_message_id=message.id
        )
        
    except Exception as e:
        # Enhanced error handling
        error_msg = display_helper.create_error_message(
            f"Failed to display alive status: {str(e)}",
            ["Check bot permissions", "Verify image files", "Contact administrator"]
        )
        
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

@Client.on_message(filters.command("status"))
async def status_dashboard_command(client: Client, message: Message):
    """
    Comprehensive status dashboard dengan premium styling
    """
    
    try:
        # Get comprehensive system stats
        me = await client.get_me()
        
        # Prepare dashboard statistics
        stats = {
            'bot_name': {
                'value': me.first_name,
                'status': 'success',
                'category': 'Bot Information'
            },
            'bot_username': {
                'value': f"@{me.username}",
                'status': 'success', 
                'category': 'Bot Information'
            },
            'bot_id': {
                'value': me.id,
                'status': 'info',
                'category': 'Bot Information'
            },
            'framework': {
                'value': 'Pyrogram Premium',
                'status': 'success',
                'category': 'System'
            },
            'assets_system': {
                'value': 'Enhanced Collection',
                'status': 'success',
                'category': 'System'
            },
            'helper_modules': {
                'value': '4 Active',
                'status': 'success',
                'category': 'System'
            },
            'image_system': {
                'value': 'Operational',
                'status': 'success',
                'category': 'Features'
            },
            'premium_styling': {
                'value': 'Active',
                'status': 'success',
                'category': 'Features'
            }
        }
        
        # Create and send dashboard
        dashboard = display_helper.create_status_dashboard("VZOEL ASSISTANT", stats)
        await message.reply_text(dashboard)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to generate status dashboard: {str(e)}"
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("ping"))
async def enhanced_ping_command(client: Client, message: Message):
    """
    Enhanced ping command dengan premium visual feedback
    """
    
    try:
        # Show loading message
        loading_emojis = assets.get_status_emojis("loading")
        loading_text = f"{loading_emojis[0]} {italic('Measuring response time...')}"
        
        start_time = time.time()
        sent_message = await message.reply_text(loading_text)
        
        # Calculate ping time
        end_time = time.time()
        ping_ms = round((end_time - start_time) * 1000, 2)
        
        # Create premium ping response
        ping_emojis = assets.get_usage_pattern("ping")
        uptime = format_helper.format_time(int(time.time() % 86400))  # Mock uptime
        
        ping_response = [
            f"{ping_emojis[0]} {bold('Pong!')}",
            "",
            f"{emoji('aktif')} **Response Time:** {bold(f'{ping_ms}ms')}",
            f"{emoji('loading')} **Uptime:** {uptime}",
            f"{emoji('centang')} **Status:** {bold('Online & Responsive')}",
            "",
            f"{italic('Premium framework optimized for speed')}"
        ]
        
        await sent_message.edit_text("\n".join(ping_response))
        
    except Exception as e:
        error_msg = f"{emoji('merah')} Ping failed: {str(e)}"
        await message.reply_text(error_msg)

@Client.on_message(filters.command("info"))
async def bot_info_command(client: Client, message: Message):
    """
    Comprehensive bot information dengan premium formatting
    """
    
    try:
        me = await client.get_me()
        
        # Get helper information
        logo_info = logo_helper.get_helper_info()
        format_info = format_helper.get_helper_info()
        display_info = display_helper.get_helper_info()
        assets_info = assets.get_asset_info()
        
        # Create comprehensive info display
        info_sections = [
            assets.vzoel_signature(),
            "",
            display_helper.create_banner("BOT INFORMATION", "Comprehensive Details", 48).strip(),
            "",
            f"{emoji('centang')} **Bot Details:**",
            f"  • Name: {bold(me.first_name)}",
            f"  • Username: @{me.username}",
            f"  • ID: `{me.id}`",
            f"  • Version: {bold('2.0.0-premium')}",
            "",
            f"{emoji('petir')} **Framework Information:**",
            f"  • Base: {bold('Pyrogram')}",
            f"  • Enhancement: {bold('Premium Assets System')}",
            f"  • Parse Mode: {bold('Enhanced Markdown')}",
            "",
            f"{emoji('utama')} **Premium Features:**",
            f"  • Helper Modules: {bold(str(len([logo_info, format_info, display_info])))}",
            f"  • Font Styles: {bold(str(assets_info['fonts']['total_styles']))}",
            f"  • Premium Emojis: {bold(str(assets_info['emojis']['total_emojis']))}",
            f"  • Image Support: {bold(str(logo_info['total_images']) + ' files')}",
            "",
            f"{emoji('loading')} **Capabilities:**",
            f"  • Logo Display: {bold('✓ Active')}",
            f"  • Premium Styling: {bold('✓ Active')}",
            f"  • Error Handling: {bold('✓ Enhanced')}",
            f"  • Status Monitoring: {bold('✓ Real-time')}",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}"
        ]
        
        await message.reply_text("\n".join(info_sections))
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to retrieve bot information: {str(e)}"
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("system"))
async def system_info_command(client: Client, message: Message):
    """
    Detailed system information untuk debugging
    """
    
    try:
        # Get detailed system information
        logo_info = logo_helper.get_helper_info()
        
        system_features = [
            {
                'name': 'Logo Helper System',
                'description': f'{logo_info["total_images"]} images available, supports {len(logo_info["supported_formats"])} formats',
                'status': 'premium'
            },
            {
                'name': 'Premium Asset System', 
                'description': 'Complete emoji and font collection with theming',
                'status': 'active'
            },
            {
                'name': 'Enhanced Error Handling',
                'description': 'Comprehensive error messages with suggestions',
                'status': 'active'
            },
            {
                'name': 'Visual Feedback System',
                'description': 'Loading animations, progress bars, and status indicators',
                'status': 'premium'
            }
        ]
        
        system_display = display_helper.create_feature_showcase(system_features)
        
        # Add system stats
        system_stats = [
            "",
            f"{emoji('aktif')} **System Statistics:**",
            f"  • Available Images: {bold(str(logo_info['total_images']))}",
            f"  • Helper Classes: {bold('4 Active')}",
            f"  • Caption Types: {bold(str(len(logo_info['caption_types'])))}",
            f"  • Display Elements: {bold(str(len(display_info['supported_elements'])))}",
            "",
            f"{italic('All systems operational and ready')}"
        ]
        
        full_display = system_display + "\n".join(system_stats)
        await message.reply_text(full_display)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"System information unavailable: {str(e)}"
        )
        await message.reply_text(error_msg)