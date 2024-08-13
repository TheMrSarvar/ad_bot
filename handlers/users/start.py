from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.builtin import CommandStart
from sqlalchemy import select, insert

from database import async_session_maker
from functions import following, is_admin, is_super_admin, delete_photos
from loader import dp, bot

from keyboards.inline.inline import channels, language
from keyboards.default.ad import ad_for_uzbek, ad_for_russian, admins_keyboard, super_admins_keyboard

from models.models import users


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Message, state: FSMContext):
    if await is_super_admin(int(message.from_user.id)):
        await message.answer('Quyidagilardan birini tanlang', reply_markup=super_admins_keyboard)
    elif await is_admin(int(message.from_user.id)):
        await message.answer('Quyidagilardan birini tanlang', reply_markup=admins_keyboard)
    else:
        async with async_session_maker() as session:
            query = select(users).where(users.c.chat_id == int(message.from_user.id))
            query = await session.execute(query)
            query = query.fetchone()
        if query is None:
            await message.answer(f'👋 Assalomu alaykum {message.from_user.first_name} botimizga xush kelibsiz.')
            await message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)
        elif await following(message.from_user.id):
            await message.answer("Botga e'lon bermoqchi bolsangi pastdagi e'lon berish tugmachasini bosing",
                                 reply_markup=ad_for_uzbek)
            current_state = await state.get_state()
            if current_state:
                data = await state.get_data()
                await delete_photos(data)
            else:
                pass
            await state.finish()
        else:
            await message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)
        await state.finish()


@dp.callback_query_handler(text='check')
async def bot_check(call: CallbackQuery):
    async with async_session_maker() as session:
        query_ = select(users).where(users.c.chat_id == int(call.from_user.id))
        query_ = await session.execute(query_)
        query_ = query_.fetchone()
    if await following(call.from_user.id) and query_ is None:
        await call.message.delete()
        async with async_session_maker() as session:
            query = insert(users).values(chat_id=int(call.from_user.id))
            await session.execute(query)
            await session.commit()
        await call.message.answer("Botga e'lon bermoqchi bolsangi pastdagi e'lon berish tugmachasini bosing",
                                  reply_markup=ad_for_uzbek)
    elif await following(call.from_user.id) is False and query_ is None:
        await call.answer('Siz kanallarga obuna bolmadingiz')
    elif await following(call.from_user.id) is False and query_:
        await call.answer('Siz kanallarga obuna bolmadingiz')
    else:
        await call.message.delete()
        await call.message.answer("Botga e'lon bermoqchi bolsangi pastdagi e'lon berish tugmachasini bosing",
                                  reply_markup=ad_for_uzbek)


@dp.callback_query_handler(text='uzbek')
async def uzbek(call: CallbackQuery):
    if await following(call.from_user.id):
        await call.message.delete()
        await call.answer('Til ozgardi')
        async with async_session_maker() as session:
            query = insert(users).values(chat_id=int(call.from_user.id), language='uzbek')
            await session.execute(query)
            await session.commit()
            await session.close()
        await call.message.answer("Botga e'lon bermoqchi bolsangi pastdagi e'lon berish tugmachasini bosing",
                                  reply_markup=ad_for_uzbek)
    else:
        await call.message.answer("Botdan foydalanish uchun quyidagi kanalarga a'zo bo'ling", reply_markup=channels)


@dp.callback_query_handler(text='russian')
async def uzbek(call: CallbackQuery):
    if await following(call.from_user.id):
        await call.message.delete()
        await call.answer('Язык изменился')
        async with async_session_maker() as session:
            query = insert(users).values(chat_id=int(call.from_user.id), language='russian')
            await session.execute(query)
            await session.commit()
            await session.close()
        await call.message.answer('Если вы хотите разместить рекламу боту, нажмите кнопку «Рекламировать» ниже.',
                                  reply_markup=ad_for_russian)
    else:
        await call.message.answer("Для использования бота подпишитесь на следующие каналам", reply_markup=channels)


@dp.message_handler(commands='admin')
async def admin(message: Message):
    await message.answer("Bosh sahifa", reply_markup=admins_keyboard)


@dp.message_handler(commands='superadmin')
async def superadmin(message: Message):
    await message.answer("Bosh sahifa", reply_markup=super_admins_keyboard)
