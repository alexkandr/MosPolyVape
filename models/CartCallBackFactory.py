from typing import Optional
from aiogram.filters.callback_data import CallbackData

class CartCallbackFactory(CallbackData, prefix="cart"):
    action : str
    user_id : int
    item : Optional[int]