from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}! \n"
                         f"Я - СириусБот! \n"
                         f"Я расскажу тебе о том, что происходит на Федеральной территории Сириус. \n"
                         f"Нажми /get_list, чтобы увидеть, какие события ожидают тебя здесь в ближайшее время.",
                         reply_markup=ReplyKeyboardRemove())
