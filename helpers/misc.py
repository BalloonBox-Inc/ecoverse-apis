'''This module contains a miscellaneous collection of unit functions.'''

import json
from decimal import Decimal
from datetime import date, datetime


class TypeConvertion:
    '''Data type conversion class.'''

    def json_serial(obj) -> str | float:
        '''JSON serializer for objects not serializable by default json code.'''
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(obj)


class FileManagement:
    '''File management class.'''

    def read_json(filename: str) -> dict:
        '''Read a JSON file.'''
        with open(filename, mode='r', encoding='utf-8') as f:
            return json.load(f)

    def read_sql(filename: str) -> str:
        '''Read a SQL file.'''
        with open(filename, mode='r') as f:
            return f.read()
