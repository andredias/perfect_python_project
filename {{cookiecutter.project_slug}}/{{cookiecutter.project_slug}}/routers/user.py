from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status
from loguru import logger
from sqlalchemy.exc import IntegrityError

from ..models import diff_models
from ..models.user import UserInfo, UserInsert, UserPatch, delete, get_all, get_user, insert, update

router = APIRouter(prefix='/users', tags=['users'])


@router.get('')
async def get_all_users() -> list[UserInfo]:
    return await get_all()


@router.post('', status_code=status.HTTP_201_CREATED)
async def insert_user(info: UserInsert, response: Response) -> UserInfo:
    try:
        id = await insert(info)
    except IntegrityError:
        logger.info(f'Integrity violation inserting {info}')
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY) from None
    response.headers['Location'] = f'/users/{id}'
    return UserInfo(id=id, name=info.name, email=info.email)


@router.get('/{id}')
async def get_user_info(id: UUID) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


@router.put('/{id}')
async def update_user(id: UUID, patch: UserPatch) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    patch = UserPatch(**diff_models(user, patch))
    try:
        await update(id, patch)
    except IntegrityError:
        logger.info(f'Integrity violation in {user} vs {patch}')
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY) from None
    return UserInfo(id=id, name=patch.name or user.name, email=patch.email or user.email)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: UUID) -> None:
    await delete(id)
