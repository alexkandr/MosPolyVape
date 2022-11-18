from dataclasses import dataclass
from decimal import *
from datetime import *

@dataclass
class order:
    id : int
    user_id : int
    address_id : int
    total_sum : Decimal
    payment_method : str
    status : str
    creating_time : datetime

    def __init__(self, id : int = 0, user_id : int = 0, address_id : int = 0, total_sum : Decimal = 0, payment_method : str = '', status : str = 'created', creating_time : datetime = datetime.now()):
        self.id = id
        self.user_id = user_id
        self.address_id = address_id
        self.total_sum = total_sum
        self.payment_method = payment_method
        self.status = status
        self.creating_time = creating_time

    def values_as_tuple(self) -> tuple[int, int, Decimal, str, str, datetime]:
        return (self.user_id, self.address_id, self.total_sum, self.payment_method, self.status, self.creating_time)