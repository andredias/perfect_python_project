import os

from dotenv import load_dotenv

load_dotenv()

ENV: str = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. '
        "It should be 'production', 'development' or 'testing'"
    )
DEBUG: bool = ENV == 'development'
TESTING: bool = ENV == 'testing'

os.environ['LOGURU_LEVEL'] = os.getenv('LOG_LEVEL') or ((DEBUG or TESTING) and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'
REQUEST_ID_LENGTH = int(os.getenv('REQUEST_ID_LENGTH', '8'))
PYGMENTS_STYLE = os.getenv('PYGMENTS_STYLE', 'github-dark')

DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = TESTING and 'localhost' or os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = (TESTING and 'test_' or '') + os.environ['DB_NAME']
DATABASE_URL = f'postgresql://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

PASSWORD_MIN_LENGTH = int(os.environ['PASSWORD_MIN_LENGTH']) if 'PASSWORD_MIN_LENGTH' in os.environ else 15
PASSWORD_MIN_VARIETY = int(os.environ['PASSWORD_MIN_VARIETY']) if 'PASSWORD_MIN_VARIETY' in os.environ else 5
