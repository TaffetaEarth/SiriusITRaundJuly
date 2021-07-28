from statistics import mean

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters.ListFilter import ListFilter
from loader import dp, db


@dp.message_handler(Command("get_list"))
@dp.message_handler(state="start")
async def get_list(message: types.Message, state: FSMContext):
    data = db.get_list_of_events()
    list_of_events = []
    for i in range(len(data)):
        event = data[i]
        list_of_events.append(event[0] + '.' + event[-1])
    single_event = "\n".join(list_of_events)
    await message.answer(f"Вот список ближайших мероприятий: \n"
                         f"{single_event}")
    await message.answer(f"Выберите, пожалуйста, номер интересующего вас мероприятия")
    await state.set_state("list_got")


@dp.message_handler(state="list_got")
async def choose_event(message: types.Message, state: FSMContext):
    event_id = message.text
    await state.update_data(event_id=event_id)
    data = db.select_event(id=event_id)
    single_event = []
    for i in range(len(data)):
        event = data[i]
        if len(str(int(event[1]) % 100)) == 1:
            day: str = "0" + str(int(event[1]) % 100)
        else:
            day: str = str(int(event[1]) % 100)
        if len(str(int(event[1]) // 100)) == 1:
            month: str = "0" + str(int(event[1]) // 100)
        else:
            month: str = str(int(event[1]) // 100)
        if len(str(int(event[2]) % 100)) == 1:
            minutes: str = "0" + str(int(event[2]) % 100)
        else:
            minutes: str = str(int(event[2]) % 100)
        single_event.append(event[0] + '\n' + day + "/" + month
                            + " " + str(int(event[2]) // 100) + ":" + minutes + '\n' + event[3])
    one_event = "\n".join(single_event)
    amount = db.get_amount_of_places(event_id)[0]
    handled = db.get_handled_places(id=event_id)
    print(handled)
    amount_of_handled = 0
    for f in range(len(handled)):
        amount_of_handled += int(handled[f][0])
    await state.update_data(one_event=one_event)
    print(amount - amount_of_handled)
    if amount - amount_of_handled > 0:
        await message.answer(f"Вы выбрали событие: \n"
                             f"{one_event} \n"
                             f"Доступно {int(amount - amount_of_handled)} мест")
        await message.answer(f"Введите количество мест,"
                             f" которые вы хотите забронировать")
        await state.set_state("amount_got")
    elif amount - amount_of_handled == 0:
        await message.answer("К сожалению, мест больше нет \n"
                             "Пожалуйста, выберите другое мероприятие")
        data = db.get_list_of_events()
        list_of_events = []
        for i in range(len(data)):
            event = data[i]
            list_of_events.append(event[0] + '.' + event[-1])
        single_event = "\n".join(list_of_events)
        await message.answer(f"Вот список ближайших мероприятий: \n"
                             f"{single_event}")
        await message.answer(f"Выберите, пожалуйста, номер интересующего вас мероприятия")
        await state.set_state("list_got")
    else:
        await message.answer(f"К сожалению, свободных мест не хватает. \n"
                             f"Пожалуйста, выберите корректное количество мест")


@dp.message_handler(state="amount_got")
async def book_the_tickets(message: types.Message, state: FSMContext):
    amount_to_book = message.text
    if amount_to_book.isdigit():
        data = await state.get_data()
        event_id = data.get("event_id")
        event = data.get("one_event")
        db.book_the_event(id=event_id, user_id=message.from_user.id,
                          amount=amount_to_book)
        if int(amount_to_book) % 10 == 1:
            await message.answer(f"Вы успешно забронировали {amount_to_book} место "
                                 f"на мероприятие: \n"
                                 f"{event}"
                                 f"Хотите забронировать еще билеты?")
        elif (int(amount_to_book) % 10 >= 2) and (int(amount_to_book) % 10 <= 4) \
                and (int(amount_to_book) // 10 != 1):
            await message.answer(f"Вы успешно забронировали {amount_to_book} места "
                                 f"на мероприятие: \n"
                                 f"{event}"
                                 f"Хотите забронировать еще билеты?")
        else:
            await message.answer(f"Вы успешно забронировали {amount_to_book} мест "
                                 f"на мероприятие: \n"
                                 f"{event} \n"
                                 f"Хотите забронировать еще билеты?")
        await state.set_state("ask_to_book_again")
    else:
        await message.answer(f"Пожалуйста, введите корректное количество")
        await state.set_state("amount_got")


@dp.message_handler(state="ask_to_book_again")
async def return_to_book(message: types.Message, state: FSMContext):
    if message.text != "Да" and message.text != "Нет":
        await message.answer("Пожалуйста, ответьте Да/Нет")
    if message.text == "Да":
        await state.set_state("start")
        # data = db.get_list_of_events()
        # list_of_events = []
        # for i in range(len(data)):
        #     event = data[i]
        #     list_of_events.append(event[0] + '.' + event[-1])
        # single_event = "\n".join(list_of_events)
        # await message.answer(f"Вот список ближайших мероприятий: \n"
        #                      f"{single_event}")
        # await message.answer(f"Выберите, пожалуйста, номер интересующего вас мероприятия")
        # await state.set_state("list_got")
    if message.text == "Нет":
        await state.finish()
        await message.answer("Поздравляем с успешным бронированием!")



