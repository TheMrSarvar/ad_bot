from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

ad_for_uzbek = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("E'lon berish")
        ],
        [
            KeyboardButton('Adminga murojat')
        ],
    ],
    resize_keyboard=True,
)

ad_for_russian = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Рекламировать")
        ],
        [
            KeyboardButton("Свяжитесь с администратором")
        ],
        [
            KeyboardButton("Изменить язык")
        ]
    ],
    resize_keyboard=True,
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ha✅")
        ],
        [
            KeyboardButton("Yoq❌")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

admins_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("So'rovlar")
        ],
    ],
    resize_keyboard=True
)

super_admins_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("So'rovlar"),
        ],
        [
            KeyboardButton("Admin qoshish"),
            KeyboardButton("Admindan chiqarish")
        ],
        [
            KeyboardButton("Hisobot"),
            KeyboardButton("To'lov bo'limi"),
        ],
        [
            KeyboardButton("Botga reklama joylash")
        ],
    ],
    resize_keyboard=True,
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ortga🔙")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

back_space = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ortga 🔙")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

back_to_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Orqaga🔙")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

to_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Rasmlarni tasdiqlash ✅"),
        ],
        [
            KeyboardButton("Ortga🔙")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

back_to_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Назад🔙")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

edit_back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("orqaga🔙")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

admin_add = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Orqaga 🔙")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)

to_admin_russ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Подтверждение изображений ✅"),
        ],
        [
            KeyboardButton("Назад🔙")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)


money = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Sana boyicha hisobot"),
        ],
        [
            KeyboardButton("Orqaga 🔙")
        ]
    ],
    one_time_keyboard=True,
    resize_keyboard=True
)
