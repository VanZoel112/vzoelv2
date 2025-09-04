# plugins/broadcast/gcast.py

import asyncio
import aiosqlite
import time
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, UserIsBlocked, ChatAdminRequired, MessageNotModified

# Import semua helper kita yang udah cihuy
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG
from helper_logger import LOGGER
from helper_vzoel_emojis import EMOJIS
from helper_vzoel_fonts import style_text

DB_PATH = "broadcast_chats.db"

async def init_db():
    """Bikin tabel database kalo belum ada."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER PRIMARY KEY, type TEXT)")
        await db.commit()

def process_message_content(text: str) -> str:
    """Fungsi terpusat buat ngolah teks dengan font style dan emoji."""
    processed_text = text
    style_to_apply = None

    # Deteksi dan terapkan font style
    if "-bold" in text:
        style_to_apply = "bold"
        processed_text = text.replace("-bold", "").strip()
    elif "-italic" in text:
        style_to_apply = "italic"
        processed_text = text.replace("-italic", "").strip()
    elif "-monospace" in text:
        style_to_apply = "monospace"
        processed_text = text.replace("-monospace", "").strip()
    
    if style_to_apply:
        processed_text = style_text(processed_text, style=style_to_apply)

    # Ganti shortcode emoji dari vzoel_emojis.json
    for key, details in EMOJIS.emojis.items():
        processed_text = processed_text.replace(f":{key}:", details["emoji_char"])
        
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
    msg = await message.reply_text(f"{EMOJIS.get_char('loading')} Mengumpulkan daftar chat...")
    
    count = 0
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM chats")
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                await db.execute("INSERT OR IGNORE INTO chats (chat_id, type) VALUES (?, ?)", (dialog.chat.id, dialog.chat.type.name))
                count += 1
        await db.commit()

    await msg.edit_text(f"{EMOJIS.get_char('centang')} Selesai! {count} grup disimpan ke database.")

async def gcast_handler(client: VzoelClient, message: Message):
    """Handler utama buat broadcast pesan dengan animasi keren."""
    args = get_arguments(message)
    target_message = message.reply_to_message
    
    if not args and not target_message:
        usage = (
            f"{EMOJIS.get_char('utama')} **Perintah Gcast**\n\n"
            f"{EMOJIS.get_char('telegram')} **Teks Gcast**: `.gcast <pesan>`\n"
            f"{EMOJIS.get_char('telegram')} **Style**: `.gcast -bold <pesan>`\n"
            f"{EMOJIS.get_char('telegram')} **Reply Gcast**: Reply ke pesan + `.gcast`\n"
            f"{EMOJIS.get_char('telegram')} **Emoji**: Gunakan shortcode, cth: `:utama:`"
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
        await message.reply_text(f"{EMOJIS.get_char('merah')} Database chat kosong. Jalankan `.updatechats` dulu.")
        return

    # --- ANIMASI START ---
    startup_frames = [
        f"{EMOJIS.get_char('proses')} Memulai Gcast...",
        f"{EMOJIS.get_char('aktif')} Memeriksa {len(active_chats)} target...",
        f"{EMOJIS.get_char('petir')} Menghapus {len(blacklist)} grup dari blacklist...",
        f"{EMOJIS.get_char('telegram')} Siap untuk broadcast! {EMOJIS.get_char('utama')}"
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
                pesan_final = process_message_content(args)
                await client.send_message(chat_id, pesan_final, disable_web_page_preview=True)
            sukses += 1
            await asyncio.sleep(1.5)  # Jeda aman
        except (FloodWait, UserIsBlocked, ChatAdminRequired) as e:
            LOGGER.error(f"Gagal kirim gcast ke {chat_id}: {e}")
            gagal += 1
        except Exception as e:
            LOGGER.error(f"Error gcast tidak diketahui di {chat_id}: {e}")
            gagal += 1

        # Update Progres Setiap 5 Chat
        if (sukses + gagal) % 5 == 0:
            try:
                progress_bar = '█' * int(sukses / len(active_chats) * 10)
                progress_bar += '░' * (10 - len(progress_bar))
                await progress_msg.edit_text(
                    f"{EMOJIS.get_char('loading')} **BROADCASTING...**\n"
                    f"`[{progress_bar}]`\n\n"
                    f"{EMOJIS.get_char('centang')} Sukses: `{sukses}`\n"
                    f"{EMOJIS.get_char('merah')} Gagal: `{gagal}`\n"
                    f"🎯 Target: `{len(active_chats)}`"
                )
            except MessageNotModified: pass

    # --- LAPORAN AKHIR ---
    end_time = time.time()
    total_time = round(end_time - start_time)
    await progress_msg.edit_text(
        f"{EMOJIS.get_char('utama')} **BROADCAST SELESAI** {EMOJIS.get_char('adder1')}\n\n"
        f"{EMOJIS.get_char('centang')} **Berhasil Terkirim:** `{sukses}` grup\n"
        f"{EMOJIS.get_char('merah')} **Gagal Terkirim:** `{gagal}` grup\n"
        f"{EMOJIS.get_char('loading')} **Total Waktu:** `{total_time}` detik"
    )

async def gcastbl_handler(client: VzoelClient, message: Message):
    """Handler buat cek status blacklist gcast."""
    args = get_arguments(message).lower()
    blacklist = CONFIG.blacklist.groups
    
    if args == "list":
        if not blacklist:
            await message.reply_text(f"{EMOJIS.get_char('centang')} Blacklist gcast kosong.")
            return
        
        pesan = f"**Total Blacklist Gcast: `{len(blacklist)}` grup**\n\n"
        for i, chat_id in enumerate(blacklist[:15], 1): # Tampilkan maks 15
            pesan += f"`{i}`. `{chat_id}`\n"
        if len(blacklist) > 15:
            pesan += f"\n...dan `{len(blacklist) - 15}` lainnya."
        await message.reply_text(pesan)
    else:
        status_text = (
            f"{EMOJIS.get_char('aktif')} **Status Blacklist Gcast**\n\n"
            f"**Total Grup di Blacklist:** `{len(blacklist)}`\n"
            f"**Sumber Data:** `config.json`\n"
            f"**Perintah:** `.gcastbl list` untuk melihat daftar."
        )
        await message.reply_text(status_text)

# Inisialisasi DB saat bot pertama kali jalan
asyncio.get_event_loop().run_until_complete(init_db())
