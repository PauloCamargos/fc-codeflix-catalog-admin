from typing import Any
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.application.list_categories import DEFAULT_CATEGORY_LIST_ORDER
from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(
        name="Movie",
        description="Movie description",
        is_active=False,
    )


@pytest.fixture
def category_serie() -> Category:
    return Category(
        name="Serie",
        description="Serie description",
        is_active=False,
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListCategoryAPI:
    @pytest.mark.parametrize(
        "order_by",
        [None, "name", "-name", "description", "-description"]
    )
    def test_list_categories(
        self,
        order_by: str,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_serie)

        expected_categories: list[dict[str, Any]] = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            },
            {
                "id": str(category_serie.id),
                "name": category_serie.name,
                "description": category_serie.description,
                "is_active": category_serie.is_active,
            },
        ]

        if order_by is None:
            order_by = DEFAULT_CATEGORY_LIST_ORDER
            params = {}
        else:
            params = {
                "order_by": order_by,
            }

        expected_data = {
            "data": sorted(
                expected_categories,
                key=lambda item: item[order_by.strip("-")],
                reverse=order_by.startswith("-"),
            )
        }

        url = "/api/categories/"
        response = APIClient().get(url, params)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_get_category_when_on_invalid_id(self):
        url = "/api/categories/some-invalid-id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_category_when_exists(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_serie)

        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        }

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_get_category_when_does_not_exists(self):
        does_not_exist_id = str(uuid4())
        url = f"/api/categories/{does_not_exist_id}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_category_invalid_payload_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = "/api/categories/"
        response = APIClient().post(
            path=url,
            data={
                "name": "",
                "description": "Some description",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_category_valid_payload_success(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):

        post_data = {
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": category_movie.is_active,
        }

        url = "/api/categories/"
        response = APIClient().post(path=url, data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

        created_category_id = response.data["id"]
        created_category = category_repository.get_by_id(
            id=UUID(created_category_id)
        )

        assert created_category is not None

        assert created_category.name == post_data["name"]
        assert created_category.description == post_data["description"]
        assert created_category.is_active == post_data["is_active"]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_category_invalid_payload_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": "",
            "description": category_movie.description,
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_update_category_invalid_id_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": not category_movie.is_active,
        }

        url = "/api/categories/invalid-id/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }

    def test_update_category_non_existing_category_error(
        self,
        category_movie: Category,
    ):
        post_data = {
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": not category_movie.is_active,
        }

        url = f"/api/categories/{str(uuid4())}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_category_valid_payload_success(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": "Film",
            "description": "Film category",
            "is_active": not category_movie.is_active,
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(category_movie.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == post_data["name"]
        assert updated_category_movie.description == post_data["description"]
        assert updated_category_movie.is_active == post_data["is_active"]


@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_partial_update_category_invalid_payload_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": "",
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }

    def test_partial_update_category_invalid_id_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": category_movie.name,
            "description": category_movie.description,
            "is_active": not category_movie.is_active,
        }

        url = "/api/categories/invalid-id/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }

    def test_partial_update_category_non_existing_category_error(
        self,
        category_movie: Category,
    ):
        post_data = {
            "description": "Film description",
        }

        url = f"/api/categories/{str(uuid4())}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_category_name_valid_payload_success(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "name": "Film"
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(category_movie.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == post_data["name"]
        assert updated_category_movie.description == category_movie.description
        assert updated_category_movie.is_active == category_movie.is_active

    def test_partial_update_category_description_valid_payload_success(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "description": "Film description"
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(category_movie.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == category_movie.name
        assert updated_category_movie.description == post_data["description"]
        assert updated_category_movie.is_active == category_movie.is_active

    def test_partial_update_category_is_active_valid_payload_success(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category=category_movie)

        post_data = {
            "is_active": not category_movie.is_active,
        }

        url = f"/api/categories/{str(category_movie.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(category_movie.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == category_movie.name
        assert updated_category_movie.description == category_movie.description
        assert updated_category_movie.is_active == post_data["is_active"]


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_category_success(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        found_category = category_repository.get_by_id(id=category_movie.id)
        assert found_category is None

    def test_delete_category_non_existing_id_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = f"/api/categories/{category_movie.id}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_non_invalid_id_error(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = "/api/categories/invalid-id/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
