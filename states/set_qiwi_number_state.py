from aiogram.dispatcher.filters.state import StatesGroup, State


class SetQIWINumber(StatesGroup):
    number = State()
