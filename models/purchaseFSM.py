from aiogram.fsm.state import StatesGroup, State

class PurchaseState(StatesGroup):
    ChooseAddress = State()
    PaymentMethod = State()
    Accept = State()
