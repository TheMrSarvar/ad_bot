from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Ha✅", callback_data='yes_'),
        ],
        [
            InlineKeyboardButton("Orqaga🔙", callback_data="back_")
        ]
    ]
)

paid = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Ha✅", callback_data="paid_yes"),
            InlineKeyboardButton("Yoq❌", callback_data="paid_no")
        ],
        [
            InlineKeyboardButton("Orqaga🔙", callback_data="back_")
        ]
    ]
)

paid_messa = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Javob yozish", callback_data="paid_message"),
        ]
    ]
)
