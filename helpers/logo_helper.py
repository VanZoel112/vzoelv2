"""
Premium Logo Helper - Enhanced Image Management for Bot Assistant
Enhanced with premium emoji and font system for superior user experience  
Created by: Vzoel Fox's
"""

import os
import logging
from typing import Optional, Dict, Any, List
from pyrogram import Client
from pyrogram.types import Message, InputMediaPhoto
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

class LogoHelper:
    """
    Premium Logo Helper dengan enhanced features:
    - Smart image loading dari vzoel directory
    - Premium caption formatting dengan branding
    - Multiple image support untuk alive/help commands
    - Enhanced error handling dengan emoji feedback
    - Automatic image detection dan validation
    """
    
    def __init__(self, assets: Optional[VzoelAssets] = None):
        """
        Initialize Premium Logo Helper
        
        Args:
            assets: VzoelAssets instance untuk premium styling
        """
        self.assets = assets or VzoelAssets()
        self.logger = self._setup_premium_logging()
        self.vzoel_images_dir = "vzoel"
        
        # Available images
        self.available_images = self._discover_images()
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self) -> logging.Logger:
        """Setup enhanced logging dengan premium styling"""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("utama")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        init_msg = [
            f"{emoji('petir')} {bold('Premium Logo Helper')} initialized",
            f"{emoji('centang')} Images directory: {bold(self.vzoel_images_dir)}",
            f"{emoji('loading')} Available images: {bold(str(len(self.available_images)))}",
            f"{emoji('utama')} Premium features: {bold('ACTIVE')}"
        ]
        
        for line in init_msg:
            self.logger.info(line)
    
    def _discover_images(self) -> Dict[str, str]:
        """
        Discover semua image files dalam vzoel directory
        
        Returns:
            Dictionary mapping image names to file paths
        """
        images = {}
        
        if not os.path.exists(self.vzoel_images_dir):
            self.logger.warning(f"{emoji('loading')} Images directory '{self.vzoel_images_dir}' not found")
            return images
        
        # Supported image formats
        supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        
        for filename in os.listdir(self.vzoel_images_dir):
            if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                name = os.path.splitext(filename)[0]
                full_path = os.path.join(self.vzoel_images_dir, filename)
                images[name] = full_path
        
        self.logger.info(f"{emoji('centang')} Discovered {bold(str(len(images)))} image files")
        return images
    
    def get_image_path(self, image_name: str) -> Optional[str]:
        """
        Get full path untuk specific image
        
        Args:
            image_name: Nama image (tanpa extension)
            
        Returns:
            Full path to image or None if not found
        """
        path = self.available_images.get(image_name)
        if path and os.path.exists(path):
            return path
        
        self.logger.warning(f"{emoji('loading')} Image '{image_name}' not found")
        return None
    
    def get_logo_path(self) -> Optional[str]:
        """
        Get path untuk main logo image
        
        Returns:
            Path to logo.jpg or first available image
        """
        # Try logo first
        logo_path = self.get_image_path('logo')
        if logo_path:
            return logo_path
        
        # Fallback to first available image
        if self.available_images:
            first_image = list(self.available_images.values())[0]
            self.logger.info(f"{emoji('loading')} Using fallback image: {first_image}")
            return first_image
        
        self.logger.error(f"{emoji('merah')} No images available")
        return None
    
    def create_alive_caption(self, bot_info: Dict[str, Any] = None) -> str:
        """
        Create premium caption untuk alive command
        
        Args:
            bot_info: Dictionary dengan bot information
            
        Returns:
            Formatted caption dengan premium styling
        """
        signature = self.assets.vzoel_signature()
        
        caption_lines = [
            signature,
            "",
            f"{emoji('centang')} **Status Bot:** {bold('ONLINE & READY')}",
            ""
        ]
        
        # Add bot information if provided
        if bot_info:
            caption_lines.extend([
                f"{emoji('petir')} **Bot Information:**",
                f"  • Name: {bold(bot_info.get('first_name', 'VzoelBot'))}",
                f"  • Username: @{bot_info.get('username', 'vzoel_bot')}",
                f"  • ID: `{bot_info.get('id', '000000000')}`",
                ""
            ])
        
        # Add feature status
        caption_lines.extend([
            f"{emoji('utama')} **Premium Features:**",
            f"  • Enhanced Framework: {bold('✓ ACTIVE')}",
            f"  • Premium Assets: {bold('✓ LOADED')}",
            f"  • Image System: {bold('✓ OPERATIONAL')}",
            f"  • Error Handling: {bold('✓ ENHANCED')}",
            "",
            f"{emoji('loading')} **Performance:** {bold('Optimized')}",
            f"{emoji('aktif')} **All Systems:** {bold('OPERATIONAL')}",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}",
            ""
        ])
        
        return "\n".join(caption_lines)
    
    def create_help_caption(self, command_count: int = 0) -> str:
        """
        Create premium caption untuk help command
        
        Args:
            command_count: Number of available commands
            
        Returns:
            Formatted caption untuk help display
        """
        signature = self.assets.vzoel_signature()
        
        caption_lines = [
            signature,
            "",
            f"{emoji('centang')} **Selamat Datang di Help Center!**",
            "",
            f"Bot assistant premium dengan fitur-fitur canggih",
            f"untuk membantu kebutuhan Anda.",
            "",
            f"{emoji('petir')} **Informasi Sistem:**"
        ]
        
        if command_count > 0:
            caption_lines.extend([
                f"  • Total Commands: {bold(str(command_count))}",
                f"  • Premium Features: {bold('ACTIVE')}",
                f"  • Response Time: {bold('Optimized')}",
                ""
            ])
        
        caption_lines.extend([
            f"{emoji('utama')} **Fitur Unggulan:**",
            f"  • Premium styling & emoji",
            f"  • Interactive command system", 
            f"  • Enhanced error handling",
            f"  • Real-time performance monitoring",
            "",
            f"{emoji('loading')} **Gunakan tombol di bawah** untuk navigasi,",
            f"atau ketik command langsung untuk akses cepat.",
            "",
            f"{italic('Powered by Vzoel Fox Premium Framework')}",
            ""
        ])
        
        return "\n".join(caption_lines)
    
    def create_custom_caption(self, title: str, description: str = "", 
                            features: List[str] = None) -> str:
        """
        Create custom caption dengan premium formatting
        
        Args:
            title: Main title untuk caption
            description: Optional description
            features: List of features to highlight
            
        Returns:
            Formatted custom caption
        """
        signature = self.assets.vzoel_signature()
        
        caption_lines = [
            signature,
            "",
            f"{emoji('centang')} **{title}**",
            ""
        ]
        
        if description:
            caption_lines.extend([
                description,
                ""
            ])
        
        if features:
            caption_lines.append(f"{emoji('utama')} **Features:**")
            for feature in features:
                caption_lines.append(f"  • {feature}")
            caption_lines.append("")
        
        caption_lines.extend([
            f"{emoji('loading')} **Status:** {bold('READY')}",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}"
        ])
        
        return "\n".join(caption_lines)
    
    async def send_logo_with_caption(self, client: Client, chat_id: int,
                                   caption_type: str = "alive",
                                   custom_data: Dict[str, Any] = None,
                                   reply_to_message_id: Optional[int] = None) -> Optional[Message]:
        """
        Send logo dengan premium caption
        
        Args:
            client: Pyrogram client instance
            chat_id: Target chat ID
            caption_type: Type of caption ("alive", "help", "custom")
            custom_data: Additional data untuk caption generation
            reply_to_message_id: Message ID to reply to
            
        Returns:
            Sent message or None if failed
        """
        try:
            # Get logo path
            logo_path = self.get_logo_path()
            if not logo_path:
                # Send text-only message if no image
                return await self._send_text_fallback(client, chat_id, caption_type, 
                                                    custom_data, reply_to_message_id)
            
            # Generate appropriate caption
            if caption_type == "alive":
                caption = self.create_alive_caption(custom_data or {})
            elif caption_type == "help":
                command_count = custom_data.get('command_count', 0) if custom_data else 0
                caption = self.create_help_caption(command_count)
            elif caption_type == "custom":
                title = custom_data.get('title', 'Custom Message') if custom_data else 'Custom Message'
                description = custom_data.get('description', '') if custom_data else ''
                features = custom_data.get('features', []) if custom_data else []
                caption = self.create_custom_caption(title, description, features)
            else:
                caption = self.create_alive_caption(custom_data or {})
            
            # Send photo dengan caption
            loading_emojis = self.assets.get_status_emojis("loading")
            self.logger.info(f"{loading_emojis[0] if loading_emojis else '⏳'} Sending logo with {caption_type} caption")
            
            sent_message = await client.send_photo(
                chat_id=chat_id,
                photo=logo_path,
                caption=caption,
                reply_to_message_id=reply_to_message_id
            )
            
            success_emojis = self.assets.get_status_emojis("success")
            self.logger.info(f"{success_emojis[0] if success_emojis else '✅'} Logo sent successfully")
            
            return sent_message
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Failed to send logo: {e}"
            self.logger.error(error_msg)
            
            # Fallback to text message
            return await self._send_text_fallback(client, chat_id, caption_type,
                                                custom_data, reply_to_message_id)
    
    async def _send_text_fallback(self, client: Client, chat_id: int,
                                caption_type: str, custom_data: Dict[str, Any] = None,
                                reply_to_message_id: Optional[int] = None) -> Optional[Message]:
        """Send text-only message sebagai fallback"""
        try:
            # Generate caption without image
            if caption_type == "alive":
                text = self.create_alive_caption(custom_data or {})
            elif caption_type == "help":
                command_count = custom_data.get('command_count', 0) if custom_data else 0
                text = self.create_help_caption(command_count)
            else:
                text = self.create_alive_caption(custom_data or {})
            
            return await client.send_message(
                chat_id=chat_id,
                text=text,
                reply_to_message_id=reply_to_message_id
            )
            
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Text fallback also failed: {e}")
            return None
    
    async def send_image_gallery(self, client: Client, chat_id: int,
                               caption: str = "", image_names: List[str] = None) -> Optional[Message]:
        """
        Send multiple images sebagai media group
        
        Args:
            client: Pyrogram client
            chat_id: Target chat ID  
            caption: Caption untuk gallery
            image_names: List of image names to send
            
        Returns:
            Sent message or None
        """
        try:
            if not image_names:
                image_names = list(self.available_images.keys())
            
            if not image_names:
                self.logger.warning(f"{emoji('loading')} No images available for gallery")
                return None
            
            # Prepare media list
            media_list = []
            for i, image_name in enumerate(image_names[:10]):  # Max 10 images
                image_path = self.get_image_path(image_name)
                if image_path:
                    # First image gets the caption
                    img_caption = caption if i == 0 else ""
                    media_list.append(InputMediaPhoto(media=image_path, caption=img_caption))
            
            if not media_list:
                self.logger.warning(f"{emoji('loading')} No valid images found for gallery")
                return None
            
            # Send media group
            sent_messages = await client.send_media_group(
                chat_id=chat_id,
                media=media_list
            )
            
            success_emojis = self.assets.get_status_emojis("success")
            self.logger.info(f"{success_emojis[0] if success_emojis else '✅'} Image gallery sent: {len(media_list)} images")
            
            return sent_messages[0] if sent_messages else None
            
        except Exception as e:
            error_msg = f"{emoji('merah')} Failed to send image gallery: {e}"
            self.logger.error(error_msg)
            return None
    
    def get_helper_info(self) -> Dict[str, Any]:
        """Get comprehensive logo helper information"""
        return {
            "helper_class": self.__class__.__name__,
            "images_directory": self.vzoel_images_dir,
            "available_images": list(self.available_images.keys()),
            "total_images": len(self.available_images),
            "features": {
                "premium_captions": True,
                "multiple_image_support": True,
                "auto_fallback": True,
                "media_gallery": True,
                "error_handling": True
            },
            "supported_formats": ['.jpg', '.jpeg', '.png', '.webp'],
            "caption_types": ["alive", "help", "custom"]
        }

# Convenience functions untuk quick access
async def send_logo_message(client: Client, chat_id: int, message_type: str = "alive",
                          bot_info: Dict[str, Any] = None,
                          reply_to_message_id: Optional[int] = None) -> Optional[Message]:
    """
    Quick function untuk send logo message
    
    Args:
        client: Pyrogram client
        chat_id: Target chat ID
        message_type: Type of message ("alive", "help")
        bot_info: Bot information dictionary
        reply_to_message_id: Message to reply to
        
    Returns:
        Sent message or None
    """
    helper = LogoHelper()
    return await helper.send_logo_with_caption(
        client=client,
        chat_id=chat_id,
        caption_type=message_type,
        custom_data=bot_info,
        reply_to_message_id=reply_to_message_id
    )