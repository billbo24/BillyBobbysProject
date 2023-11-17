from typing import Any, Iterable
import psycopg2
from src.config import get_billy_bobbys_db_cred

from psycopg2._psycopg import connection

def get_default_con() -> connection:
    return psycopg2.connect(**get_billy_bobbys_db_cred())

def query_db(con: connection, query_string: str, parameters: list[Any]=None) -> Iterable[str]:
    crsr = con.cursor()
    yield from crsr.execute(query_string, parameters)

def insert_db(con: connection, query_string: str, parameters: list[Any]=None) -> None:
    crsr = con.cursor()
    crsr.execute(query_string, parameters)