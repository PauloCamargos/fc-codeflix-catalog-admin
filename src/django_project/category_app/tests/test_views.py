from typing import Any
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.application.list_categories import DEFAULT_CATEGORY_LIST_ORDER
from src.core.category.domain.category import Category
from src.core.shared import settings as core_settings
from src.django_project.category_app.fixtures.factory import (
    make_category,
    movie_category,
    serie_category,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository


# @pytest.fixture
# def movie_category() -> Category:
#     return Category(
#         name="Movie",
#         description="Movie description",
#         is_active=False,
#     )


# @pytest.fixture
# def serie_category() -> Category:
#     return Category(
#         name="Serie",
#         description="Serie description",
#         is_active=False,
#     )


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
        movie_category: Category,
        serie_category: Category,
    ):
        expected_categories: list[dict[str, Any]] = [
            {
                "id": str(movie_category.id),
                "name": movie_category.name,
                "description": movie_category.description,
                "is_active": movie_category.is_active,
            },
            {
                "id": str(serie_category.id),
                "name": serie_category.name,
                "description": serie_category.description,
                "is_active": serie_category.is_active,
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

    @pytest.mark.parametrize(
        "page",
        [1, 2, 3],
    )
    def test_list_categories_with_pagination(
        self,
        page: int,
        make_category,
    ):
        movie_category = make_category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        serie_category = make_category(
            name="Serie",
            description="Serie description",
            is_active=True,
        )

        documentary_category = make_category(
            name="Documentary",
            description="Documentary category",
            is_active=True,
        )

        music_category = make_category(
            name="Music clip",
            description="Music clip category",
            is_active=True,
        )

        lecture_category = make_category(
            name="Lecture",
            description="Lecture category",
            is_active=True,
        )

        expected_categories_per_page: dict[dict[str, Any]] = {
            1: [
                    {
                        "id": str(serie_category.id),
                        "name": serie_category.name,
                        "description": serie_category.description,
                        "is_active": serie_category.is_active,
                    },
                    {
                        "id": str(music_category.id),
                        "name": music_category.name,
                        "description": music_category.description,
                        "is_active": music_category.is_active,
                    },
            ],
            2: [
                    {
                        "id": str(movie_category.id),
                        "name": movie_category.name,
                        "description": movie_category.description,
                        "is_active": movie_category.is_active,
                    },
                    {
                        "id": str(lecture_category.id),
                        "name": lecture_category.name,
                        "description": lecture_category.description,
                        "is_active": lecture_category.is_active,
                    },
            ],
            3: [
                    {
                        "id": str(documentary_category.id),
                        "name": documentary_category.name,
                        "description": documentary_category.description,
                        "is_active": documentary_category.is_active,
                    },
            ],
        }

        params = {
            "order_by": "-description",
            "page": page,
        }

        expected_data = {
            "data": expected_categories_per_page[page]
        }

        overriden_page_size = 2

        url = "/api/categories/"
        with patch.dict(
            core_settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
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
        movie_category: Category,
    ):
        expected_data = {
            "data": {
                "id": str(movie_category.id),
                "name": movie_category.name,
                "description": movie_category.description,
                "is_active": movie_category.is_active,
            }
        }

        url = f"/api/categories/{movie_category.id}/"
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
        assert category_repository.count() == 0

    def test_create_category_valid_payload_success(
        self,
        serie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):

        post_data = {
            "name": "New category",
            "description": "New category description",
            "is_active": True,
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

        assert category_repository.count() == 2


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_category_invalid_payload_error(
        self,
        movie_category: Category,
    ):
        post_data = {
            "name": "",
            "description": movie_category.description,
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_update_category_invalid_id_error(
        self,
        movie_category: Category,
    ):
        post_data = {
            "name": movie_category.name,
            "description": movie_category.description,
            "is_active": not movie_category.is_active,
        }

        url = "/api/categories/invalid-id/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }

    def test_update_category_non_existing_category_error(
        self,
        movie_category: Category,
    ):
        post_data = {
            "name": movie_category.name,
            "description": movie_category.description,
            "is_active": not movie_category.is_active,
        }

        url = f"/api/categories/{str(uuid4())}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_category_valid_payload_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        post_data = {
            "name": "Film",
            "description": "Film category",
            "is_active": not movie_category.is_active,
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(movie_category.id)

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
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        post_data = {
            "name": "",
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
        }

    def test_partial_update_category_invalid_id_error(
        self,
        movie_category: Category,
    ):
        post_data = {
            "name": movie_category.name,
            "description": movie_category.description,
            "is_active": not movie_category.is_active,
        }

        url = "/api/categories/invalid-id/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }

    def test_partial_update_category_non_existing_category_error(
        self,
    ):
        post_data = {
            "description": "Film description",
        }

        url = f"/api/categories/{str(uuid4())}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_category_name_valid_payload_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        post_data = {
            "name": "Film"
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(movie_category.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == post_data["name"]
        assert updated_category_movie.description == movie_category.description
        assert updated_category_movie.is_active == movie_category.is_active

    def test_partial_update_category_description_valid_payload_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        post_data = {
            "description": "Film description"
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(movie_category.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == movie_category.name
        assert updated_category_movie.description == post_data["description"]
        assert updated_category_movie.is_active == movie_category.is_active

    def test_partial_update_category_is_active_valid_payload_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        post_data = {
            "is_active": not movie_category.is_active,
        }

        url = f"/api/categories/{str(movie_category.id)}/"
        response = APIClient().patch(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert response.data["id"] == str(movie_category.id)

        updated_category_movie = category_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_category_movie is not None

        assert updated_category_movie.name == movie_category.name
        assert updated_category_movie.description == movie_category.description
        assert updated_category_movie.is_active == post_data["is_active"]


@pytest.mark.django_db
class TestDeleteCategory:
    def test_delete_category_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        url = f"/api/categories/{movie_category.id}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        found_category = category_repository.get_by_id(id=movie_category.id)
        assert found_category is None

    def test_delete_category_non_existing_id_error(
        self,
    ):
        url = f"/api/categories/{uuid4()}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_category_non_invalid_id_error(
        self,
    ):
        url = "/api/categories/invalid-id/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
