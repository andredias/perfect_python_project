from pydantic import BaseModel
from pytest import mark, raises
from sqlalchemy.exc import IntegrityError
from uuid_extensions import uuid7

from {{cookiecutter.project_slug}}.models import diff_models, user
from {{cookiecutter.project_slug}}.models.user import UserInsert, UserPatch, check_password

Users = list[user.UserInfo]


async def test_get_user(users: Users) -> None:
    all_users = await user.get_all()
    assert all_users == users


async def test_get_user_by_id(users: Users) -> None:
    # ok
    user_info = await user.get_user(users[0].id)
    assert user_info == users[0]

    # inexistent user
    user_info = await user.get_user(uuid7())
    assert user_info is None


async def test_get_user_by_email(users: Users) -> None:
    # ok
    user_info = await user.get_user_by_email(users[0].email)
    assert user_info == users[0]

    # inexistent user
    user_info = await user.get_user_by_email('valid@email.com')
    assert user_info is None


async def test_get_user_by_login(users: Users) -> None:
    # ok
    user_info = await user.get_user_by_login(users[0].email, 'Paulo Paulada Power')
    assert user_info == users[0]

    # incorrect email + password
    user_info = await user.get_user_by_login(users[0].email, 'abcdefgh1234567890')
    assert user_info is None


def test_diff_models() -> None:
    insert = UserInsert(name='Fulano', email='fulano@email.com', password='123456 foo bar.')
    update = UserPatch(name='Beltrano', password='123456 foo bar.')
    diff = diff_models(insert, update)
    assert diff == {'name': 'Beltrano'}

    diff = diff_models(update, insert)
    assert diff == {'name': 'Fulano', 'email': 'fulano@email.com'}

    diff = diff_models(insert, insert)
    assert diff == {}


def test_password() -> None:
    with raises(ValueError) as error:
        check_password('1234')
    assert 'Password length' in str(error)

    with raises(ValueError) as error:
        check_password('1234123412341234')
    assert 'Variety <' in str(error)

    check_password('new password!!!')


@mark.parametrize('UserSchema', [UserInsert, UserPatch])
def test_user_schema(UserSchema: BaseModel) -> None:  # noqa: N803
    with raises(ValueError):
        UserSchema(  # type: ignore
            name='abcdef',
            email='invalid.email.com',
            password='valid password!!!',
        )

    with raises(ValueError) as error:
        UserSchema(name='abcdef', email='valid@email.com', password='invalid')  # type: ignore
    assert 'Password length' in str(error)

    UserSchema(name='abcdef', email='valid@email.com', password='valid password!!!')  # type: ignore

async def test_insert_user(users: Users) -> None:
    new_user = UserInsert(name='Paulo', email='paulo@email.com', password='Paulo Paulada Power')
    id = await user.insert(new_user)
    assert id and id not in [u.id for u in users]

    with raises(IntegrityError):
        await user.insert(new_user)


async def test_update_user(users: Users) -> None:
    password = 'Another Valid Password 123!!!'
    patch = UserPatch(name='Alfredo', password=password)
    await user.update(users[0].id, patch)
    updated_user = await user.get_user(users[0].id)
    assert updated_user
    assert updated_user.name == 'Alfredo'

    assert (await user.get_user_by_login(users[0].email, password)) == updated_user

    with raises(IntegrityError):
        await user.update(users[0].id, UserPatch(email=users[1].email))


async def test_delete_user(users: Users) -> None:
    await user.delete(users[0].id)
    deleted_user = await user.get_user(users[0].id)
    assert deleted_user is None

    await user.delete(users[0].id)  # shouldn't raise any error
