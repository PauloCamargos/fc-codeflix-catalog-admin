from typing import Any
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.shared import settings as core_settings
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.genre_app.repository import (
    DEFAULT_GENRE_LIST_ORDER,
    DjangoORMGenreRepository,
)

BASE_GENRE_URL = "/api/genres/"


@pytest.mark.django_db
class TestListAPI:
    @pytest.mark.parametrize(
        "order_by",
        [None, "name", "-name"]
    )
    def test_list_genres_and_categories_success(
        self,
        order_by: str,
        romance_genre_model_with_categories: GenreModel,
        drama_genre_model_without_categories: GenreModel,
    ):
        expected_genres: list[dict[str, Any]] = [
            {
                "id": str(drama_genre_model_without_categories.id),
                "name": drama_genre_model_without_categories.name,
                "is_active": drama_genre_model_without_categories.is_active,
                "categories": [],
            },
            {
                "id": str(romance_genre_model_with_categories.id),
                "name": romance_genre_model_with_categories.name,
                "is_active": romance_genre_model_with_categories.is_active,
                "categories": [
                    str(category.id)
                    for category in (
                        romance_genre_model_with_categories.categories
                        .order_by("name")
                    )
                ],
            },
        ]

        if order_by is None:
            order_by = DEFAULT_GENRE_LIST_ORDER
            params = {}
        else:
            params = {
                "order_by": order_by,
            }

        expected_data = {
            "data": sorted(
                expected_genres,
                key=lambda item: item[order_by.strip("-")],
                reverse=order_by.startswith("-"),
            ),
            "meta": {
                "page": 1,
                "total": 2,
                "per_page": core_settings.REPOSITORY["page_size"],
            }
        }

        response = APIClient().get(BASE_GENRE_URL, params)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_empty_list_genres_and_categories(
        self,
    ):
        expected_data = {
            "data": [],
            "meta": {
                "page": 1,
                "total": 0,
                "per_page": core_settings.REPOSITORY["page_size"],
            },
        }

        response = APIClient().get(path=BASE_GENRE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    @pytest.mark.parametrize(
        "page",
        [1, 2, 3],
    )
    def test_list_genres_with_pagination(
        self,
        page: int,
        romance_genre_model_with_categories: GenreModel,
        drama_genre_model_without_categories: GenreModel,
        horror_genre_model_without_categories: GenreModel,
        scifi_genre_model_without_categories: GenreModel,
        action_genre_model_without_categories: GenreModel,
    ):
        expected_genres_per_page: dict[int, list[Any]] = {
            1: [
                    {
                        "id": str(scifi_genre_model_without_categories.id),
                        "name": scifi_genre_model_without_categories.name,
                        "is_active": scifi_genre_model_without_categories.is_active,
                        "categories": [],
                    },
                    {
                        "id": str(romance_genre_model_with_categories.id),
                        "name": romance_genre_model_with_categories.name,
                        "is_active": romance_genre_model_with_categories.is_active,
                        "categories": [
                            str(category.id)
                            for category in (
                                romance_genre_model_with_categories.categories
                                .order_by("name")
                            )
                        ],
                    },
            ],
            2: [
                    {
                        "id": str(horror_genre_model_without_categories.id),
                        "name": horror_genre_model_without_categories.name,
                        "is_active": horror_genre_model_without_categories.is_active,
                        "categories": [],
                    },
                    {
                        "id": str(drama_genre_model_without_categories.id),
                        "name": drama_genre_model_without_categories.name,
                        "is_active": drama_genre_model_without_categories.is_active,
                        "categories": [],
                    },
            ],
            3: [
                    {
                        "id": str(action_genre_model_without_categories.id),
                        "name": action_genre_model_without_categories.name,
                        "is_active": action_genre_model_without_categories.is_active,
                        "categories": [],
                    },
            ],
        }

        params = {
            "order_by": "-name",
            "page": page,
        }

        overriden_page_size = 2

        expected_data = {
            "data": expected_genres_per_page[page],
            "meta": {
                "page": page,
                "total": 5,
                "per_page": overriden_page_size,
            },
        }

        url = "/api/genres/"
        with patch.dict(
            core_settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
            response = APIClient().get(url, params)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_genre_with_categories_success(
        self,
        movie_category: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ):
        category_repository.save(category=movie_category)

        post_data = {
            "name": "Horror",
            "is_active": True,
            "categories": [str(movie_category.id)],
        }

        response = APIClient().post(
            path=BASE_GENRE_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_genre_id = UUID(response.data["id"])

        created_genre = genre_repository.get_by_id(id=created_genre_id)

        assert created_genre is not None

        assert created_genre.name == post_data["name"]
        assert created_genre.is_active == post_data["is_active"]
        assert created_genre.categories == [movie_category.id]

    def test_create_genre_without_categories_success(
        self,
        genre_repository: DjangoORMGenreRepository,
    ):

        post_data = {
            "name": "Horror",
            "is_active": True,
        }

        response = APIClient().post(
            path=BASE_GENRE_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_genre_id = UUID(response.data["id"])

        created_genre = genre_repository.get_by_id(id=created_genre_id)

        assert created_genre is not None

        assert created_genre.name == post_data["name"]
        assert created_genre.is_active == post_data["is_active"]
        assert created_genre.categories == list()

    def test_create_genre_invalid_data_error(
        self,
    ):
        post_data = {
            "name": "",
            "is_active": True,
        }

        response = APIClient().post(
            path=BASE_GENRE_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_genre_category_does_not_exist_error(
        self,
    ):
        inexisting_category_ids = {uuid4()}

        post_data = {
            "name": "Horror",
            "is_active": True,
            "categories": [str(id) for id in inexisting_category_ids],
        }

        response = APIClient().post(
            path=BASE_GENRE_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": f"Categories not found: {inexisting_category_ids}"
        }


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_genre_invalid_payload_error(
        self,
        drama_genre_model_without_categories: GenreModel,
    ):
        post_data = {
            "name": "",
        }

        url = BASE_GENRE_URL + f"{str(drama_genre_model_without_categories.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
            "categories": ["This field is required."],
        }

    def test_update_category_invalid_id_error(
        self,
        drama_genre_model_without_categories: GenreModel,
    ):
        post_data = {
            "name": drama_genre_model_without_categories.name,
            "is_active": not drama_genre_model_without_categories.is_active,
        }

        url = BASE_GENRE_URL + "invalid-id/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "categories": ["This field is required."]
        }

    def test_update_non_existing_genre_error(
        self,
    ):
        post_data = {
            "name": "foo",
            "is_active": False,
            "categories": [],
        }

        url = BASE_GENRE_URL + f"/{str(uuid4())}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_genre_non_existing_categories_error(
        self,
        drama_genre_model_without_categories: GenreModel,
    ):
        inexisting_category_ids = {uuid4()}
        post_data = {
            "name": drama_genre_model_without_categories.name,
            "is_active": drama_genre_model_without_categories.is_active,
            "categories": [str(id) for id in inexisting_category_ids],
        }

        url = BASE_GENRE_URL + f"{str(drama_genre_model_without_categories.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": f"Categories not found: {inexisting_category_ids}"
        }

    def test_update_genre_valid_payload_success(
        self,
        drama_genre_model_without_categories: GenreModel,
        genre_repository: DjangoORMGenreRepository,
        category_repository: DjangoORMCategoryRepository,
    ):
        serie_category = Category(name="Serie")
        category_repository.save(category=serie_category)

        post_data = {
            "name": "New Drama",
            "is_active": not drama_genre_model_without_categories.is_active,
            "categories": [str(serie_category.id)]
        }

        url = BASE_GENRE_URL + f"{str(drama_genre_model_without_categories.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["id"] == str(drama_genre_model_without_categories.id)

        updated_genre = genre_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_genre is not None

        assert updated_genre.name == post_data["name"]
        assert updated_genre.is_active == post_data["is_active"]
        assert updated_genre.categories == [serie_category.id]


@pytest.mark.django_db
class TestDeleteGenre:
    def test_delete_genre_success(
        self,
        romance_genre_model_with_categories: GenreModel,
        genre_repository: DjangoORMGenreRepository,
    ):
        url = BASE_GENRE_URL + f"{str(romance_genre_model_with_categories.id)}/"
        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        found_genre = genre_repository.get_by_id(
            id=romance_genre_model_with_categories.id
        )
        assert found_genre is None

    def test_delete_genre_non_existing_id_error(
        self,
    ):
        url = f"/api/categories/{str(uuid4())}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_genre_non_invalid_id_error(
        self,
    ):
        url = "/api/categories/invalid-id/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
