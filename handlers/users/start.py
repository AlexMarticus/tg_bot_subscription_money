import asyncio
from contextlib import suppress
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from db_func import check_is_new_user, add_new_user
from keyboards.inline.start_buttons_inl_kb import new_user, old_user
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    flag = check_is_new_user(message.from_user.id)
    if flag == 'new':
        add_new_user(message.from_user.id, message.from_user.username)
        await message.answer("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто из 
ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так.\nПоподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘Ввести код’, если тебе его прислал друг. В ином случае - 'Задания': """, reply_markup=new_user)
    elif flag == 'new_but_not_first':
        await message.answer("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто из 
ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так.\nПоподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘Ввести код’, если тебе его прислал друг. В ином случае - 'Задания': """, reply_markup=new_user)
    else:
        await message.answer("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто из 
ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так.\nПоподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘Задания’: """, reply_markup=old_user)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()
