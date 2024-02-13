from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository

BASE_GENRE_URL = "/api/genres/"


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Category")


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def presisted_romance_genre_with_categories(
    movie_category: Category,
    documentary_category: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_repository: DjangoORMGenreRepository,
) -> Genre:
    category_repository.save(category=movie_category)
    category_repository.save(category=documentary_category)

    romance_genre = Genre(
        name="Romance",
        categories={
            movie_category.id,
            documentary_category.id,
        },
    )

    genre_repository.save(genre=romance_genre)

    return romance_genre


@pytest.fixture
def persisted_drama_genre_without_categories(
    genre_repository: DjangoORMGenreRepository,
) -> Genre:
    drama_genre = Genre(name="Drama")
    genre_repository.save(genre=drama_genre)
    return drama_genre


@pytest.mark.django_db
class TestListAPI:
    def test_list_genres_and_categories_success(
        self,
        presisted_romance_genre_with_categories: Genre,
        persisted_drama_genre_without_categories: Genre,
    ):

        expected_data = {
            "data": [
                {
                    "id": str(presisted_romance_genre_with_categories.id),
                    "name": presisted_romance_genre_with_categories.name,
                    "is_active": presisted_romance_genre_with_categories.is_active,
                    "categories": [
                        str(category_id)
                        for category_id in (
                            presisted_romance_genre_with_categories.categories
                        )
                    ],
                },
                {
                    "id": str(persisted_drama_genre_without_categories.id),
                    "name": persisted_drama_genre_without_categories.name,
                    "is_active": persisted_drama_genre_without_categories.is_active,
                    "categories": [],
                }
            ]
        }

        response = APIClient().get(path=BASE_GENRE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_no_list_genres_and_categories(
        self,
    ):
        expected_data = {"data": []}

        response = APIClient().get(path=BASE_GENRE_URL)

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
        assert created_genre.categories == {movie_category.id}

    def test_create_genre_without_categories_success(
        self,
        category_repository: DjangoORMCategoryRepository,
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
        assert created_genre.categories == set()

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
