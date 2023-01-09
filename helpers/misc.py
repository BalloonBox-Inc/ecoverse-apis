'''This module contains a miscellaneous collection of unit functions.'''

import json
from typing import Any
from uuid import UUID
from decimal import Decimal
from datetime import date, datetime
from caseconverter import camelcase
from pandas import DataFrame


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

    def postgresql(s: str) -> str:
        '''Format PostgreSQL URI string.'''
        if 'postgresql' not in s:  # pylint: disable=[E1135]
            return s.replace('postgres', 'postgresql')
        return s

    def class_to_dict_list(lst: list) -> list:
        '''Convert a list of objects to a list of dicts.'''
        return [item.__dict__ for item in lst]  # pylint: disable=[E1133]

    def column_string_to_list(data: DataFrame, column: str, sep: str) -> DataFrame:
        '''Convert string to list in a given dataframe column.'''
        data[column] = data[column].apply(lambda x: x.split(sep))  # pylint: disable=[E1137]
        return data


class FileManagement:
    '''File management class.'''

    def read_file(filename: str) -> str | dict | None:
        '''Read HTML, JSON, SQL, and TXT files.'''
        _type = filename.split('.')[-1]
        with open(filename, mode='r', encoding='utf-8') as f:
            if _type in ['html', 'sql', 'txt']:
                return f.read()
            if _type == 'json':
                return json.load(f)
        return None


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
        for d in data:  # pylint: disable=[E1133]
            for k in list(d.keys()):
                d[DataFormatter.camel_case(k)] = d.pop(k)
        return data

    def obj_list_strip_string(data: list) -> list:
        '''Remove the leading and the trailing characters of the string values of a list of dictionaries.'''
        for d in data:  # pylint: disable=[E1133]
            for k, v in d.items():
                if isinstance(v, str):
                    d[k] = v.strip()
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
