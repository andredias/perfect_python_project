import json
import sys

from loguru import logger
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import JsonLexer

from . import config

lexer = JsonLexer()
formatter = Terminal256Formatter(style=config.PYGMENTS_STYLE)


def serialize(record: dict) -> str:
    subset = {
        'time': record['time'].isoformat(),
        'level': record['level'].name,
        'message': record['message'],
        'source': f'{record["file"].name}:{record["function"]}:{record["line"]}',
    }
    subset.update(record['extra'])
    if record['exception']:
        subset['exception'] = record['exception']
    if config.DEBUG:
        formatted_json = json.dumps(subset, indent=4)
        return highlight(formatted_json, lexer, formatter)
    return json.dumps(subset)


def init_loguru() -> None:
    logger.remove()
    # https://loguru.readthedocs.io/en/stable/resources/recipes.html#serializing-log-messages-using-a-custom-function
    logger.add(lambda message: print(serialize(message.record), file=sys.stderr))  # type: ignore
