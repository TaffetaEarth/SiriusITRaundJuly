from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

description_key = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Описание"),
        ],
    ],
    resize_keyboard=True
)