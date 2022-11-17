'''This module contains a miscellaneous collection of unit functions.'''

import json
from decimal import Decimal
from datetime import date, datetime


class AppSettings():
    '''Application settings class.'''

    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [AppSettings(x) if isinstance(
                    x, dict) else x for x in v])
            else:
                setattr(self, k, AppSettings(v) if isinstance(v, dict) else v)


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


class TypeConvertion:
    '''Data type conversion class.'''

    def json_serial(obj) -> str | float:
        '''JSON serializer for objects not serializable by default json code.'''
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(obj)


class UnitMeasureConversion:
    '''Unit measure conversion class.'''

    def length(value: float, unit_in: str, unit_out: str, settings: AppSettings) -> float:
        '''Convert lenght measures from a unit to another.'''
        if unit_in == 'cm' and unit_out == 'in':
            unit = settings.UNIT_CONVERSION.length.cmIn
        elif unit_in == 'm' and unit_out == 'ft':
            unit = settings.UNIT_CONVERSION.length.mFt
        return value*unit

    def weight(value: float, unit_in: str, unit_out: str, settings: AppSettings) -> float:
        '''Convert weight measures from a unit to another.'''
        if unit_in == 'ton' and unit_out == 'lb':
            unit = settings.UNIT_CONVERSION.weight.tonLb
        return value*unit
