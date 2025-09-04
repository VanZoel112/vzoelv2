# plugins/broadcast/blacklist.py

import json
from pyrogram.types import Message

# Import semua helper kita
from helper_client import VzoelClient
from helper_cmd_handler import CMD_HANDLER, get_command, get_arguments
from helper_config import CONFIG, CONFIG_JSON_PATH
from helper_logger import LOGGER
from helper_vzoel_emojis import EMOJIS
from helper_vzoel_fonts import style_text

def save_config_changes():
    """Fungsi sakti buat nyimpen perubahan blacklist ke config.json."""
    try:
        # Baca seluruh config sebagai dictionary
        with open(CONFIG_JSON_PATH, 'r') as f:
            full_config_data = json.load(f)
        
        # Update bagian blacklist-nya aja
        full_config_data["blacklist"]["groups"] = CONFIG.blacklist.groups
        
        # Tulis ulang seluruh file config dengan data terbaru
        with open(CONFIG_JSON_PATH, 'w') as f:
            json.dump(full_config_data, f, indent=2)
        
        LOGGER.info(f"Config.json berhasil di-update dengan {len(CONFIG.blacklist.groups)} blacklist.")
        return True
    except Exception as e:
        LOGGER.error(f"Gagal menyimpan config.json: {e}")
        return False

@VzoelClient.on_message(CMD_HANDLER)
async def blacklist_router(client: VzoelClient, message: Message):
    """Router buat semua perintah manajemen blacklist."""
    command = get_command(message)
    
    if command == "addbl":
        await addbl_handler(client, message)
    elif command == "rmbl":
        await rmbl_handler(client, message)
    elif command == "listbl":
        await listbl_handler(client, message)
    elif command == "clearbl":
        await clearbl_handler(client, message)

async def addbl_handler(client: VzoelClient, message: Message):
    """Menambahkan chat ke blacklist gcast."""
    args = get_arguments(message)
    chat_id_to_add = 0
    
    try:
        if args:
            chat_id_to_add = int(args)
        else:
            chat_id_to_add = message.chat.id
    except ValueError:
        await message.reply_text(f"{EMOJIS.get_char('merah')} ID chat tidak valid, Master.")
        return

    if chat_id_to_add in CONFIG.blacklist.groups:
        await message.reply_text(f"{EMOJIS.get_char('kuning')} Chat ini sudah ada di dalam blacklist.")
        return

    CONFIG.blacklist.groups.append(chat_id_to_add)
    
    if save_config_changes():
        response = (
            f"{EMOJIS.get_char('adder2')} **BLACKLIST DITAMBAHKAN**\n\n"
            f"{EMOJIS.get_char('aktif')} **Proteksi Gcast Aktif**\n"
            f"**ID Chat:** `{chat_id_to_add}`\n"
            f"**Total Blacklist:** `{len(CONFIG.blacklist.groups)}` grup"
        )
        await message.reply_text(response)
    else:
        # Kalo gagal simpen, balikin lagi data di memori
        CONFIG.blacklist.groups.remove(chat_id_to_add)
        await message.reply_text(f"{EMOJIS.get_char('merah')} Gagal menyimpan perubahan ke config.json.")

async def rmbl_handler(client: VzoelClient, message: Message):
    """Menghapus chat dari blacklist gcast."""
    args = get_arguments(message)
    chat_id_to_remove = 0

    try:
        if args:
            chat_id_to_remove = int(args)
        else:
            chat_id_to_remove = message.chat.id
    except ValueError:
        await message.reply_text(f"{EMOJIS.get_char('merah')} ID chat tidak valid, Master.")
        return

    if chat_id_to_remove not in CONFIG.blacklist.groups:
        await message.reply_text(f"{EMOJIS.get_char('kuning')} Chat ini tidak ada di dalam blacklist.")
        return

    CONFIG.blacklist.groups.remove(chat_id_to_remove)
    
    if save_config_changes():
        response = (
            f"{EMOJIS.get_char('adder1')} **BLACKLIST DIHAPUS**\n\n"
            f"{EMOJIS.get_char('telegram')} **Proteksi Gcast Dinonaktifkan**\n"
            f"**ID Chat:** `{chat_id_to_remove}`\n"
            f"**Sisa Blacklist:** `{len(CONFIG.blacklist.groups)}` grup"
        )
        await message.reply_text(response)
    else:
        # Kalo gagal simpen, balikin lagi data di memori
        CONFIG.blacklist.groups.append(chat_id_to_remove)
        await message.reply_text(f"{EMOJIS.get_char('merah')} Gagal menyimpan perubahan ke config.json.")
        
async def listbl_handler(client: VzoelClient, message: Message):
    """Menampilkan daftar chat di blacklist."""
    blacklist = CONFIG.blacklist.groups
    if not blacklist:
        await message.reply_text(f"{EMOJIS.get_char('centang')} Blacklist gcast saat ini kosong.")
        return
    
    pesan = f"**Total Blacklist Gcast: `{len(blacklist)}` grup**\n\n"
    for i, chat_id in enumerate(blacklist[:20], 1): # Tampilkan maks 20
        pesan += f"`{i}`. `{chat_id}`\n"
    if len(blacklist) > 20:
        pesan += f"\n...dan `{len(blacklist) - 20}` lainnya."
        
    await message.reply_text(pesan)

async def clearbl_handler(client: VzoelClient, message: Message):
    """Menghapus semua chat dari blacklist."""
    args = get_arguments(message)
    
    if args.lower() != "confirm":
        await message.reply_text(
            f"{EMOJIS.get_char('merah')} **PERINGATAN!**\n"
            "Ini akan menghapus SEMUA blacklist.\n\n"
            "Ketik `.clearbl confirm` untuk melanjutkan."
        )
        return

    original_blacklist = list(CONFIG.blacklist.groups)
    CONFIG.blacklist.groups.clear()
    
    if save_config_changes():
        response = (
            f"{EMOJIS.get_char('utama')} **BLACKLIST DIBERSIHKAN**\n\n"
            f"Berhasil menghapus `{len(original_blacklist)}` grup dari blacklist."
        )
        await message.reply_text(response)
    else:
        # Kalo gagal simpen, balikin lagi data di memori
        CONFIG.blacklist.groups = original_blacklist
        await message.reply_text(f"{EMOJIS.get_char('merah')} Gagal menyimpan perubahan ke config.json.")
