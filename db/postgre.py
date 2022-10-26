from typing import Union
from os import getenv
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool


class DataBase:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(getenv('DATABASE_ID'))
        await self.execute('''create table if not exists SKLAD(
            Id serial primary key,
            name character varying(30),
            description character varying(200),
            image character varying(100),
            taste character varying(30),
            puffs integer,
            avaible integer''')

    async def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
        return result

postgredb = DataBase()