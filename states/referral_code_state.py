from aiogram.dispatcher.filters.state import StatesGroup, State


class TakeRefCode(StatesGroup):
    code = State()
