from aiogram.fsm.state import StatesGroup, State

class AddressState(StatesGroup):
    delete_address = State()
    choose_obshaga = State()
    choose_room = State()


class ItemState(StatesGroup):
    name = State()
    description = State()
    image = State()
    taste = State()
    puffs = State()
    price = State()
    avaible = State()
    add_amount = State()


class PurchaseState(StatesGroup):
    ChooseAddress = State()
    PaymentMethod = State()
    Accept = State()


class GiveIdState(StatesGroup):
    recieve_image = State()