"""
Enhanced Help Plugin - Premium Help System with Logo Display
Enhanced with premium helper integration and interactive navigation
Created by: Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from helpers.logo_helper import LogoHelper
from helpers.display_helper import DisplayHelper
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

# Initialize premium components
logo_helper = LogoHelper()
display_helper = DisplayHelper()
assets = VzoelAssets()

# Comprehensive help database dengan kategorisasi
HELP_CATEGORIES = {
    "basic": {
        "title": "Basic Commands",
        "description": "Essential commands untuk penggunaan sehari-hari",
        "emoji": "centang",
        "commands": [
            {
                "command": "/start",
                "description": "Memulai bot dan menampilkan pesan selamat datang",
                "usage": "/start"
            },
            {
                "command": "/help",
                "description": "Menampilkan menu bantuan interaktif dengan logo",
                "usage": "/help [kategori]"
            },
            {
                "command": "/alive", 
                "description": "Cek status bot dengan tampilan premium dan logo",
                "usage": "/alive"
            },
            {
                "command": "/ping",
                "description": "Mengukur response time bot dengan styling premium",
                "usage": "/ping"
            }
        ]
    },
    "system": {
        "title": "System Commands",
        "description": "Commands untuk monitoring dan informasi sistem",
        "emoji": "loading",
        "commands": [
            {
                "command": "/status",
                "description": "Dashboard lengkap status sistem dengan statistics",
                "usage": "/status"
            },
            {
                "command": "/info", 
                "description": "Informasi lengkap tentang bot dan capabilities",
                "usage": "/info"
            },
            {
                "command": "/system",
                "description": "Detailed system information untuk debugging",
                "usage": "/system"
            },
            {
                "command": "/vzoel",
                "description": "Showcase premium features dan asset system",
                "usage": "/vzoel"
            }
        ]
    },
    "premium": {
        "title": "Premium Features", 
        "description": "Fitur-fitur premium exclusive Vzoel Assistant",
        "emoji": "utama",
        "commands": [
            {
                "command": "/logo",
                "description": "Display logo dengan berbagai caption types",
                "usage": "/logo [type]"
            },
            {
                "command": "/gallery",
                "description": "Tampilkan gallery semua images yang tersedia",
                "usage": "/gallery"
            },
            {
                "command": "/style",
                "description": "Demonstrasi premium styling dan formatting",
                "usage": "/style [text]"
            },
            {
                "command": "/theme",
                "description": "Explore berbagai theme combinations",
                "usage": "/theme [theme_name]"
            }
        ]
    },
    "tools": {
        "title": "Utility Tools",
        "description": "Tools dan utilities untuk productive tasks", 
        "emoji": "aktif",
        "commands": [
            {
                "command": "/format",
                "description": "Format text dengan premium styling options",
                "usage": "/format <text> [style]"
            },
            {
                "command": "/time",
                "description": "Display waktu dengan formatting premium",
                "usage": "/time [format]"
            },
            {
                "command": "/calc",
                "description": "Calculator dengan premium output formatting",
                "usage": "/calc <expression>"
            }
        ]
    }
}

@Client.on_message(filters.command("help"))
async def enhanced_help_command(client: Client, message: Message):
    """
    Enhanced help command dengan logo display dan interactive navigation
    """
    
    try:
        # Extract category dari command arguments
        command_parts = message.text.split()
        requested_category = command_parts[1] if len(command_parts) > 1 else None
        
        # Show specific category help
        if requested_category and requested_category in HELP_CATEGORIES:
            await show_category_help(client, message, requested_category)
            return
        
        # Show main help dengan logo
        total_commands = sum(len(cat["commands"]) for cat in HELP_CATEGORIES.values())
        
        # Prepare help data
        help_data = {
            'command_count': total_commands,
            'categories': list(HELP_CATEGORIES.keys()),
            'version': '2.0.0-premium'
        }
        
        # Create navigation keyboard
        keyboard = create_help_navigation_keyboard()
        
        # Send help dengan logo
        sent_message = await logo_helper.send_logo_with_caption(
            client=client,
            chat_id=message.chat.id,
            caption_type="help",
            custom_data=help_data,
            reply_to_message_id=message.id
        )
        
        # Add navigation buttons if message sent successfully
        if sent_message and keyboard:
            try:
                await sent_message.edit_reply_markup(reply_markup=keyboard)
            except:
                # If edit fails, send keyboard separately
                keyboard_msg = create_category_overview()
                await message.reply_text(keyboard_msg, reply_markup=keyboard)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to display help: {str(e)}",
            ["Try /help again", "Use /help <category>", "Contact administrator"]
        )
        await message.reply_text(error_msg)

def create_help_navigation_keyboard() -> InlineKeyboardMarkup:
    """Create interactive navigation keyboard untuk help system"""
    
    buttons = []
    
    # Category buttons (2 per row)
    category_buttons = []
    for cat_key, cat_data in HELP_CATEGORIES.items():
        emoji_char = emoji(cat_data["emoji"])
        button_text = f"{emoji_char} {cat_data['title']}"
        category_buttons.append(
            InlineKeyboardButton(button_text, callback_data=f"help_category_{cat_key}")
        )
    
    # Arrange in rows of 2
    for i in range(0, len(category_buttons), 2):
        row = category_buttons[i:i+2]
        buttons.append(row)
    
    # Add utility buttons
    utility_row = [
        InlineKeyboardButton(f"{emoji('loading')} Quick Start", callback_data="help_quickstart"),
        InlineKeyboardButton(f"{emoji('centang')} All Commands", callback_data="help_all")
    ]
    buttons.append(utility_row)
    
    # Add close button
    close_row = [
        InlineKeyboardButton(f"{emoji('merah')} Close Help", callback_data="help_close")
    ]
    buttons.append(close_row)
    
    return InlineKeyboardMarkup(buttons)

def create_category_overview() -> str:
    """Create overview of all available categories"""
    
    overview_lines = [
        "",
        f"{assets.vzoel_signature()}",
        "",
        f"{emoji('centang')} **Available Help Categories:**",
        ""
    ]
    
    for cat_key, cat_data in HELP_CATEGORIES.items():
        emoji_char = emoji(cat_data["emoji"])
        command_count = len(cat_data["commands"])
        
        overview_lines.extend([
            f"{emoji_char} **{cat_data['title']}** ({command_count} commands)",
            f"     {italic(cat_data['description'])}",
            f"     Usage: `/help {cat_key}`",
            ""
        ])
    
    overview_lines.extend([
        f"{emoji('loading')} **Quick Access:**",
        f"• Use buttons above untuk navigate",
        f"• Type `/help <category>` untuk direct access",
        f"• All commands support premium styling",
        "",
        f"{italic('Select a category to explore commands')}"
    ])
    
    return "\n".join(overview_lines)

async def show_category_help(client: Client, message: Message, category: str):
    """Show detailed help untuk specific category"""
    
    if category not in HELP_CATEGORIES:
        await message.reply_text(f"{emoji('merah')} Category '{category}' not found")
        return
    
    cat_data = HELP_CATEGORIES[category]
    
    # Create detailed help display
    help_display = display_helper.create_help_section(cat_data["title"], cat_data["commands"])
    
    # Add navigation info
    navigation_info = [
        "",
        f"{emoji('aktif')} **Navigation:**",
        f"• `/help` - Return to main help",
        f"• `/help <other_category>` - View other categories",
        f"• Available categories: {', '.join(HELP_CATEGORIES.keys())}",
        ""
    ]
    
    full_help = help_display + "\n".join(navigation_info)
    
    # Create back button
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{emoji('loading')} ← Back to Help Menu", callback_data="help_main")]
    ])
    
    await message.reply_text(full_help, reply_markup=back_keyboard)

# Callback query handlers untuk interactive navigation
@Client.on_callback_query(filters.regex(r"help_category_(.+)"))
async def help_category_callback(client: Client, callback_query: CallbackQuery):
    """Handle category selection dari inline buttons"""
    
    try:
        category = callback_query.matches[0].group(1)
        
        if category not in HELP_CATEGORIES:
            await callback_query.answer("❌ Category not found", show_alert=True)
            return
        
        cat_data = HELP_CATEGORIES[category]
        
        # Create category help display
        help_display = display_helper.create_help_section(cat_data["title"], cat_data["commands"])
        
        # Add category description
        category_header = [
            f"{emoji(cat_data['emoji'])} **{cat_data['title']}**",
            f"{italic(cat_data['description'])}",
            ""
        ]
        
        full_display = "\n".join(category_header) + help_display
        
        # Create navigation keyboard
        nav_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"{emoji('loading')} ← Back", callback_data="help_main"),
                InlineKeyboardButton(f"{emoji('centang')} All Commands", callback_data="help_all")
            ]
        ])
        
        await callback_query.edit_message_text(full_display, reply_markup=nav_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("help_main"))
async def help_main_callback(client: Client, callback_query: CallbackQuery):
    """Return to main help menu"""
    
    try:
        # Recreate main help display
        total_commands = sum(len(cat["commands"]) for cat in HELP_CATEGORIES.values())
        
        main_help = logo_helper.create_help_caption(total_commands)
        keyboard = create_help_navigation_keyboard()
        
        await callback_query.edit_message_text(main_help, reply_markup=keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("help_all"))
async def help_all_callback(client: Client, callback_query: CallbackQuery):
    """Show all commands in compact format"""
    
    try:
        all_commands_lines = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('centang')} **All Available Commands**",
            ""
        ]
        
        for cat_key, cat_data in HELP_CATEGORIES.items():
            emoji_char = emoji(cat_data["emoji"])
            all_commands_lines.append(f"{emoji_char} **{cat_data['title']}:**")
            
            for cmd in cat_data["commands"]:
                all_commands_lines.append(f"  • {bold(cmd['command'])} - {cmd['description']}")
            
            all_commands_lines.append("")
        
        all_commands_lines.extend([
            f"{emoji('loading')} **Total Commands:** {bold(str(sum(len(cat['commands']) for cat in HELP_CATEGORIES.values())))}",
            "",
            f"{italic('Use /help <category> for detailed information')}"
        ])
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Help", callback_data="help_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(all_commands_lines), reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("help_quickstart"))
async def help_quickstart_callback(client: Client, callback_query: CallbackQuery):
    """Show quick start guide"""
    
    try:
        quickstart_guide = [
            f"{emoji('utama')} **Quick Start Guide**",
            "",
            f"{emoji('centang')} **Getting Started:**",
            f"1. Type `/alive` to check bot status",
            f"2. Use `/help basic` for essential commands", 
            f"3. Try `/vzoel` for premium features demo",
            f"4. Explore `/system` for detailed information",
            "",
            f"{emoji('loading')} **Tips:**",
            f"• All commands support premium styling",
            f"• Use inline buttons untuk easy navigation",
            f"• Commands with logo display show enhanced UI",
            f"• Type `/help <category>` untuk specific help",
            "",
            f"{emoji('aktif')} **Popular Commands:**",
            f"• `/alive` - Premium status dengan logo",
            f"• `/status` - Comprehensive dashboard",
            f"• `/info` - Complete bot information",
            "",
            f"{italic('Ready to explore? Start dengan any command!')}"
        ]
        
        back_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{emoji('loading')} ← Back to Help", callback_data="help_main")]
        ])
        
        await callback_query.edit_message_text("\n".join(quickstart_guide), reply_markup=back_keyboard)
        await callback_query.answer()
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex("help_close"))
async def help_close_callback(client: Client, callback_query: CallbackQuery):
    """Close help menu"""
    
    try:
        close_message = [
            f"{emoji('centang')} **Help Menu Closed**",
            "",
            f"Thank you for using Vzoel Assistant!",
            f"Type `/help` anytime to reopen this menu.",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}"
        ]
        
        await callback_query.edit_message_text("\n".join(close_message))
        await callback_query.answer("Help menu closed", show_alert=False)
        
    except Exception as e:
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)