'''This module access the MSSQL external database. It might need to install some dependencies first.
Learn more about it at https://github.com/pymssql/pymssql/issues/731'''

from typing import Generator
import json
import pymssql

from config import get_settings
from helpers.misc import JSONCustomEncoder


settings = get_settings()


class MSSQLDatabase:
    '''MSSQL database class.'''

    def connect(server: str, username: str, password: str, database: str) -> Generator:
        '''Connect to a MSSQL database.'''
        return pymssql.connect(server, username, password, database)

    def query(conn: pymssql, query: str) -> list:
        '''Query a MSSQL database.'''
        with conn.cursor(as_dict=True) as cursor:  # pylint: disable=[E1101]
            cursor.execute(query)
            data = cursor.fetchall()
            data = [i for n, i in enumerate(data) if i not in data[n + 1:]]
            data = json.dumps(
                obj=data,
                allow_nan=False,
                cls=JSONCustomEncoder
            )
        return json.loads(data)

    def get_db() -> Generator:  # pylint: disable=[E0211]
        '''Database generator.'''
        try:
            server = settings.DATABASE.MSSQL.SERVER
            username = settings.DATABASE.MSSQL.USERNAME
            password = settings.DATABASE.MSSQL.PASSWORD
            database = settings.DATABASE.MSSQL.DATABASE
            db = pymssql.connect(server, username, password, database)
            yield db
        finally:
            db.close()
