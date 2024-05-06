import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.shared import settings

BASE_CAST_MEMBERS_URL = "/api/cast_members/"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditDeleteCastMember:
    def test_user_can_create_and_edit_cast_member(self, api_client: APIClient) -> None:
        list_response = api_client.get(BASE_CAST_MEMBERS_URL)
        assert list_response.data == {
            "data": [],
            "meta": {
                "page": 1,
                "total": 0,
                "per_page": settings.REPOSITORY["page_size"],
            },
        }

        create_response = api_client.post(
            BASE_CAST_MEMBERS_URL,
            {
                "name": "John Doe",
                "type": "ACTOR",
            },
        )
        assert create_response.status_code == 201
        created_cast_member_id = create_response.data["id"]

        assert api_client.get(BASE_CAST_MEMBERS_URL).data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "John Doe",
                    "type": "ACTOR",
                }
            ],
            "meta": {
                "page": 1,
                "total": 1,
                "per_page": settings.REPOSITORY["page_size"],
            },
        }

        edit_response = api_client.put(
            f"{BASE_CAST_MEMBERS_URL}{created_cast_member_id}/",
            {
                "name": "Jonathan Doe",
                "type": "DIRECTOR",
            },
        )
        assert edit_response.status_code == 204

        api_client.get(BASE_CAST_MEMBERS_URL).data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Jonathan Doe",
                    "type": "DIRECTOR",
                },
            ]
        }

        api_client.delete(f"{BASE_CAST_MEMBERS_URL}{created_cast_member_id}/")
        api_client.get(BASE_CAST_MEMBERS_URL).status_code == status.HTTP_404_NOT_FOUND
