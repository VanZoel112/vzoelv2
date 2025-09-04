# core/loader/loader_plugins.py
import os
import importlib
from helpers import LOGGER

def load_all_plugins():
    """
    Mandor yang secara dinamis mencari dan memuat semua
    file plugin dari folder 'plugins'.
    """
    plugins_dir = "plugins"
    LOGGER.info("Mandor Pemuat Plugin mulai bekerja...")
    
    # Menyisir semua folder dan subfolder di dalam 'plugins'
    for root, _, files in os.walk(plugins_dir):
        for file in files:
            # Hanya proses file Python, bukan file lain
            if file.endswith(".py") and not file.startswith("__"):
                # Mengubah path file menjadi format modul Python
                # Contoh: 'plugins/tools/ping.py' -> 'plugins.tools.ping'
                plugin_path = os.path.join(root, file)
                module_path = plugin_path.replace(os.sep, ".")[:-3]
                
                try:
                    # 'Memungut' atau mengimpor modulnya secara dinamis
                    importlib.import_module(module_path)
                    LOGGER.info(f"✅ Plugin '{module_path}' berhasil dimuat.")
                except Exception as e:
                    LOGGER.error(f"❌ Gagal memuat plugin '{module_path}': {e}")

