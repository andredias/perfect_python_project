from pydantic import BaseModel
from pytest import mark, raises

from {{cookiecutter.project_slug}}.schemas import diff_models
from {{cookiecutter.project_slug}}.schemas.user import UserInsert, UserPatch, check_password


def test_diff_models() -> None:
    insert = UserInsert(
        name='Fulano',
        email='fulano@email.com',
        password='123456 foo bar.'
    )
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
