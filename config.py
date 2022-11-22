'''This module configures application settings from config.yaml'''

from pyaml_env import parse_config
from dotenv import load_dotenv

from helpers.misc import AppSettings, FileManagement
from helpers.lru_caching import timed_lru_cache


load_dotenv()


@timed_lru_cache(seconds=60)
def get_settings() -> AppSettings:
    '''Set up settings in cache for the above lifetime, then refreshes it.'''
    return AppSettings(config)


def postgresql_uri(uri: str) -> str:
    '''Format PostgreSQL URI string.'''
    if 'postgresql' not in uri:
        uri = uri.replace('postgres', 'postgresql')
    return uri


# project settings
config = parse_config('config.yaml')

# set up environment
if config['APP']['ENVIRONMENT'] == 'development':
    config['APP']['DEBUG'] = True
    config['APP']['TESTING'] = True

# set up database
config['DATABASE']['POSTGRESQL']['URI'] = postgresql_uri(config['DATABASE']['POSTGRESQL']['URI'])


# set up support files
config['SQL_QUERY'] = {}
config['SQL_QUERY']['rubber_wood'] = FileManagement.read_sql('supporting_data/sql/rubber_wood.sql')

config['ATOMIC_WEIGHT'] = FileManagement.read_json('supporting_data/json/atomic_weight.json')
config['UNIT_CONVERSION'] = FileManagement.read_json('supporting_data/json/unit_conversion.json')
config['PLANTATION_METRICS'] = FileManagement.read_json('supporting_data/json/plantation_metrics.json')
