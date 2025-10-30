from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder

def get_main_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="🎮 Каталог игр")
    kb.button(text="ℹ️ Помощь")
    kb.adjust(1, 1)

    return kb.as_markup(resize_keyboard=True)