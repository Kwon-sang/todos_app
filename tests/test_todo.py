import pytest

from httpx import AsyncClient


async def create_todo(client: AsyncClient) -> dict:
    request_body = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': None}
    response = await client.post(url="/todos", json=request_body)
    return response.json()


@pytest.mark.anyio
async def test_create_todo(client: AsyncClient):
    # Given
    request_body = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': None}
    # When
    response = await client.post(url="/todos", json=request_body)
    expected = {'id': 1, **request_body}
    # Then
    assert response.status_code == 201
    assert response.json() == expected


@pytest.mark.anyio
async def test_read_todo_all(client: AsyncClient):
    # Given
    created_todo = await create_todo(client)
    # When
    response = await client.get(url="/todos")
    print(response.json())
    # Then
    assert response.status_code == 200
    assert response.json() == [created_todo]


@pytest.mark.anyio
async def test_read_todo(client: AsyncClient):
    # Given
    created_todo = await create_todo(client)
    # When
    response = await client.get(url="/todos/1")
    # Then
    assert response.status_code == 200
    assert response.json() == created_todo


@pytest.mark.anyio
async def test_read_todo_not_found(client: AsyncClient):
    # When
    response = await client.get(url="/todos/1")
    # Then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_todo_partial(client: AsyncClient):
    # Given
    test_bodies = [
        {
            "title": "Changed Title",
            "description": "Changed Description",
            "priority": 3,
            "complete": False
        },
        {"title": "Changed Title"},
        {"description": "Changed Description"},
        {"priority": 3},
        {"complete": True}
    ]
    for body in test_bodies:
        await create_todo(client)
        # When
        response = await client.put(url="/todos/1", json=body)
        # Then
        assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_todo(client: AsyncClient):
    # Given
    await create_todo(client)
    # When
    response = await client.delete(url="/todos/1")
    # Then
    assert response.status_code == 204
