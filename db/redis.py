import redis
from os import getenv

REDIS_DB_URL = getenv('RDIS_DB_URL') if getenv('REDIS_DB_URL') is not None else open('tokens.txt', 'r').readlines()[2].strip()

class DATABASE:
    def __init__(self):
        self.r = redis.StrictRedis(
            host= REDIS_DB_URL,
            port= 13316,
            password= 'x4hyZnntzVLiYF3iyXbgQ0ZPzy25MdkQ',
            decode_responses= True
        )

    def add_to_cart(self, user_id : int | str, item_id : int | str, amount : int) -> None:
        amnt = self.r.hget(name=user_id, key=item_id)
        if amnt:
            self.r.hset(name=str(user_id), key=int(item_id), value=amount+ amnt)    
            return
            
        self.r.hset(name=str(user_id), key=int(item_id), value=amount)

    def change_amount(self, user_id : int | str, item_id : int | str, amount : int) -> None:
        self.r.hset(name=str(user_id), key=int(item_id), value=amount)

    def get_cart(self, user_id : int | str) -> dict:
        return self.r.hgetall(name=str(user_id))
    
    def get_amount(self, user_id, item_id) -> int:
        return self.r.hget(name=str(user_id), key=item_id)

    def remove_item(self, user_id : int | str, item_id : int | str) -> None:
        self.r.hdel(str(user_id), int(item_id))

    def clear_cart(self, user_id : int | str) -> dict:
        cart = self.r.hgetall(str(user_id))
        self.r.hdel(str(user_id), *self.r.hkeys(user_id))
        return cart

redisdb = DATABASE()