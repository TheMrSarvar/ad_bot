from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from database import async_session_maker
from keyboards.default.ad import back_space, ad_for_uzbek
from loader import dp, bot
from models.models import message_adding
from states.for_message import MessageToAdmin


@dp.callback_query_handler(text="write_message")
async def process_message(message: CallbackQuery, state: FSMContext):
    await state.update_data({"message_id": message.message.message_id})
    await message.message.answer("Javobingiz:", reply_markup=back_space)
    await MessageToAdmin.state1.set()


@dp.message_handler(state=MessageToAdmin.state1)
async def process_message(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data["message_id"]
    if message.text == "Ortga 🔙":
        await message.answer("Bosh sahifa:", reply_markup=ad_for_uzbek)
    async with async_session_maker() as session:
        query = select(message_adding).where(message_adding.c.message_id == int(message_id))
        query = await session.execute(query)
        query = query.fetchone()
    await bot.send_message(chat_id=query[1],
                           text=f"Savol: {query[2]}\nJavob: {message.text}\nReklama raqami: <code>{query[-1]}</code>")
    await message.answer("Javobingiz qabul qilindi!")
    await state.finish()
