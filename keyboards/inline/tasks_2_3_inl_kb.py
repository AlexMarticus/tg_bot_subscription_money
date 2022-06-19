from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

task_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Перейти ко 2му заданию", callback_data="2task_inl_bt"),
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start'),
    ],
])

task_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Перейти к 3му заданию", callback_data="3task_inl_bt"),
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start'),
    ],
])

after_3_task = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Профиль", callback_data="profile_bt_inl_kb"),
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start'),
    ],
])
