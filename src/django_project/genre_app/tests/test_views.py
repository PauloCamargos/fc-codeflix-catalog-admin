import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


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
    @classmethod
    def setup_method(self):
        self.client = APIClient()
        self.list_base_url = "/api/genres/"

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

        response = self.client.get(path=self.list_base_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_no_list_genres_and_categories(
        self,
    ):
        expected_data = {"data": []}

        response = self.client.get(path=self.list_base_url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data
