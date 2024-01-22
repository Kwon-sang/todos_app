import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_todo(client: AsyncClient, issue_token: dict):
    """
    새 Todos 생성 테스트 입니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
    # Given
    request_body = {
        'title': 'Test Todo',
        'description': 'Test Description',
        'priority': 1,
        'complete': False,
        'owner_id': 1}
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.post(url="/todos", json=request_body, headers=header)
    expected = {'id': 1, **request_body}
    # Then
    assert response.status_code == 201
    assert response.json() == expected


@pytest.mark.anyio
async def test_retrieve_todo_all(client: AsyncClient, create_todo: dict, issue_token: dict):
    """
    생성된 모든 Todos 리스트를 조회 합니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
    # Given
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.get(url="/todos", headers=header)
    # Then
    assert response.status_code == 200
    assert response.json() == [create_todo]


@pytest.mark.anyio
async def test_retrieve_todo(client: AsyncClient, create_todo: dict, issue_token: dict):
    """
    하나의 Todos 데이터를 조회 합니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
    # Given
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.get(url="/todos/1", headers=header)
    # Then
    assert response.status_code == 200
    assert response.json() == create_todo


@pytest.mark.anyio
async def test_retrieve_todo_not_found(client: AsyncClient, create_todo: dict, issue_token: dict):
    """
    하나의 Todos 데이터를 조회 합니다.
    todo_id 에 대한 리소스가 존재하지 않을 경우 HTTP status code 404 Not found가 반환되어야 합니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
    # Given
    not_exist_todo_id = 2
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.get(url=f"/todos/{not_exist_todo_id}", headers=header)
    # Then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_todo_partial(client: AsyncClient, create_todo: dict, issue_token: dict):
    """
    업데이트 테스트 입니다.
    데이터의 모든 정보를 변경가능하며, 부분 업데이트 또한 가능해야 합니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
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
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    for body in test_bodies:
        # When
        response = await client.put(url="/todos/1", json=body, headers=header)
        # Then
        assert response.status_code == 204


@pytest.mark.anyio
async def test_delete_todo(client: AsyncClient, create_todo: dict, issue_token: dict):
    # Given
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.delete(url="/todos/1", headers=header)
    # Then
    assert response.status_code == 204
