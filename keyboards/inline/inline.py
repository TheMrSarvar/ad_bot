from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-Kanal📣", url="https://t.me/thetest_sarvar"),
        ],
        [
            InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check"),
        ]
    ]
)

language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇷🇺 Русский', callback_data='russian')
        ],
        [
            InlineKeyboardButton(text='🇺🇿 Uzbekcha', callback_data='uzbek')
        ]
    ]
)

change_language = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🇷🇺 Русский', callback_data='russian1')
        ],
        [
            InlineKeyboardButton(text='🇺🇿 Uzbekcha', callback_data='uzbek1')
        ]
    ]
)

location = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Joylash", callback_data="placement"),
            InlineKeyboardButton("O'zgartirish", callback_data="edit"),
        ],
        [
            InlineKeyboardButton("Foydalanuvchidan so'rash", callback_data="to_ask"),
        ],
        [
            InlineKeyboardButton("To'lovni tasdiqlash", callback_data="check_paid"),
        ],
        [
            InlineKeyboardButton("E'loni o'chirib yuborish 🗑", callback_data="delete_add")
        ]
    ]
)

card_ = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Kartani o'zgartirish", callback_data="card_change"),
        ],
        [
            InlineKeyboardButton("Reklama narxini o'zgartirish", callback_data="amount_change"),
        ]
    ]
)

message_ = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Javob yozish", callback_data="write_message"),
        ]
    ]
)

edits = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("👣Probeg", callback_data="edit_probeg"),
            InlineKeyboardButton("🛠Holati", callback_data="edit_status"),
        ],
        [
            InlineKeyboardButton("🎨Rangi", callback_data="edit_color"),
            InlineKeyboardButton("⛽️Yoqilg'isi", callback_data="edit_fuel"),
        ],
        [
            InlineKeyboardButton("💰Narxi:", callback_data="edit_paid"),
            InlineKeyboardButton("🚩Manzil", callback_data="edit_address"),
        ],
        [
            InlineKeyboardButton("❄️Konditsioner", callback_data="edit_conditioning"),
            InlineKeyboardButton("🖼Rasmlar", callback_data="edit_photo"),
        ],
        [
            InlineKeyboardButton("✅Qo’shimcha jihozlar", callback_data="edit_facilities"),
        ],
        [
            InlineKeyboardButton("☎️Telefon raqami", callback_data="edit_phone"),
        ],
        [
            InlineKeyboardButton("📅Ishlab chiqarilgan yili", callback_data="edit_year"),
        ],
        [
            InlineKeyboardButton("Mashina nomi", callback_data="edit_text"),
        ],
        [
            InlineKeyboardButton("🔙Orqaga", callback_data="back_"),
        ],
    ]
)

to_ask = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("👣Probeg", callback_data="ask_probeg"),
            InlineKeyboardButton("🛠Holati", callback_data="ask_status"),
        ],
        [
            InlineKeyboardButton("🎨Rangi", callback_data="ask_color"),
            InlineKeyboardButton("⛽️Yoqilg'isi", callback_data="ask_fuel"),
        ],
        [
            InlineKeyboardButton("💰Narxi:", callback_data="ask_paid"),
            InlineKeyboardButton("🚩Manzil", callback_data="ask_address"),
        ],
        [
            InlineKeyboardButton("❄️Konditsioner", callback_data="ask_conditioning"),
        ],
        [
            InlineKeyboardButton("✅Qo’shimcha jihozlar", callback_data="ask_facilities"),
        ],
        [
            InlineKeyboardButton("☎️Telefon raqami", callback_data="ask_phone"),
        ],
        [
            InlineKeyboardButton("📅Ishlab chiqarilgan yili", callback_data="ask_year"),
        ],
        [
            InlineKeyboardButton("Mashina nomi", callback_data="ask_text"),
        ],
        [
            InlineKeyboardButton("Reklama uchun to'lov", callback_data="paid_user")
        ],
        [
            InlineKeyboardButton("🔙Orqaga", callback_data="back_"),
        ],
    ]
)

to_ask_answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Javob yozish", callback_data="to_ask_answer"),
        ]
    ]
)

to_ask_answer_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Написать ответ", callback_data="to_ask_answer"),
        ]
    ]
)

place_answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Javobni joylash", callback_data="place_answer"),
        ],
        [
            InlineKeyboardButton("Javobni o'zgartirib joylash", callback_data="place_edit_answer"),
        ],
    ]
)

edit_photo = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("1-rasm", callback_data="first_photo"),
        ],
        [
            InlineKeyboardButton("2-rasm", callback_data="second_photo"),
        ],
        [
            InlineKeyboardButton("3-rasm", callback_data="third_photo"),
        ],
        [
            InlineKeyboardButton("4-rasm", callback_data="fourth_photo"),
        ],
        [
            InlineKeyboardButton("5-rasm", callback_data="fifth_photo"),
        ],
        [
            InlineKeyboardButton("6-rasm", callback_data="sixth_photo"),
        ],
        [
            InlineKeyboardButton("🔙Orqaga", callback_data="back_"),
        ]
    ]
)

delete_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Ha✅", callback_data="delete_yes"),
        ],
        [
            InlineKeyboardButton("Yoq❌", callback_data="delete_no"),
        ]
    ]
)
