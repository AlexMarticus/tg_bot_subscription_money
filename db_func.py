import sqlite3
from random import randint
from datetime import datetime, timedelta


def change_qiwi_token(token):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    cur.execute(f'UPDATE QIWI_token SET TOKEN = "{token}", DATE = "{datetime.today()}"').fetchone()
    sq_c.commit()
    cur.close()


def info_of_user(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    ref = cur.execute(f"""SELECT balance, profit, referral, tasks_completed, num_of_ref_used
FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return ref


def all_ref_codes():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = list(map(lambda x: x[0], cur.execute(f"""SELECT referral FROM users""").fetchall()))
    list_of_referrals = []
    for ref in sqlite_insert_query:
        list_of_referrals.append(ref)
    cur.close()
    return list_of_referrals


def check_is_not_his_ref(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    ref = cur.execute(f"""SELECT referral FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return ref


def check_is_new_user(tg_id):
    # сколько дней считается пользователь новым
    DAYS = 3
    ########

    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute("""SELECT tg_id, when_created, is_from_ref FROM users""")
    list_of_registred_users = []
    for id_, _date, is_ref in sqlite_insert_query:
        list_of_registred_users.append(id_)
        if id_ == tg_id:
            _date = datetime.strptime(_date, "%Y-%m-%d %H:%M:%S.%f")
            if _date + timedelta(days=DAYS) >= datetime.now() and is_ref == 0:
                return 'new_but_not_first'
            return 'old'
    cur.close()
    if tg_id in list_of_registred_users:
        return 'old'
    return 'new'


def add_new_user(tg_id, tg_username):
    LEN_OF_REFFERAL_CODE = 10

    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute("""SELECT referral FROM users""")
    list_of_refferals = []
    for i in sqlite_insert_query:
        list_of_refferals.append(i)
    refferal_code = ''
    for i in range(LEN_OF_REFFERAL_CODE):
        refferal_code += str(randint(0, 9))
    while refferal_code in list_of_refferals:
        refferal_code = ''
        for i in range(LEN_OF_REFFERAL_CODE):
            refferal_code += str(randint(0, 9))
    values = (tg_id, tg_username, refferal_code, 0, datetime.now(), 0, 0, 0, 0, 0, 0)
    sqlite_insert_query = """INSERT INTO users
                                      (tg_id, username, referral, balance, when_created, is_from_ref, num_of_ref_used,
                                      profit, tasks_completed, new_tasks, is_3_task_completed)
                                      VALUES
                                      (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cur.execute(sqlite_insert_query, values)
    sq_c.commit()
    cur.close()


def plus_one_num_of_tasks_completed(tg_id, summ=0.5):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    n_of_task = cur.execute(f"""SELECT tasks_completed FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.execute(f"""UPDATE users SET tasks_completed = {n_of_task[0] + 1} WHERE tg_id = {tg_id}""").fetchone()

    n_of_task = cur.execute(f"""SELECT new_tasks FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.execute(f"""UPDATE users SET new_tasks = {n_of_task[0] + 1} WHERE tg_id = {tg_id}""").fetchone()

    n_of_task = cur.execute(f"""SELECT balance FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.execute(f"""UPDATE users SET balance = {n_of_task[0] + summ} WHERE tg_id = {tg_id}""").fetchone()

    n_of_task = cur.execute(f"""SELECT profit FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.execute(f"""UPDATE users SET profit = {n_of_task[0] + summ} WHERE tg_id = {tg_id}""").fetchone()
    sq_c.commit()
    cur.close()


def from_ref(tg_id, ref):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = f"""UPDATE users SET is_from_ref = {1}, ref_of_friend = {int(ref)} WHERE tg_id = {tg_id}"""
    n_of_ref = cur.execute(f"""SELECT num_of_ref_used FROM users WHERE referral = {ref}""").fetchone()
    cur.execute(f"""UPDATE users SET num_of_ref_used = {n_of_ref[0] + 1} WHERE referral = {ref}""").fetchone()
    cur.execute(sqlite_insert_query).fetchone()
    sq_c.commit()
    cur.close()


def take_first_tasks():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute("""SELECT first_chat_id, second_chat_id, third_chat_id, fourth_chat_id
FROM first_task""").fetchall()
    cur.close()
    return sqlite_insert_query[0]


def take_second_tasks():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute("""SELECT first_chat_id, second_chat_id, third_chat_id, fourth_chat_id
FROM second_task""").fetchone()
    cur.close()
    return sqlite_insert_query


def check_lvl_in_tasks(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT new_tasks FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def check_used_ref(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT num_of_ref_used FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def give_ref(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT referral FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def give_qiwi_token():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT TOKEN FROM QIWI_token""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def set_qiwi_n(tg_id, qiwi):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    cur.execute(f"""UPDATE users SET qiwi = {qiwi} WHERE tg_id = {tg_id}""").fetchone()
    sq_c.commit()
    cur.close()


def change_tasks_1(t1, t2, t3, t4):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    cur.execute(f'UPDATE first_task SET first_chat_id = "{t1}", second_chat_id = "{t2}", third_chat_id = "{t3}", '
                f'fourth_chat_id = "{t4}"').fetchone()
    sq_c.commit()
    cur.close()


def when_qiwi_token_was_added():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT DATE FROM QIWI_token""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def task_3_completed_or_not(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT is_3_task_completed FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return sqlite_insert_query[0]


def minus_balance(tg_id, summ):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    balance = cur.execute(f"""SELECT balance FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.execute(f"""UPDATE users SET balance = {balance[0] - summ} WHERE tg_id = {tg_id}""").fetchone()
    sq_c.commit()
    cur.close()


def task_3_completed(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    cur.execute(f"""UPDATE users SET is_3_task_completed = 1 WHERE tg_id = {tg_id}""").fetchone()
    sq_c.commit()
    cur.close()


def change_tasks_2(t1, t2, t3, t4):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    cur.execute(f'UPDATE second_task SET first_chat_id = "{t1}", second_chat_id = "{t2}", third_chat_id = "{t3}", '
                f'fourth_chat_id = "{t4}"').fetchone()

    cur.execute(f'UPDATE users SET new_tasks = {0}').fetchone()
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute("""SELECT tg_id FROM users""")
    list_of_registred_users = []
    for id_ in sqlite_insert_query:
        list_of_registred_users.append(id_)
    sq_c.commit()
    cur.close()
    return list_of_registred_users


def give_all_tasks():
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    all_tasks = []
    sqlite_insert_query = cur.execute(f"""SELECT first_chat_id, second_chat_id,
third_chat_id, fourth_chat_id FROM first_task""").fetchone()
    all_tasks.append(sqlite_insert_query)
    sqlite_insert_query = cur.execute(f"""SELECT first_chat_id, second_chat_id,
third_chat_id, fourth_chat_id FROM second_task""").fetchone()
    all_tasks.append(sqlite_insert_query)
    cur.close()
    return all_tasks


def give_balance_and_qiwicard(tg_id):
    sq_c = sqlite3.connect('db_tg_money_subscribe.db')
    cur = sq_c.cursor()
    sqlite_insert_query = cur.execute(f"""SELECT balance, qiwi FROM users WHERE tg_id = {tg_id}""").fetchone()
    cur.close()
    return sqlite_insert_query
