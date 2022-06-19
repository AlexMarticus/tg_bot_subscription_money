from aiogram import types
from data.config import ADMINS
from db_func import give_all_tasks
from loader import dp


@dp.message_handler(commands='show_tasks')
async def change_tasks(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        all_tasks = give_all_tasks()
        print(all_tasks)
        text = f"""
Первое задание\n
{all_tasks[0][0]}\n
{all_tasks[0][1]}\n
{all_tasks[0][2]}\n
{all_tasks[0][3]}\n
\n
Второе задание\n
{all_tasks[1][0]}\n
{all_tasks[1][1]}\n
{all_tasks[1][2]}\n
{all_tasks[1][3]}
"""
        await message.answer(text)
