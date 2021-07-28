from aiogram import Dispatcher
from .ListFilter import ListFilter

from loader import dp

# from .is_admin import AdminFilter


if __name__ == "filters":
    # dp.filters_factory.bind(is_admin)
    dp.filters_factory.bind(ListFilter)
    pass
