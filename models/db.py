from os import getenv
import asyncio

import psycopg
from psycopg.rows import class_row
from psycopg.rows import dict_row
from redis import asyncio as aioredis

from models.dao import ParilkaDAO, OrderDAO

DATABASE_URL = getenv('DATABASE_URL') if getenv('DATABASE_URL') is not None else open('tokens.txt', 'r').readlines()[1].strip()
CART_DB_URL = getenv('CART_DB_URL') if getenv('CART_DB_URL') is not None else open('tokens.txt', 'r').readlines()[2].strip()
PASSWORD = getenv('PASSWORD') if getenv('PASSWORD') is not None else open('tokens.txt', 'r').readlines()[3].strip()

class SkladTable:
    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)

    async def add_amount(self, id : int, amount : int) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute('''update sklad set avaible = avaible + %s where Id = %s''', (amount, id))

    async def subtract_amount(self, id : int, amount : int) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute('''update sklad set avaible = avaible - %s where Id = %s''', (amount, id))

    async def get_all(self) -> list[ParilkaDAO]:
        async with self.conn.cursor(row_factory=class_row(ParilkaDAO)) as cur:
            await cur.execute('''select * from sklad''')
            return await cur.fetchall()

    async def get_by_category(self, how_many : str) -> list[ParilkaDAO]:
        match how_many:
            case 'lt1000':
                where = 'where puffs <= 1000 and avaible > 0'
            case 'lt2000':
                where = 'where puffs >= 1000 and puffs <= 2000 and avaible > 0'
            case 'lt4000':
                where = 'where puffs >= 2000 and puffs <= 4000 and avaible > 0'
            case 'gt4000':
                where = 'where puffs >= 4000 and avaible > 0'
        async with self.conn.cursor(row_factory=class_row(ParilkaDAO)) as cur:
            await cur.execute(f'select * from sklad {where}')
            return await cur.fetchall()

    async def get_by_id(self, item_id : int) -> ParilkaDAO:
        async with self.conn.cursor(row_factory=class_row(ParilkaDAO)) as cur:
            await cur.execute(f'select * from sklad where id = {item_id}')
            return await cur.fetchone()

    async def add(self, item : ParilkaDAO) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(
                '''insert into sklad (name, description, image, taste, puffs, price, avaible) 
                values (%s, %s, %s, %s, %s, %s, %s)''', item.values_as_tuple() )

    async def get_names(self) -> list[dict]:
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute('''select id, name from sklad''')
            return await cur.fetchall()

    async def delete_by_id(self, id : int) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(f''' delete from sklad where id = {id}''')


class AddressesTable:
    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)

    async def get_by_user_id(self, user_id : int) -> list[dict]:
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'select * from addresses where user_id = {user_id}')
            return await cur.fetchall()

    async def get_by_id(self, id : int) -> dict:
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'select * from addresses where id = {id}')
            return await cur.fetchone()

    async def delete_by_user_id(self, user_id : int):
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'delete from addresses where user_id = {user_id}')

    async def delete(self, user_id : int, obshaga : int, room_number : int):
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'delete from addresses where user_id = {user_id} and room_number={room_number} and obshaga = {obshaga}')

    async def add(self, user_id : int, obshaga : int, room_number : int):
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'insert into addresses (user_id, room_number, obshaga) values({user_id}, {room_number}, {obshaga})')

            
class OrdersTable:
    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)

    async def add(self, order : OrderDAO) -> int:
        async with self.conn.cursor() as cur:
            await cur.execute(
                '''insert into orders (user_id, address_id, total_sum, payment_method, status, creating_time) 
                values ( %s, %s, %s, %s, %s, %s) returning id''', 
                order.values_as_tuple() )
            return (await cur.fetchone())[0]

    async def get_all(self, status : str = '') -> list[OrderDAO]:
        async with self.conn.cursor(row_factory=class_row(OrderDAO)) as cur:
            filter = f"where status = '{status}'" if status != '' else ''
            await cur.execute(f'''select * from orders {filter}''')
            return await cur.fetchall()


class ImagesTable:
    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)

    async def add(self, file_id : str, file_name : str) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(f'''insert into images (file_id, file_name) values ('{file_id}', '{file_name}')''')
    
    async def get_all(self) -> list[dict]:
        async with self.conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(f'''select (file_name, file_id) from images''')
            return await cur.fetchall()

    async def delete(self, id : int) -> None:
        async with self.conn.cursor() as cur:
            await cur.execute(f'''delete from sklad where id = {id}''')
    
    async def get_by_name(self, file_name : str) -> str:
        async with self.conn.cursor() as cur:
            await cur.execute(f'''select file_id from images where file_name = '{file_name}' ''')
            return (await cur.fetchone())[0]


class OrderedItemsTable:
    async def connect(self):
        self.conn = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)

    async def add_cart(self, cart : dict, order_id : int) -> None:
        async with self.conn.cursor() as cur:
            for item_id, amount in cart.items():
                await cur.execute(f'''insert into ordered_items (order_id, item_id, amount) values ({order_id}, {item_id}, {amount})''')

    async def get_by_order_id(self, order_id : int) -> list[ParilkaDAO]:
        async with self.conn.cursor(row_factory=class_row(ParilkaDAO)) as cur:
            await cur.execute(f'''select * from ordered_items where order_id = {order_id}''')
            return await cur.fetchall()


class DataBase:
    async def connect(self):
        self.conn = psycopg.connect(DATABASE_URL)
        self.conn.autocommit = True

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.conn.cursor() as cur:
                if fetch:
                    result =  cur.fetch(command, *args)
                elif fetchval:
                    result = cur.fetchval(command, *args)
                elif fetchrow:
                    result = cur.fetchrow(command, *args)
                elif execute:
                    result =  await cur.execute(command, *args)
        return result

class Carts:
    async def connect(self):
        self.r = aioredis.StrictRedis(host= CART_DB_URL, port= 13316, password= PASSWORD, decode_responses= True )

    async def add_to_cart(self, user_id : int | str, item_id : int | str, amount : int) -> dict:
        amnt = await self.r.hget(name=user_id, key=item_id)
        if amnt:
            await self.r.hset(name=str(user_id), key=int(item_id), value=amount+ amnt)    
            return await self.r.hgetall(name=user_id)
            
        await self.r.hset(name=str(user_id), key=int(item_id), value=amount)
        return await self.r.hgetall(name=user_id)

    async def change_amount(self, user_id : int | str, item_id : int | str, amount : int) -> dict:
        if amount <= 0:
            await self.r.hdel(user_id, item_id)
        else:
            await self.r.hset(name=str(user_id), key=int(item_id), value=amount)
        return await self.r.hgetall(name=user_id)

    async def get_cart(self, user_id : int | str) -> dict:
        return await self.r.hgetall(name=str(user_id))
    
    async def get_amount(self, user_id, item_id) -> int:
        return await self.r.hget(name=str(user_id), key=item_id)

    async def remove_item(self, user_id : int | str, item_id : int | str) -> dict:
        await self.r.hdel(str(user_id), int(item_id))
        return await self.r.hgetall(name=user_id)

    async def clear_cart(self, user_id : int | str) -> dict:
        cart = await self.r.hgetall(str(user_id))
        if cart:
            await self.r.hdel(str(user_id), * (await self.r.hkeys(user_id)))
        return cart

async def connect():
    await sklad_tab.connect()
    await orders_tab.connect()
    await ordered_items_tab.connect()
    await addresses_tab.connect()
    await images_tab.connect()
    await cart_rep.connect()

sklad_tab = SkladTable()
orders_tab = OrdersTable()
ordered_items_tab = OrderedItemsTable()
images_tab = ImagesTable()
addresses_tab = AddressesTable()
cart_rep = Carts()

asyncio.run(connect())

