from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_qr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить QR-код"),
        ],
    ],
    resize_keyboard=True
)