from asyncpg.exceptions import IntegrityConstraintViolationError
from fastapi import APIRouter, HTTPException, Response
from loguru import logger

from ..models.user import delete, get_all, get_user, insert, update
from ..resources import db
from ..schemas import diff_models
from ..schemas.user import UserInfo, UserInsert, UserPatch

router = APIRouter(prefix='/users', tags=['users'])


@router.get('')
async def get_all_users() -> list[UserInfo]:
    return await get_all()


@router.post('', status_code=201)
@db.transaction()
async def insert_user(info: UserInsert, response: Response) -> UserInfo:
    id = await insert(info)
    response.headers['Location'] = f'/users/{id}'
    return await get_user(id)  # type: ignore


@router.get('/{id}')
async def get_user_info(id: int) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(404)
    return user


@router.put('/{id}')
@db.transaction()
async def update_user(
    id: int,
    patch: UserPatch,
) -> UserInfo:
    user = await get_user(id)
    if not user:
        raise HTTPException(404)
    patch = UserPatch(**diff_models(user, patch))
    try:
        await update(id, patch)
    except IntegrityConstraintViolationError:
        logger.info(f'Integrity violation in {user} vs {patch}')
        raise HTTPException(422) from None
    return await get_user(id)  # type: ignore


@router.delete('/{id}', status_code=204)
@db.transaction()
async def delete_user(id: int) -> None:
    await delete(id)
    return
