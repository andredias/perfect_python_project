from uuid import UUID

from asyncpg.exceptions import IntegrityConstraintViolationError
from fastapi import APIRouter, HTTPException, Response, status
from loguru import logger

from ..models import diff_models
from ..models.user import UserInfo, UserInsert, UserPatch, delete, get_all, get_user, insert, update
from ..resources import db

router = APIRouter(prefix='/users', tags=['users'])


@router.get('')
async def get_all_users() -> list[UserInfo]:
    return await get_all()


@router.post('', status_code=status.HTTP_201_CREATED)
@db.transaction()
async def insert_user(info: UserInsert, response: Response) -> UserInfo:
    id = await insert(info)
    response.headers['Location'] = f'/users/{id}'
    return await get_user(id)  # type: ignore


@router.get('/{id}')
async def get_user_info(id: UUID) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


@router.put('/{id}')
@db.transaction()
async def update_user(
    id: UUID,
    patch: UserPatch,
) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    patch = UserPatch(**diff_models(user, patch))
    try:
        await update(id, patch)
    except IntegrityConstraintViolationError:
        logger.info(f'Integrity violation in {user} vs {patch}')
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY) from None
    return await get_user(id)  # type: ignore


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@db.transaction()
async def delete_user(id: UUID) -> None:
    await delete(id)
