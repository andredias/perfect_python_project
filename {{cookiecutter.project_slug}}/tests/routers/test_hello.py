from httpx import AsyncClient


async def test_hello(client: AsyncClient) -> None:
    response = await client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}
