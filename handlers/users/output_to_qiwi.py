import requests
import time

# Перевод на QIWI Кошелек
from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import bot_start
from keyboards.inline.output_to_qiwi_inl_kb import outp_qiwi_bt
from states.set_qiwi_number_state import SetQIWINumber
from db_func import give_balance_and_qiwicard, give_qiwi_token, set_qiwi_n, minus_balance
from loader import dp


@dp.callback_query_handler(text="output_qiwi_inl_bt")
async def send_money(call: types.CallbackQuery):
    summ, qiwi_card = give_balance_and_qiwicard(call.from_user.id)
    if summ > 50:
        summ -= 50
    elif summ == 50:
        summ = 0
    if qiwi_card == '' or qiwi_card is None:
        await call.message.edit_text('Введите номер телефона или карты QIWI в формате +7/+994/+998/+375 и т.д.\n'
                                     'или "назад" для возврата в главное меню')
        await SetQIWINumber.number.set()
    elif balance('79196804453', give_qiwi_token())['accounts'][0]['balance']['amount'] < summ:
        await call.message.edit_text('Попробуйте вывести деньги завтра, на данный момент лимит исчерпан.')
    elif summ < 1:
        await call.message.edit_text('Минимальная сумма вывода - 1 рубль')
    else:
        send = send_p2p(give_qiwi_token(), "+" + str(qiwi_card), float(summ))
        print(send)
        if send['transaction']['state']['code'] == 'Accepted':
            minus_balance(call.from_user.id, 1)
            await call.message.edit_text('Платёж выполнен успешно')
        elif send['message'] == 'Пул номеров страны не активен':
            await call.message.edit_text('Ошибка при выводе средств, обратитесь к @seerb')
        elif send['message'] == 'Платеж невозможен ':
            await call.message.edit_text('Самому себе переводить странное занятие :)')
        elif send['message'] == 'Статус кошелька получателя не позволяет совершить платеж. Попросите владельца ' \
                                'кошелька пройти идентификацию — ввести паспортные данные.':
            await call.message.edit_text('Статус Вашего кошелька не позволяет совершать платёж. Ввеедите паспортные '
                                         'данные в QIWI.\nhttps://qiwi.com/settings/identification/form?utm_source'
                                         '=web&utm_medium=system_banner&utm_campaign=an_p2p')
        else:
            await call.message.edit_text('Ошибка при выводе средств, обратитесь к @seerb')


def balance(login, api_access_token):
    # Баланс QIWI Кошелька
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    return b.json()


@dp.message_handler(state=SetQIWINumber.number)
async def set_qiwi(message: types.Message, state: FSMContext):
    number = message.text
    if number.lower() == 'назад':
        await bot_start(message)
    else:
        if number[0] != '+':
            await state.reset_state(with_data=False)
            await message.answer('Номер телефона введён неверно')
            await bot_start(message)
        else:
            set_qiwi_n(message.from_user.id, number)
            await state.reset_state(with_data=False)
            await message.answer('Ваши данные сохранены', reply_markup=outp_qiwi_bt)


def send_p2p(api_access_token, to_qw, sum_p2p):
    s = requests.Session()
    s.headers = {'content-type': 'application/json', 'authorization': 'Bearer ' + api_access_token,
                 'User-Agent': 'Android v3.2.0 MKT', 'Accept': 'application/json'}
    postjson = {"sum": {"amount": "", "currency": ""},
                "paymentMethod": {"type": "Account", "accountId": "643"}, "comment": "Ваши лёгкие деньги",
                "fields": {"account": ""}, 'id': str(int(time.time() * 1000))}
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=postjson)
    return res.json()
