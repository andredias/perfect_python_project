from httpx import AsyncClient


async def test_hello(client: AsyncClient) -> None:
    response = await client.get("/fragment/hello")
    assert response.status_code == 200
    assert response.text == "<h1>Hello World!</h1>"
