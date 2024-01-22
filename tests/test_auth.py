import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_token(client: AsyncClient, create_user):
    """
    올바른 유저 정보를 바탕으로 토큰 생성 테스트 합니다.
    테스트 성공시, HTTP status code 200 OK 를 반환하며, HTTP body에는 access token token type 정보가 담겨 있어야 합니다..
    """
    # Given
    data = {
        "username": "testuser",
        "password": "1234"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # When
    response = await client.post("/auth", data=data, headers=headers)
    # Then
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_create_token_non_exist_user(client: AsyncClient, create_user):
    """
    Form 입력 유저의 정보가 DB에 존재하지 않을 경우, 토큰 생성 테스트는 실패합니다.
    이 경우, HTTP status code 404 Not found 를 반환합니다.
    """
    # Given
    data = {
        "username": "NoneExistUser",
        "password": "1234"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # When
    response = await client.post("/auth", data=data, headers=headers)
    # Then
    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_token_invalid_user_password(client: AsyncClient, create_user):
    """
    Form 입력 유저의 패스워드 정보가 올바르지 않을 경우, 토큰 생성 테스트는 실패합니다.
    이 경우, HTTP status code 401 Unauthorized 를 반환합니다.
    """
    # Given
    data = {
        "username": "testuser",
        "password": "wrong"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # When
    response = await client.post("/auth", data=data, headers=headers)
    # Then
    assert response.status_code == 401



# @pytest.mark.anyio
# async def test_user_password_hashing_ok(client: AsyncClient):
#     """
#         유저 정보를 DB에 저장하고,
#         DB에 저장된 유저의 패스워드가 암호화 되었는지를 테스트 합니다.
#     """
#     # Given
#     create_user_body = {
#         "email": "testuser@email.com",
#         "username": "testuser",
#         "password": "1234",            # Testing Target
#         "first_name": "test",
#         "last_name": "user",
#     }
#     # When
#     response = await client.post(url="/auth", json=create_user_body)
#     # Then
#     result = response.json().get('hashed_password')
#     assert response.status_code == 201
#     assert bcrypt_context.verify(create_user_body["password"], result)