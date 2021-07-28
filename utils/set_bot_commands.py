from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("get_list", "Вывести список мероприятий"),
            types.BotCommand("my_orders", "Посмотреть, что вы уже забронировали")
        ]
    )
