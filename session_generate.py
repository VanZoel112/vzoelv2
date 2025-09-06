#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Session Generator
Pure user session string generator (NO BOT TOKENS)
Created by: VZLfxs @Lutpan
"""

import asyncio
import os
from pyrogram import Client
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid
)

class VzoelSessionGenerator:
    """Pure user session generator"""
    
    def __init__(self):
        # API credentials for user authentication ONLY
        self.api_id = 29919905
        self.api_hash = "717957f0e3ae20a7db004d08b66bfd30"
        self.session_name = "vzoel_user_session"
    
    def display_banner(self):
        """Display session generator banner"""
        print("\n" + "═" * 60)
        print("║     VZOEL ASSISTANT v2 - SESSION GENERATOR        ║")
        print("║      Generate user session string ONLY            ║")
        print("║           Created by: VZLfxs @Lutpan               ║")
        print("═" * 60 + "\n")
    
    def get_phone_number(self):
        """Get phone number input"""
        while True:
            phone = input("📱 Masukkan nomor HP (dengan kode negara, contoh: +6283199218067): ").strip()
            if phone.startswith('+') and len(phone) >= 10:
                print(f"✅ Nomor HP: {phone}")
                return phone
            else:
                print("❌ Format nomor HP salah! Gunakan format +628xxxxxxxxxx")
    
    def get_verification_code(self):
        """Get verification code input"""
        while True:
            try:
                code = input("🔑 Masukkan kode verifikasi (5 digit): ").strip()
                if len(code) == 5 and code.isdigit():
                    return code
                else:
                    print("❌ Kode verifikasi harus 5 digit angka!")
            except KeyboardInterrupt:
                print("\n❌ Dibatalkan oleh user")
                return None
    
    def get_password(self):
        """Get 2FA password if needed"""
        password = input("🔐 Masukkan 2FA password (kosongkan jika tidak ada): ").strip()
        return password if password else None
    
    async def generate_session(self):
        """Generate user session string"""
        try:
            self.display_banner()
            
            print("📋 Session Generator Info:")
            print(f"   • API ID: {self.api_id}")
            print(f"   • API Hash: {self.api_hash}")
            print(f"   • Session Name: {self.session_name}")
            print(f"   • Mode: USER SESSION ONLY")
            print("")
            
            # Get phone number
            phone_number = self.get_phone_number()
            
            print("🔄 Creating USER client (NO BOT TOKEN)...")
            # Create client for USER session generation only
            client = Client(
                name=self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash
            )
            
            print("📞 Sending verification code...")
            await client.connect()
            sent_code = await client.send_code(phone_number)
            
            print(f"✅ Kode verifikasi dikirim ke {phone_number}")
            print("💬 Cek SMS/Telegram untuk mendapatkan kode verifikasi")
            
            # Get verification code
            code = self.get_verification_code()
            if not code:
                await client.disconnect()
                return None
            
            print("🔑 Memverifikasi kode...")
            try:
                await client.sign_in(phone_number, sent_code.phone_code_hash, code)
                print("✅ Login berhasil!")
                
            except SessionPasswordNeeded:
                print("🔐 2FA diperlukan...")
                password = self.get_password()
                if password:
                    await client.check_password(password)
                    print("✅ 2FA berhasil!")
                else:
                    print("❌ 2FA diperlukan tapi tidak dimasukkan")
                    await client.disconnect()
                    return None
                    
            except (PhoneCodeInvalid, PhoneCodeExpired) as e:
                print(f"❌ Error kode verifikasi: {e}")
                await client.disconnect()
                return None
            
            # Get user info
            me = await client.get_me()
            print(f"\n🎉 Session berhasil dibuat untuk USER:")
            print(f"   • Nama: {me.first_name} {me.last_name or ''}")
            print(f"   • Username: @{me.username or 'Tidak ada'}")
            print(f"   • ID: {me.id}")
            print(f"   • Type: USER (bukan bot)")
            
            # Export session string
            session_string = await client.export_session_string()
            await client.disconnect()
            
            print(f"\n💾 Session string berhasil di-generate!")
            print(f"📋 Session string: {session_string[:20]}...")
            
            return session_string
            
        except PhoneNumberInvalid:
            print("❌ Nomor HP tidak valid")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def save_session_to_file(self, session_string):
        """Save session string to vzoel_session.txt"""
        try:
            with open('vzoel_session.txt', 'w') as f:
                f.write(session_string)
            print(f"💾 Session disimpan ke vzoel_session.txt")
            return True
        except Exception as e:
            print(f"❌ Error menyimpan session: {e}")
            return False

async def main():
    """Main function"""
    generator = VzoelSessionGenerator()
    session_string = await generator.generate_session()
    
    if session_string:
        generator.save_session_to_file(session_string)
        print("\n🎉 SESSION GENERATION COMPLETE!")
        print("📱 User session string berhasil dibuat")
        print("🚀 Sekarang jalankan: python3 main.py")
    else:
        print("\n❌ Session generation failed")
        print("💡 Coba lagi dengan nomor HP dan kode yang benar")

if __name__ == "__main__":
    print("🚀 Starting Vzoel Session Generator...")
    print("⚠️  Mode: USER SESSION ONLY (NO BOT TOKENS)")
    asyncio.run(main())