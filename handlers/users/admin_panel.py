from aiogram import types

from data.config import ADMINS
from loader import dp


@dp.message_handler(commands='admin')
async def admin(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        text = '/change_tasks - изменить задания\n' \
               '/change_qiwi_token - изменить токен QIWI\n' \
               '/show_tasks - просмотр заданий\n' \
               '/when_QIWI_token_was_added - посмотреть когда был добавлен токен'
        await message.answer(text)
