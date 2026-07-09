from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🖼 Compress Image", callback_data="menu_img"),
         InlineKeyboardButton("🎥 Compress Video", callback_data="menu_vid")],
        [InlineKeyboardButton("⚙ Settings", callback_data="menu_settings")],
        [InlineKeyboardButton("❓ Help", callback_data="menu_help"),
         InlineKeyboardButton("ℹ About", callback_data="menu_about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_compression_keyboard(file_type: str):
    keyboard = [
        [InlineKeyboardButton("🟢 Low Compression (High Quality)", callback_data=f"comp_{file_type}_low")],
        [InlineKeyboardButton("🟡 Medium Compression (Balanced)", callback_data=f"comp_{file_type}_medium")],
        [InlineKeyboardButton("🔴 High Compression (Small Size)", callback_data=f"comp_{file_type}_high")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard(current_settings: dict):
    img_lbl = current_settings['img_level'].upper()
    vid_lbl = current_settings['vid_level'].upper()
    
    keyboard = [
        [InlineKeyboardButton(f"Image Profile: {img_lbl}", callback_data="toggle_img_level")],
        [InlineKeyboardButton(f"Video Profile: {vid_lbl}", callback_data="toggle_vid_level")],
        [InlineKeyboardButton("↩️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)
