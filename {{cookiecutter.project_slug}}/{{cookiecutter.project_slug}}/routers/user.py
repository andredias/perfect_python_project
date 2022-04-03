from asyncpg.exceptions import IntegrityConstraintViolationError
from fastapi import APIRouter, HTTPException
from loguru import logger

from ..models.user import delete, get_all, get_user, insert, update
from ..resources import db
from ..schemas import diff_models
from ..schemas.user import UserInfo, UserInsert, UserPatch

router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=list[UserInfo])
async def get_all_users() -> list[UserInfo]:
    return await get_all()


@router.post('', status_code=201)
@db.transaction()
async def insert_user(info: UserInsert) -> dict:
    id_ = await insert(info)
    return {'id': id_}


@router.get('/{id_}', response_model=UserInfo)
async def get_user_info(id_: int) -> UserInfo:
    user = await get_user(id_)
    if not user:
        raise HTTPException(404)
    return user


@router.put('/{id_}', status_code=204)
@db.transaction()
async def update_user(
    id_: int,
    patch: UserPatch,
) -> None:
    user = await get_user(id_)
    if not user:
        raise HTTPException(404)
    patch = UserPatch(**diff_models(user, patch))
    try:
        await update(id_, patch)
    except IntegrityConstraintViolationError:
        logger.info(f'Integrity violation in {user} vs {patch}')
        raise HTTPException(422)
    return


@router.delete('/{id_}', status_code=204)
@db.transaction()
async def delete_user(id_: int) -> None:
    await delete(id_)
    return
