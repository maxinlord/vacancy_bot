from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    start_registration = State()
    pick_city = State()
    accept_terms = State()
    any_state = State()


class AdminState(StatesGroup):
    any_state = State()
