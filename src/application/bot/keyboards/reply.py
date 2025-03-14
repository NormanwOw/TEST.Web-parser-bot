from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_kb() -> ReplyKeyboardMarkup:
    row = [
        KeyboardButton(text='📥 Загрузить файл')
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
    return keyboard