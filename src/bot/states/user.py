from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    start_registration = State()
    pick_city = State()
    pick_city_to_edit = State()
    accept_terms = State()
    any_state = State()


class AdminState(StatesGroup):
    admin_panel = State()
    pick_city_for_post = State()
    delay_between_posts = State()
    wait_posts = State()
    delete_post = State()
