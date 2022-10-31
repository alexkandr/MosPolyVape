from aiogram.fsm.state import StatesGroup, State

class GiveIdState(StatesGroup):
    recieve_image = State()
