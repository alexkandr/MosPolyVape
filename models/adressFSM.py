from aiogram.dispatcher.fsm.state import StatesGroup, State

class AddressState(StatesGroup):
    delete_address = State()
    choose_obshaga = State()
    choose_room = State()
