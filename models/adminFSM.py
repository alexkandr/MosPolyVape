from aiogram.fsm.state import StatesGroup, State

class itemState(StatesGroup):
    name = State()
    description = State()
    image = State()
    taste = State()
    puffs = State()
    price = State()
    avaible = State()
    add_amount = State()