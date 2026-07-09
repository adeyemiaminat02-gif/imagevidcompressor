import os
from PIL import Image
from utils.logger import logger

def compress_image_file(input_path: str, output_path: str, level: str) -> bool:
    try:
        with Image.open(input_path) as img:
            img_format = img.format if img.format else "JPEG"
            
            if level == "low":
                quality = 85
                resize_factor = 1.0
            elif level == "high":
                quality = 40
                resize_factor = 0.6
            else: # medium / balanced
                quality = 65
                resize_factor = 0.8
                
            if resize_factor < 1.0:
                new_width = int(img.width * resize_factor)
                new_height = int(img.height * resize_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
            if img.mode in ("RGBA", "P") and img_format in ("JPEG", "JPG"):
                img = img.convert("RGB")
                
            img.save(output_path, format=img_format, quality=quality, optimize=True)
            return True
    except Exception as e:
        logger.error(f"Image reduction crash profile: {e}")
        return False
