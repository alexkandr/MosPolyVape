from aiogram import html
class parilka:
    
    def __init__(self, name: str ='', description: str ='', 
    image : str ='', taste: str ='', puffs: int = 0, avaible : int = 0) -> None:
        self.name = name
        self.description = description
        self.image = image
        self.puffs = puffs
        self.taste = taste
        self.avaible = avaible

    def message_info(self) -> str:
        return (f"{self.name}\n" 
            f"{self.description}\n" 
            f"Вкус    {self.taste}\n" 
            f"Тяжек   {self.puffs}\n" 
            f"Цена    {html.italic(self.price)} рублей")
        