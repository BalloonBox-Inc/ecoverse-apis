'''This module configures application settings from config.yaml'''

from pyaml_env import parse_config
from dotenv import load_dotenv

from helpers.misc import AppSettings, DataFormatter, FileManagement
from helpers.lru_caching import timed_lru_cache


load_dotenv()


@timed_lru_cache(seconds=10)
def get_settings() -> AppSettings:
    '''Set up settings in cache for the above lifetime, then refreshes it.'''
    return AppSettings(config)


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
config['DATABASE']['POSTGRESQL']['URI'] = DataFormatter.postgresql(config['DATABASE']['POSTGRESQL']['URI'])

# set up supporting data
path_json = 'supporting_data/json'  # pylint: disable=[C0103]
config['ATOMIC_WEIGHT'] = FileManagement.read_file(f'{path_json}/atomic_weight.json')
config['UNIT_CONVERSION'] = FileManagement.read_file(f'{path_json}/unit_conversion.json')
config['PLANTATION_METRICS'] = FileManagement.read_file(f'{path_json}/plantation_metrics.json')
