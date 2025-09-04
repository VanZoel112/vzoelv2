import os

# Menentukan lokasi "gudang" aset kita saat ini
# __file__ akan mengambil path dari file __init__.py ini sendiri
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- PETA LOKASI BAHAN BAKU ---
# Di sini kita mendaftarkan path lengkap ke setiap file aset

# Path ke file konfigurasi utama
CONFIG_PATH = os.path.join(_BASE_DIR, "config.json")

# Path ke file database emoji
EMOJIS_PATH = os.path.join(_BASE_DIR, "vzoel_emojis.json")

# Path ke file peta gaya font (markdown)
FONTS_PATH = os.path.join(_BASE_DIR, "vzoel_fonts.json")

# Path ke folder logo (jika dibutuhkan)
LOGO_DIR = os.path.join(_BASE_DIR, "logo")

# Pesan konfirmasi bahwa peta aset berhasil dimuat
print("✅ Peta Aset (assets/__init__.py) berhasil dimuat.")

