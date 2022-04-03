from httpx import AsyncClient

from {{cookiecutter.project_slug}}.models.user import UserInfo, UserInsert, get_user_by_login

Users = list[UserInfo]


async def test_get_users(users: Users, client: AsyncClient) -> None:
    resp = await client.get('/users')
    assert resp.status_code == 200
    assert resp.json() == users


async def test_get_user(users: Users, client: AsyncClient) -> None:
    url = '/users/{}'

    # tries to get an existing user
    resp = await client.get(url.format(users[0].id))
    assert resp.status_code == 200
    assert UserInfo(**resp.json()) == users[0]

    # tries to get inexistent user
    resp = await client.get(url.format(-1))
    assert resp.status_code == 404


async def test_update_user(users: Users, client: AsyncClient) -> None:
    url = '/users/{}'
    password = 'valid password!!!'
    name = 'Belafonte'

    # update ok
    resp = await client.put(url.format(users[0].id), json={'password': password})
    assert resp.status_code == 204
    resp = await client.get(url.format(users[0].id))
    user = await get_user_by_login(users[0].email, password)
    assert user

    # invalid password that doesn't satisfy the criteria
    resp = await client.put(
        url.format(users[0].id),
        json={'email': 'valid@email.com', 'password': 'too short'},
    )
    assert resp.status_code == 422

    # tries to update using an existing email
    resp = await client.put(url.format(users[0].id), json={'email': users[1].email})
    assert resp.status_code == 422

    # tries to update inexistent user
    resp = await client.put(url.format(-1), json={'name': name})
    assert resp.status_code == 404


async def test_delete_user(users: Users, client: AsyncClient) -> None:
    url = '/users/{}'

    # ok - delete a user account
    resp = await client.delete(url.format(users[0].id))
    assert resp.status_code == 204
    resp = await client.get(url.format(users[0].id))
    assert resp.status_code == 404

    # tries to delete inexistent user
    resp = await client.delete(url.format(users[0].id))
    assert resp.status_code == 204


async def test_create_user(client: AsyncClient) -> None:
    from faker import Faker

    fake = Faker()
    Faker.seed(0)
    user = UserInsert(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(20),
    )
    resp = await client.post('/users', content=user.json())
    assert resp.status_code == 201
    assert isinstance(resp.json()['id'], int)
