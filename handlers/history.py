from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_history

async def history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    records = get_history(user_id)
    
    if not records:
        await update.message.reply_text("🗄️ No recorded conversion jobs found on your profile history.")
        return
        
    response = "📊 *Your Last 10 Processing Events*\n\n"
    for i, rec in enumerate(records, 1):
        orig_mb = rec[1] / (1024 * 1024)
        comp_mb = rec[2] / (1024 * 1024)
        saved = ((rec[1] - rec[2]) / rec[1]) * 100 if rec[1] > 0 else 0
        response += f"*{i}. {rec[0]}*\n ⏬ {orig_mb:.2f}MB → 📦 {comp_mb:.2f}MB ( Saved: {saved:.1f}% )\n 🕒 _{rec[3]}_\n\n"
        
    await update.message.reply_text(response, parse_mode="Markdown")
