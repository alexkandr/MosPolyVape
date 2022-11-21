from datetime import datetime
from decimal import *
from aiogram import html
from dataclasses import dataclass


@dataclass
class ParilkaDAO:
    id: int
    name: str  
    description: str  
    image : str  
    taste: str  
    puffs: int  
    price : Decimal  
    avaible : int = 0

    def __init__(self, id : int = 0, name: str ='', description: str ='', 
    image : str ='', taste: str ='', puffs: int = 0, price : Decimal = 0, avaible : int = 0) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.puffs = puffs
        self.price = price
        self.taste = taste
        self.avaible = avaible

    def values_as_tuple(self) -> tuple[str, str, str, str, int, Decimal, int]:
        return (self.name, self.description, self.image, self.taste, self.puffs, self.price, self.avaible)

    def message_info(self) -> str:
        return (f"{self.name}\n" 
            f"{self.description}\n" 
            f"Вкус    {self.taste}\n" 
            f"Тяжек   {self.puffs}\n" 
            f"Цена    {html.italic(self.price)} рублей")
        

@dataclass
class OrderDAO:
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