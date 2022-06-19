from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

outp_qiwi_bt = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вывод средств на QIWI (минимум 1 рубль)", callback_data="output_qiwi_inl_bt")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="back_to_start")
    ]
])
