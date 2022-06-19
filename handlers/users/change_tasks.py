from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from db_func import change_tasks_1, change_tasks_2
from handlers.users.start import bot_start
from states.change_tasks_state import Task1, Task2
from loader import dp, bot


@dp.message_handler(commands='change_tasks')
async def change_tasks(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        text = 'Введите id канала в формате @название или "отмена" для возврата в главное меню (Первое задание)'
        await message.answer(text)
        await Task1.first_task.set()


@dp.message_handler(state=Task1.first_task)
async def change_task_1_1(message: types.Message, state: FSMContext):
    id_1 = message.text
    if id_1.lower() != 'отмена':
        await message.answer('Заполнено 1/4 (Первое задание)')
        answers_all = [id_1]
        async with state.proxy() as data:
            data['ref10'] = answers_all
        await Task1.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task1.second_task)
async def change_task_1_2(message: types.Message, state: FSMContext):
    id_2 = message.text
    if id_2.lower() != 'отмена':
        await message.answer('Заполнено 2/4 (Первое задание)')
        async with state.proxy() as data:
            answers_all = data['ref10']
        answers_all.append(id_2)
        async with state.proxy() as data:
            data['ref10'] = answers_all
        await Task1.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task1.third_task)
async def change_task_1_3(message: types.Message, state: FSMContext):
    id_3 = message.text
    if id_3.lower() != 'отмена':
        await message.answer('Заполнено 3/4 (Первое задание)')
        async with state.proxy() as data:
            answers_all = data['ref10']
        answers_all.append(id_3)
        async with state.proxy() as data:
            data['ref10'] = answers_all
        await Task1.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task1.fourth_task)
async def change_task_1_3(message: types.Message, state: FSMContext):
    id_4 = message.text
    if id_4.lower() != 'отмена':
        await message.answer('Заполнено 4/4. (Первое задание). Продолжайте ввод для 2 задания')
        async with state.proxy() as data:
            answers_all = data['ref10']
        answers_all.append(id_4)
        async with state.proxy() as data:
            data['ref10'] = answers_all
        await Task2.first_task.set()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task2.first_task)
async def change_task_1_1(message: types.Message, state: FSMContext):
    id_1 = message.text
    if id_1.lower() != 'отмена':
        await message.answer('Заполнено 1/4 (Второе задание)')
        answers_all_2 = [id_1]
        async with state.proxy() as data:
            data['ref1'] = answers_all_2
        await Task2.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task2.second_task)
async def change_task_1_2(message: types.Message, state: FSMContext):
    id_2 = message.text
    if id_2.lower() != 'отмена':
        await message.answer('Заполнено 2/4 (Второе задание)')
        async with state.proxy() as data:
            answers_all_2 = data['ref1']
        answers_all_2.append(id_2)
        async with state.proxy() as data:
            data['ref1'] = answers_all_2
        await Task2.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task2.third_task)
async def change_task_1_3(message: types.Message, state: FSMContext):
    id_3 = message.text
    if id_3.lower() != 'отмена':
        await message.answer('Заполнено 3/4 (Второе задание)')
        async with state.proxy() as data:
            answers_all_2 = data['ref1']
        answers_all_2.append(id_3)
        async with state.proxy() as data:
            data['ref1'] = answers_all_2
        await Task2.next()
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)


@dp.message_handler(state=Task2.fourth_task)
async def change_task_1_3(message: types.Message, state: FSMContext):
    id_4 = message.text
    if id_4.lower() != 'отмена':
        await message.answer('Заполнено 4/4. (Второе задание) Данные записаны.')
        async with state.proxy() as data:
            answers_all_2 = data['ref1']
            answers_all = data['ref10']
        answers_all_2.append(id_4)
        change_tasks_1(*answers_all)
        users = change_tasks_2(*answers_all_2)
        for i in users:
            await bot.send_message(i, 'Задания 1 и 2 обновлены')
        await state.reset_state(with_data=False)
    else:
        await state.reset_state(with_data=False)
        await bot_start(message)
