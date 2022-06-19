import asyncio

import aioschedule
from aiogram import types
from aiogram.dispatcher import FSMContext

from db_func import change_qiwi_token
from handlers.users.start import bot_start
from states.qiwi_change_token_state import ChangeQIWIToken
from loader import dp, bot
from data.config import ADMINS


@dp.message_handler(commands='change_qiwi_token')
async def profile(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Напишите новый токен или "отмена" для возврата в главное меню')
        await ChangeQIWIToken.token.set()


async def pls_change_token():
    for i in ADMINS:
        await bot.send_message(i, 'Завтра токен QIWI станет недействительным. Обновите его')


async def scheduler():
    await aioschedule.run_pending()
    await asyncio.sleep(179 * 24 * 60 * 60)
    await pls_change_token()


@dp.message_handler(state=ChangeQIWIToken.token)
async def take_ref(message: types.Message, state: FSMContext):
    token = message.text
    if token.lower() != 'отмена':
        change_qiwi_token(token)
        await state.reset_state(with_data=False)
        await message.answer('Токен изменён')
        asyncio.create_task(scheduler())
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)
