#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Premium Help System with Inline Buttons
Enhanced help dengan inline keyboard, premium emoji mapping, dan markdown support
Created by: VZLfxs @Lutpan Assistant
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.filters import vzoel_command
from pyrogram.enums import ParseMode

# Import sistem terintegrasi premium
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace, vzoel_signature, emoji

class VzoelHelpSystem:
    """Premium Help System dengan inline keyboard dan auto-discovery"""
    
    def __init__(self):
        self.commands_data = self._load_commands_data()
        self.categories = self._organize_categories()
        
    def _load_commands_data(self) -> Dict[str, Dict]:
        """Load data commands dari definisi internal"""
        return {
            "start": {
                "description": "Memulai bot dan menampilkan welcome message",
                "usage": ".start",
                "category": "basic",
                "emoji": "utama",
                "examples": [".start"]
            },
            "help": {
                "description": "Menampilkan menu bantuan dengan inline keyboard",
                "usage": ".help [kategori]",
                "category": "basic", 
                "emoji": "loading",
                "examples": [".help", ".help basic", ".help admin"]
            },
            "ping": {
                "description": "Mengecek response time bot dan status koneksi",
                "usage": ".ping",
                "category": "basic",
                "emoji": "aktif",
                "examples": [".ping"]
            },
            "alive": {
                "description": "Menampilkan status bot dan informasi system",
                "usage": ".alive",
                "category": "basic",
                "emoji": "centang",
                "examples": [".alive"]
            },
            "info": {
                "description": "Menampilkan informasi lengkap bot dan assets",
                "usage": ".info",
                "category": "basic",
                "emoji": "telegram",
                "examples": [".info"]
            },
            "gcast": {
                "description": "Broadcast pesan ke semua grup (admin only)",
                "usage": ".gcast <pesan>",
                "category": "admin",
                "emoji": "telegram",
                "examples": [".gcast Hello everyone!", ".gcast -bold Important announcement"]
            },
            "addbl": {
                "description": "Menambahkan grup ke blacklist broadcast",
                "usage": ".addbl [chat_id]",
                "category": "admin",
                "emoji": "adder2",
                "examples": [".addbl", ".addbl -1001234567890"]
            },
            "rmbl": {
                "description": "Menghapus grup dari blacklist broadcast",
                "usage": ".rmbl [chat_id]",
                "category": "admin", 
                "emoji": "adder1",
                "examples": [".rmbl", ".rmbl -1001234567890"]
            },
            "listbl": {
                "description": "Menampilkan daftar grup dalam blacklist",
                "usage": ".listbl",
                "category": "admin",
                "emoji": "proses",
                "examples": [".listbl"]
            },
            "clearbl": {
                "description": "Menghapus semua grup dari blacklist (konfirmasi required)",
                "usage": ".clearbl confirm",
                "category": "admin",
                "emoji": "merah",
                "examples": [".clearbl confirm"]
            }
        }
    
    def _organize_categories(self) -> Dict[str, List[str]]:
        """Organize commands by categories"""
        categories = {}
        for cmd, data in self.commands_data.items():
            category = data.get("category", "other")
            if category not in categories:
                categories[category] = []
            categories[category].append(cmd)
        return categories
    
    def get_category_emoji(self, category: str) -> str:
        """Get emoji untuk setiap kategori"""
        category_emojis = {
            "basic": "utama",
            "admin": "petir", 
            "broadcast": "telegram",
            "system": "loading",
            "fun": "kuning",
            "other": "proses"
        }
        return emoji(category_emojis.get(category, "proses"))
    
    def get_category_description(self, category: str) -> str:
        """Get description untuk setiap kategori"""
        descriptions = {
            "basic": "Perintah dasar untuk semua user",
            "admin": "Perintah khusus admin dan owner", 
            "broadcast": "Sistem broadcast dan gcast",
            "system": "Perintah sistem dan maintenance",
            "fun": "Perintah hiburan dan fun features",
            "other": "Perintah lainnya"
        }
        return descriptions.get(category, "Perintah lainnya")
    
    def create_main_keyboard(self) -> InlineKeyboardMarkup:
        """Buat keyboard utama dengan kategori"""
        buttons = []
        
        # Buat tombol untuk setiap kategori
        for category, commands in self.categories.items():
            emoji_char = self.get_category_emoji(category)
            button_text = f"{emoji_char} {category.title()} ({len(commands)})"
            buttons.append([InlineKeyboardButton(button_text, callback_data=f"help_cat_{category}")])
        
        # Tambah tombol khusus
        buttons.append([
            InlineKeyboardButton(f"{emoji('loading')} All Commands", callback_data="help_all"),
            InlineKeyboardButton(f"{emoji('telegram')} About Bot", callback_data="help_about")
        ])
        
        buttons.append([InlineKeyboardButton(f"{emoji('merah')} Close Menu", callback_data="help_close")])
        
        return InlineKeyboardMarkup(buttons)
    
    def create_category_keyboard(self, category: str) -> InlineKeyboardMarkup:
        """Buat keyboard untuk kategori spesifik"""
        buttons = []
        commands = self.categories.get(category, [])
        
        # Buat tombol untuk setiap command dalam kategori
        for i in range(0, len(commands), 2):
            row = []
            for j in range(2):
                if i + j < len(commands):
                    cmd = commands[i + j]
                    cmd_data = self.commands_data[cmd]
                    cmd_emoji = emoji(cmd_data.get("emoji", "proses"))
                    row.append(InlineKeyboardButton(
                        f"{cmd_emoji} {cmd}", 
                        callback_data=f"help_cmd_{cmd}"
                    ))
            buttons.append(row)
        
        # Tombol navigasi
        buttons.append([
            InlineKeyboardButton(f"{emoji('centang')} Back to Menu", callback_data="help_main"),
            InlineKeyboardButton(f"{emoji('merah')} Close", callback_data="help_close")
        ])
        
        return InlineKeyboardMarkup(buttons)
    
    def create_command_keyboard(self, command: str) -> InlineKeyboardMarkup:
        """Buat keyboard untuk command spesifik"""
        buttons = [
            [InlineKeyboardButton(f"{emoji('centang')} Back to Category", callback_data=f"help_cat_{self.commands_data[command]['category']}")],
            [InlineKeyboardButton(f"{emoji('utama')} Main Menu", callback_data="help_main")],
            [InlineKeyboardButton(f"{emoji('merah')} Close", callback_data="help_close")]
        ]
        return InlineKeyboardMarkup(buttons)
    
    def format_main_help(self) -> str:
        """Format pesan help utama dengan premium styling"""
        signature = vzoel_signature()
        
        lines = [
            f"{signature}",
            "",
            f"{emoji('loading')} **VZOEL HELP SYSTEM**",
            "",
            f"Selamat datang di sistem bantuan {bold('Vzoel VZLfxs @Lutpan Assistant')}!",
            f"Pilih kategori di bawah untuk melihat perintah yang tersedia:",
            ""
        ]
        
        # Tampilkan ringkasan kategori
        for category, commands in self.categories.items():
            category_emoji = self.get_category_emoji(category)
            category_desc = self.get_category_description(category)
            lines.append(f"{category_emoji} **{category.title()}** - {category_desc} ({bold(str(len(commands)))} commands)")
        
        lines.extend([
            "",
            f"{emoji('utama')} **Total Commands:** {bold(str(len(self.commands_data)))}",
            f"{emoji('aktif')} **Prefix:** {monospace('.')} (dot)",
            "",
            f"{italic('Gunakan tombol di bawah untuk navigasi!')}"
        ])
        
        return "\n".join(lines)
    
    def format_category_help(self, category: str) -> str:
        """Format help untuk kategori spesifik"""
        if category not in self.categories:
            return f"{emoji('merah')} Kategori tidak ditemukan!"
        
        commands = self.categories[category]
        category_emoji = self.get_category_emoji(category)
        category_desc = self.get_category_description(category)
        
        lines = [
            f"{vzoel_signature()}",
            "",
            f"{category_emoji} **{category.upper()} COMMANDS**",
            "",
            f"{italic(category_desc)}",
            f"Total perintah: {bold(str(len(commands)))}",
            ""
        ]
        
        for cmd in commands:
            cmd_data = self.commands_data[cmd]
            cmd_emoji = emoji(cmd_data.get("emoji", "proses"))
            lines.append(f"{cmd_emoji} **{cmd}** - {cmd_data['description']}")
        
        lines.extend([
            "",
            f"{emoji('centang')} Klik tombol command di bawah untuk detail lengkap!",
            f"{emoji('loading')} Atau kembali ke menu utama."
        ])
        
        return "\n".join(lines)
    
    def format_command_help(self, command: str) -> str:
        """Format help untuk command spesifik"""
        if command not in self.commands_data:
            return f"{emoji('merah')} Command tidak ditemukan!"
        
        cmd_data = self.commands_data[command]
        cmd_emoji = emoji(cmd_data.get("emoji", "proses"))
        
        lines = [
            f"{vzoel_signature()}",
            "",
            f"{cmd_emoji} **COMMAND: {command.upper()}**",
            "",
            f"{emoji('telegram')} **Deskripsi:**",
            f"{cmd_data['description']}",
            "",
            f"{emoji('loading')} **Penggunaan:**",
            f"{monospace(cmd_data['usage'])}",
            "",
            f"{emoji('centang')} **Kategori:** {bold(cmd_data['category'].title())}",
            ""
        ]
        
        # Tambah contoh jika ada
        if "examples" in cmd_data and cmd_data["examples"]:
            lines.append(f"{emoji('kuning')} **Contoh Penggunaan:**")
            for example in cmd_data["examples"]:
                lines.append(f"• {monospace(example)}")
            lines.append("")
        
        # Tambah catatan khusus jika ada
        if command in ["gcast", "addbl", "rmbl", "clearbl"]:
            lines.extend([
                f"{emoji('petir')} **Catatan Penting:**",
                f"Command ini memerlukan akses admin atau owner.",
                ""
            ])
        
        lines.append(f"{italic('Gunakan tombol di bawah untuk navigasi!')}")
        
        return "\n".join(lines)
    
    def format_about_page(self) -> str:
        """Format halaman about bot"""
        asset_info = vzoel_assets.get_asset_info()
        
        lines = [
            f"{vzoel_signature()}",
            "",
            f"{emoji('utama')} **ABOUT VZOEL ASSISTANT**",
            "",
            f"{emoji('centang')} **Framework:** Pyrogram + uvloop",
            f"{emoji('loading')} **Version:** Premium v2.0.0", 
            f"{emoji('aktif')} **Created by:** VZLfxs @Lutpan",
            "",
            f"{emoji('petir')} **Premium Features:**",
            f"• Enhanced Markdown Support",
            f"• Premium Emoji Collection ({bold(str(asset_info['emojis']['total_emojis']))} emojis)",
            f"• Interactive Inline Keyboards",
            f"• High-Performance Framework",
            f"• Auto Plugin Discovery",
            "",
            f"{emoji('telegram')} **Asset Information:**",
            f"• Font Styles: {bold(str(asset_info['fonts']['total_styles']))}",
            f"• Emoji Categories: {bold(str(asset_info['emojis']['total_categories']))}",
            f"• Asset Version: {bold(asset_info['version'])}",
            "",
            f"{emoji('adder2')} {italic('Enhanced by Vzoel VZLfxs @Lutpan Premium Collection')}"
        ]
        
        return "\n".join(lines)
    
    def format_all_commands(self) -> str:
        """Format daftar semua commands"""
        lines = [
            f"{vzoel_signature()}",
            "",
            f"{emoji('loading')} **ALL COMMANDS LIST**",
            "",
            f"Berikut adalah daftar lengkap semua perintah yang tersedia:",
            ""
        ]
        
        for category, commands in self.categories.items():
            category_emoji = self.get_category_emoji(category)
            lines.append(f"{category_emoji} **{category.upper()}:**")
            
            for cmd in commands:
                cmd_data = self.commands_data[cmd]
                cmd_emoji = emoji(cmd_data.get("emoji", "proses"))
                lines.append(f"  {cmd_emoji} {monospace('.' + cmd)} - {cmd_data['description']}")
            
            lines.append("")
        
        lines.extend([
            f"{emoji('centang')} **Total:** {bold(str(len(self.commands_data)))} commands",
            f"{emoji('utama')} Gunakan tombol untuk kembali ke menu utama!"
        ])
        
        return "\n".join(lines)

# Initialize help system
help_system = VzoelHelpSystem()

@Client.on_message(filters.command("help") & filters.me)
async def help_command(client: VzoelClient, message: Message):
    """Main help command dengan inline keyboard"""
    args = get_arguments(message)
    
    try:
        if args:
            # Jika ada argumen, tampilkan help untuk kategori/command spesifik
            if args in help_system.categories:
                text = help_system.format_category_help(args)
                keyboard = help_system.create_category_keyboard(args)
            elif args in help_system.commands_data:
                text = help_system.format_command_help(args)
                keyboard = help_system.create_command_keyboard(args)
            else:
                text = f"{emoji('merah')} Kategori atau command '{args}' tidak ditemukan!"
                keyboard = help_system.create_main_keyboard()
        else:
            # Default: tampilkan menu utama
            text = help_system.format_main_help()
            keyboard = help_system.create_main_keyboard()
        
        await message.reply_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        LOGGER.error(f"Error in help command: {e}")
        error_text = f"{emoji('merah')} Terjadi error saat memproses help command: {str(e)}"
        await message.reply_text(error_text)

@Client.on_callback_query(filters.regex(r"^help_"))
async def help_callback_handler(client: VzoelClient, callback_query: CallbackQuery):
    """Handler untuk callback query help system"""
    data = callback_query.data
    
    try:
        if data == "help_main":
            # Kembali ke menu utama
            text = help_system.format_main_help()
            keyboard = help_system.create_main_keyboard()
            
        elif data == "help_all":
            # Tampilkan semua commands
            text = help_system.format_all_commands()
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(f"{emoji('utama')} Main Menu", callback_data="help_main"),
                InlineKeyboardButton(f"{emoji('merah')} Close", callback_data="help_close")
            ]])
            
        elif data == "help_about":
            # Tampilkan about page
            text = help_system.format_about_page()
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(f"{emoji('utama')} Main Menu", callback_data="help_main"),
                InlineKeyboardButton(f"{emoji('merah')} Close", callback_data="help_close")
            ]])
            
        elif data == "help_close":
            # Close menu
            await callback_query.message.delete()
            await callback_query.answer(f"{emoji('centang')} Help menu ditutup!")
            return
            
        elif data.startswith("help_cat_"):
            # Tampilkan kategori spesifik
            category = data.replace("help_cat_", "")
            text = help_system.format_category_help(category)
            keyboard = help_system.create_category_keyboard(category)
            
        elif data.startswith("help_cmd_"):
            # Tampilkan command spesifik
            command = data.replace("help_cmd_", "")
            text = help_system.format_command_help(command)
            keyboard = help_system.create_command_keyboard(command)
            
        else:
            # Unknown callback
            await callback_query.answer(f"{emoji('merah')} Unknown action!")
            return
        
        # Edit message dengan konten baru
        await callback_query.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Answer callback query
        await callback_query.answer()
        
    except Exception as e:
        LOGGER.error(f"Error in help callback: {e}")
        await callback_query.answer(f"{emoji('merah')} Error: {str(e)}")

# Register plugin info
LOGGER.info(f"{emoji('centang')} Premium Help System loaded with {len(help_system.commands_data)} commands")