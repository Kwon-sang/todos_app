import pytest

from httpx import AsyncClient


@pytest.mark.anyio
async def test_user_create(client: AsyncClient):
    """
    유저 생성 테스트 입니다.
    성공시 HTTP status code 201 create 가 반환되어야 합니다.
    """
    # Given
    user_create_request_body = {
        "email": "test@google.com",
        "username": "testuser",
        "password": "1234",
        "first_name": "test",
        "last_name": "user"
    }
    # When
    response = await client.post(url="/users", json=user_create_request_body)
    # Then
    assert response.status_code == 201


@pytest.mark.anyio
async def test_user_create_miss_required_filed(client: AsyncClient):
    """
    유저 생성 테스트 입니다.
    Body 데이터 중 필수 필드 누락이 존재할 경우, HTTP status code 422 Unprocessable entity 가 발생해야 합니다.
    """
    # Given
    user_create_request_body = {
        "email": "test@google.com",
        "username": "testuser",
        "password": "1234",
        "first_name": "test",
        "last_name": "user"
    }
    for key in user_create_request_body.keys():
        # When
        test_body = user_create_request_body.copy().pop(key)
        response = await client.post(url="/users", json=test_body)
        # Then
        assert response.status_code == 422


@pytest.mark.anyio
async def test_retrieve_user_info(client: AsyncClient, create_user: dict, issue_token: dict):
    """
    유저 정보 조회 테스트 입니다.
    해당 엔드포인트는 현재 접속한 유저의 id로 제한됩니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    성공시 HTTP status code 200 OK 를 반환합니다.
    성공 시 반환되는 Response body data는 유저 데이터의 부분집합입니다.
    """
    # Given
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.get(url="/users/1", headers=header)
    # Then
    assert response.status_code == 200
    assert response.json().items() <= create_user.items()


@pytest.mark.anyio
async def test_retrieve_user_info_not_authority(client: AsyncClient, create_user: dict, issue_token: dict):
    """
    유저 정보 조회 실패 테스트 입니다.
    JWT Token 정보가 없을 경우, HTTP status code 401 Unauthorized 가 발생합니다.
    """
    # When
    response = await client.get(url=f"/users/1")
    # Then
    assert response.status_code == 401


@pytest.mark.anyio
async def test_retrieve_user_info_not_authority(client: AsyncClient, create_user: dict, issue_token: dict):
    """
    유저 정보 조회 실패 테스트 입니다.
    자신 이외 타인의 유저 정보를 조회할 시 HTTP 403 forbidden이 발생합니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    """
    # Given
    target_user_id = 2
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.get(url=f"/users/{target_user_id}", headers=header)
    # Then
    assert response.status_code == 403


@pytest.mark.anyio
async def test_change_password(client: AsyncClient, create_user: dict, issue_token: dict):
    """
    유저 비밀 번호 변경 테스트 입니다.
    해당 엔드포인트는 JWT 토큰 인증을 통해 보호됩니다.
    비밀 번호 변경 성공시 HTTP status code 204 No content 발생합니다.
    """
    # Given
    user_chanege_password_request_body = {
        "password": "1234",
        "new_password1": "4321",
        "new_password2": "4321"
    }
    header = {
        "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
    }
    # When
    response = await client.patch(url="/users/1/password",
                                  json=user_chanege_password_request_body,
                                  headers=header)
    # Then
    assert response.status_code == 204
