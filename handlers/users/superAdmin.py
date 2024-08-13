import datetime
from datetime import timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert, delete, update

from functions import is_super_admin
from keyboards.default.ad import yes_no, to_admin, super_admins_keyboard, admin_add, back_to_admin, money
from keyboards.inline.inline import card_
from loader import dp, bot
from models.models import users, admins, card, adding
from database import async_session_maker
from states.money import Money
from states.superadmin import SuperAdmin
from states.users import Users


@dp.message_handler(text="Botga reklama joylash")
async def reklama(message: Message):
    if await is_super_admin(message.from_user.id):
        await message.answer("Reklamani yuboring:", reply_markup=admin_add)
        await SuperAdmin.state1.set()
    else:
        pass


@dp.message_handler(content_types=['text'], state=SuperAdmin.state1)
async def reklama(message: Message, state: FSMContext):
    if message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa:", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        pass


@dp.message_handler(content_types=["video"], state=SuperAdmin.state1)
async def reklama(message: Message, state: FSMContext):
    await state.update_data({"back": "reklama1"})
    await message.answer("Reklama botga yuklansinmi?", reply_markup=yes_no)
    await state.update_data({"message_id": message.message_id})
    await SuperAdmin.state2.set()


@dp.message_handler(content_types=["photo"], state=SuperAdmin.state1)
async def reklama(message: Message, state: FSMContext):
    await state.update_data({"back": "reklama1"})
    await message.answer("Reklama botga yuklansinmi?", reply_markup=yes_no)
    await state.update_data({"message_id": message.message_id})
    await SuperAdmin.state2.set()


@dp.message_handler(text="Ha✅", state=SuperAdmin.state2)
async def reklama(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data["message_id"]
    async with async_session_maker() as session:
        query = select(users)
        query = await session.execute(query)
        query = query.fetchall()
    for qi in query:
        await bot.copy_message(chat_id=int(qi[1]), from_chat_id=message.from_user.id, message_id=message_id)
    await message.answer("Reklama botga yuklandi", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Yoq❌", state=SuperAdmin.state2)
async def reklama(message: Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Admin qoshish")
async def reklama(message: Message):
    if await is_super_admin(message.from_user.id):
        await message.answer(
            "Foydalanuvchinig IDsini yuboring:\n\nHozirgi qoshilayotgan foydalanuvchi botga start bosgan bo'lishi kerak va Idni tekshirgan holda qoshing.Agar shunday holat boladigan bolsa bot ishlamay qolishi mumkin",
            reply_markup=admin_add)
        await SuperAdmin.state3.set()


@dp.message_handler(state=SuperAdmin.state3)
async def reklama(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({"back": "admin1"})
        await state.update_data({"user_id": message.text})
        await SuperAdmin.state4.set()
        await message.answer("Foydalanuvchi ismi:", reply_markup=admin_add)
    elif message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        await message.answer("ID hato yuborildi")


@dp.message_handler(state=SuperAdmin.state4)
async def reklama(message: Message, state: FSMContext):
    if message.text == "Orqaga 🔙":
        await message.answer("Foydalanuvchinig IDsini yuboring:", reply_markup=admin_add)
        await SuperAdmin.state3.set()
    else:
        await message.answer("Admin qoshishni tasdiqlaysizmi:", reply_markup=yes_no)
        await state.update_data({"name": message.text})
        await SuperAdmin.state15.set()


@dp.message_handler(text="Ha✅", state=SuperAdmin.state15)
async def reklama(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    name = data["name"]
    async with async_session_maker() as session:
        query = insert(admins).values(chat_id=int(user_id), name=name)
        await session.execute(query)
        await session.commit()
    await message.answer("Yangi admin qoshildi", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Yoq❌", state=SuperAdmin.state4)
async def reklama(message: Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Admindan chiqarish")
async def gfd(message: Message):
    if await is_super_admin(message.from_user.id):
        async with async_session_maker() as session:
            query = select(admins)
            query = await session.execute(query)
            query = query.fetchall()
        text = ""
        for qi in query:
            if qi[3] is False:
                text += f"{qi[2]} - <code>{qi[1]}</code>\n"
        if text == "":
            await message.answer("Hech qanday admin yoq")
        else:
            await message.answer(text)
            await message.answer("Admindan chiqarmoqchi bolgan admin Idsini yuboring:", reply_markup=admin_add)
            await SuperAdmin.state5.set()
    else:
        pass


@dp.message_handler(state=SuperAdmin.state5)
async def ghjk(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({"user_id": message.text})
        await state.update_data({"back": "admin2"})
        await message.answer("Tasdiqlash", reply_markup=yes_no)
        await SuperAdmin.state6.set()
    elif message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa:", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        await message.answer("ID hato yuborildi:")


@dp.message_handler(text="Ha✅", state=SuperAdmin.state6)
async def fg(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["user_id"]
    async with async_session_maker() as session:
        query = delete(admins).where(admins.c.chat_id == int(user_id))
        await session.execute(query)
        await session.commit()
    await message.answer("Admindan chiqarildi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Yoq❌", state=SuperAdmin.state6)
async def ghjk(message: Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="To'lov bo'limi")
async def ghjk(message: Message):
    if await is_super_admin(message.from_user.id):
        async with async_session_maker() as session:
            query = select(card)
            query = await session.execute(query)
            query = query.fetchone()
        await message.answer(f"Karta raqami: {query[1]}\n\nBitta reklama narxi: {query[2]} so'm",
                             reply_markup=card_)
    else:
        pass


@dp.callback_query_handler(text="card_change")
async def card_change(call: CallbackQuery):
    if await is_super_admin(call.from_user.id):
        await call.message.answer("Yangi karta raqamini kiriting:", reply_markup=back_to_admin)
        await SuperAdmin.state7.set()
    else:
        pass


@dp.message_handler(state=SuperAdmin.state7)
async def card_change(message: Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) == 16:
        await message.answer("Tasdiqlash", reply_markup=yes_no)
        card_id = message.text
        await state.update_data({"back": "card"})
        await state.update_data({"card_id": card_id})
        await SuperAdmin.state8.set()
    elif message.text == "Orqaga🔙":
        await message.answer("Bosh sahifa:", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        await message.answer("Karta raqami hato!!!")


@dp.message_handler(text="Ha✅", state=SuperAdmin.state8)
async def card_change(message: Message, state: FSMContext):
    data = await state.get_data()
    card_id = int(data["card_id"])
    async with async_session_maker() as session:
        query = update(card).where(card.c.id == 1).values(card_id=card_id)
        await session.execute(query)
        await session.commit()
    await message.answer("Karta raqami ozgardi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Yoq❌", state=SuperAdmin.state8)
async def card_change(message: Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.callback_query_handler(text="amount_change")
async def card_change(call: CallbackQuery):
    if await is_super_admin(call.from_user.id):
        await call.message.answer("Yangi reklama narxini yuboring: ", reply_markup=back_to_admin)
        await SuperAdmin.state10.set()
    else:
        pass


@dp.message_handler(state=SuperAdmin.state10)
async def card_change(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data({"back": "amount1"})
        await state.update_data({"amount": int(message.text)})
        await message.answer("Tasdiqlash", reply_markup=yes_no)
        await SuperAdmin.state11.set()
    elif message.text == "Orqaga🔙":
        await message.answer("Bosh sahifa:", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        await message.answer("Miqdorni hato belgiladingiz", reply_markup=to_admin)


@dp.message_handler(text="Ha✅", state=SuperAdmin.state11)
async def card_change(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = int(data["amount"])
    async with async_session_maker() as session:
        query = update(card).where(card.c.id == 1).values(amount_som=int(amount))
        await session.execute(query)
        await session.commit()
    await message.answer("Miqdor ozgardi!", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Yoq❌", state=SuperAdmin.state11)
async def card_change(message: Message, state: FSMContext):
    await message.answer("Buyruq bekor qilindi", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.message_handler(text="Hisobot")
async def card_change(message: Message):
    if await is_super_admin(message.from_user.id):
        now = datetime.datetime.utcnow()
        start_of_today = datetime.datetime(now.year, now.month, now.day)
        start_of_tomorrow = start_of_today + timedelta(days=1)
        one_week_ago = now - timedelta(weeks=1)
        one_month_ago = now - timedelta(days=30)
        one_year_ago = now - timedelta(days=365)
        async with async_session_maker() as session:
            query_last_day = select(adding).where(adding.c.date_added >= start_of_today,
                                                  adding.c.date_added < start_of_tomorrow)
            query_last_week = select(adding).where(adding.c.date_added >= one_week_ago)
            query_last_year = select(adding).where(adding.c.date_added >= one_year_ago)
            query_last_month = select(adding).where(adding.c.date_added >= one_month_ago)
            query_last_day = await session.execute(query_last_day)
            query_last_week = await session.execute(query_last_week)
            query_last_year = await session.execute(query_last_year)
            query_last_month = await session.execute(query_last_month)
            query_last_day = query_last_day.fetchall()
            query_last_week = query_last_week.fetchall()
            query_last_year = query_last_year.fetchall()
            query_last_month = query_last_month.fetchall()
        last_day_number = 0
        last_day_money = 0
        last_day_deleted = 0
        last_day_no_confirm = 0
        for day in query_last_day:
            if day[4] is True and day[19] is False:
                last_day_number += 1
                last_day_money += int(day[17])
            if day[4] is False:
                last_day_no_confirm += 1
            if day[19] is True:
                last_day_deleted += 1
        last_week_number = 0
        last_week_money = 0
        last_week_deleted = 0
        last_week_no_confirm = 0
        for day in query_last_week:
            if day[4] is True and day[19] is False:
                last_week_number += 1
                last_week_money += int(day[17])
            if day[4] is False:
                last_week_no_confirm += 1
            if day[19] is True:
                last_week_deleted += 1
        last_month_number = 0
        last_month_money = 0
        last_month_deleted = 0
        last_month_no_confirm = 0
        for day in query_last_month:
            if day[4] is True and day[19] is False:
                last_month_number += 1
                last_month_money += int(day[17])
            if day[4] is False:
                last_month_no_confirm += 1
            if day[19] is True:
                last_month_deleted += 1
        last_year_number = 0
        last_year_money = 0
        last_year_deleted = 0
        last_year_no_confirm = 0
        for day in query_last_year:
            if day[4] is True and day[19] is False:
                last_year_number += 1
                last_year_money += int(day[17])
            if day[4] is False:
                last_year_no_confirm += 1
            if day[19] is True:
                last_year_deleted += 1
        await message.answer(
            f"Bir kunlik:\n\n❌Bekor qilinganlari:  {last_day_deleted}\n⏳Hali tasdiqlanmaganlari:  {last_day_no_confirm}\n✅Tasdiqlanganlari:  {last_day_number}\n💸To'lovlar summasi:  {last_day_money} so'm\n\nBir haftalik:\n\n❌Bekor qilinganlari:  {last_week_deleted}\n⏳Hali tasdiqlanmaganlari:  {last_week_no_confirm}\n✅Tasdiqlanganlari:  {last_week_number}\n💸To'lovlar summasi:  {last_week_money} so'm\n\nBir oylik\n\n❌Bekor qilinganlari:  {last_month_deleted}\n⏳Hali tasdiqlanmaganlari:  {last_month_no_confirm}\n✅Tasdiqlanganlari:  {last_month_number}\n💸To'lovlar summasi:  {last_month_money} so'm\n\nBir yilik\n\n❌Bekor qilinganlari:  {last_year_deleted}\n⏳Hali tasdiqlanmaganlari:  {last_year_no_confirm}\n✅Tasdiqlanganlari:  {last_year_number}\n💸To'lovlar summasi:  {last_year_money} so'm",
            reply_markup=money)
        await Money.state1.set()


@dp.message_handler(text="Sana boyicha hisobot", state=Money.state1)
async def boyicha(message: Message, state: FSMContext):
    if message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        await message.answer("Sanani kiritish namuna yil-oy-sana: 2024-01-01", reply_markup=admin_add)
        await Money.state2.set()


@dp.message_handler(text="Orqaga 🔙", state=Money.state1)
async def boyicha(message: Message, state: FSMContext):
    if message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()


@dp.message_handler(state=Money.state2)
async def boyicha(message: Message, state: FSMContext):
    if message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        specific_date = datetime.datetime(int(message.text.split("-")[0]), int(message.text.split("-")[1]),
                                          int(message.text.split("-")[2]))
        start_of_specific_day = datetime.datetime(specific_date.year, specific_date.month, specific_date.day)
        start_of_next_day = start_of_specific_day + timedelta(days=1)
        async with async_session_maker() as session:
            query_specific_day = select(adding).where(adding.c.date_added >= start_of_specific_day,
                                                      adding.c.date_added < start_of_next_day)
            query_specific_day = await session.execute(query_specific_day)
            query_specific_day = query_specific_day.fetchall()
        last_day_number = 0
        last_day_money = 0
        last_day_deleted = 0
        last_day_no_confirm = 0
        for day in query_specific_day:
            if day[4] is True and day[19] is False:
                last_day_number += 1
                last_day_money += int(day[17])
            if day[4] is False:
                last_day_no_confirm += 1
            if day[19] is True:
                last_day_deleted += 1
        await message.answer(
            f"Sana {message.text}:\n\n❌Bekor qilinganlari:  {last_day_deleted}\n⏳Hali tasdiqlanmaganlari:  {last_day_no_confirm}\n✅Tasdiqlanganlari:  {last_day_number}\n💸To'lovlar summasi:  {last_day_money}so'm",
            reply_markup=super_admins_keyboard)
        await state.finish()


@dp.message_handler(commands="superadmin")
async def superadmin(message: Message):
    if await is_super_admin(message.from_user.id):
        await message.answer("Id yuboring:", reply_markup=admin_add)
        await Users.state1.set()


@dp.message_handler(state=Users.state1)
async def superadmin(message: Message, state: FSMContext):
    if message.text.isdigit():
        async with async_session_maker() as session:
            query = select(admins).where(admins.c.chat_id == int(message.text))
            query = await session.execute(query)
            query = query.fetchone()
        if query is not None:
            if query[3] is False:
                async with async_session_maker() as session:
                    query = update(admins).where(admins.c.chat_id == int(message.text)).values(superadmin=True)
                    await session.execute(query)
                    await session.commit()
                    await state.finish()
                await message.answer("Admin bosh adminga o'zgardi", reply_markup=super_admins_keyboard)
            else:
                async with async_session_maker() as session:
                    query = update(admins).where(admins.c.chat_id == int(message.text)).values(superadmin=False)
                    await session.execute(query)
                    await session.commit()
                    await state.finish()
                await message.answer("Admin bosh admindan chiqarildi", reply_markup=super_admins_keyboard)
        else:
            await message.answer("Bunday admin yoq", reply_markup=super_admins_keyboard)
            await state.finish()
    elif message.text == "Orqaga 🔙":
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()
    await state.finish()
