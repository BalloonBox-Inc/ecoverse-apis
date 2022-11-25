'''This module contains a miscellaneous collection of unit functions.'''

import json
from typing import Any
from uuid import UUID
from decimal import Decimal
from datetime import date, datetime
from caseconverter import camelcase


class AppSettings():
    '''Application settings class.'''

    def __init__(self, d):
        for k, v in d.items():
            if isinstance(k, (list, tuple)):
                setattr(self, k, [AppSettings(x) if isinstance(x, dict) else x for x in v])
            else:
                setattr(self, k, AppSettings(v) if isinstance(v, dict) else v)


class DataAggregator:
    '''Data aggregator class.'''

    def list_mean(lst: list) -> float:
        '''Take the average of a list of numbers.'''
        return sum(lst)/len(lst)


class DataFormatter:
    '''Data formatter class.'''

    def camel_case(s: str) -> str:
        '''Convert a string case to camel style.'''
        return camelcase(s)


class FileManagement:
    '''File management class.'''

    def read_json(filename: str) -> dict:
        '''Read a JSON file.'''
        with open(filename, mode='r', encoding='utf-8') as f:
            return json.load(f)

    def read_txt(filename: str) -> str:
        '''Read a text file.'''
        with open(filename, mode='r', encoding='utf-8') as f:
            return f.read()

    def read_sql(filename: str) -> str:
        '''Read a SQL file.'''
        with open(filename, mode='r', encoding='utf-8') as f:
            return f.read()


class JSONCustomEncoder(json.JSONEncoder):
    '''JSON custom encoder class.'''

    def default(self, o: Any) -> str | float:
        '''JSON serializer for objects not serializable by default json code.'''
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, UUID):
            return o.hex
        return super().default(o)


class ResponseFormatter:
    '''HTTP Response formatter class.'''

    def obj_list_to_camel_case(data: list) -> list:
        '''Convert the keys of a list of dictionaries to camel style.'''
        keys = list(data[0].keys())
        keys = [DataFormatter.camel_case(k) for k in keys]
        for d in data:  # pylint: disable=[E1133]
            for k1, k2 in zip(keys, d.keys()):  # pylint: disable=[C0103]
                d[k1] = d.pop(k2)
        return data


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
