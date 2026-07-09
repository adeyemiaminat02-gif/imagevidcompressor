import os
from telegram import Update
from telegram.ext import ContextTypes
from utils.config import MAX_IMAGE_SIZE, DOWNLOAD_DIR, OUTPUT_DIR
from utils.logger import logger
from services.queue_manager import queue_manager
from services.image_compressor import compress_image_file
from services.database import get_settings, log_history
from keyboards.inline import get_compression_keyboard

async def image_file_receiver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    photo_file = msg.photo[-1] if msg.photo else (msg.document if msg.document.mime_type.startswith("image/") else None)
    
    if not photo_file:
        await msg.reply_text("❌ Unsupported document system structure.")
        return
        
    if photo_file.file_size > MAX_IMAGE_SIZE:
        await msg.reply_text("⚠️ This file exceeds our structural 25MB processing limits.")
        return
        
    context.user_data["pending_file_id"] = photo_file.file_id
    context.user_data["pending_file_type"] = "image"
    context.user_data["pending_filename"] = getattr(photo_file, "file_name", "image.jpg")
    
    await msg.reply_text(
        f"📊 *File Recognized Successfully*\n\n"
        f"• Size: {photo_file.file_size / (1024*1024):.2f} MB\n\n"
        f"Select requested optimization matrix parameters below:",
        parse_mode="Markdown",
        reply_markup=get_compression_keyboard("image")
    )

async def image_processing_pipeline(update: Update, context: ContextTypes.DEFAULT_TYPE, level: str):
    query = update.callback_query
    user_id = query.from_user.id
    
    file_id = context.user_data.get("pending_file_id")
    filename = context.user_data.get("pending_filename", "image.jpg")
    
    if not file_id:
        await query.message.reply_text("❌ Session lost. Please upload your file asset again.")
        return
        
    status_msg = await query.message.reply_text("⏳ Request entered service queue pipeline... awaiting allocation slot.")
    await queue_manager.acquire(user_id)
    
    try:
        await status_msg.edit_text("⚡ Downloading media source files from Telegram datacenter nodes...")
        tg_file = await context.bot.get_file(file_id)
        
        in_path = os.path.join(DOWNLOAD_DIR, f"{user_id}_{file_id}_{filename}")
        out_path = os.path.join(OUTPUT_DIR, f"compressed_{user_id}_{file_id}_{filename}")
        
        await tg_file.download_to_drive(in_path)
        await status_msg.edit_text("⚙️ Compressing image matrices... optimizing structural buffers.")
        
        success = compress_image_file(in_path, out_path, level)
        
        if success and os.path.exists(out_path):
            await status_msg.edit_text("📤 Delivering optimization yields back to user workspace...")
            orig_size = os.path.getsize(in_path)
            comp_size = os.path.getsize(out_path)
            saved_pct = ((orig_size - comp_size) / orig_size) * 100
            
            with open(out_path, "rb") as delivery_file:
                await query.message.reply_document(
                    document=delivery_file,
                    filename=f"compressed_{filename}",
                    caption=(
                        "✅ *Compression Matrix Cycle Executed Perfectly!*\n\n"
                        f"• Original Size: {orig_size/(1024*1024):.2f} MB\n"
                        f"• Processed Size: {comp_size/(1024*1024):.2f} MB\n"
                        f"• Storage Recovered: *{saved_pct:.1f}%*"
                    ),
                    parse_mode="Markdown"
                )
            log_history(user_id, filename, orig_size, comp_size)
        else:
            await query.message.reply_text("❌ System error encountered in file optimization pass.")
            
        # Cleanup routine
        for p in (in_path, out_path):
            if os.path.exists(p): os.remove(p)
            
    except Exception as e:
        logger.error(f"Global execution catch hook triggered: {e}")
        await query.message.reply_text("💥 Fatal crash pipeline anomaly terminated processing jobs.")
    finally:
        queue_manager.release(user_id)
        await status_msg.delete()
