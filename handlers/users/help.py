from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/get_list - Вывести ближайшие мероприятия",
            "/my_orders - Посмотреть, что ты уже забронировал")
    
    await message.answer("\n".join(text))
