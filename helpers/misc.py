'''This module contains a miscellaneous collection of unit functions.'''

import json
from typing import Any
from uuid import UUID
from decimal import Decimal
from datetime import date, datetime
from caseconverter import camelcase, pascalcase
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

    def dict_mismatch(d1: dict, d2: dict) -> dict:
        '''Find the difference between two dictionaries.'''
        return {k: v for k, v in d2.items() if k in [k for k in d1.keys() & d2 if d1[k] != d2[k]]}


class DataFormatter:
    '''Data formatter class.'''

    def camel_case(s: str) -> str:
        '''Convert a string case to camel style.'''
        return camelcase(s)

    def pascal_case(s: str) -> str:
        '''Convert a string case to pascal style.'''
        return pascalcase(s)

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


class DatabaseFormatter:
    '''Database formatter class.'''

    def nft_table(data: dict) -> dict:
        d = ResponseFormatter.obj_list_case_converter(data=[data], format='camel')[0]
        for k in ['saInstanceState', 'id', 'createdAt', 'updatedAt']:
            d.pop(k)
        for k in ['genusName', 'speciesName']:
            d.update({k: d[k].replace('{', '').replace('}', '').split(',')})
        return d


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

    def obj_list_case_converter(data: list, format: str) -> list:
        '''Convert the keys case style of a list of dictionaries based on format, e.g. camel, pascal.'''
        if format == 'camel':
            for d in data:  # pylint: disable=[E1133]
                for k in list(d.keys()):
                    d[DataFormatter.camel_case(k)] = d.pop(k)
        elif format == 'pascal':
            for d in data:  # pylint: disable=[E1133]
                for k in list(d.keys()):
                    d[DataFormatter.pascal_case(k)] = d.pop(k)
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
