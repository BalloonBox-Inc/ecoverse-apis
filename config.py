'''This module configures application settings from config.yaml'''

from pyaml_env import parse_config
from dotenv import load_dotenv

from helpers.misc import AppSettings, FileManagement
from helpers.lru_caching import timed_lru_cache


load_dotenv()


@timed_lru_cache(seconds=10)
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

# set up API prefix
version = config['APP']['PROJECT_VERSION']
config['API'] = {}
config['API']['PREFIX'] = f'/api/v{version.split(".")[0]}'

# set up environment
if config['APP']['ENVIRONMENT'] == 'development':
    config['APP']['DEBUG'] = True
    config['APP']['TESTING'] = True

# set up database
config['DATABASE']['POSTGRESQL']['URI'] = postgresql_uri(config['DATABASE']['POSTGRESQL']['URI'])

# set up supporting data
config['SQL_QUERY'] = {}
config['SQL_QUERY']['rubber_wood'] = FileManagement.read_sql('supporting_data/sql/rubber_wood.sql')
config['SQL_QUERY']['farm'] = FileManagement.read_sql('supporting_data/sql/farm.sql')
config['SQL_QUERY']['farm_finder'] = FileManagement.read_sql('supporting_data/sql/farm_finder.sql')

config['ATOMIC_WEIGHT'] = FileManagement.read_json('supporting_data/json/atomic_weight.json')
config['UNIT_CONVERSION'] = FileManagement.read_json('supporting_data/json/unit_conversion.json')
config['PLANTATION_METRICS'] = FileManagement.read_json('supporting_data/json/plantation_metrics.json')
