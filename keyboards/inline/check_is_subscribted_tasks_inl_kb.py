from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

task_1_check = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Проверить", callback_data="check_1task_inl_bt"),
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start')
    ],
])

task_2_check = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Проверить", callback_data="check_2task_inl_bt"),
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start')
    ],
])

task_3_check = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Проверить", callback_data="check_3task_inl_bt"),
    ],
    [
        InlineKeyboardButton(text='Назад в меню', callback_data='back_to_start'),
        InlineKeyboardButton(text="Профиль", callback_data='profile_bt_inl_kb')
    ],
])
