from os import getenv
import psycopg
from models.item import parilka
from psycopg.rows import class_row

DATABASE_URL = getenv('DATABASE_URL') if getenv('DATABASE_URL') is str else open('tokens.txt', 'r').readlines()[2].strip()

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
                where = 'where puffs <= 1000'
            case 'lt2000':
                where = 'where puffs >= 1000 and puffs <= 2000'
            case 'lt4000':
                where = 'where puffs >= 2000 and puffs <= 4000'
            case 'gt4000':
                where = 'where puffs >= 4000'
        with self.conn.cursor(row_factory=class_row(parilka)) as cur:
            return cur.execute(f'select * from sklad {where}').fetchall()


postgredb = DataBase()