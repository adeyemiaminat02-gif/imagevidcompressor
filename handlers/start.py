from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_main_menu
from services.database import add_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username or "Unknown")
    
    welcome_text = (
        "🗜️ *Welcome to Image & Video Compressor Bot!*\n\n"
        "I can reduce file sizes effectively while preserving excellent visual properties.\n\n"
        "*Supported Ecosystem Formats:*\n"
        "• Images: JPG, JPEG, PNG, WEBP\n"
        "• Videos: MP4, MOV, AVI, MKV, WEBM\n\n"
        "Select an option below to begin process routing:"
    )
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())
