# plugins/broadcast/gcast.py

import asyncio
import aiosqlite
import time
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, UserIsBlocked, ChatAdminRequired, MessageNotModified

# Import sistem terintegrasi
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from utils.assets import vzoel_assets, premium_emoji, bold, italic, monospace

DB_PATH = "broadcast_chats.db"

async def init_db():
    """Bikin tabel database kalo belum ada."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER PRIMARY KEY, type TEXT)")
        await db.commit()

def process_message_content(text: str, premium_format: bool = False) -> str:
    """Fungsi terpusat buat ngolah teks dengan premium font style dan emoji."""
    processed_text = text
    style_to_apply = None

    # Deteksi dan terapkan antibug font system
    if "-bold" in text:
        style_to_apply = "bold"
        processed_text = text.replace("-bold", "").strip()
    elif "-italic" in text:
        style_to_apply = "italic"
        processed_text = text.replace("-italic", "").strip()
    elif "-monospace" in text:
        style_to_apply = "monospace"
        processed_text = text.replace("-monospace", "").strip()
    
    # Terapkan antibug font menggunakan VzoelAssets
    if style_to_apply == "bold":
        processed_text = bold(processed_text)
    elif style_to_apply == "italic":
        processed_text = italic(processed_text)
    elif style_to_apply == "monospace":
        processed_text = monospace(processed_text)

    # Ganti shortcode emoji dengan premium mapping
    for emoji_key in vzoel_assets.emojis.get("emojis", {}):
        shortcode = f":{emoji_key}:"
        if shortcode in processed_text:
            if premium_format:
                emoji_replacement = premium_emoji(emoji_key)
            else:
                emoji_replacement = vzoel_assets.get_emoji(emoji_key)
            processed_text = processed_text.replace(shortcode, emoji_replacement)
        
    return processed_text

@VzoelClient.on_message(CMD_HANDLER)
async def broadcast_router(client: VzoelClient, message: Message):
    """Router utama buat semua perintah yang berhubungan dengan gcast."""
    command = get_command(message)
    
    if command == "updatechats":
        await update_chats_handler(client, message)
    elif command == "gcast":
        await gcast_handler(client, message)
    elif command == "gcastbl":
        await gcastbl_handler(client, message)

async def update_chats_handler(client: VzoelClient, message: Message):
    """Perintah buat ngumpulin dan nyimpen semua ID chat ke database."""
    loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
    success_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
    
    msg = await message.reply_text(f"{loading_emoji} Mengumpulkan daftar chat...")
    
    count = 0
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM chats")
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                await db.execute("INSERT OR IGNORE INTO chats (chat_id, type) VALUES (?, ?)", (dialog.chat.id, dialog.chat.type.name))
                count += 1
        await db.commit()

    await msg.edit_text(f"{success_emoji} Selesai! {count} grup disimpan ke database.")

async def gcast_handler(client: VzoelClient, message: Message):
    """Handler utama buat broadcast pesan dengan animasi keren."""
    args = get_arguments(message)
    target_message = message.reply_to_message
    
    if not args and not target_message:
        utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
        telegram_emoji = vzoel_assets.get_emoji('telegram', premium_format=True)
        
        usage = (
            f"{utama_emoji} **Perintah Gcast**\n\n"
            f"{telegram_emoji} **Teks Gcast**: `.gcast <pesan>`\n"
            f"{telegram_emoji} **Style**: `.gcast -bold <pesan>`\n"
            f"{telegram_emoji} **Reply Gcast**: Reply ke pesan + `.gcast`\n"
            f"{telegram_emoji} **Emoji**: Gunakan shortcode, cth: `:utama:`"
        )
        await message.reply_text(usage)
        return

    blacklist = CONFIG.blacklist.groups
    active_chats = []
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT chat_id FROM chats") as cursor:
            async for row in cursor:
                if row[0] not in blacklist:
                    active_chats.append(row[0])

    if not active_chats:
        merah_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
        await message.reply_text(f"{merah_emoji} Database chat kosong. Jalankan `.updatechats` dulu.")
        return

    # --- PREMIUM ANIMASI START ---
    proses_emoji = vzoel_assets.get_emoji('proses', premium_format=True)
    aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
    petir_emoji = vzoel_assets.get_emoji('petir', premium_format=True)
    telegram_emoji = vzoel_assets.get_emoji('telegram', premium_format=True)
    utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
    
    startup_frames = [
        f"{proses_emoji} Memulai Gcast...",
        f"{aktif_emoji} Memeriksa {len(active_chats)} target...",
        f"{petir_emoji} Menghapus {len(blacklist)} grup dari blacklist...",
        f"{telegram_emoji} Siap untuk broadcast! {utama_emoji}"
    ]
    progress_msg = await message.reply_text(startup_frames[0])
    for frame in startup_frames[1:]:
        await asyncio.sleep(0.8)
        try:
            await progress_msg.edit_text(frame)
        except MessageNotModified: pass
    
    # --- PROSES BROADCAST ---
    sukses, gagal = 0, 0
    start_time = time.time()
    for chat_id in active_chats:
        try:
            if target_message:
                await target_message.copy(chat_id)
            else:
                pesan_final = process_message_content(args, premium_format=True)
                await client.send_message(chat_id, pesan_final, disable_web_page_preview=True)
            sukses += 1
            await asyncio.sleep(1.5)  # Jeda aman
        except (FloodWait, UserIsBlocked, ChatAdminRequired) as e:
            LOGGER.error(f"Gagal kirim gcast ke {chat_id}: {e}")
            gagal += 1
        except Exception as e:
            LOGGER.error(f"Error gcast tidak diketahui di {chat_id}: {e}")
            gagal += 1

        # Update Progres Setiap 5 Chat dengan Premium Emojis
        if (sukses + gagal) % 5 == 0:
            try:
                progress_bar = '█' * int(sukses / len(active_chats) * 10)
                progress_bar += '░' * (10 - len(progress_bar))
                loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
                centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
                merah_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
                
                await progress_msg.edit_text(
                    f"{loading_emoji} **BROADCASTING...**\n"
                    f"`[{progress_bar}]`\n\n"
                    f"{centang_emoji} Sukses: `{sukses}`\n"
                    f"{merah_emoji} Gagal: `{gagal}`\n"
                    f"🎯 Target: `{len(active_chats)}`"
                )
            except MessageNotModified: pass

    # --- LAPORAN AKHIR PREMIUM ---
    end_time = time.time()
    total_time = round(end_time - start_time)
    
    utama_emoji = vzoel_assets.get_emoji('utama', premium_format=True)
    adder1_emoji = vzoel_assets.get_emoji('adder1', premium_format=True)
    centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
    merah_emoji = vzoel_assets.get_emoji('merah', premium_format=True)
    loading_emoji = vzoel_assets.get_emoji('loading', premium_format=True)
    
    await progress_msg.edit_text(
        f"{utama_emoji} **BROADCAST SELESAI** {adder1_emoji}\n\n"
        f"{centang_emoji} **Berhasil Terkirim:** `{sukses}` grup\n"
        f"{merah_emoji} **Gagal Terkirim:** `{gagal}` grup\n"
        f"{loading_emoji} **Total Waktu:** `{total_time}` detik"
    )

async def gcastbl_handler(client: VzoelClient, message: Message):
    """Handler buat cek status blacklist gcast dengan premium emojis."""
    args = get_arguments(message).lower()
    blacklist = CONFIG.blacklist.groups
    
    if args == "list":
        centang_emoji = vzoel_assets.get_emoji('centang', premium_format=True)
        if not blacklist:
            await message.reply_text(f"{centang_emoji} Blacklist gcast kosong.")
            return
        
        pesan = f"**Total Blacklist Gcast: `{len(blacklist)}` grup**\n\n"
        for i, chat_id in enumerate(blacklist[:15], 1): # Tampilkan maks 15
            pesan += f"`{i}`. `{chat_id}`\n"
        if len(blacklist) > 15:
            pesan += f"\n...dan `{len(blacklist) - 15}` lainnya."
        await message.reply_text(pesan)
    else:
        aktif_emoji = vzoel_assets.get_emoji('aktif', premium_format=True)
        status_text = (
            f"{aktif_emoji} **Status Blacklist Gcast**\n\n"
            f"**Total Grup di Blacklist:** `{len(blacklist)}`\n"
            f"**Sumber Data:** `config.json`\n"
            f"**Perintah:** `.gcastbl list` untuk melihat daftar."
        )
        await message.reply_text(status_text)

# Inisialisasi DB saat bot pertama kali jalan
asyncio.get_event_loop().run_until_complete(init_db())
