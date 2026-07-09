from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_settings_keyboard
from services.database import get_settings, update_settings

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current = get_settings(user_id)
    text = "⚙️ *User Processing Architecture Configurations*"
    
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=get_settings_keyboard(current))
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, parse_mode="Markdown", reply_markup=get_settings_keyboard(current))

async def settings_callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    current = get_settings(user_id)
    
    if query.data == "toggle_img_level":
        next_level = "high" if current["img_level"] == "medium" else ("low" if current["img_level"] == "high" else "medium")
        update_settings(user_id, "img_level", next_level)
    elif query.data == "toggle_vid_level":
        next_level = "high" if current["vid_level"] == "balanced" else ("low" if current["vid_level"] == "high" else "balanced")
        update_settings(user_id, "vid_level", next_level)
        
    updated_settings = get_settings(user_id)
    await query.message.edit_reply_markup(reply_markup=get_settings_keyboard(updated_settings))
