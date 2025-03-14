from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text='Отмена', callback_data='cancel'),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard