from aiogram.dispatcher import FSMContext
from sqlalchemy import select, update, insert

from database import async_session_maker
from functions import is_admin, is_super_admin, adding_language
from keyboards.default.ad import back_to_admin, super_admins_keyboard, admins_keyboard, ad_for_uzbek, ad_for_russian, \
    back_to_ru, edit_back, admin_add
from keyboards.inline.inline import location, edits, to_ask, to_ask_answer, place_answer, delete_confirm, \
    to_ask_answer_ru
from keyboards.inline.yes_no import yes_no, paid, paid_messa
from loader import dp, bot
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from models.models import adding, paid_message, users
from states.admins import Admins
from states.for_ask import Ask
from states.for_edit import Edits
from functions import create_inline_keyboard


@dp.message_handler(text="So'rovlar")
async def fgf(message: Message):
    if await is_admin(int(message.from_user.id)) or await is_super_admin(int(message.from_user.id)):
        async with async_session_maker() as session:
            query = select(adding)
            query = await session.execute(query)
            query = query.fetchall()
        status = 0
        for q in query:
            if q[4] is False:
                status += 1
        if status == 0:
            await message.answer("Hozirda hech qanday so'rov yoq!")
        if query:
            for q in query:
                if q[3] == True and q[4] == False and q[19] == False:
                    file_ids = q[18].split(",")
                    file_ids = file_ids[:-1]
                    if len(file_ids) > 1:
                        media = [InputMediaPhoto(file_id) for file_id in file_ids]
                        media[
                            0].caption = f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n"
                        await bot.send_media_group(chat_id=message.from_user.id, media=media)
                        await bot.send_photo(chat_id=message.from_user.id, photo=q[5],
                                             caption=f"E'lon raqami: {q[0]}\nTo'langan✅",
                                             reply_markup=location)
                    elif len(file_ids) == 1:
                        photo = file_ids[0]
                        await bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                             caption=f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n")
                        await bot.send_photo(chat_id=message.from_user.id, photo=q[5],
                                             caption=f"E'lon raqami: {q[0]}\nTo'langan✅",
                                             reply_markup=location)
                elif q[3] == False and q[4] == False and q[19] == False:
                    file_ids = q[18].split(",")
                    file_ids = file_ids[:-1]
                    if len(file_ids) > 1:
                        media = [InputMediaPhoto(file_id) for file_id in file_ids]
                        media[
                            0].caption = f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n"
                        await bot.send_media_group(chat_id=message.from_user.id, media=media)
                        await bot.send_photo(chat_id=message.from_user.id, photo=q[5],
                                             caption=f"E'lon raqami: {q[0]}\nTo'lanamagan❌",
                                             reply_markup=location)
                    elif len(file_ids) == 1:
                        photo = file_ids[0]
                        await bot.send_photo(chat_id=message.from_user.id, photo=photo,
                                             caption=f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n")
                        await bot.send_photo(chat_id=message.from_user.id, photo=q[5],
                                             caption=f"E'lon raqami: {q[0]}\nTo'lanamagan❌",
                                             reply_markup=location)


@dp.callback_query_handler(text="placement")
async def placement(call: CallbackQuery):
    message_id = call.message.message_id
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=yes_no)


@dp.callback_query_handler(text="yes_")
async def back(call: CallbackQuery):
    text = call.message.caption
    num = int(((text.split("\n"))[0]).split(": ")[1])
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == num)
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    file_ids = query[15].split(",")
    for_media = []
    for file_id in file_ids:
        if file_id != "None":
            for_media.append(file_id)
    media = [InputMediaPhoto(file_id) for file_id in for_media]
    media[
        0].caption = f"Mashina nomi: {query[2]}\n\n📅Ishlab chiqarilgan yili: {query[6]}\n👣Probeg: {query[7]}\n🛠Holati: {query[8]}\n🎨Rangi: {query[16]}\n❄️Konditsioner: {query[10]}\n✅Qo’shimcha jihozlar: {query[9]}\n⛽️Yoqilg'isi: {query[11]}\n💰Narxi: {query[12]}\n☎️Telefon raqami: {query[13]}\n🚩Manzil: {query[14]}\n"
    if query[3]:
        await bot.send_media_group(chat_id=-1002053603769, media=media)
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(confirm=True)
            await session.execute(query)
            await session.commit()
        await call.message.delete()
        await call.answer("E'lon kanalga joylandi")
        await bot.send_message(chat_id=int(chat_id), text="E'loningiz kanalga joylandi korishingiz mumkin")
    else:
        await call.answer("To'lanamagan❌")


@dp.callback_query_handler(text="back_")
async def back(call: CallbackQuery):
    message_id = call.message.message_id
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=location)


@dp.callback_query_handler(text="check_paid")
async def check_paid(call: CallbackQuery):
    message_id = call.message.message_id
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=paid)


@dp.callback_query_handler(text="paid_yes")
async def paid_yes(call: CallbackQuery):
    message_id = call.message.message_id
    text = call.message.caption
    text = text.replace("To'lanamagan❌", "To'langan✅")
    num = int(((text.split("\n"))[0]).split(": ")[1])
    async with async_session_maker() as session:
        query = update(adding).where(adding.c.id == num).values(paid=True)
        await session.execute(query)
        await session.commit()
    await bot.edit_message_caption(chat_id=call.from_user.id, message_id=message_id, caption=text,
                                   reply_markup=location)


@dp.callback_query_handler(text="paid_no")
async def paid_yes(call: CallbackQuery):
    message_id = call.message.message_id
    text = call.message.caption
    text = text.replace("To'langan✅", "To'lanamagan❌")
    num = int(((text.split("\n"))[0]).split(": ")[1])
    async with async_session_maker() as session:
        query = update(adding).where(adding.c.id == num).values(paid=False)
        await session.execute(query)
        await session.commit()
    await bot.edit_message_caption(chat_id=call.from_user.id, message_id=message_id, caption=text,
                                   reply_markup=location)


@dp.callback_query_handler(text="paid_user")
async def paid_user(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = int(((text.split("\n"))[0]).split(": ")[1])
    await state.update_data({"num": num})
    await bot.send_message(chat_id=call.from_user.id, text="To'lovdagi muamoni yozing:", reply_markup=back_to_admin)
    await Admins.state1.set()


@dp.message_handler(state=Admins.state1)
async def state1(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "Orqaga🔙" and await is_super_admin(message.from_user.id):
        await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
        await state.finish()
    elif message.text == "Orqaga🔙" and await is_admin(message.from_user.id):
        await message.answer("Bosh sahifa", reply_markup=admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = select(adding).where(adding.c.id == num)
            query = await session.execute(query)
            query = query.fetchone()
        chat_id = query[1]
        message_id = await bot.send_message(chat_id=chat_id, text=message.text, reply_markup=paid_messa)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message=message.text, num=num,
                                                admin_id=message.from_user.id, message_id=message_id.message_id)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Savol yuborildi!", reply_markup=super_admins_keyboard)
            await state.finish()
        else:
            await message.answer("Savol yuborildi!", reply_markup=admins_keyboard)
            await state.finish()


@dp.callback_query_handler(text="paid_message")
async def paid_message_(call: CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    await call.message.answer("Screenshotni yuboring:", reply_markup=back_to_admin)
    await state.update_data({"message_id": message_id})
    await Admins.state3.set()


@dp.message_handler(content_types="text", state=Admins.state3)
async def paid_message_(message: Message, state: FSMContext):
    if message.text == "Orqaga🔙":
        await message.answer("Bosh sahifa", reply_markup=ad_for_uzbek)
        await state.finish()
    else:
        data = await state.get_data()
        message_id = int(data["message_id"])
        async with async_session_maker() as session_:
            query = select(paid_message).where(paid_message.c.message_id == message_id)
            query = await session_.execute(query)
            query = query.fetchone()
        num = query[2]
        chat_id = query[4]
        async with async_session_maker() as session:
            q = select(adding).where(adding.c.id == int(num))
            q = await session.execute(q)
            q = q.fetchone()
        file_ids = q[18].split(",")
        file_ids = file_ids[:-1]
        media = [InputMediaPhoto(file_id) for file_id in file_ids]
        media[
            0].caption = f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n"
        await bot.send_media_group(chat_id=query[4], media=media)
        if q[3] is True:
            await bot.send_photo(chat_id=chat_id, photo=q[5],
                                 caption=f"E'lon raqami: {num}\nTo'lanamagan❌\n\nSavol: {query[3]}\nJavob: {message.text}",
                                 reply_markup=location)
        else:
            await bot.send_photo(chat_id=chat_id, photo=q[5],
                                 caption=f"E'lon raqami: {num}\nTo'langan✅\n\nSavol: {query[3]}\nJavob: {message.text}",
                                 reply_markup=location)
        await message.answer("So'rov qabul qilindi!", reply_markup=ad_for_uzbek)
        await state.finish()


@dp.message_handler(content_types="photo", state=Admins.state3)
async def paid_message_(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = int(data["message_id"])
    photo_id = message.photo[-1].file_id
    async with async_session_maker() as session_:
        query = select(paid_message).where(paid_message.c.message_id == message_id)
        query = await session_.execute(query)
        query = query.fetchone()
    num = query[2]
    chat_id = query[4]
    async with async_session_maker() as session:
        q = select(adding).where(adding.c.id == int(num))
        q = await session.execute(q)
        q = q.fetchone()
    file_ids = q[18].split(",")
    file_ids = file_ids[:-1]
    media = [InputMediaPhoto(file_id) for file_id in file_ids]
    media[
        0].caption = f"Mashina nomi: {q[2]}\n\n📅Ishlab chiqarilgan yili: {q[6]}\n👣Probeg: {q[7]}\n🛠Holati: {q[8]}\n🎨Rangi: {q[16]}\n❄️Konditsioner: {q[10]}\n✅Qo’shimcha jihozlar: {q[9]}\n⛽️Yoqilg'isi: {q[11]}\n💰Narxi: {q[12]}\n☎️Telefon raqami: {q[13]}\n🚩Manzil: {q[14]}\n"
    await bot.send_media_group(chat_id=query[4], media=media)
    if q[3] is True:
        await bot.send_photo(chat_id=chat_id, photo=photo_id,
                             caption=f"E'lon raqami: {num}\nTo'lanamagan❌\nSavol: {query[3]}",
                             reply_markup=location)
    else:
        await bot.send_photo(chat_id=chat_id, photo=photo_id,
                             caption=f"E'lon raqami: {num}\nTo'langan✅\nSavol: {query[3]}",
                             reply_markup=location)
    async with async_session_maker() as session:
        query = update(adding).where(adding.c.id == int(num)).values(photo_id=photo_id)
        await session.execute(query)
        await session.commit()
    await message.answer("So'rov qabul qilindi!", reply_markup=ad_for_uzbek)
    await state.finish()


@dp.callback_query_handler(text="edit")
async def paid_message_(call: CallbackQuery):
    message_id = call.message.message_id
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="edit_year")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state1.set()


@dp.message_handler(state=Edits.state1)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(years=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.message_handler(text='orqaga🔙')
async def orqaga(message: Message, state: FSMContext):
    await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
    await state.finish()


@dp.callback_query_handler(text="edit_text")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state2.set()


@dp.message_handler(state=Edits.state2)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(text=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_phone")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state3.set()


@dp.message_handler(state=Edits.state3)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(phone_number=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_facilities")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state4.set()


@dp.message_handler(state=Edits.state4)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(amenities=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_conditioning")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state5.set()


@dp.message_handler(state=Edits.state5)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(condition=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_address")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state6.set()


@dp.message_handler(state=Edits.state6)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(address=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_fuel")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state7.set()


@dp.message_handler(state=Edits.state7)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(fuel=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_color")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state8.set()


@dp.message_handler(state=Edits.state8)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(color=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_status")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state9.set()


@dp.message_handler(state=Edits.state9)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(status=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_probeg")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state10.set()


@dp.message_handler(state=Edits.state10)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(probeg=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="edit_paid")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    await state.update_data({"num": num})
    await call.message.answer("O'zgartirmoqchi bolgan malumotingizni yuboring", reply_markup=edit_back)
    await Edits.state11.set()


@dp.message_handler(state=Edits.state11)
async def defe(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    if message.text == "orqaga🔙":
        await message.answer("Bosh menyu", reply_markup=super_admins_keyboard)
        await state.finish()
    else:
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == num).values(payment=message.text)
            await session.execute(query)
            await session.commit()
        if await is_super_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=super_admins_keyboard)
        elif await is_admin(message.from_user.id):
            await message.answer("Qabul qilindi!", reply_markup=admins_keyboard)
        await state.finish()


@dp.callback_query_handler(text="to_ask")
async def paid_mess(call: CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        reply_markup=to_ask)


@dp.callback_query_handler(text="ask_text")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring:", reply_markup=edit_back)
    await Ask.state1.set()


@dp.message_handler(state=Ask.state1)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_text',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_text',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_year")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state3.set()


@dp.message_handler(state=Ask.state3)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_year',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_year',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_phone")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state4.set()


@dp.message_handler(state=Ask.state4)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_phone',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_phone',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_facilities")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state5.set()


@dp.message_handler(state=Ask.state5)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_facilities',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_facilities',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_conditioning")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state6.set()


@dp.message_handler(state=Ask.state6)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_conditioning',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_conditioning',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_address")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state7.set()


@dp.message_handler(state=Ask.state7)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_address',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_address',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_color")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state8.set()


@dp.message_handler(state=Ask.state8)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_color',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_color',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_fuel")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state9.set()


@dp.message_handler(state=Ask.state9)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_fuel',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_fuel',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_status")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state10.set()


@dp.message_handler(state=Ask.state10)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_status',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_status',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_probeg")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state11.set()


@dp.message_handler(state=Ask.state11)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_probeg',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_probeg',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="ask_paid")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    chat_id = query[1]
    await state.update_data({"num": num})
    await state.update_data({"chat_id": chat_id})
    await call.message.answer("Savolingizni yuboring!", reply_markup=edit_back)
    await Ask.state12.set()


@dp.message_handler(state=Ask.state12)
async def paid_mess(message: Message, state: FSMContext):
    data = await state.get_data()
    num = int(data["num"])
    chat_id = int(data["chat_id"])
    language = await adding_language(num)
    if language == "uzbek":
        try:
            message_id = await bot.send_message(chat_id=chat_id,
                                                text=f"{message.text}\n\nJavobingizni javob yozish tugmasini bosib yozing",
                                                reply_markup=to_ask_answer)
            async with async_session_maker() as session:
                query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_paid',
                                                    message=message.text, admin_id=message.from_user.id, num=num)
                if await is_super_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
                elif await is_admin(message.from_user.id):
                    await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
                await state.finish()
                await session.execute(query)
                await session.commit()
        except Exception as e:
            if await is_super_admin(message.from_user.id):
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=super_admins_keyboard)
                await state.finish()
            else:
                await message.answer("Bu foydalanuvchi botni bloklab qoygan bu foydalanuvchiga habar yozib bolmaydi",
                                     reply_markup=admins_keyboard)
                await state.finish()
    elif language == "russian":
        message_id = await bot.send_message(chat_id=chat_id,
                                            text=f"{message.text}\n\nНапишите свой ответ, нажав кнопку ответить",
                                            reply_markup=to_ask_answer_ru)
        async with async_session_maker() as session:
            query = insert(paid_message).values(chat_id=chat_id, message_id=message_id, type='ask_paid',
                                                message=message.text, admin_id=message.from_user.id, num=num)
            await session.execute(query)
            await session.commit()


@dp.callback_query_handler(text="to_ask_answer")
async def paid_mess(call: CallbackQuery, state: FSMContext):
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(paid_message).where(paid_message.c.message_id == message_id)
        query = await session.execute(query)
        query = query.fetchone()
    num = int(query[2])
    language = await adding_language(num)
    text = call.message.text.split('\n')[0]
    await state.update_data({"message_id": message_id})
    await state.update_data({"text": text})
    await state.update_data({"language": language})
    if language == "uzbek":
        await call.message.answer("Javobingiz:", reply_markup=back_to_admin)
    else:
        await call.message.answer("Ваш ответ:", reply_markup=back_to_ru)
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=None)
    await Ask.state2.set()


@dp.message_handler(state=Ask.state2)
async def paid_mess(message: Message, state: FSMContext):
    if message.text == "Orqaga🔙":
        await message.answer("Bosh sahifa", reply_markup=ad_for_uzbek)
        await state.finish()
    elif message.text == "Назад🔙":
        await message.answer("Главная страница", reply_markup=ad_for_russian)
        await state.finish()
    else:
        data = await state.get_data()
        message_id = int(data["message_id"])
        question = data["text"]
        language = data["language"]
        async with async_session_maker() as session:
            query = select(paid_message).where(paid_message.c.message_id == message_id)
            query = await session.execute(query)
            query = query.fetchone()
        admin_id = query[4]
        typed = query[-1]
        num = int(query[2])
        async with async_session_maker() as session:
            query_ = select(adding).where(adding.c.id == num)
            query_ = await session.execute(query_)
            query_ = query_.fetchone()
        file_ids = query_[18].split(",")
        file_ids = file_ids[:-1]
        media = [InputMediaPhoto(file_id) for file_id in file_ids]
        media[
            0].caption = f"Mashina nomi: {query_[2]}\n\n📅Ishlab chiqarilgan yili: {query_[6]}\n👣Probeg: {query_[7]}\n🛠Holati: {query_[8]}\n🎨Rangi: {query_[16]}\n❄️Konditsioner: {query_[10]}\n✅Qo’shimcha jihozlar: {query_[9]}\n⛽️Yoqilg'isi: {query_[11]}\n💰Narx: {query_[12]}\n☎️Telefon raqami: {query_[13]}\n🚩Manzil: {query_[14]}\n"
        await bot.send_media_group(chat_id=int(query[4]), media=media)
        if language == "uzbek":
            await message.answer("Javobingiz qabul qilindi", reply_markup=ad_for_uzbek)
        elif language == "russian":
            await message.answer("Ваш ответ принят", reply_markup=ad_for_russian)
        await bot.send_message(chat_id=admin_id,
                               text=f"E'lon raqami: {query[2]}\nSavol: {question}\nJavob: {message.text}\n\n{typed}",
                               reply_markup=place_answer)
        await state.finish()


@dp.callback_query_handler(text="place_answer")
async def paid_mess(call: CallbackQuery):
    text = call.message.text
    num = (text.split("\n"))[0].split(": ")[1]
    answer = (text.split("\n"))[2].split(": ")[1]
    typed = (text.split("\n"))[4]
    if typed == "ask_text":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(text=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_year":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(years=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_phone":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(phone_number=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_facilities":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(amenities=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_conditioning":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(condition=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_address":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(address=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_paid":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(payment=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_fuel":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(fuel=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_color":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(color=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_status":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(status=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_probeg":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(probeg=answer)
            await session.execute(query)
            await session.commit()
    elif typed == "ask_paid":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(payment=answer)
            await session.execute(query)
            await session.commit()
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=None)
    await call.answer("Javob qabul qilindi!")


@dp.callback_query_handler(text="edit_photo")
async def edit_photo_(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    new = []
    for i in photo_num:
        if i != "None":
            new.append(i)
    if len(new) <= 1:
        await call.answer("Bittalik rasmlarni o'chirib bolmaydi❌")
    else:
        key = await create_inline_keyboard(photo_num)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=message_id,
                                            reply_markup=key)


@dp.callback_query_handler(text="photo_1")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"None,{photo_num[1]},{photo_num[2]},{photo_num[3]},{photo_num[4]},{photo_num[5]}"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[4]},{numeration_photo[5]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[4]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[1]},{numeration_photo[2]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[1]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="photo_2")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"{photo_num[0]},None,{photo_num[2]},{photo_num[3]},{photo_num[4]},{photo_num[5]}"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[4]},{numeration_photo[5]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[4]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[2]},{numeration_photo[3]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[2]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[0]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="photo_3")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"{photo_num[0]},{photo_num[1]},None,{photo_num[3]},{photo_num[4]},{photo_num[5]}"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[3]},{numeration_photo[4]},{numeration_photo[5]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[3]},{numeration_photo[4]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[3]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[0]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="photo_4")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"{photo_num[0]},{photo_num[1]},{photo_num[2]},None,{photo_num[4]},{photo_num[5]}"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[4]},{numeration_photo[5]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[4]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[0]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="photo_5")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"{photo_num[0]},{photo_num[1]},{photo_num[2]},{photo_num[3]},None,{photo_num[5]}"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[5]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[0]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="photo_6")
async def first_photo(call: CallbackQuery):
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    message_id = call.message.message_id
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == int(num))
        query = await session.execute(query)
        query = query.fetchone()
    photo_num = query[15].split(",")
    numeration_photo = query[18].split(",")
    new_photos = f"{photo_num[0]},{photo_num[1]},{photo_num[2]},{photo_num[3]},{photo_num[4]},None"
    new_numeration_photo = ""
    if len(numeration_photo) == 7:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},{numeration_photo[4]},"
    elif len(numeration_photo) == 6:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},{numeration_photo[3]},"
    elif len(numeration_photo) == 5:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},{numeration_photo[2]},"
    elif len(numeration_photo) == 4:
        new_numeration_photo = f"{numeration_photo[0]},{numeration_photo[1]},"
    elif len(numeration_photo) == 3:
        new_numeration_photo = f"{numeration_photo[0]},"
    async with async_session_maker() as session:
        q = update(adding).where(adding.c.id == int(num)).values(subject_photo=new_photos,
                                                                 numeration_files=new_numeration_photo)
        await session.execute(q)
        await session.commit()
    await call.answer("Rasm o'chirildi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=edits)


@dp.callback_query_handler(text="place_edit_answer")
async def place_edit_answer(call: CallbackQuery, state: FSMContext):
    text = call.message.text
    message_id = call.message.message_id
    await state.update_data({"text": text})
    await state.update_data({"message_id": message_id})
    await call.message.answer("O'zgartirilgan javobni yozing:", reply_markup=admin_add)
    await Ask.state13.set()


@dp.message_handler(state=Ask.state13)
async def place_edit_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    text = data["text"]
    message_id = data["message_id"]
    num = (text.split("\n"))[0].split(": ")[1]
    asks = (text.split("\n"))[4]
    if asks == "ask_probeg":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(probeg=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_status":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(status=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_color":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(color=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_fuel":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(fuel=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_paid":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(payment=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_address":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(address=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_conditioning":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(condition=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_facilities":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(amenities=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_phone":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(phone_number=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_year":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(years=message.text)
            await session.execute(query)
            await session.commit()
    elif asks == "ask_text":
        async with async_session_maker() as session:
            query = update(adding).where(adding.c.id == int(num)).values(text=message.text)
            await session.execute(query)
            await session.commit()
    if await is_super_admin(message.from_user.id):
        await message.answer("Javob qabul qilindi!", reply_markup=super_admins_keyboard)
    elif await is_admin(message.from_user.id):
        await message.answer("Javob qabul qilindi!", reply_markup=admins_keyboard)
    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message_id, reply_markup=None)
    await state.finish()


@dp.callback_query_handler(text="delete_add")
async def delete_add(call: CallbackQuery):
    message_id = call.message.message_id
    await call.answer("Tasdiqlash")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id,
                                        reply_markup=delete_confirm)


@dp.callback_query_handler(text="delete_yes")
async def delete_yes(call: CallbackQuery):
    message_id = call.message.message_id
    text = call.message.caption
    num = (text.split("\n"))[0].split(": ")[1]
    async with async_session_maker() as session:
        query = update(adding).where(adding.c.id == int(num)).values(rejected=True, confirm=True)
        await session.execute(query)
        await session.commit()
    await call.answer("E'lon o'chirildi")
    await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)


@dp.callback_query_handler(text="delete_no")
async def delete_no(call: CallbackQuery):
    message_id = call.message.message_id
    await call.answer("Bekor qilindi")
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message_id, reply_markup=None)