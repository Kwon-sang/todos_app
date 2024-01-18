import pytest
from httpx import AsyncClient

from src.auth.service import bcrypt_context


@pytest.mark.anyio
async def test_user_password_hashing_ok(client: AsyncClient):
    """
        유저 정보를 DB에 저장하고,
        DB에 저장된 유저의 패스워드가 암호화 되었는지를 테스트 합니다.
    """
    # Given
    create_user_body = {
        "email": "testuser@email.com",
        "username": "testuser",
        "password": "1234",            # Testing Target
        "first_name": "test",
        "last_name": "user",
    }
    # When
    response = await client.post(url="/auth", json=create_user_body)
    # Then
    result = response.json().get('hashed_password')
    assert response.status_code == 201
    assert bcrypt_context.verify(create_user_body["password"], result)