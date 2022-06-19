from aiogram import types

from data.config import ADMINS
from db_func import when_qiwi_token_was_added
from loader import dp


@dp.message_handler(commands='when_QIWI_token_was_added')
async def QIWI_token_was_added(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        date = when_qiwi_token_was_added()
        text = f'токен был добавлен {date}'
        await message.answer(text)
