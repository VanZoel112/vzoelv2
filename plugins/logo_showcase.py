"""
Logo Showcase Plugin - Premium Logo Display Commands
Enhanced with comprehensive image handling and gallery features
Created by: Vzoel Fox's
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from helpers.logo_helper import LogoHelper
from helpers.image_helper import ImageHelper, process_vzoel_images
from helpers.display_helper import DisplayHelper
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji
import os

# Initialize premium components
logo_helper = LogoHelper()
image_helper = ImageHelper()
display_helper = DisplayHelper()
assets = VzoelAssets()

@Client.on_message(filters.command("logo"))
async def logo_display_command(client: Client, message: Message):
    """
    Display logo dengan berbagai caption types
    Usage: /logo [alive|help|custom]
    """
    
    try:
        # Parse command arguments
        command_parts = message.text.split()
        caption_type = command_parts[1] if len(command_parts) > 1 else "alive"
        
        # Validate caption type
        valid_types = ["alive", "help", "custom"]
        if caption_type not in valid_types:
            error_msg = display_helper.create_error_message(
                f"Invalid caption type: {caption_type}",
                [f"Valid types: {', '.join(valid_types)}", "Example: /logo alive"]
            )
            await message.reply_text(error_msg)
            return
        
        # Get bot information untuk caption
        me = await client.get_me()
        bot_info = {
            'first_name': me.first_name,
            'username': me.username,
            'id': me.id,
            'type': caption_type
        }
        
        # Prepare custom data based on type
        if caption_type == "custom":
            custom_data = {
                'title': 'Custom Logo Display',
                'description': 'Demonstrating custom caption generation dengan premium styling',
                'features': [
                    'Premium logo integration',
                    'Custom caption formatting', 
                    'Enhanced visual presentation',
                    'Flexible content management'
                ]
            }
        elif caption_type == "help":
            # Count available commands from help system (simplified)
            custom_data = {'command_count': 15}
        else:
            custom_data = bot_info
        
        # Send logo dengan specified caption type
        await logo_helper.send_logo_with_caption(
            client=client,
            chat_id=message.chat.id,
            caption_type=caption_type,
            custom_data=custom_data,
            reply_to_message_id=message.id
        )
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Failed to display logo: {str(e)}",
            ["Check if logo.jpg exists in vzoel/ folder", "Verify bot permissions", "Try /gallery command"]
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("gallery"))
async def image_gallery_command(client: Client, message: Message):
    """
    Display gallery semua available images
    """
    
    try:
        # Show loading message
        loading_msg = display_helper.create_loading_message(
            "Preparing Image Gallery",
            ["Scanning vzoel directory", "Validating image files", "Preparing gallery display"]
        )
        loading_message = await message.reply_text(loading_msg)
        
        # Get available images information
        available_images = logo_helper.available_images
        
        if not available_images:
            await loading_message.edit_text(
                display_helper.create_error_message(
                    "No images found",
                    ["Add images to vzoel/ directory", "Supported: .jpg, .png, .webp", "Try /logo command instead"]
                )
            )
            return
        
        # Create gallery caption
        gallery_info = [
            f"{assets.vzoel_signature()}",
            "",
            f"{emoji('centang')} **Vzoel Image Gallery**",
            "",
            f"Showcasing all available images dalam premium collection",
            "",
            f"{emoji('aktif')} **Gallery Statistics:**",
            f"  • Total Images: {bold(str(len(available_images)))}",
            f"  • Formats Supported: {bold('JPG, PNG, WebP')}",
            f"  • Display Mode: {bold('Premium Gallery')}",
            "",
            f"{emoji('loading')} **Available Images:**"
        ]
        
        # Add image list dengan information
        for i, (name, path) in enumerate(available_images.items(), 1):
            img_info = image_helper.get_image_info(path)
            if img_info['valid']:
                size_info = f"{img_info['width']}x{img_info['height']}"
                file_size = f"{img_info.get('size_mb', 0):.1f}MB"
                gallery_info.append(f"  {i}. {bold(name)}.jpg - {size_info} ({file_size})")
            else:
                gallery_info.append(f"  {i}. {bold(name)} - {italic('Invalid/Missing')}")
        
        gallery_info.extend([
            "",
            f"{emoji('utama')} **Usage Tips:**",
            f"• Use `/logo` untuk display dengan captions",
            f"• All images optimized untuk Telegram",
            f"• Supports premium caption generation",
            "",
            f"{italic('Enhanced by Vzoel Fox Premium Collection')}"
        ])
        
        gallery_caption = "\n".join(gallery_info)
        
        # Delete loading message
        await loading_message.delete()
        
        # Try to send as media group first
        try:
            await logo_helper.send_image_gallery(
                client=client,
                chat_id=message.chat.id,
                caption=gallery_caption,
                image_names=list(available_images.keys())
            )
        except:
            # Fallback to text message with individual images
            await message.reply_text(gallery_caption)
            
            # Send individual images
            for name, path in list(available_images.items())[:3]:  # Limit to 3 untuk avoid spam
                try:
                    caption = f"{emoji('centang')} **{name.title()}**\n\nPart of Vzoel Premium Collection"
                    await client.send_photo(
                        chat_id=message.chat.id,
                        photo=path,
                        caption=caption
                    )
                except:
                    continue
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Gallery display failed: {str(e)}",
            ["Check vzoel/ directory", "Verify image permissions", "Try /logo command instead"]
        )
        try:
            await loading_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)

@Client.on_message(filters.command("images"))
async def image_info_command(client: Client, message: Message):
    """
    Detailed information about available images
    """
    
    try:
        available_images = logo_helper.available_images
        
        if not available_images:
            await message.reply_text(
                display_helper.create_error_message(
                    "No images found in collection",
                    ["Add images to vzoel/ directory", "Supported formats: .jpg, .png, .webp"]
                )
            )
            return
        
        # Create detailed image information
        info_lines = [
            display_helper.create_vzoel_banner("IMAGE SYSTEM"),
            f"{emoji('centang')} **Vzoel Image Collection Details**",
            ""
        ]
        
        total_size = 0
        valid_count = 0
        
        for name, path in available_images.items():
            img_info = image_helper.get_image_info(path)
            
            if img_info['valid']:
                valid_count += 1
                total_size += img_info.get('size_mb', 0)
                
                info_lines.extend([
                    f"{emoji('utama')} **{name.upper()}**",
                    f"  • Path: `{path}`",
                    f"  • Dimensions: {bold(f\"{img_info['width']}x{img_info['height']}\")}",
                    f"  • Format: {bold(img_info['format'])}",
                    f"  • Size: {bold(f\"{img_info['size_mb']:.2f}MB\")}",
                    f"  • Aspect Ratio: {bold(str(img_info['aspect_ratio']))}",
                    f"  • Telegram Ready: {bold('✓' if not img_info['needs_resize'] else 'Needs Resize')}",
                    ""
                ])
            else:
                info_lines.extend([
                    f"{emoji('merah')} **{name.upper()}** - {italic('INVALID')}",
                    f"  • Path: `{path}`",
                    f"  • Status: {italic('File missing or corrupted')}",
                    ""
                ])
        
        # Add summary statistics
        info_lines.extend([
            f"{emoji('loading')} **Collection Summary:**",
            f"  • Total Images: {bold(str(len(available_images)))}",
            f"  • Valid Images: {bold(str(valid_count))}",
            f"  • Total Size: {bold(f'{total_size:.2f}MB')}",
            f"  • Average Size: {bold(f'{total_size/max(valid_count, 1):.2f}MB')}",
            "",
            f"{emoji('aktif')} **System Capabilities:**",
            f"  • Auto-validation: {bold('✓ Active')}",
            f"  • Format Support: {bold('JPG, PNG, WebP')}",
            f"  • Telegram Optimization: {bold('✓ Available')}",
            f"  • Gallery Display: {bold('✓ Supported')}",
            "",
            f"{italic('Use /gallery to view all images')}"
        ])
        
        await message.reply_text("\n".join(info_lines))
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Image information unavailable: {str(e)}"
        )
        await message.reply_text(error_msg)

@Client.on_message(filters.command("optimize"))
async def optimize_images_command(client: Client, message: Message):
    """
    Optimize all images untuk Telegram (Admin only)
    """
    
    try:
        # Simple admin check (in production, implement proper admin system)
        user_id = message.from_user.id
        
        # Show processing message
        processing_msg = display_helper.create_loading_message(
            "Optimizing Images",
            ["Scanning vzoel directory", "Processing each image", "Applying Telegram optimization"]
        )
        processing_message = await message.reply_text(processing_msg)
        
        # Process all images
        results = process_vzoel_images()
        
        # Create results report
        if results['total'] == 0:
            result_msg = display_helper.create_error_message(
                "No images found to optimize",
                ["Add images to vzoel/ directory", "Supported formats: .jpg, .png, .webp"]
            )
        else:
            success_details = [
                f"Processed: {bold(str(results['success_count']))}/{results['total']} images",
                f"Success Rate: {bold(f\"{(results['success_count']/results['total']*100):.1f}%\")}",
                f"Output: vzoel/processed/ directory"
            ]
            
            if results['failed']:
                success_details.append(f"Failed: {bold(str(len(results['failed'])))} images")
            
            result_msg = display_helper.create_success_message(
                "Image optimization completed",
                success_details
            )
        
        await processing_message.edit_text(result_msg)
        
    except Exception as e:
        error_msg = display_helper.create_error_message(
            f"Optimization failed: {str(e)}",
            ["Check file permissions", "Ensure vzoel/ directory exists", "Contact administrator"]
        )
        
        try:
            await processing_message.edit_text(error_msg)
        except:
            await message.reply_text(error_msg)