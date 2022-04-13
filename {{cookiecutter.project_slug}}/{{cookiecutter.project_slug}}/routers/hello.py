from fastapi import APIRouter
from loguru import logger

router = APIRouter()


@router.get('/hello')
async def hello_world() -> dict[str, str]:
    logger.info('Hello world!')
    return {'message': 'Hello World'}
