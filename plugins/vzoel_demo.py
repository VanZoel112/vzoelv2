"""
Vzoel Demo Plugin - Showcase Font & Emoji Premium Features
Demonstrasi lengkap penggunaan asset premium Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

# Initialize assets manager
assets = VzoelAssets()

@Client.on_message(filters.command("vzoel"))
async def vzoel_showcase(client, message):
    """Showcase Vzoel Fox's premium features"""
    
    # Format title dengan signature
    title = assets.vzoel_signature()
    
    # Build showcase message
    showcase_text = f"{title}\n\n"
    
    # Font demonstrations
    showcase_text += f"{emoji('utama')} **Font Styling Showcase:**\n"
    showcase_text += f"Bold: {bold('Vzoel Fox Premium')}\n"
    showcase_text += f"Italic: {italic('Enhanced Experience')}\n"
    showcase_text += f"Monospace: {assets.monospace('System Ready')}\n\n"
    
    # Emoji demonstrations  
    showcase_text += f"{emoji('petir')} **Premium Emoji Collection:**\n"
    for category in ["primary", "system", "fun", "special"]:
        emojis = assets.get_emojis_by_category(category)
        showcase_text += f"{category.title()}: {' '.join(emojis)}\n"
    
    showcase_text += f"\n{emoji('centang')} Status: Sistem Premium Aktif!"
    
    # Create interactive buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎨 Font Test", callback_data="vzoel_font"),
            InlineKeyboardButton("😀 Emoji Test", callback_data="vzoel_emoji")
        ],
        [
            InlineKeyboardButton("🎭 Theme Test", callback_data="vzoel_theme"),
            InlineKeyboardButton("📊 Asset Info", callback_data="vzoel_info")
        ]
    ])
    
    await message.reply_text(showcase_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("vzoel_font"))
async def font_demo(client, callback_query):
    """Interactive font styling demo"""
    
    demo_text = f"{emoji('utama')} **Font Styling Demo**\n\n"
    
    sample_texts = [
        "Vzoel Fox's Assistant",
        "Premium Quality Bot",
        "Enhanced Experience",
        "System Ready 2025"
    ]
    
    for text in sample_texts:
        demo_text += f"Original: {text}\n"
        demo_text += f"Bold: {bold(text)}\n"
        demo_text += f"Italic: {italic(text)}\n"
        demo_text += f"Mono: {assets.monospace(text)}\n\n"
    
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="vzoel_back")]
    ])
    
    await callback_query.edit_message_text(demo_text, reply_markup=back_keyboard)

@Client.on_callback_query(filters.regex("vzoel_emoji"))
async def emoji_demo(client, callback_query):
    """Interactive emoji demo"""
    
    demo_text = f"{emoji('petir')} **Premium Emoji Demo**\n\n"
    
    # Show command patterns
    demo_text += "**Command Response Patterns:**\n"
    commands = ["ping", "alive", "gcast", "vzoel"]
    for cmd in commands:
        pattern_emojis = assets.get_usage_pattern(cmd)
        if pattern_emojis:
            demo_text += f"/{cmd}: {' '.join(pattern_emojis)}\n"
    
    demo_text += "\n**Status Indicators:**\n"
    statuses = ["success", "loading", "error", "active"]
    for status in statuses:
        status_emojis = assets.get_status_emojis(status)
        if status_emojis:
            demo_text += f"{status}: {' '.join(status_emojis)}\n"
    
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="vzoel_back")]
    ])
    
    await callback_query.edit_message_text(demo_text, reply_markup=back_keyboard)

@Client.on_callback_query(filters.regex("vzoel_theme"))
async def theme_demo(client, callback_query):
    """Interactive theme demo"""
    
    demo_text = f"{emoji('biru')} **Theme Combination Demo**\n\n"
    
    themes = ["vzoel_primary", "vzoel_fun", "vzoel_system", "vzoel_special"]
    
    for theme in themes:
        theme_emojis = assets.get_theme_emojis(theme)
        if theme_emojis:
            theme_name = theme.replace("vzoel_", "").title()
            demo_text += f"**{theme_name} Theme:** {' '.join(theme_emojis)}\n"
            demo_text += f"Perfect for: {theme.replace('_', ' ')} commands\n\n"
    
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="vzoel_back")]
    ])
    
    await callback_query.edit_message_text(demo_text, reply_markup=back_keyboard)

@Client.on_callback_query(filters.regex("vzoel_info"))
async def asset_info(client, callback_query):
    """Show comprehensive asset information"""
    
    info = assets.get_asset_info()
    
    info_text = f"{emoji('aktif')} **Asset Information**\n\n"
    
    # Font info
    info_text += "**Font System:**\n"
    info_text += f"Styles: {', '.join(info['fonts']['available_styles'])}\n"
    info_text += f"Total: {info['fonts']['total_styles']} styles\n\n"
    
    # Emoji info
    info_text += "**Emoji System:**\n"
    info_text += f"Total Emojis: {info['emojis']['total_emojis']}\n"
    info_text += f"Categories: {info['emojis']['total_categories']}\n"
    info_text += f"Version: {info['version']}\n\n"
    
    # Branding info
    branding = info.get('branding', {})
    info_text += "**Branding:**\n"
    for key, value in branding.items():
        info_text += f"{key.replace('_', ' ').title()}: {value}\n"
    
    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back", callback_data="vzoel_back")]
    ])
    
    await callback_query.edit_message_text(info_text, reply_markup=back_keyboard)

@Client.on_callback_query(filters.regex("vzoel_back"))
async def back_to_main(client, callback_query):
    """Return to main vzoel showcase"""
    # Re-run the main showcase
    await vzoel_showcase(client, callback_query.message)

@Client.on_message(filters.command("ping"))
async def ping_premium(client, message):
    """Enhanced ping command with premium assets"""
    
    # Use loading pattern first
    loading_emojis = assets.get_status_emojis("loading")
    loading_msg = f"{loading_emojis[0]} {italic('Checking connection...')}"
    
    sent = await message.reply_text(loading_msg)
    
    # Calculate ping (simplified)
    import time
    start_time = time.time()
    # Simulate some processing
    await asyncio.sleep(0.1)
    ping_time = round((time.time() - start_time) * 1000, 2)
    
    # Use success pattern
    success_emojis = assets.get_status_emojis("success")
    result_msg = vzoel_msg(f"Pong! {ping_time}ms", "bold", "ping")
    
    await sent.edit_text(result_msg)

@Client.on_message(filters.command("alive"))
async def alive_premium(client, message):
    """Enhanced alive command with premium assets"""
    
    alive_text = f"{assets.vzoel_signature()}\n\n"
    alive_text += vzoel_msg("Bot Status: Online", "bold", "alive") + "\n"
    alive_text += f"{emoji('aktif')} System: Premium Mode\n"
    alive_text += f"{emoji('centang')} Assets: Loaded Successfully\n"
    alive_text += f"{emoji('petir')} Performance: Optimized\n\n"
    alive_text += f"{italic('Enhanced by Vzoel Fox\\'s Premium Assets')}"
    
    await message.reply_text(alive_text)

# Example of using assets in existing help plugin enhancement
@Client.on_message(filters.command("vhelp"))
async def enhanced_help(client, message):
    """Enhanced help with premium styling"""
    
    help_text = f"{assets.vzoel_signature()}\n\n"
    help_text += f"{bold('Available Commands:')}\n\n"
    
    commands = [
        ("/vzoel", "Showcase premium features", "vzoel"),
        ("/ping", "Check bot response time", "ping"), 
        ("/alive", "Check bot status", "alive"),
        ("/vhelp", "Show this help message", None)
    ]
    
    for cmd, desc, pattern in commands:
        if pattern:
            pattern_emojis = assets.get_usage_pattern(pattern)
            if pattern_emojis:
                help_text += f"{pattern_emojis[0]} {bold(cmd)} - {desc}\n"
            else:
                help_text += f"{emoji('centang')} {bold(cmd)} - {desc}\n"
        else:
            help_text += f"{emoji('centang')} {bold(cmd)} - {desc}\n"
    
    help_text += f"\n{italic('Powered by Vzoel Fox\\'s Premium Assets')}"
    
    await message.reply_text(help_text)

import asyncio