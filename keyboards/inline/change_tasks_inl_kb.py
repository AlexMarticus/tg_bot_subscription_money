from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

change_tasks_ = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Первое задание", callback_data="change_1_task"),
        InlineKeyboardMarkup(text='Второе задание', callback_data='change_2_task')
    ],
])
