# core/client.py
import os
from dotenv import load_dotenv
from pyrogram import Client

# Muat semua variabel rahasia dari file .env di root directory
load_dotenv()

# Ciptakan "Jati Diri" bot menggunakan data dari .env
# Pyrogram akan secara otomatis mencari folder 'plugins' di root
VzoelClient = Client(
    "VzoelAssistantSession", # Nama file session yang akan dibuat
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    plugins={"root": "plugins"}
)
