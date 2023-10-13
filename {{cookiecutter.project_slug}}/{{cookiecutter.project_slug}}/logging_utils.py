import sys

from loguru import logger


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

def init_loguru() -> None:
    logger.remove()
    logger.add(sys.stderr, format=formatter)  # type: ignore
