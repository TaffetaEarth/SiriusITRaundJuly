from aiogram.dispatcher.filters import BoundFilter, Command, state
from aiogram import types


class ListFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if Command("get_list") is True:
            return True
        if state == "start":
            return True
