from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData

class AddressCallbackFactory(CallbackData, prefix="address"):
    action : str
    address_index : Optional[int]