from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

new_user = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Задания", callback_data="tasks_bt_inl_kb"),
        InlineKeyboardButton(text="Профиль", callback_data="profile_bt_inl_kb")
    ],
    [
        InlineKeyboardButton(text="Ввести код", callback_data="referral_inl_kb")
    ]
])
old_user = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Профиль", callback_data="profile_bt_inl_kb")
    ],
    [
        InlineKeyboardButton(text="Задания", callback_data="tasks_bt_inl_kb")
    ],
])
