"""
Premium Image Helper - Enhanced Image Processing for Bot Assistant
Enhanced with premium emoji and font system for superior image handling
Created by: Vzoel Fox's
"""

import os
import logging
from typing import Optional, Dict, Any, List, Tuple
from utils.assets import VzoelAssets, vzoel_msg, bold, italic, emoji

# Optional PIL import dengan fallback
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print(f"{emoji('loading')} PIL not available - advanced image processing disabled")

class ImageHelper:
    """
    Premium Image Helper dengan enhanced features:
    - Image validation dan processing
    - Smart image resizing untuk optimal display
    - Metadata extraction dari images
    - Premium watermark support
    - Batch image processing
    """
    
    def __init__(self, assets: Optional[VzoelAssets] = None):
        """
        Initialize Premium Image Helper
        
        Args:
            assets: VzoelAssets instance untuk premium styling
        """
        self.assets = assets or VzoelAssets()
        self.logger = self._setup_premium_logging()
        
        # Image processing settings
        self.max_size = (1280, 1280)  # Maximum image dimensions
        self.quality = 90  # JPEG quality
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
        
        # Log initialization
        self._log_initialization()
    
    def _setup_premium_logging(self) -> logging.Logger:
        """Setup enhanced logging dengan premium styling"""
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {emoji("biru")} %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _log_initialization(self):
        """Log initialization dengan premium styling"""
        init_msg = [
            f"{emoji('petir')} {bold('Premium Image Helper')} initialized",
            f"{emoji('centang')} Max size: {bold(f'{self.max_size[0]}x{self.max_size[1]}')}",
            f"{emoji('loading')} Quality: {bold(f'{self.quality}%')}",
            f"{emoji('utama')} Supported formats: {bold(str(len(self.supported_formats)))}"
        ]
        
        for line in init_msg:
            self.logger.info(line)
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if not os.path.exists(image_path):
                self.logger.warning(f"{emoji('loading')} Image not found: {image_path}")
                return False
            
            # Check file extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in self.supported_formats:
                self.logger.warning(f"{emoji('loading')} Unsupported format: {ext}")
                return False
            
            # Basic file size check
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                self.logger.warning(f"{emoji('loading')} Empty image file: {image_path}")
                return False
            
            # Try PIL validation if available
            if PIL_AVAILABLE:
                try:
                    with Image.open(image_path) as img:
                        img.verify()  # Verify image integrity
                except:
                    return False
            
            self.logger.info(f"{emoji('centang')} Image validation successful: {os.path.basename(image_path)}")
            return True
            
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Image validation failed: {e}")
            return False
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """
        Get comprehensive image information
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary dengan image metadata
        """
        info = {
            "path": image_path,
            "filename": os.path.basename(image_path),
            "exists": False,
            "valid": False
        }
        
        try:
            if not os.path.exists(image_path):
                return info
            
            info["exists"] = True
            info["size_bytes"] = os.path.getsize(image_path)
            info["size_mb"] = round(info["size_bytes"] / (1024 * 1024), 2)
            
            if PIL_AVAILABLE:
                with Image.open(image_path) as img:
                    info["dimensions"] = img.size
                    info["width"] = img.size[0]
                    info["height"] = img.size[1]
                    info["format"] = img.format
                    info["mode"] = img.mode
                    info["valid"] = True
                    
                    # Calculate aspect ratio
                    info["aspect_ratio"] = round(info["width"] / info["height"], 2)
                    
                    # Determine if resize needed
                    needs_resize = (info["width"] > self.max_size[0] or 
                                  info["height"] > self.max_size[1])
                    info["needs_resize"] = needs_resize
            else:
                # Basic info without PIL
                info["valid"] = self.validate_image(image_path)
                info["width"] = "Unknown"
                info["height"] = "Unknown"
                info["format"] = "Unknown"
                info["needs_resize"] = False
            
            self.logger.info(f"{emoji('centang')} Image info extracted: {info['filename']}")
            
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Failed to get image info: {e}")
        
        return info
    
    def resize_image(self, input_path: str, output_path: str = None,
                    max_size: Tuple[int, int] = None) -> Optional[str]:
        """
        Resize image untuk optimal display
        
        Args:
            input_path: Path to input image
            output_path: Path untuk output (optional)
            max_size: Maximum dimensions (optional)
            
        Returns:
            Path to resized image or None
        """
        if not PIL_AVAILABLE:
            self.logger.warning(f"{emoji('loading')} PIL not available - image resizing disabled")
            return input_path  # Return original path as fallback
        
        try:
            if not self.validate_image(input_path):
                return None
            
            max_size = max_size or self.max_size
            
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Calculate new size maintaining aspect ratio
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Generate output path if not provided
                if not output_path:
                    name, ext = os.path.splitext(input_path)
                    output_path = f"{name}_resized{ext}"
                
                # Save resized image
                img.save(output_path, optimize=True, quality=self.quality)
                
                self.logger.info(f"{emoji('centang')} Image resized: {os.path.basename(output_path)}")
                return output_path
                
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Failed to resize image: {e}")
            return None
    
    def add_watermark(self, image_path: str, watermark_text: str,
                     output_path: str = None, position: str = "bottom-right") -> Optional[str]:
        """
        Add watermark to image
        
        Args:
            image_path: Path to image
            watermark_text: Text untuk watermark
            output_path: Output path (optional)
            position: Watermark position
            
        Returns:
            Path to watermarked image or None
        """
        if not PIL_AVAILABLE:
            self.logger.warning(f"{emoji('loading')} PIL not available - watermarking disabled")
            return input_path
        
        try:
            if not self.validate_image(image_path):
                return None
            
            with Image.open(image_path) as img:
                # Convert to RGBA untuk transparency support
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Create transparent overlay
                overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(overlay)
                
                # Calculate text size dan position
                try:
                    # Try to use better font if available
                    font_size = max(20, img.size[0] // 30)  # Scale font with image
                    font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Get text dimensions
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Calculate position
                margin = 20
                positions = {
                    "bottom-right": (img.size[0] - text_width - margin, 
                                   img.size[1] - text_height - margin),
                    "bottom-left": (margin, img.size[1] - text_height - margin),
                    "top-right": (img.size[0] - text_width - margin, margin),
                    "top-left": (margin, margin),
                    "center": ((img.size[0] - text_width) // 2, 
                             (img.size[1] - text_height) // 2)
                }
                
                text_pos = positions.get(position, positions["bottom-right"])
                
                # Draw watermark with semi-transparent background
                draw.rectangle([text_pos[0] - 5, text_pos[1] - 5,
                               text_pos[0] + text_width + 5, text_pos[1] + text_height + 5],
                              fill=(0, 0, 0, 128))
                
                # Draw text
                draw.text(text_pos, watermark_text, font=font, fill=(255, 255, 255, 200))
                
                # Composite overlay onto image
                watermarked = Image.alpha_composite(img, overlay)
                
                # Convert back to RGB untuk saving
                if watermarked.mode == 'RGBA':
                    final_img = Image.new('RGB', watermarked.size, (255, 255, 255))
                    final_img.paste(watermarked, mask=watermarked.split()[-1])
                else:
                    final_img = watermarked
                
                # Generate output path if not provided
                if not output_path:
                    name, ext = os.path.splitext(image_path)
                    output_path = f"{name}_watermarked{ext}"
                
                # Save watermarked image
                final_img.save(output_path, optimize=True, quality=self.quality)
                
                self.logger.info(f"{emoji('centang')} Watermark added: {os.path.basename(output_path)}")
                return output_path
                
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Failed to add watermark: {e}")
            return None
    
    def optimize_for_telegram(self, image_path: str, output_path: str = None) -> Optional[str]:
        """
        Optimize image specifically untuk Telegram
        
        Args:
            image_path: Path to input image
            output_path: Path untuk output (optional)
            
        Returns:
            Path to optimized image or None
        """
        if not PIL_AVAILABLE:
            self.logger.warning(f"{emoji('loading')} PIL not available - using original image")
            return image_path
        
        try:
            if not self.validate_image(image_path):
                return None
            
            # Telegram photo limits: 10MB, max 1280x1280
            telegram_max_size = (1280, 1280)
            telegram_quality = 85
            
            with Image.open(image_path) as img:
                # Convert to RGB
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if needed
                if img.size[0] > telegram_max_size[0] or img.size[1] > telegram_max_size[1]:
                    img.thumbnail(telegram_max_size, Image.Resampling.LANCZOS)
                
                # Generate output path
                if not output_path:
                    name, ext = os.path.splitext(image_path)
                    output_path = f"{name}_telegram{ext}"
                
                # Save optimized image
                img.save(output_path, format='JPEG', optimize=True, 
                        quality=telegram_quality, progressive=True)
                
                # Check file size (should be under 10MB)
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                
                self.logger.info(f"{emoji('centang')} Telegram optimization complete: {file_size:.2f}MB")
                return output_path
                
        except Exception as e:
            self.logger.error(f"{emoji('merah')} Failed to optimize for Telegram: {e}")
            return None
    
    def get_helper_info(self) -> Dict[str, Any]:
        """Get comprehensive image helper information"""
        return {
            "helper_class": self.__class__.__name__,
            "max_size": self.max_size,
            "quality": self.quality,
            "supported_formats": self.supported_formats,
            "features": {
                "validation": True,
                "resizing": True,
                "watermarking": True,
                "telegram_optimization": True,
                "metadata_extraction": True
            },
            "watermark_positions": ["bottom-right", "bottom-left", "top-right", "top-left", "center"]
        }

# Convenience functions
def process_vzoel_images(input_dir: str = "vzoel", output_dir: str = "vzoel/processed") -> Dict[str, Any]:
    """
    Process all images dalam vzoel directory
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        
    Returns:
        Processing results dictionary
    """
    helper = ImageHelper()
    results = {
        "processed": [],
        "failed": [],
        "total": 0,
        "success_count": 0
    }
    
    if not os.path.exists(input_dir):
        helper.logger.warning(f"{emoji('loading')} Input directory not found: {input_dir}")
        return results
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all images
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(fmt) for fmt in helper.supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            results["total"] += 1
            
            # Optimize for Telegram
            optimized = helper.optimize_for_telegram(input_path, output_path)
            
            if optimized:
                results["processed"].append({
                    "filename": filename,
                    "input_path": input_path,
                    "output_path": optimized,
                    "info": helper.get_image_info(optimized)
                })
                results["success_count"] += 1
            else:
                results["failed"].append({
                    "filename": filename,
                    "input_path": input_path,
                    "error": "Processing failed"
                })
    
    helper.logger.info(f"{emoji('centang')} Batch processing complete: {results['success_count']}/{results['total']}")
    return results