from aiogram import types
from aiogram.dispatcher import FSMContext

from db_func import from_ref, all_ref_codes, check_is_not_his_ref
from handlers.users.start import bot_start
from keyboards.inline.start_buttons_inl_kb import old_user
from states.referral_code_state import TakeRefCode
from loader import dp


@dp.callback_query_handler(text="referral_inl_kb")
async def text_for_take_ref(call: types.CallbackQuery):
    text = """Введите реферальный код или 'назад' для возвращения в главное меню"""
    await call.message.edit_text(text)
    await TakeRefCode.code.set()


@dp.message_handler(state=TakeRefCode.code)
async def take_ref(message: types.Message, state: FSMContext):
    ref = message.text
    if ref.lower() == 'назад':
        await bot_start(message)
    else:
        all_refs = all_ref_codes()
        is_my = check_is_not_his_ref(message.from_user.id)[0] != int(ref)
        if int(ref) in all_refs and is_my:
            from_ref(message.from_user.id, ref)
            await message.answer('Вы воспользовались реферальным кодом.')
            await message.answer("""Привет, это бот “ЛЕГКИЕ ДЕНЬГИ”. Мы даем возможность человеку заработать просто из 
ничего. Как ты знаешь таких проектов как наш очень мало. Ведь никто-бы не раздавал деньги какому-то 
незнакомому человеку просто так. Поподробнее о нас: За подписку на разные телеграмм каналы, 
боты и т.д будем давать деньги. За выполнение первого задания 0.5 рублей, за 2 задание 0.5 руб и т.д. В 
течение недели мы сможем оплатить. Так как в нашем банке лимит по переводам (100 людей за 1 день). Нажимай 
‘да’: """, reply_markup=old_user)
        elif not is_my:
            await message.answer('Это же Ваш реферальный код')
        else:
            await message.answer('Такой реферальный код не найден')
    await state.reset_state(with_data=False)
