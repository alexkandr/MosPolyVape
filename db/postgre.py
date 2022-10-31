from os import getenv
import psycopg
from models.item import parilka
from psycopg.rows import class_row
from psycopg.rows import dict_row

DATABASE_URL = getenv('DATABASE_URL') if getenv('DATABASE_URL') is not None else open('tokens.txt', 'r').readlines()[1].strip()

class DataBase:
    def __init__(self):
        self.conn = psycopg.connect(DATABASE_URL)
        self.conn.autocommit = True

    def execute(self, command: str, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        with self.conn.cursor() as cur:
                if fetch:
                    result =  cur.fetch(command, *args)
                elif fetchval:
                    result =  cur.fetchval(command, *args)
                elif fetchrow:
                    result =  cur.fetchrow(command, *args)
                elif execute:
                    result =  cur.execute(command, *args)
        return result

    def buy_some_parilkas(self, id : int, amount : int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                '''update sklad set avaible = avaible - %s where Id = %s''', (amount, id) )

    def select_all(self) -> list[parilka]:
        with self.conn.cursor(row_factory=class_row(parilka)) as cur:
            return cur.execute('''select * from sklad''').fetchall()
    
    def select_by_puffs(self, how_many : str) -> list[parilka]:
        match how_many:
            case 'lt1000':
                where = 'where puffs <= 1000 and avaible > 0'
            case 'lt2000':
                where = 'where puffs >= 1000 and puffs <= 2000 and avaible > 0'
            case 'lt4000':
                where = 'where puffs >= 2000 and puffs <= 4000 and avaible > 0'
            case 'gt4000':
                where = 'where puffs >= 4000 and avaible > 0'
        with self.conn.cursor(row_factory=class_row(parilka)) as cur:
            return cur.execute(f'select * from sklad {where}').fetchall()
    
    def select_by_id(self, item_id : int) -> parilka:
        with self.conn.cursor(row_factory=class_row(parilka)) as cur:
            return cur.execute(f'select * from sklad where id = {item_id}').fetchone()

    def get_addresses_by_user_id(self, user_id : int) -> list[dict]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            return cur.execute(f'select * from addresses where user_id = {user_id}').fetchall()

    def delete_addresses_by_user_id(self, user_id : int):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f'delete from addresses where user_id = {user_id}')

    def delete_address(self, user_id : int, obshaga : int, room_number : int):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f'delete from addresses where user_id = {user_id} and room_number={room_number} and obshaga = {obshaga}')
    
    def add_address(self, user_id : int, obshaga : int, room_number : int):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(f'insert into addresses (user_id, room_number, obshaga) values({user_id}, {room_number}, {obshaga})')

    def add_new_parilkas(self, item : parilka) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                '''insert into sklad (name, description, image, taste, puffs, price, avaible) 
                values (%s, %s, %s, %s, %s, %s, %s)''', 
                item.values_as_tuple() )

    def add_existing_parilkas(self, id : int, amount : int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                '''update sklad set avaible = avaible + %s where Id = %s''', (amount, id) )

    def select_all(self) -> list[parilka]:
        with self.conn.cursor(row_factory=class_row(parilka)) as cur:
            return cur.execute('''select * from sklad''').fetchall()

    def select_all_names(self) -> list[dict]:
        with self.conn.cursor(row_factory=dict_row) as cur:
            return cur.execute('''select id, name from sklad''').fetchall()

    def delete_by_item_id(self, id : int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(f''' delete from sklad where id = {id}''')

postgredb = DataBase()