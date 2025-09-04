# =================================================================
# 1. THE ULTIMATE OPENER: UVLOOP & CLIENT
# Paling pertama, biar performa bot langsung ngebut dari awal.
# Setelah itu, langsung definisikan client utama (app) biar bisa
# dipake sama modul-modul lain di bawahnya.
# =================================================================
import uvloop
from pyrogram import Client

uvloop.install()

app = Client(
    "MusicPlayer",
    # Config.API_ID, Config.API_HASH, dll. bakal dibaca dari bawah nanti
)


# =================================================================
# 2. IMPOR PASUKAN HELPER
# Di sini kita panggil semua modul custom buatan Master dulu.
# Anggep aja ini manggil asisten-asisten internal.
# =================================================================
from helpers.database import db
from helpers.decorators import authorized_users_only
from utils.filters import command
from utils.formatters import format_time
# ... dan helper-helper lainnya ...


# =================================================================
# 3. IMPOR AMUNISI BERAT
# Setelah helper internal siap, baru kita panggil modul eksternal
# yang jadi senjata utama buat fitur musiknya.
# =================================================================
import yt_dlp as youtube_dl
from pytgcalls import PyTgCalls

# Inisialisasi PyTgCalls di sini, karena butuh 'app' yang sudah ada
pytg = PyTgCalls(app)


# =================================================================
# 4. DAPUR PACU BOT
# Di sini tempat semua logika dan handler perintah bot berada.
# Kayak @app.on_message(command("play")) dan teman-temannya.
# =================================================================

"""
DI SINI TEMPAT SEMUA LOGIKA PERINTAH BOT
SEPERTI @app.on_message(...) UNTUK /play, /skip, /pause, DLL.

Contoh:
@app.on_message(command("start"))
async def start_command(_, message):
    await message.reply_text("Bot Aktif!")

"""


# =================================================================
# 5. PRINTILAN ESTETIK & KONFIGURASI (PALING BAWAH)
# Sesuai request Master, semua config, emoji, dan font kita
# kumpulin di paling bawah biar gampang dicari dan di-edit.
# =================================================================
class Config:
    API_ID = 1234567 # Ganti punya Master
    API_HASH = "abcdefg123456" # Ganti punya Master
    BOT_TOKEN = "..." # Ganti punya Master
    SESSION_STRING = "..." # Ganti punya Master
    # ... variabel config lainnya ...

class EMOJI:
    # Kumpulan emoji premium biar keliatan kece
    PLAY = "▶️"
    PAUSE = "⏸️"
    LOADING = "⏳"
    SUCCESS = "✅"
    ERROR = "❌"
    GEM = "💎"
    STAR = "🌟"

class FONTS:
    BOLD = "**{}**"
    ITALIC = "*{}*"
    CODE = "`{}`"


# =================================================================
# 6. THE "GO!" BUTTON
# Bagian terakhir untuk menjalankan semua yang udah kita siapin.
# =================================================================
async def main():
    # Masukin variabel config ke dalam client 'app'
    app.api_id = Config.API_ID
    app.api_hash = Config.API_HASH
    app.bot_token = Config.BOT_TOKEN
    
    await app.start()
    await pytg.start()
    print(f"{EMOJI.STAR} Bot dan PyTgCalls sudah ON! {EMOJI.STAR}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    app.run(main())
