from aiogram import types
from db_func import info_of_user, check_is_new_user
from keyboards.inline.output_to_qiwi_inl_kb import outp_qiwi_bt
from keyboards.inline.start_buttons_inl_kb import old_user, new_user
from loader import dp


@dp.message_handler(commands='profile')
async def profile(message: types.Message):
    bal, prof, ref, tasks, n_ref_used = info_of_user(message.from_user.id)
    text = f"""Баланс: {bal}\n
Общий профит: {prof}\n
Реферальная ссылка: {ref}\n
Прошло по Вашей реферальной ссылке: {n_ref_used}\n
Кол-во выполненных заданий: {tasks}\n
"""
    await message.answer(text, reply_markup=outp_qiwi_bt)


@dp.callback_query_handler(text="profile_bt_inl_kb")
async def profile(call: types.CallbackQuery):
    bal, prof, ref, tasks, n_ref_used = info_of_user(call.from_user.id)
    text = f"""Баланс: {bal}\n
Общий профит: {prof}\n
Реферальная ссылка: {ref}\n
Прошло по Вашей реферальной ссылке: {n_ref_used}\n
Кол-во выполненных заданий: {tasks}\n
"""
    await call.message.edit_text(text, reply_markup=outp_qiwi_bt)


@dp.callback_query_handler(text="back_to_start")
async def back_to_start(call: types.CallbackQuery):
    flag = check_is_new_user(call.from_user.id)
    if flag == 'new_but_not_first':
        await call.message.edit_text("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто 
из ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так.\nПоподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘Ввести код’, если тебе его прислал друг. В ином случае - 'Задания': """, reply_markup=new_user)
    else:
        await call.message.edit_text("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто 
из ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так.\nПоподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘Задания’: """, reply_markup=old_user)
