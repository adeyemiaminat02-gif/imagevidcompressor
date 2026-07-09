from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_main_menu

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "❓ *How to use this Bot*\n\n"
        "1. Send an image or video directly as a file attachment or media file.\n"
        "2. Choose your preferred processing profile from the runtime button grid.\n"
        "3. Wait briefly for our server worker engine queue to route execution.\n\n"
        "⚠️ Max Processing File Sizes: *25MB* for images / *250MB* for video objects."
    )
    if update.message:
        await update.message.reply_text(help_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(help_text, parse_mode="Markdown", reply_markup=get_main_menu())

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        "ℹ️ *About @ImageVidCompressorBot*\n\n"
        "• *Version:* 1.0.0 (Production-stable)\n"
        "• *Engine:* Python 3.12 Core + FFmpeg Native Binary integration Layer\n"
        "• *Architecture:* Fully Asynchronous Event Processing Framework\n\n"
        "Designed for reliable, fast processing on cloud runtimes."
    )
    if update.message:
        await update.message.reply_text(about_text, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(about_text, parse_mode="Markdown", reply_markup=get_main_menu())
