'''This module configures application settings from config.yaml'''

from pyaml_env import parse_config
from dotenv import load_dotenv

from helpers.lru_caching import timed_lru_cache
from helpers.misc import AppSettings, FileManagement


load_dotenv()


@timed_lru_cache(seconds=60)
def get_settings():
    '''Set up settings in cache for the above lifetime, then refreshes it.'''
    return AppSettings(config)


# project settings
config = parse_config('config.yaml')

# set up environment
env = config['APP']['ENVIRONMENT']
if env == 'development':
    config['APP']['DEBUG'] = True
    config['APP']['TESTING'] = True

# set up support files
config['SQL_QUERY'] = {}
config['SQL_QUERY']['rubber_wood'] = FileManagement.read_sql(
    'support_files/sql/rubber_wood.sql')

config['ATOMIC_WEIGHT'] = FileManagement.read_json(
    'support_files/json/atomic_weight.json')
config['UNIT_CONVERSION'] = FileManagement.read_json(
    'support_files/json/unit_conversion.json')
config['PLANTATION_METRICS'] = FileManagement.read_json(
    'support_files/json/plantation_metrics.json')
