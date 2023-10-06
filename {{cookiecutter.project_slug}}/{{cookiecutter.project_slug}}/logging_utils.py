import json
import sys

from loguru import logger

from . import config


LOGURU_FORMAT_PARTS = [
    '<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green>',
    '<level>{level: <}</level>',
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>',
    '<level>{message}</level>',
]

{% raw %}
def formatter(record: dict) -> str:
    """
    This is a custom formatter for Loguru.
    It will include extra fields in the log message format string.
    """
    if 'extra' in record:
        extras = [f'<level>{{extra[{key}]}}</level>' for key in record['extra'].keys()]
    else:
        extras = []
    return (
        ' | '.join(LOGURU_FORMAT_PARTS + extras) + '\n{exception}'
    )  # ref: https://loguru.readthedocs.io/en/stable/api/logger.html#message
{% endraw %}


def serialize(record: dict) -> str:
    subset = {
        'time': record['time'].isoformat(),
        'level': record['level'].name,
        'message': record['message'],
        'source': f'{record["file"].name}:{record["function"]}:{record["line"]}',
        'exception': record['exception'],
    }
    subset.update(record['extra'])
    return json.dumps(subset)


def init_loguru() -> None:
    logger.remove()
    if config.LOG_JSON_FORMAT:
        # https://loguru.readthedocs.io/en/stable/resources/recipes.html#serializing-log-messages-using-a-custom-function
        logger.add(lambda message: print(serialize(message.record), file=sys.stderr))  # type: ignore
    else:
        logger.add(sys.stderr, format=formatter)  # type: ignore
