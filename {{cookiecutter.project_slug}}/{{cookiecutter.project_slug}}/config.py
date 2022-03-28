import os

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

DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']
DATABASE_URL = (
    os.getenv('DATABASE_URL')
    or f'postgresql://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 15))
PASSWORD_MIN_VARIETY = int(os.getenv('PASSWORD_MIN_VARIETY', 5))
