from fastapi import APIRouter, Request, Response

from ..resources import templates

router = APIRouter()


@router.get('/')
async def home(request: Request) -> Response:
    context = {
        'request': request,
        'title': 'Home',
    }
    return templates.TemplateResponse('home.html', context)
