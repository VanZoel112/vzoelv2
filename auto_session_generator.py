#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Auto Session Generator
Generate Pyrogram session string otomatis dengan input phone dan code
Created by: VZLfxs @Lutpan
"""

import asyncio
import os
from pyrogram import Client
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AutoSessionGenerator:
    def __init__(self):
        self.api_id = int(os.getenv('TELEGRAM_API_ID', '24194005'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH', '717957f0e3ae20a7db004d08b66bfd30')
        self.session_name = os.getenv('SESSION_NAME', 'vzoel_assistant_session')
        self.phone_number = None
        self.client = None
        
    def display_banner(self):
        """Display banner"""
        print("\n" + "="*60)
        print("║        VZOEL ASSISTANT v2 - SESSION GENERATOR        ║")
        print("║           Auto generate user session string          ║")
        print("║              Created by: VZLfxs @Lutpan              ║")
        print("="*60 + "\n")
        
    def get_phone_number(self):
        """Get phone number input"""
        while True:
            phone = input("📱 Masukkan nomor HP (dengan kode negara, contoh: +6283199218067): ").strip()
            if phone.startswith('+') and len(phone) >= 10:
                self.phone_number = phone
                print(f"✅ Nomor HP: {phone}")
                return True
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
        """Generate session string"""
        try:
            print("🔄 Membuat client Pyrogram...")
            self.client = Client(
                name=self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone_number=self.phone_number
            )
            
            print("📞 Mengirim kode verifikasi...")
            await self.client.connect()
            sent_code = await self.client.send_code(self.phone_number)
            
            print(f"✅ Kode verifikasi dikirim ke {self.phone_number}")
            print("💬 Cek SMS/Telegram untuk mendapatkan kode verifikasi")
            
            # Get verification code
            code = self.get_verification_code()
            if not code:
                return False
                
            print("🔑 Memverifikasi kode...")
            try:
                await self.client.sign_in(self.phone_number, sent_code.phone_code_hash, code)
                print("✅ Login berhasil!")
                
            except SessionPasswordNeeded:
                print("🔐 2FA diperlukan...")
                password = self.get_password()
                if password:
                    await self.client.check_password(password)
                    print("✅ 2FA berhasil!")
                else:
                    print("❌ 2FA diperlukan tapi tidak dimasukkan")
                    return False
                    
            except (PhoneCodeInvalid, PhoneCodeExpired) as e:
                print(f"❌ Error kode verifikasi: {e}")
                return False
                
            # Get user info
            me = await self.client.get_me()
            print(f"\n🎉 Session berhasil dibuat untuk:")
            print(f"   • Nama: {me.first_name} {me.last_name or ''}")
            print(f"   • Username: @{me.username or 'Tidak ada'}")
            print(f"   • ID: {me.id}")
            
            # Get session string
            session_string = await self.client.export_session_string()
            
            # Save to .env file
            await self.save_session_to_env(session_string)
            
            print(f"\n✅ Session string berhasil disimpan ke .env")
            print("🚀 Bot siap dijalankan sebagai userbot!")
            
            await self.client.disconnect()
            return True
            
        except PhoneNumberInvalid:
            print("❌ Nomor HP tidak valid")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
            
    async def save_session_to_env(self, session_string):
        """Save session string to .env file"""
        try:
            # Read current .env content
            with open('.env', 'r') as f:
                lines = f.readlines()
            
            # Update or add SESSION_STRING
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('SESSION_STRING='):
                    lines[i] = f'SESSION_STRING={session_string}\n'
                    updated = True
                    break
            
            # Add if not found
            if not updated:
                lines.append(f'\nSESSION_STRING={session_string}\n')
            
            # Write back to file
            with open('.env', 'w') as f:
                f.writelines(lines)
                
            print("💾 Session string tersimpan di .env")
            
        except Exception as e:
            print(f"❌ Error menyimpan ke .env: {e}")
            print(f"\n📋 Session String (copy manual ke .env):")
            print(f"SESSION_STRING={session_string}")
            
    async def run(self):
        """Main run function"""
        self.display_banner()
        
        print("📋 Informasi API:")
        print(f"   • API ID: {self.api_id}")
        print(f"   • API Hash: {self.api_hash}")
        print(f"   • Session Name: {self.session_name}")
        
        if not self.get_phone_number():
            return
            
        success = await self.generate_session()
        
        if success:
            print("\n🎉 SELESAI! Session berhasil dibuat!")
            print("💡 Sekarang jalankan: python3 main.py")
        else:
            print("\n❌ Gagal membuat session. Coba lagi!")

async def main():
    generator = AutoSessionGenerator()
    await generator.run()

if __name__ == "__main__":
    print("🚀 Starting Auto Session Generator...")
    asyncio.run(main())