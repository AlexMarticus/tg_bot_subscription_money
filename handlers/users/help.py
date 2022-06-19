from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('Возникли проблемы или недоработки. Ну или хочешь купить у нас рекламу. Напиши нам: '
                         'changed_for_github')
