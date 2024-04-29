import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.shared import settings


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditDeleteCategory:
    def test_user_can_create_and_edit_category(self, api_client: APIClient) -> None:
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
                "page": 1,
                "total": 0,
                "per_page": settings.REPOSITORY["page_size"],
            },
        }

        create_response = api_client.post(
            "/api/categories/",
            {
                "name": "Movie",
                "description": "Movie description",
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        assert api_client.get("/api/categories/").data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ],
            "meta": {
                "page": 1,
                "total": 1,
                "per_page": settings.REPOSITORY["page_size"],
            },
        }

        edit_response = api_client.put(
            f"/api/categories/{created_category_id}/",
            {
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True,
            },
        )
        assert edit_response.status_code == 204

        api_client.get("/api/categories/").data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                }
            ]
        }

        api_client.delete(f"/api/categories/{created_category_id}/")
        api_client.get("/api/categories/").status_code == status.HTTP_404_NOT_FOUND
