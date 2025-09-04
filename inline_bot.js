// Impor library Telegraf
const { Telegraf, Markup } = require('telegraf');

// Ganti 'BOT_TOKEN' dengan token bot Master dari BotFather
const bot = new Telegraf('BOT_TOKEN');

// --- DATABASE BANTUAN ---
// Di sini kita simpen semua teks bantuan per halaman
const helpPages = [
    // Halaman 1 (index 0)
    "📖 **Selamat Datang di Menu Bantuan!**\n\nIni adalah daftar perintah dasar yang bisa kamu gunakan:",
    // Halaman 2 (index 1)
    "🎵 **Perintah Musik**\n\n`/play [judul]` - Untuk memutar lagu.\n`/skip` - Untuk melewati lagu.\n`/stop` - Untuk menghentikan musik.",
    // Halaman 3 (index 2)
    "🛠️ **Perintah Utilitas**\n\n`/ping` - Untuk cek kecepatan respon bot.\n`/id` - Untuk melihat ID chat kamu.",
];

// Fungsi untuk membuat tombol inline secara dinamis
const createHelpKeyboard = (currentPage) => {
    const buttons = [];
    
    // Tampilkan tombol 'Back' (⬅️) jika bukan di halaman pertama
    if (currentPage > 0) {
        buttons.push(Markup.button.callback('⬅️ Back', `help_back_${currentPage}`));
    }

    // Tampilkan tombol 'Next' (➡️) jika bukan di halaman terakhir
    if (currentPage < helpPages.length - 1) {
        buttons.push(Markup.button.callback('Next ➡️', `help_next_${currentPage}`));
    }

    return Markup.inlineKeyboard(buttons);
};

// --- HANDLER PERINTAH /help ---
// Ini yang bakal jalan kalo user ngetik /help
bot.command('help', (ctx) => {
    const pageIndex = 0; // Mulai dari halaman pertama
    const text = helpPages[pageIndex];
    const keyboard = createHelpKeyboard(pageIndex);

    ctx.reply(text, {
        parse_mode: 'Markdown',
        ...keyboard
    });
});

// --- HANDLER UNTUK TOMBOL INLINE (CALLBACK QUERY) ---
// Ini 'otak' dari tombolnya, dia dengerin kalo ada yang mencet tombol
bot.action(/help_(next|back)_(\d+)/, (ctx) => {
    const action = ctx.match[1]; // 'next' atau 'back'
    const currentPage = parseInt(ctx.match[2]); // Halaman saat ini (misal: 0, 1, 2)
    
    let newPage = currentPage;
    
    if (action === 'next') {
        newPage++;
    } else if (action === 'back') {
        newPage--;
    }
    
    // Pastikan index halaman valid
    if (newPage >= 0 && newPage < helpPages.length) {
        const text = helpPages[newPage];
        const keyboard = createHelpKeyboard(newPage);
        
        // Edit pesan yang ada, biar nggak nge-spam chat
        ctx.editMessageText(text, {
            parse_mode: 'Markdown',
            ...keyboard
        }).catch((err) => console.log("Error edit message:", err)); // antisipasi error kalo user spam klik
    }
});


// Jalankan botnya
bot.launch();
console.log('Bot bantuan sudah ON, Master! 🚀');

// Biar bot nggak gampang mati
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

