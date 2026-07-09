import sys
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler, 
    filters, 
    ContextTypes
)

from utils.config import BOT_TOKEN
from utils.logger import logger
from services.database import init_db

# Component Handlers Imports
from handlers.start import start_handler
from handlers.help_about import help_handler, about_handler
from handlers.settings import settings_handler, settings_callback_router
from handlers.history import history_handler
from handlers.image import image_file_receiver, image_processing_pipeline
from handlers.video import video_file_receiver, video_processing_pipeline

async def global_callback_query_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "menu_main":
        await start_handler(update, context)
    elif data == "menu_help":
        await help_handler(update, context)
    elif data == "menu_about":
        await about_handler(update, context)
    elif data == "menu_settings":
        await settings_handler(update, context)
    elif data.startswith("toggle_"):
        await settings_callback_router(update, context)
    elif data.startswith("comp_image_"):
        level = data.replace("comp_image_", "")
        await image_processing_pipeline(update, context, level)
    elif data.startswith("comp_video_"):
        level = data.replace("comp_video_", "")
        await video_processing_pipeline(update, context, level)

def main():
    if not BOT_TOKEN:
        logger.critical("Missing core runtime configuration context token: BOT_TOKEN environmental variable absent.")
        sys.exit(1)
        
    logger.info("Initializing configuration databases engines schema mappings...")
    init_db()
    
    logger.info("Starting production runtime network application wrapper context loops...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Text Interface Mapping Arrays
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("about", about_handler))
    app.add_handler(CommandHandler("settings", settings_handler))
    app.add_handler(CommandHandler("history", history_handler))
    
    # Document/Media Stream Observers
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, image_file_receiver))
    app.add_handler(MessageHandler(filters.VIDEO | filters.ANIMATION | filters.Document.VIDEO, video_file_receiver))
    
    # Global Callback Automation Node Routing
    app.add_handler(CallbackQueryHandler(global_callback_query_router))
    
    logger.info("Bot ecosystem operational nodes actively online. Intercepting update packets loop.")
    app.run_polling()

if __name__ == "__main__":
    main()
