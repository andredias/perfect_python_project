import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ENV: str = os.getenv('ENV', 'production').lower()
if ENV not in ('production', 'development', 'testing'):
    raise ValueError(
        f'ENV={ENV} is not valid. ' "It should be 'production', 'development' or 'testing'"
    )
DEBUG: bool = ENV != 'production'
TESTING: bool = ENV == 'testing'

os.environ['LOGURU_LEVEL'] = os.getenv('LOG_LEVEL') or (DEBUG and 'DEBUG') or 'INFO'
os.environ['LOGURU_DEBUG_COLOR'] = '<fg #777>'
REQUEST_ID_LENGTH = int(os.getenv('REQUEST_ID_LENGTH', '8'))
PYGMENTS_STYLE = os.getenv('PYGMENTS_STYLE', 'github-dark')

root_dir: Path = Path(__file__).resolve().parent.parent
STATIC_DIR: Path = root_dir / 'static'
TEMPLATE_DIR: Path = root_dir / 'templates'
