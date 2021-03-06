from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, reply_keyboard

from keyboards.default.description_keyboard import description_key
from keyboards.default.get_qr_keyboard import get_qr
from keyboards.default.question_keyboard import question
from loader import dp, db, bot


@dp.message_handler(Command("cancel"), state="*")
async def back(message: types.Message, state: FSMContext):
    await message.answer("Вы будете возвращены к началу списка. Продолжить?", reply_markup=question)


@dp.message_handler(text="Да", state="*")
async def return_to_list(message: types.Message, state: FSMContext):
    await message.answer("Введите /get_list", reply_markup=ReplyKeyboardRemove())
    await state.reset_state()


@dp.message_handler(text="Нет", state="my_orders")
async def exit_book_procedure(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Ждем вас снова!", reply_markup=ReplyKeyboardRemove())
    await message.answer("Пссс, если захотите что-нибудь забронировать, просто нажмите /get_list")
    await state.reset_state()


@dp.message_handler(text="Нет", state="*")
async def exit_book_procedure(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Поздравляем с успешным бронированием!", reply_markup=ReplyKeyboardRemove())
    await message.answer("Пссс, если захотите что-нибудь забронировать, просто нажмите /get_list")
    await state.reset_state()


@dp.message_handler(Command("get_list"), state="*")
async def get_list(message: types.Message, state: FSMContext):
    data = db.get_list_of_events()
    print(data)
    list_of_events = []
    i = 0
    for i in range(len(data)):
        event = data[i]
        list_of_events.append(str(i + 1) + '.' + event[-1])
    await state.update_data(max_number=i + 1)
    single_event = "\n".join(list_of_events)
    await message.answer(f"Вот список ближайших мероприятий: \n"
                         f"{single_event}")
    await message.answer(f"Выберите, пожалуйста, номер интересующего вас мероприятия",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state("list_got")


@dp.message_handler(Command("my_orders"), state="*")
async def my_orders(message: types.Message, state: FSMContext):
    orders = db.my_orders(id=message.from_user.id)
    if orders is None:
        await message.answer("Ой, кажется, вы ещё ничего не бронировали",
                             "Чтобы что-нибудь забронировать, нажмите /get_list")
    else:
        print(orders)
        list_of_orders = []
        order_list = []
        for i in range(len(orders)):
            event = db.select_event(orders[i][0])
            print(event)
            if len(str(int(event[0][1]) % 100)) == 1:
                day: str = "0" + str(int(event[0][1]) % 100)
            else:
                day: str = str(int(event[0][1]) % 100)
            if len(str(int(event[0][1]) // 100)) == 1:
                month: str = "0" + str(int(event[0][1]) // 100)
            else:
                month: str = str(int(event[0][1]) // 100)
            if len(str(int(event[0][2]) % 100)) == 1:
                minutes: str = "0" + str(int(event[0][2]) % 100)
            else:
                minutes: str = str(int(event[0][2]) % 100)
            list_of_orders.append(event[0][0] + '\n' + day + "/" + month
                                  + " " + str(int(event[0][2]) // 100) + ":" + minutes + '\n' + event[0][3]
                                  + "\n Количество: " + str(orders[i][1]))
            one_event = "\n".join(list_of_orders)
            order_list.append(one_event)
        all_orders = "\n".join(order_list)
        await message.answer(f"Вы забронировали билеты на следующие события: \n"
                             f"{all_orders} \n"
                             f"Хотите вернуться к бронированию?", reply_markup=question)
        await state.set_state("my_orders")


@dp.message_handler(text="Описание", state="amount_got")
async def description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event_id = data.get("event_id")
    descr = db.description(event_id)
    await message.answer(f"Описание: \n"
                         f"{descr[0][0]}")
    await message.answer(f"Введите количество мест,"
                         f" которые вы хотите забронировать")
    await state.set_state("amount_got")


@dp.message_handler(state="list_got")
async def choose_event(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        number = message.text
        data = db.get_list_of_events()
        if int(number) > len(data):
            await message.answer("Такого мероприятия не существует. \n"
                                 "Пожалуйста, введите номер существующего события")
        else:
            event_id = data[int(number) - 1][0]
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
            list_numbers = await state.get_data()
            max_number = list_numbers.get("max_number")
            if amount - amount_of_handled > 0:
                await message.answer(f"Вы выбрали событие: \n"
                                     f"{one_event} \n"
                                     f"Доступно {int(amount - amount_of_handled)} мест", reply_markup=description_key)
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
    else:
        await message.answer("Вы ввели неправильный формат данных, пожалуйста, введите номер с помощью цифр")


@dp.message_handler(state="amount_got")
async def book_the_tickets(message: types.Message, state: FSMContext):
    amount_to_book = message.text
    if amount_to_book.isdigit():
        data = await state.get_data()
        event_id = data.get("event_id")
        event = data.get("one_event")
        await state.update_data(event=event)
        await state.update_data(amount_to_book=amount_to_book)

        db.book_the_event(id=event_id, user_id=message.from_user.id,
                          amount=amount_to_book)
        if int(amount_to_book) % 10 == 1:
            await message.answer(f"Вы успешно забронировали {amount_to_book} место "
                                 f"на мероприятие: \n"
                                 f"{event} \n", reply_markup=get_qr)
            await state.set_state("qr")
        elif (int(amount_to_book) % 10 >= 2) and (int(amount_to_book) % 10 <= 4) \
                and (int(amount_to_book) // 10 != 1):
            await message.answer(f"Вы успешно забронировали {amount_to_book} места "
                                 f"на мероприятие: \n"
                                 f"{event} \n", reply_markup=get_qr)
            await state.set_state("qr")

        else:
            await message.answer(f"Вы успешно забронировали {amount_to_book} мест "
                                 f"на мероприятие: \n"
                                 f"{event} \n", reply_markup=get_qr)
            await state.set_state("qr")
    else:
        await message.answer(f"Пожалуйста, введите корректное количество")
        await state.set_state("amount_got")


@dp.message_handler(text="Получить QR-код", state="qr")
async def qrcode(message: types.Message, state: FSMContext):
    import qrcode
    data = await state.get_data()
    event = data.get("event")
    amount_to_book = data.get("amount_to_book")
    img = qrcode.make(event + "\n Количество билетов: " + amount_to_book)
    type(img)
    img.save("some_file.png")
    await bot.send_photo(photo=open("some_file.png", "rb"), caption="Ваш QR-код", chat_id=message.from_user.id)
    await state.reset_state()
    await message.answer("Вы получили QR-код. \n"
                         "Хотите вернуться к выбору мероприятий?", reply_markup=question)


@dp.message_handler(Command("my_orders"), state="*")
async def my_orders(message: types.Message, state: FSMContext):
    orders = db.my_orders(id=message.from_user.id)
    if orders is None:
        await message.answer("Ой, кажется, вы ещё ничего не бронировали",
                             "Чтобы что-нибудь забронировать, нажмите /get_list")
    else:
        print(orders)
        list_of_orders = []
        order_list = []
        for i in range(len(orders)):
            event = db.select_event(orders[i][0])
            print(event)
            if len(str(int(event[0][1]) % 100)) == 1:
                day: str = "0" + str(int(event[0][1]) % 100)
            else:
                day: str = str(int(event[0][1]) % 100)
            if len(str(int(event[0][1]) // 100)) == 1:
                month: str = "0" + str(int(event[0][1]) // 100)
            else:
                month: str = str(int(event[0][1]) // 100)
            if len(str(int(event[0][2]) % 100)) == 1:
                minutes: str = "0" + str(int(event[0][2]) % 100)
            else:
                minutes: str = str(int(event[0][2]) % 100)
            list_of_orders.append(event[0][0] + '\n' + day + "/" + month
                                  + " " + str(int(event[0][2]) // 100) + ":" + minutes + '\n' + event[0][3])
            one_event = "\n".join(list_of_orders)
            order_list.append(one_event + "\n Количество: " + str(orders[i][1]))
        all_orders = "\n".join(order_list)
        await message.answer(f"Вы забронировали билеты на следующие события: \n"
                             f"{all_orders} \n"
                             f"Хотите вернуться к бронированию?", reply_markup=question)
        await state.set_state("my_orders")
