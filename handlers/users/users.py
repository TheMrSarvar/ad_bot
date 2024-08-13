import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from sqlalchemy import insert, select, update
from functions import following, numeration, delete_photos
from database import async_session_maker
from keyboards.inline.inline import channels, change_language, location
from loader import dp, bot
from models.models import adding, users, card, admins
from states.for_adding import Adding
from keyboards.default.ad import ad_for_uzbek, back, ad_for_russian, to_admin


@dp.message_handler(text="E'lon berish", state="*")
async def add_user(message: Message):
    if await following(message.from_user.id):
        await message.answer("Mashina nomini yozing:", reply_markup=back)
        await Adding.state1.set()
    else:
        await message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)


@dp.message_handler(state=Adding.state1)
async def add_user_(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("Bo'sh sahifa", reply_markup=ad_for_uzbek)
        await state.finish()
    else:
        await state.update_data({"name": message.text})
        await state.update_data({"num": 1})
        await message.answer(
            f"Mashina rasmini yuboring(Eng ko'pi bilan 6 ta rasm yuborishingiz mumkin va hamma rasmlar yuborilgandan so'ng ✅Tasdiqlash tugmasini bosing):",
            reply_markup=to_admin)
        await state.update_data({"pic1": None})
        await state.update_data({"pic2": None})
        await state.update_data({"pic3": None})
        await state.update_data({"pic4": None})
        await state.update_data({"pic5": None})
        await state.update_data({"pic6": None})
        await Adding.state2.set()


@dp.message_handler(content_types='video', state=Adding.state2)
async def add_user_(message: Message):
    await message.answer("Iltimos rasm yuboring", reply_markup=to_admin)


@dp.message_handler(content_types='photo', state=Adding.state2)
async def send_six_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    num = data['num']
    if num == 1:
        await state.update_data({"num": 2})
        photos = message.photo
        highest_res_photo = photos[-1]
        file_id = highest_res_photo.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)
        local_file_path = f"{file_id}.jpg"
        with open(local_file_path, 'wb') as f:
            f.write(downloaded_file.getvalue())
        await state.update_data({"pic1": file_id})
    elif num == 2:
        if message.photo:
            await state.update_data({"num": 3})
            photos = message.photo
            highest_res_photo = photos[-1]
            file_id = highest_res_photo.file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            local_file_path = f"{file_id}.jpg"
            with open(local_file_path, 'wb') as f:
                f.write(downloaded_file.getvalue())
            await state.update_data({"pic2": file_id})
        else:
            await state.update_data({"pic2": None})
    elif num == 3:
        if message.photo:
            await state.update_data({"num": 4})
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            local_file_path = f"{file_id}.jpg"
            with open(local_file_path, 'wb') as f:
                f.write(downloaded_file.getvalue())
            await state.update_data({"pic3": file_id})
        else:
            await state.update_data({"pic3": None})
    elif num == 4:
        if message.photo:
            await state.update_data({"num": 5})
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            local_file_path = f"{file_id}.jpg"
            with open(local_file_path, 'wb') as f:
                f.write(downloaded_file.getvalue())
            await state.update_data({"pic4": file_id})
        else:
            await state.update_data({"pic4": None})
    elif num == 5:
        if message.photo:
            await state.update_data({"num": 6})
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            local_file_path = f"{file_id}.jpg"
            with open(local_file_path, 'wb') as f:
                f.write(downloaded_file.getvalue())
            await state.update_data({"pic5": file_id})
        else:
            await state.update_data({"pic5": None})
    elif num == 6:
        if message.photo:
            await state.update_data({"num": 7})
            file_id = message.photo[-1].file_id
            file_info = await bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = await bot.download_file(file_path)
            local_file_path = f"{file_id}.jpg"
            with open(local_file_path, 'wb') as f:
                f.write(downloaded_file.getvalue())
            await state.update_data({"pic6": file_id})
        else:
            await state.update_data({"pic6": None})


@dp.message_handler(content_types='text', state=Adding.state2)
async def add_user_(message: Message, state: FSMContext):
    data = await state.get_data()
    num = data['num']
    if message.text == "Ortga🔙":
        await message.answer("Mashina nomini yozing:", reply_markup=back)
        current_state = await state.get_state()
        if current_state:
            data = await state.get_data()
            await delete_photos(data)
        else:
            pass
        await Adding.state1.set()
    elif message.text == "Rasmlarni tasdiqlash ✅":
        if data['pic1'] and num < 7:
            await message.answer("📆 Ishlab chiqarilgan yili", reply_markup=back)
            await Adding.state3.set()
        elif data["pic1"] and num == 1:
            await message.answer("Siz birorta ham rasm yubormadingiz", reply_markup=to_admin)
        else:
            await message.answer("Rasmlar oltitadan oshmasligi kerak iltimos qayta yuboring:", reply_markup=to_admin)
            await Adding.state2.set()
    else:
        await message.answer("Iltimos mashinani rasmini yuboring:")


@dp.message_handler(state=Adding.state3)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await state.update_data({"num": 1})
        await message.answer(
            f"Mashina rasmini yuboring(Eng ko'pi bilan 6 ta rasm yuborishingiz mumkin va hamma rasmlar yuborilgandan so'ng ✅Tasdiqlash tugmasini bosing):",
            reply_markup=to_admin)
        await Adding.state2.set()
    else:
        await state.update_data({"years": message.text})
        await message.answer("👣 Probeg", reply_markup=back)
        await Adding.state4.set()


@dp.message_handler(state=Adding.state4)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("📆 Ishlab chiqarilgan yili", reply_markup=back)
        await Adding.state3.set()
    else:
        await state.update_data({"probeg": message.text})
        await message.answer("🛠 Mashina holati haqida yozing:")
        await Adding.state5.set()


@dp.message_handler(state=Adding.state5)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("👣 Probeg", reply_markup=back)
        await Adding.state4.set()
    else:
        await state.update_data({"status": message.text})
        await message.answer("🎨 Mashina rangi")
        await Adding.state6.set()


@dp.message_handler(state=Adding.state6)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("🛠 Mashina holati haqida yozing:", reply_markup=back)
        await Adding.state5.set()
    else:
        await state.update_data({"color": message.text})
        await message.answer("❄️ Konditsioner haqida:")
        await Adding.state7.set()


@dp.message_handler(state=Adding.state7)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("🎨 Mashina rangi:", reply_markup=back)
        await Adding.state6.set()
    else:
        await state.update_data({"condition": message.text})
        await message.answer("✅ Qo’shimcha jihozlar:")
        await Adding.state8.set()


@dp.message_handler(state=Adding.state8)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("❄️ Konditsioner haqida:", reply_markup=back)
        await Adding.state7.set()
    else:
        await state.update_data({"amenities": message.text})
        await message.answer("⛽️ Yoqilg’i turi:")
        await Adding.state9.set()


@dp.message_handler(state=Adding.state9)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("✅ Qo’shimcha jihozlar:", reply_markup=back)
        await Adding.state8.set()
    else:
        await state.update_data({"fuel": message.text})
        await message.answer("💰 Narx")
        await Adding.state10.set()


@dp.message_handler(state=Adding.state10)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("⛽️ Yoqilg’i turi:", reply_markup=back)
        await Adding.state9.set()
    else:
        await state.update_data({"payment": message.text})
        await message.answer("☎️ Telefon nomer:")
        await Adding.state11.set()


@dp.message_handler(state=Adding.state11)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("💰 Narx", reply_markup=back)
        await Adding.state10.set()
    else:
        await state.update_data({"phone_number": message.text})
        await message.answer("🚩 Manzil:")
        await Adding.state12.set()


@dp.message_handler(state=Adding.state12)
async def years(message: Message, state: FSMContext):
    if message.text == "Ortga🔙":
        await message.answer("☎️ Telefon nomer:", reply_markup=back)
        await Adding.state11.set()
    else:
        await state.update_data({"address": message.text})
        async with async_session_maker() as session:
            query = select(card)
            query = await session.execute(query)
            query = query.fetchone()
        card_ = query[1]
        ammount = query[-1]
        await message.answer(
            f"Reklama narxi: {ammount} so'm\nKarta raqami: {card_}\n\n‼️To'lovni o'tkazib chekni screenshotini yuboring.")
        await Adding.state13.set()


@dp.message_handler(content_types=["text"], state=Adding.state13)
async def fjnd(message: Message):
    if message.text == "Ortga🔙":
        await message.answer("🚩 Manzil:", reply_markup=back)
        await Adding.state12.set()
    else:
        await message.answer("Iltimos to'lovni screenshotini yuboring")


@dp.message_handler(content_types=["photo"], state=Adding.state13)
async def add_user_(message: Message, state: FSMContext):
    await message.answer("E'lon qabul qilindi", reply_markup=ad_for_uzbek)
    global media_object
    data = await state.get_data()
    pic1 = data["pic1"]
    pic2 = data["pic2"]
    pic3 = data["pic3"]
    pic4 = data["pic4"]
    pic5 = data["pic5"]
    pic6 = data["pic6"]
    year = data['years']
    probeg = data['probeg']
    status = data['status']
    color = data['color']
    condition = data['condition']
    amenities = data['amenities']
    fuel = data['fuel']
    payment = data['payment']
    phone_number = data['phone_number']
    name = data['name']
    address = data["address"]
    photos = []
    if pic1 and pic2 is None:
        photos = [
            f"{pic1}.jpg",
        ]
    elif pic1 and pic2 and pic3 is None:
        photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 is None:
        photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 is None:
        photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 and pic6 is None:
        photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
            f"{pic5}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 and pic6:
        photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
            f"{pic5}.jpg",
            f"{pic6}.jpg",
        ]
    await numeration(photos)
    new_photos = []
    if pic1 and pic2 is None:
        new_photos = [
            f"{pic1}.jpg",
        ]
    elif pic1 and pic2 and pic3 is None:
        new_photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 is None:
        new_photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 is None:
        new_photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 and pic6 is None:
        new_photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
            f"{pic5}.jpg",
        ]
    elif pic1 and pic2 and pic3 and pic4 and pic5 and pic6:
        new_photos = [
            f"{pic1}.jpg",
            f"{pic2}.jpg",
            f"{pic3}.jpg",
            f"{pic4}.jpg",
            f"{pic5}.jpg",
            f"{pic6}.jpg",
        ]
    async with async_session_maker() as session:
        query_ = select(admins)
        query_ = await session.execute(query_)
        query_ = query_.fetchall()
    admins_ = len(query_)
    async with async_session_maker() as session:
        query = select(adding)
        query = await session.execute(query)
        query = query.fetchall()
    num = query[-1][0]
    for q in query:
        if q[0] > num:
            num = q[0]
    payment_photo_id = message.photo[-1].file_id
    caption = f"Mashina nomi: {name}\n\n📅Ishlab chiqarilgan yili: {year}\n👣Probeg: {probeg}\n🛠Holati: {status}\n🎨Rangi: {color}\n❄️Konditsioner: {condition}\n✅Qo’shimcha jihozlar: {amenities}\n⛽️Yoqilg'isi: {fuel}\n💰Narxi: {payment}\n☎️Telefon raqami: {phone_number}\n🚩Manzil: {address}\n"
    async with async_session_maker() as session:
        query = select(card)
        query = await session.execute(query)
        query = query.fetchone()
    ammount = query[-1]
    file_ids = ""
    media_group = []
    for photo in new_photos:
        media_group.append(InputMediaPhoto(open(photo, 'rb')))
    if len(media_group) > 1:
        media_group[0].caption = caption
        media_id = await bot.send_media_group(chat_id=1307098001, media=media_group)
        file_ids = [msg.photo[-1].file_id for msg in media_id]
        await bot.send_photo(chat_id=1307098001, photo=payment_photo_id,
                             caption=f"E'lon raqami: {num + 1}\nTo'lanamagan❌",
                             reply_markup=location)
    elif len(media_group) == 1:
        with open(new_photos[0], 'rb') as phot:
            file_ids = await bot.send_photo(chat_id=1307098001, photo=phot, caption=caption)
            file_ids = [file_ids["photo"][0]['file_id']]
        await bot.send_photo(chat_id=1307098001, photo=payment_photo_id,
                             caption=f"E'lon raqami: {num + 1}\nTo'lanamagan❌",
                             reply_markup=location)
    subject_photo = f"{pic1},{pic2},{pic3},{pic4},{pic5},{pic6}"
    edits = ""
    for i in file_ids:
        edits += f"{i},"
    async with async_session_maker() as session:
        query = insert(adding).values(chat_id=int(message.from_user.id), text=name, photo_id=payment_photo_id,
                                      years=year,
                                      probeg=probeg, status=status, color=color, condition=condition,
                                      amenities=amenities,
                                      fuel=fuel, payment=payment, phone_number=phone_number, address=address,
                                      subject_photo=subject_photo, money=str(ammount), numeration_files=edits,
                                      language="uzbek")
        await session.execute(query)
        await session.commit()
    for i in photos:
        file_path = f"{i}"
        if os.path.exists(file_path):
            os.remove(file_path)
    await state.finish()


@dp.message_handler(text="Adminga murojat", state="*")
async def message_to_admin(message: Message):
    if await following(message.from_user.id):
        await message.answer("Murojatingizni @cctuzadmin adminga qoldiring:")
    elif await following(message.from_user.id) is False:
        await message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)


@dp.message_handler(text="Свяжитесь с администратором")
async def message_to_admin(message: Message):
    if await following(message.from_user.id):
        await message.answer("Оставьте заявку администратору @TheMrSarvar:")
    elif await following(message.from_user.id):
        await message.answer("Для использования бота подпишитесь на следующие каналам", reply_markup=channels)


@dp.message_handler(text='Изменить язык')
async def language(message: Message):
    async with async_session_maker() as session:
        query = select(users).where(users.c.chat_id == int(message.from_user.id))
        query = await session.execute(query)
        query = query.fetchone()
    if query[3] == 'uzbek' and (await following(message.from_user.id)):
        await message.answer('Tilni ozgaritirish', reply_markup=change_language)
    elif query[3] == 'russian' and (await following(message.from_user.id)):
        await message.answer('Изменить язык', reply_markup=change_language)
    else:
        await message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)


@dp.callback_query_handler(text='uzbek1')
async def uzbek1(call: CallbackQuery):
    async with async_session_maker() as session:
        query = update(users).where(users.c.chat_id == int(call.from_user.id)).values(language='uzbek')
        await session.execute(query)
        await session.commit()
    await call.message.delete()
    await call.answer('Til ozgardi')
    await call.message.answer("Botga e'lon bermoqchi bolsangi pastdagi e'lon berish tugmachasini bosing",
                              reply_markup=ad_for_uzbek)


@dp.callback_query_handler(text='russian1')
async def uzbek1(call: CallbackQuery):
    async with async_session_maker() as session:
        query = update(users).where(users.c.chat_id == int(call.from_user.id)).values(language='russian')
        await session.execute(query)
        await session.commit()
    await call.message.delete()
    await call.answer('Язык изменился')
    await call.message.answer('Если вы хотите разместить рекламу боту, нажмите кнопку «Рекламировать» ниже.',
                              reply_markup=ad_for_russian)
