import os

from dotenv import load_dotenv

load_dotenv()

ENV: str = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. '
        "It should be 'production', 'development' or 'testing'"
    )
DEBUG: bool = ENV != 'production'
TESTING: bool = ENV == 'testing'

os.environ['LOGURU_LEVEL'] = os.getenv('LOG_LEVEL') or (DEBUG and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'
LOG_JSON_FORMAT = os.getenv('LOG_JSON_FORMAT', 'false').lower() in {'true', '1', 'yes'}
REQUEST_ID_LENGTH = int(os.getenv('REQUEST_ID_LENGTH', '8'))
