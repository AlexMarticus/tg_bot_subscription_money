from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

set_qiwi_bt = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Указать", callback_data="set_qiwi_inl_bt")
    ],
])
