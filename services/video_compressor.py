import subprocess
import os
from utils.logger import logger

def compress_video_file(input_path: str, output_path: str, level: str) -> bool:
    try:
        # Determine CRFs based on desired output profiles
        if level == "low":
            crf = "22"
            preset = "fast"
        elif level == "high":
            crf = "32"
            preset = "ultrafast"
        else: # balanced / medium
            crf = "28"
            preset = "medium"

        command = [
            "ffmpeg", "-y", "-i", input_path,
            "-vcodec", "libx264", "-crf", crf,
            "-preset", preset, "-acodec", "aac",
            "-b:a", "128k", output_path
        ]
        
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode == 0:
            return True
        else:
            logger.error(f"FFmpeg compression failed: {process.stderr}")
            return False
    except Exception as e:
        logger.error(f"Video execution context error: {e}")
        return False
