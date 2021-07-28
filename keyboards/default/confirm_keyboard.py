from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подтверждаю"),
        ],
    ],
    resize_keyboard=True
)