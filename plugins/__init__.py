# plugins/__init__.py

import os
import importlib

# Siapin list buat nampung semua plugin yang berhasil dimuat
SEMUA_PLUGIN = []

# Dapetin path ke folder 'plugins' ini
path_folder_plugin = os.path.dirname(__file__)
nama_folder_plugin = os.path.basename(path_folder_plugin)

# Scan semua file di dalem folder ini
for nama_file in os.listdir(path_folder_plugin):
    # Cek kalo itu file python, bukan folder, dan bukan file init ini sendiri
    if nama_file.endswith('.py') and nama_file != '__init__.py':
        # Hapus ekstensi .py buat dapetin nama modulnya
        nama_modul = nama_file[:-3]
        
        try:
            # Kita coba import modul plugin secara dinamis
            modul_plugin = importlib.import_module(f".{nama_modul}", package=nama_folder_plugin)
            
            # Kalo berhasil, tambahin ke list kita
            SEMUA_PLUGIN.append(modul_plugin)
            print(f"✅ Plugin '{nama_modul}' berhasil dimuat!")
        except Exception as e:
            print(f"❌ Gagal memuat plugin '{nama_modul}': {e}")

