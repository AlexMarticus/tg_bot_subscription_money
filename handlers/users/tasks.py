from aiogram import types

from keyboards.inline.check_is_subscribted_tasks_inl_kb import task_1_check, task_2_check, task_3_check
from keyboards.inline.tasks_2_3_inl_kb import task_2, task_3, after_3_task
from db_func import take_first_tasks, take_second_tasks, check_lvl_in_tasks, give_ref, check_used_ref, \
    plus_one_num_of_tasks_completed, task_3_completed_or_not, task_3_completed
from loader import dp, bot


@dp.callback_query_handler(text="tasks_bt_inl_kb")
async def f_task(call: types.CallbackQuery):
    print(check_lvl_in_tasks(call.from_user.id))
    if check_lvl_in_tasks(call.from_user.id) == 0:
        await f_task(call)
    elif check_lvl_in_tasks(call.from_user.id) == 1:
        await s_task(call)
    elif check_lvl_in_tasks(call.from_user.id) == 2:
        await th_task(call)


@dp.callback_query_handler(text="tasks_bt_inl_kb")
async def f_task(call: types.CallbackQuery):
    f, s, t, fo = take_first_tasks()
    text = f"""Подпишитесь на следующие 4 канала:\n
{f}\n
{s}\n
{t}\n
{fo}
"""
    await call.message.edit_text(text, reply_markup=task_1_check)


@dp.callback_query_handler(text="check_1task_inl_bt")
async def f_ch_task(call: types.CallbackQuery):
    f, s, t, fo = take_first_tasks()
    f, s, t, fo = str(f), str(s), str(t), str(fo)
    is_subscr = []
    for i in (f, s, t, fo):
        print(i)
        user_channel_status = await bot.get_chat_member(chat_id=i, user_id=call.from_user.id)
        if user_channel_status["status"] != 'left':
            is_subscr.append(True)
        else:
            is_subscr.append(False)
    if all(is_subscr):
        plus_one_num_of_tasks_completed(call.from_user.id)
        await call.message.edit_text('Вы выполнили задание и получили 0.5 руб в профиле. Не отписывайтесь '
                                     'от них чтобы мы выплатили вам деньги.', reply_markup=task_2)
    else:
        await bot.send_message(call.from_user.id, 'Вы не подписались на определенные каналы. Подпишитесь, чтобы мы '
                                                  'смогли  выплатить вам деньги.')


@dp.callback_query_handler(text="2task_inl_bt")
async def s_task(call: types.CallbackQuery):
    f, s, t, fo = take_second_tasks()
    text = f"""Подпишитесь на следующие 4 канала:\n
{f}\n
{s}\n
{t}\n
{fo}
"""
    await call.message.edit_text(text, reply_markup=task_2_check)


@dp.callback_query_handler(text="check_2task_inl_bt")
async def s_ch_task(call: types.CallbackQuery):
    f, s, t, fo = take_first_tasks()
    f, s, t, fo = str(f), str(s), str(t), str(fo)
    is_subscr = []
    for i in (f, s, t, fo):
        user_channel_status = await bot.get_chat_member(chat_id=i, user_id=call.from_user.id)
        print(user_channel_status)
        if user_channel_status["status"] != 'left':
            is_subscr.append(True)
        else:
            is_subscr.append(False)
    if all(is_subscr):
        plus_one_num_of_tasks_completed(call.from_user.id)
        await call.message.edit_text('Вы выполнили задание и получили и получили 0.5 руб в профиле. Не отписывайтесь '
                                     'то них чтобы мы выплатили вам деньги.', reply_markup=task_3)
    else:
        await bot.send_message(call.from_user.id, 'Вы не подписались на определенные каналы. Подпишитесь, чтобы мы '
                                                  'смогли  выплатить вам деньги.')


@dp.callback_query_handler(text="3task_inl_bt")
async def th_task(call: types.CallbackQuery):
    await call.message.edit_text(f'''Поделись своим реферальным кодом (ниже) с 
15 друзьями и получи 50 рублей на баланс\n
Ваш реферальный код: {give_ref(call.from_user.id)}''', reply_markup=task_3_check)


@dp.callback_query_handler(text="check_3task_inl_bt")
async def s_ch_task(call: types.CallbackQuery):
    n = check_used_ref(call.from_user.id)
    flag = task_3_completed_or_not(call.from_user.id) == 1
    if n >= 15:
        if not flag:
            task_3_completed(call.from_user.id)
            plus_one_num_of_tasks_completed(call.from_user.id, summ=50)
            await call.message.edit_text('''Вы выполнили задание и получили и получили 50 руб в профиле. Когда первые 2 
задания обновятся, мы Вам сообщим, и Вы ещё раз сможете заработать свои деньги''', reply_markup=after_3_task)
        else:
            await call.message.edit_text('Вы выполнили все задания', reply_markup=after_3_task)
    else:
        await call.message.edit_text(f'По Вашему реферальному коду прошло только {n}', reply_markup=after_3_task)
