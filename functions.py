from sqlalchemy import select
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import async_session_maker
from loader import bot
from models.models import admins, adding
import os


async def following(user_id):
    status = await bot.get_chat_member(-1002053603769, int(user_id))
    if status.status == 'creator' or status.status == 'member':
        return True
    else:
        return False


async def is_admin(user_id):
    async with async_session_maker() as session:
        query = select(admins).where(admins.c.chat_id == user_id)
        query = await session.execute(query)
        query = query.fetchone()
    if query:
        return True
    else:
        return False


async def is_super_admin(user_id):
    async with async_session_maker() as session:
        query = select(admins).where(admins.c.chat_id == int(user_id))
        query = await session.execute(query)
        query = query.fetchone()
    if query:
        if query[3]:
            return True
        else:
            return False
    else:
        return False


async def create_inline_keyboard(images):
    inline_keyboard = []
    for i in range(0, len(images)):
        if images[i] != "None":
            inline_keyboard.append([InlineKeyboardButton(f"{i + 1}-rasm", callback_data=f"photo_{i + 1}")])
    inline_keyboard.append([InlineKeyboardButton("🔙Back", callback_data="back_")])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def adding_language(num):
    async with async_session_maker() as session:
        query = select(adding).where(adding.c.id == num)
        query = await session.execute(query)
        query = query.fetchone()
    return query[21]


async def add_number_to_image(image_path, output_path, number, position="top-left", font_size=50,
                              color=(255, 255, 255)):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        try:
            # Change the font path to a common Windows font path
            font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        text = str(number)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if position == "top-right":
            x = img.width - text_width - 10
            y = 10
        elif position == "top-left":
            x = 10
            y = 10
        elif position == "bottom-right":
            x = img.width - text_width - 10
            y = img.height - text_height - 10
        elif position == "bottom-left":
            x = 10
            y = img.height - text_height - 10
        else:
            raise ValueError("Invalid position. Choose from 'top-right', 'top-left', 'bottom-right', 'bottom-left'.")
        draw.text((x, y), text, font=font, fill=color)
        img.save(output_path)


async def numeration(photos):
    n = 1
    for i in photos:
        await add_number_to_image(f"{i}", f"{i}", n)
        n += 1


async def delete_photos(data):
    pic1 = data["pic1"]
    pic2 = data["pic2"]
    pic3 = data["pic3"]
    pic4 = data["pic4"]
    pic5 = data["pic5"]
    pic6 = data["pic6"]
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
    for i in photos:
        file_path = f"{i}"
        if os.path.exists(file_path):
            os.remove(file_path)
