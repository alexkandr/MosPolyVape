from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData

class ItemCallbackFactory(CallbackData, prefix="item"):
    action : str
    item_id : int
    amount: int