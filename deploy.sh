#!/bin/bash
# VZOEL ASSISTANT v2 - Auto Deploy Script
# Created by: VZLfxs @Lutpan

echo "🚀 VZOEL ASSISTANT v2 - AUTO DEPLOY"
echo "===================================="

# Function to check if SESSION_STRING exists in .env
check_session() {
    if grep -q "^SESSION_STRING=" .env && [ -n "$(grep "^SESSION_STRING=" .env | cut -d'=' -f2-)" ]; then
        return 0  # Session exists and not empty
    else
        return 1  # Session doesn't exist or empty
    fi
}

# Check if session exists
if check_session; then
    echo "✅ Session string ditemukan di .env"
    echo "🚀 Memulai userbot..."
    source venv/bin/activate
    python3 main.py
else
    echo "❌ Session string tidak ditemukan"
    echo "📱 Menjalankan generator session..."
    echo ""
    echo "💡 Siapkan:"
    echo "   • Nomor HP: +6283199218067" 
    echo "   • Kode verifikasi dari SMS/Telegram"
    echo "   • 2FA password (jika ada)"
    echo ""
    read -p "👍 Tekan Enter untuk melanjutkan..."
    
    # Run session generator
    source venv/bin/activate
    python3 auto_session_generator.py
    
    # Check if session was created successfully
    if check_session; then
        echo ""
        echo "✅ Session berhasil dibuat!"
        echo "🚀 Memulai userbot..."
        python3 main.py
    else
        echo ""
        echo "❌ Gagal membuat session string"
        echo "💡 Coba jalankan manual: python3 auto_session_generator.py"
        exit 1
    fi
fi