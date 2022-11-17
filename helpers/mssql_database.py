'''This module access the MSSQL database. It might need to install some dependencies first.
Learn more about it at https://github.com/pymssql/pymssql/issues/731'''

import json
import pymssql

from helpers.misc import TypeConvertion


class MSSQLDatabase:
    '''MSSQL database class.'''

    def connect(server: str, username: str, password: str, database: str) -> pymssql:
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
                default=TypeConvertion.json_serial
            )
        return json.loads(data)
