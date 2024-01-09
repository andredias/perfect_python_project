from fastapi import APIRouter

router = APIRouter(prefix='/fragment', tags=['fragment'])


@router.get('/hello')
async def hello_world() -> str:
    return '<h1>Hello World!</h1>'
