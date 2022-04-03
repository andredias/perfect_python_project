from {{cookiecutter.project_slug}}.models import user

Users = list[user.UserInfo]


async def test_get_user(users: Users) -> None:
    all_users = await user.get_all()
    assert all_users == users


async def test_get_user_by_id(users: Users) -> None:
    # ok
    user_info = await user.get_user(users[0].id)
    assert user_info == users[0]

    # inexistent user
    user_info = await user.get_user(-1)
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
