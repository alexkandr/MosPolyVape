from decimal import *
from aiogram import html
from dataclasses import dataclass


@dataclass
class parilka:
    id: int
    name: str  
    description: str  
    image : str  
    taste: str  
    puffs: int  
    price : Decimal  
    avaible : int = 0

    def __init__(self, name: str ='', description: str ='', 
    image : str ='', taste: str ='', puffs: int = 0, price : Decimal = 0, avaible : int = 0) -> None:
        self.name = name
        self.description = description
        self.image = image
        self.puffs = puffs
        self.price = price
        self.taste = taste
        self.avaible = avaible

    def __init__(self, id : int, name: str ='', description: str ='', 
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
        