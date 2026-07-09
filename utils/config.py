import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "bot_database.db")
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 26214400)) # Default 25MB
MAX_VIDEO_SIZE = int(os.getenv("MAX_VIDEO_SIZE", 262144000)) # Default 250MB

DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "outputs"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
