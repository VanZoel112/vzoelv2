from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- DATABASE BANTUAN ---
# Di sini kita simpen semua teks bantuan per halaman dalam bentuk list
HELP_PAGES = [
    # Halaman 1 (index 0)
    "📖 **Selamat Datang di Menu Bantuan!**\n\n"
    "Ini adalah daftar perintah dasar yang bisa kamu gunakan:",

    # Halaman 2 (index 1)
    "🎵 **Perintah Musik**\n\n"
    "• `/play [judul/link]` - Memutar lagu dari YouTube.\n"
    "• `/skip` - Melewati lagu yang sedang diputar.\n"
    "• `/stop` - Menghentikan musik dan keluar dari Voice Chat.",

    # Halaman 3 (index 2)
    "🛠️ **Perintah Utilitas**\n\n"
    "• `/ping` - Cek kecepatan respon bot.\n"
    "• `/id` - Melihat ID chat kamu saat ini.\n"
    "• `/start` - Menampilkan pesan sapaan.",
]

# Fungsi untuk membuat tombol inline secara dinamis
def create_help_keyboard(current_page: int):
    buttons = []
    
    # Bikin baris tombol dalam satu list
    row = []

    # Tampilkan tombol 'Back' (⬅️) jika bukan di halaman pertama
    if current_page > 0:
        row.append(
            InlineKeyboardButton("⬅️ Back", callback_data=f"help_back_{current_page}")
        )

    # Tampilkan tombol 'Next' (➡️) jika bukan di halaman terakhir
    if current_page < len(HELP_PAGES) - 1:
        row.append(
            InlineKeyboardButton("Next ➡️", callback_data=f"help_next_{current_page}")
        )
    
    # Masukin baris tombol ke keyboard utama
    if row:
        buttons.append(row)
        
    return InlineKeyboardMarkup(buttons)


# --- HANDLER PERINTAH /help ---
# Ini yang bakal jalan kalo user ngetik /help
@Client.on_message(filters.command("help"))
async def help_command(client, message):
    page_index = 0  # Mulai dari halaman pertama
    text = HELP_PAGES[page_index]
    keyboard = create_help_keyboard(page_index)
    
    await message.reply_text(
        text=text,
        reply_markup=keyboard
    )


# --- HANDLER UNTUK TOMBOL INLINE (CALLBACK QUERY) ---
# Ini 'otak' dari tombolnya, dia dengerin kalo ada yang mencet tombol
@Client.on_callback_query(filters.regex(r"help_(next|back)_(\d+)"))
async def help_callback(client, callback_query):
    action = callback_query.matches[0].group(1)  # 'next' atau 'back'
    current_page = int(callback_query.matches[0].group(2)) # Halaman saat ini (misal: 0, 1, 2)
    
    new_page = current_page
    
    if action == 'next':
        new_page += 1
    elif action == 'back':
        new_page -= 1
        
    # Pastikan index halaman valid
    if 0 <= new_page < len(HELP_PAGES):
        text = HELP_PAGES[new_page]
        keyboard = create_help_keyboard(new_page)
        
        try:
            # Edit pesan yang ada, biar nggak nge-spam chat
            await callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            # antisipasi error kalo user spam klik tombol, kocak emang
            print(f"Error edit message: {e}")

