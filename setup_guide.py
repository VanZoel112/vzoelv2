#!/usr/bin/env python3
"""
VZOEL ASSISTANT v2 - Setup Guide
Interactive setup guide for new users
Created by: Vzoel Fox's
"""

import os
import sys
from utils.assets import emoji, bold, italic, vzoel_signature

def display_banner():
    """Display setup banner"""
    banner = [
        "",
        "╔" + "═" * 60 + "╗",
        "║" + f"{'VZOEL ASSISTANT v2 - SETUP GUIDE':^60}" + "║",
        "║" + f"{'Interactive Setup for New Users':^60}" + "║",
        "║" + f"{'Created by: Vzoel Fox\\\'s':^60}" + "║",
        "╚" + "═" * 60 + "╝",
        "",
        f"{vzoel_signature()}",
        ""
    ]
    
    for line in banner:
        print(line)

def check_files():
    """Check if required files exist"""
    files_to_check = [
        ".env.example",
        "vzoel/config.json",
        "generate_session.py",
        "main.py"
    ]
    
    print(f"{emoji('loading')} {bold('Checking required files...')}")
    
    missing_files = []
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  {emoji('centang')} {file}")
        else:
            print(f"  {emoji('merah')} {file} (MISSING)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n{emoji('kuning')} {bold('Warning:')} Some files are missing!")
        print("Please ensure you have a complete copy of the repository.")
        return False
    
    print(f"\n{emoji('adder2')} All required files found!")
    return True

def check_env_setup():
    """Check .env file setup"""
    print(f"\n{emoji('telegram')} {bold('Checking environment setup...')}")
    
    if not os.path.exists(".env"):
        print(f"  {emoji('kuning')} .env file not found")
        
        if os.path.exists(".env.example"):
            response = input(f"  {emoji('utama')} Create .env from template? (y/n): ")
            if response.lower() in ['y', 'yes']:
                try:
                    with open(".env.example", 'r') as example:
                        with open(".env", 'w') as env:
                            env.write(example.read())
                    print(f"  {emoji('centang')} .env file created from template!")
                    return True
                except Exception as e:
                    print(f"  {emoji('merah')} Error creating .env: {e}")
                    return False
            else:
                print(f"  {emoji('kuning')} Skipped .env creation")
                return False
        else:
            print(f"  {emoji('merah')} .env.example template not found!")
            return False
    else:
        print(f"  {emoji('centang')} .env file exists")
        return True

def display_setup_steps():
    """Display setup instructions"""
    steps = [
        "",
        f"{emoji('loading')} {bold('SETUP STEPS:')}",
        "",
        f"{emoji('utama')} **1. Get Telegram API Credentials**",
        f"   • Go to: https://my.telegram.org/auth",
        f"   • Login with your Telegram account", 
        f"   • Create a new application",
        f"   • Get your API_ID and API_HASH",
        "",
        f"{emoji('telegram')} **2. Setup Bot (Choose one method):**",
        f"   ",
        f"   {bold('Method A: Bot Token (Recommended)')}",
        f"   • Create bot via @BotFather on Telegram",
        f"   • Get bot token",
        f"   • Add to .env: BOT_TOKEN=your_bot_token",
        f"   ",
        f"   {bold('Method B: User Session (Advanced)')}",
        f"   • Add your phone number to .env: PHONE_NUMBER=+1234567890",
        f"   • Run: python3 generate_session.py",
        f"   • Follow the OTP verification process",
        "",
        f"{emoji('centang')} **3. Configure .env File**",
        f"   • Edit .env file with your credentials",
        f"   • Fill in required values (API_ID, API_HASH, etc.)",
        f"   • Set your FOUNDER_ID (your Telegram user ID)",
        f"   • Set LOG_GROUP_ID (optional but recommended)",
        "",
        f"{emoji('aktif')} **4. Start the Bot**",
        f"   • Run: python3 main.py",
        f"   • Bot should start automatically",
        f"   • Test with /help command",
        "",
        f"{emoji('adder2')} **5. Advanced Features (Optional)**",
        f"   • Configure database settings",
        f"   • Setup external services (OpenAI, etc.)",
        f"   • Customize plugins and features",
        "",
    ]
    
    for step in steps:
        print(step)

def display_troubleshooting():
    """Display troubleshooting guide"""
    troubleshooting = [
        "",
        f"{emoji('petir')} {bold('TROUBLESHOOTING:')}",
        "",
        f"{emoji('merah')} **Common Issues:**",
        f"   • Import errors: Run pip3 install -r requirements.txt",
        f"   • API errors: Check your API_ID and API_HASH",
        f"   • Session errors: Delete .session files and regenerate",
        f"   • Permission errors: Check file permissions",
        "",
        f"{emoji('kuning')} **Getting Help:**",
        f"   • Check documentation: https://github.com/VanZoel112/vzoelv2",
        f"   • Contact support: @VzoelFox on Telegram",
        f"   • Report issues: GitHub Issues page",
        "",
    ]
    
    for item in troubleshooting:
        print(item)

def main():
    """Main setup guide"""
    display_banner()
    
    # Check files
    if not check_files():
        print(f"\n{emoji('merah')} {bold('Setup cannot continue due to missing files.')}")
        return
    
    # Check environment
    env_ready = check_env_setup()
    
    # Display setup steps
    display_setup_steps()
    
    # Display troubleshooting
    display_troubleshooting()
    
    # Final message
    print(f"{emoji('centang')} {bold('Setup Guide Complete!')}")
    
    if env_ready:
        print(f"\n{emoji('utama')} {bold('Next Steps:')}")
        print(f"1. Edit your .env file with proper credentials")
        print(f"2. Run: {italic('python3 generate_session.py')} (if using user mode)")
        print(f"3. Run: {italic('python3 main.py')} to start the bot")
    else:
        print(f"\n{emoji('kuning')} {bold('Please complete .env setup first!')}")
    
    print(f"\n{italic('Enhanced by Vzoel Fox\\\'s Premium Collection')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{emoji('kuning')} Setup guide cancelled.")
    except Exception as e:
        print(f"\n{emoji('merah')} Error: {e}")
