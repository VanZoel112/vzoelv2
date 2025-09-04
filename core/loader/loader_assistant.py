# core/loader/loader_assistant.py
from core.client import VzoelClient
from helpers import LOGGER
from .loader_plugins import load_all_plugins

class VzoelAssistant:
    """
    Kelas utama yang menjadi 'Kerangka' dari Asisten.
    Dia yang mengatur siklus hidup bot (start, stop, run).
    """
    def __init__(self):
        self.bot = VzoelClient

    async def start(self):
        """Prosedur menyalakan mesin dan memuat semua sistem."""
        LOGGER.info("Memulai prosedur penyalaan Asisten...")
        
        # Nyalakan koneksi utama ke Telegram
        await self.bot.start()
        
        # Panggil mandor untuk memuat semua plugin setelah bot online
        # Catatan: Pyrogram v2 menangani ini secara otomatis jika 'plugins' diatur di Client.
        # Kode 'load_all_plugins()' ini berguna jika Master ingin kontrol lebih,
        # misalnya memuat plugin tanpa harus restart bot di masa depan.
        # Untuk sekarang, kita bisa anggap ini sebagai pencatatan/logging saja.
        load_all_plugins()

        # Dapatkan info bot setelah online
        me = await self.bot.get_me()
        LOGGER.info(f"Asisten '{me.first_name}' berhasil online!")
        print(f"[{me.first_name}] Online dan siap melayani Master!")

    def run(self):
        """Metode untuk menjalankan bot secara terus menerus."""
        # 'run' sudah secara otomatis memanggil 'start' dan 'stop'
        self.bot.run()
