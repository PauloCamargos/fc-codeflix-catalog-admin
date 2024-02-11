import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestCactegoryAPI:
    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Movie",
            description="Movie description",
            is_active=False,
        )

    @pytest.fixture
    def category_serie(self) -> Category:
        return Category(
            name="Serie",
            description="Serie description",
            is_active=False,
        )

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_list_categories(
        self,
        category_movie: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository,
    ):
        category_repository.save(category_movie)
        category_repository.save(category_serie)

        expected_data = [
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

        url = "/api/categories/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data
