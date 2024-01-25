import pytest

from httpx import AsyncClient


# @pytest.mark.anyio
# async def test_check_user_role(client: AsyncClient, create_user, issue_token: dict):
#     """
#     Admin 엔드포인트는 유저의 Role이 admin 이어야 합니다.
#     """
#     # Given
#     header = {
#         "Authorization": f"{issue_token['token_type']} {issue_token['access_token']}"
#     }
#     await client.patch(url="/admin/users/1/role", json={"role": "admin"}, headers=header)
#     # When
#     response1 = await client.get(url="/admin/users", headers=header)
#     response2 = await client.get(url="/admin/todos", headers=header)
#     # Then
#     assert response1.status_code == 200
#     assert response2.status_code == 200
