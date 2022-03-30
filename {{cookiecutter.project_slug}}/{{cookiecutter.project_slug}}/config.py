import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. '
        "It should be 'production', 'development' or 'testing'"
    )
DEBUG = ENV != 'production'
TESTING = ENV == 'testing'

LOG_LEVEL = os.getenv('LOG_LEVEL') or (DEBUG and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'
