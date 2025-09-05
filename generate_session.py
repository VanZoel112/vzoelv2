#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Session String Generator
Automatically generates and updates session strings in .env file
Created by: Vzoel Fox's
"""

import os
import asyncio
import sys
from typing import Optional
from pyrogram import Client
from pyrogram.errors import (
    ApiIdInvalid, ApiIdPublishedFlood, AccessTokenExpired, 
    AccessTokenInvalid, UserDeactivated, AuthKeyDuplicated,
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    PasswordHashInvalid, FloodWait
)
from dotenv import load_dotenv, set_key
import json
from utils.assets import emoji, bold, italic, vzoel_signature

class VzoelSessionGenerator:
    """Premium session generator dengan auto .env update"""
    
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.phone_number = None
        self.session_name = None
        self.env_file = ".env"
        self.config_file = "vzoel/config.json"
        
        # Load existing environment
        load_dotenv(self.env_file)
        
    def display_banner(self):
        """Display premium banner"""
        banner = [
            "",
            "╔" + "═" * 60 + "╗",
            "║" + f"{'VZOEL SESSION GENERATOR v2':^60}" + "║",
            "║" + f"{'Premium Session String Generator':^60}" + "║",
            "║" + f"{'Created by: Vzoel Fox\\\'s':^60}" + "║",
            "╚" + "═" * 60 + "╝",
            "",
            f"{vzoel_signature()}",
            "",
            f"{emoji('loading')} {bold('Automatic Session Generator')}",
            f"{emoji('centang')} Generates session strings automatically",
            f"{emoji('telegram')} Updates .env file automatically", 
            f"{emoji('aktif')} Premium error handling",
            ""
        ]
        
        for line in banner:
            print(line)
    
    def load_config_from_env(self) -> bool:
        """Load configuration from .env file"""
        try:
            self.api_id = os.getenv('TELEGRAM_API_ID')
            self.api_hash = os.getenv('TELEGRAM_API_HASH')
            self.phone_number = os.getenv('PHONE_NUMBER')
            self.session_name = os.getenv('SESSION_NAME', 'vzoel_session')
            
            if not self.api_id or not self.api_hash:
                return False
            
            # Convert API ID to integer
            self.api_id = int(self.api_id)
            return True
            
        except (ValueError, TypeError) as e:
            print(f"{emoji('merah')} Error loading config: {e}")
            return False
    
    def prompt_missing_config(self):
        """Prompt for missing configuration"""
        print(f"{emoji('kuning')} {bold('Missing Configuration Detected')}")
        print("Please provide the following information:")
        print()
        
        if not self.api_id:
            while True:
                try:
                    api_id_input = input(f"{emoji('telegram')} Enter your API ID: ").strip()
                    self.api_id = int(api_id_input)
                    break
                except ValueError:
                    print(f"{emoji('merah')} Invalid API ID. Please enter numbers only.")
        
        if not self.api_hash:
            self.api_hash = input(f"{emoji('loading')} Enter your API Hash: ").strip()
        
        if not self.phone_number:
            self.phone_number = input(f"{emoji('utama')} Enter your phone number (with country code): ").strip()
        
        if not self.session_name:
            self.session_name = input(f"{emoji('aktif')} Enter session name [vzoel_session]: ").strip() or "vzoel_session"
        
        # Save to .env file
        self.save_config_to_env()
    
    def save_config_to_env(self):
        """Save configuration to .env file"""
        try:
            set_key(self.env_file, 'TELEGRAM_API_ID', str(self.api_id))
            set_key(self.env_file, 'TELEGRAM_API_HASH', self.api_hash)
            set_key(self.env_file, 'PHONE_NUMBER', self.phone_number)
            set_key(self.env_file, 'SESSION_NAME', self.session_name)
            
            print(f"{emoji('centang')} Configuration saved to {bold(self.env_file)}")
            
        except Exception as e:
            print(f"{emoji('merah')} Error saving config: {e}")
    
    def save_session_to_env(self, session_string: str, session_type: str = "SESSION_STRING"):
        """Save session string to .env file"""
        try:
            set_key(self.env_file, session_type, session_string)
            print(f"{emoji('adder2')} {session_type} saved to {bold(self.env_file)}")
            return True
            
        except Exception as e:
            print(f"{emoji('merah')} Error saving session: {e}")
            return False
    
    def save_session_to_config(self, session_string: str, session_type: str = "session_string"):
        """Save session string to vzoel/config.json"""
        try:
            # Load existing config
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Update session string
            if "bot_credentials" not in config:
                config["bot_credentials"] = {}
            
            config["bot_credentials"][session_type] = session_string
            
            # Save updated config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"{emoji('telegram')} {session_type} saved to {bold(self.config_file)}")
            return True
            
        except Exception as e:
            print(f"{emoji('merah')} Error saving to config: {e}")
            return False
    
    def load_config_from_json(self) -> bool:
        """Load configuration from vzoel/config.json as fallback"""
        try:
            if not os.path.exists(self.config_file):
                return False
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            telegram_api = config.get('telegram_api', {})
            bot_creds = config.get('bot_credentials', {})
            
            if not self.api_id and telegram_api.get('api_id'):
                self.api_id = telegram_api['api_id']
            
            if not self.api_hash and telegram_api.get('api_hash'):
                self.api_hash = telegram_api['api_hash']
                
            if not self.phone_number and bot_creds.get('phone_number'):
                self.phone_number = bot_creds['phone_number']
                
            if not self.session_name and bot_creds.get('session_name'):
                self.session_name = bot_creds['session_name']
            
            return True
            
        except Exception as e:
            print(f"{emoji('kuning')} Could not load from config.json: {e}")
            return False
    
    async def generate_session_string(self) -> Optional[str]:
        """Generate session string with premium error handling"""
        print(f"{emoji('loading')} {bold('Starting session generation...')}")
        print(f"{emoji('proses')} Creating client connection...")
        
        # Create temporary client
        temp_client = Client(
            name="temp_session_gen",
            api_id=self.api_id,
            api_hash=self.api_hash,
            phone_number=self.phone_number
        )
        
        try:
            print(f"{emoji('telegram')} Connecting to Telegram...")
            await temp_client.start()
            
            # Get session string
            session_string = await temp_client.export_session_string()
            
            print(f"{emoji('centang')} {bold('Session generated successfully!')}")
            print(f"{emoji('utama')} Session length: {len(session_string)} characters")
            
            # Stop client
            await temp_client.stop()
            
            # Clean up temporary session file
            try:
                os.remove("temp_session_gen.session")
            except FileNotFoundError:
                pass
            
            return session_string
            
        except PhoneNumberInvalid:
            print(f"{emoji('merah')} {bold('Error:')} Invalid phone number format!")
            print(f"{emoji('kuning')} Please use international format: +1234567890")
            return None
            
        except ApiIdInvalid:
            print(f"{emoji('merah')} {bold('Error:')} Invalid API ID!")
            print(f"{emoji('kuning')} Get your API credentials from https://my.telegram.org")
            return None
            
        except FloodWait as e:
            print(f"{emoji('kuning')} {bold('Rate Limited!')} Please wait {e.value} seconds...")
            await asyncio.sleep(e.value)
            return await self.generate_session_string()  # Retry after waiting
            
        except PhoneCodeInvalid:
            print(f"{emoji('merah')} {bold('Error:')} Invalid verification code!")
            return None
            
        except PhoneCodeExpired:
            print(f"{emoji('merah')} {bold('Error:')} Verification code expired!")
            return None
            
        except PasswordHashInvalid:
            print(f"{emoji('merah')} {bold('Error:')} Invalid 2FA password!")
            return None
            
        except Exception as e:
            print(f"{emoji('merah')} {bold('Unexpected Error:')} {str(e)}")
            return None
        
        finally:
            # Ensure client is stopped and cleanup
            try:
                if temp_client.is_connected:
                    await temp_client.stop()
                os.remove("temp_session_gen.session")
            except:
                pass
    
    async def generate_user_session(self) -> Optional[str]:
        """Generate user session for user bot mode"""
        print(f"{emoji('biru')} {bold('Generating USER session...')}")
        
        # Similar to bot session but for user mode
        return await self.generate_session_string()
    
    def display_success_message(self, session_string: str):
        """Display success message with session info"""
        lines = [
            "",
            f"{emoji('adder2')} {bold('SESSION GENERATION SUCCESSFUL!')}",
            "",
            f"{emoji('centang')} Session string generated and saved to {bold('.env')}",
            f"{emoji('aktif')} Session length: {bold(str(len(session_string)))} characters",
            f"{emoji('telegram')} Ready for bot startup!",
            "",
            f"{emoji('utama')} {bold('Next Steps:')}",
            f"  1. Complete your .env file with other required values",
            f"  2. Run: {italic('python3 main.py')}",
            f"  3. Your bot will start automatically with the session",
            "",
            f"{emoji('petir')} {bold('Security Note:')}",
            f"  • Never share your session string",
            f"  • Keep your .env file secure",
            f"  • Add .env to .gitignore",
            "",
            f"{italic('Enhanced by Vzoel Fox\\\'s Premium Collection')}",
            ""
        ]
        
        for line in lines:
            print(line)
    
    def create_env_from_example(self):
        """Create .env from .env.example if it doesn't exist"""
        if not os.path.exists(self.env_file) and os.path.exists(".env.example"):
            try:
                with open(".env.example", 'r') as example:
                    with open(self.env_file, 'w') as env:
                        env.write(example.read())
                print(f"{emoji('centang')} Created {bold('.env')} from template")
            except Exception as e:
                print(f"{emoji('merah')} Error creating .env: {e}")
    
    async def run(self):
        """Main execution function"""
        self.display_banner()
        
        # Create .env from example if needed
        self.create_env_from_example()
        
        # Try to load config from .env first, then config.json
        env_loaded = self.load_config_from_env()
        json_loaded = self.load_config_from_json()
        
        if not env_loaded and not json_loaded:
            print(f"{emoji('kuning')} Configuration not found in {bold('.env')} or {bold('vzoel/config.json')}")
            self.prompt_missing_config()
        else:
            sources = []
            if env_loaded:
                sources.append('.env')
            if json_loaded:
                sources.append('config.json')
            print(f"{emoji('centang')} Configuration loaded from {bold(' and '.join(sources))}")
        
        print(f"{emoji('proses')} Using configuration:")
        print(f"  • API ID: {bold(str(self.api_id))}")
        print(f"  • API Hash: {bold(self.api_hash[:8] + '...')}")
        print(f"  • Phone: {bold(self.phone_number)}")
        print(f"  • Session Name: {bold(self.session_name)}")
        print()
        
        # Generate session
        session_string = await self.generate_session_string()
        
        if session_string:
            # Save to both .env and config.json
            env_success = self.save_session_to_env(session_string)
            config_success = self.save_session_to_config(session_string)
            
            if env_success or config_success:
                self.display_success_message(session_string)
                return True
            else:
                print(f"{emoji('merah')} {bold('Failed to save session to files!')}")
                return False
        else:
            print(f"{emoji('merah')} {bold('Session generation failed!')}")
            print(f"{emoji('kuning')} Please check your credentials and try again.")
            return False

async def main():
    """Main entry point"""
    try:
        generator = VzoelSessionGenerator()
        success = await generator.run()
        
        if success:
            print(f"{emoji('centang')} {bold('All done!')} You can now start your bot.")
            sys.exit(0)
        else:
            print(f"{emoji('merah')} {bold('Generation failed!')} Please try again.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{emoji('kuning')} {bold('Generation cancelled by user.')}")
        sys.exit(1)
    except Exception as e:
        print(f"{emoji('merah')} {bold('Critical Error:')} {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)