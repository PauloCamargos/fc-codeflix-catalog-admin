from rest_framework import status
from rest_framework.test import APITestCase

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


class TestCactegoryAPI(APITestCase):
    def test_list_categories(self):
        movie = Category(
            name="Movie",
            description="Movie description",
            is_active=False,
        )
        serie = Category(
            name="Serie",
            description="Serie description",
            is_active=False,
        )

        repository = DjangoORMCategoryRepository()
        repository.save(movie)
        repository.save(serie)

        expected_data = [
            {
                "id": str(movie.id),
                "name": movie.name,
                "description": movie.description,
                "is_active": movie.is_active,
            },
            {
                "id": str(serie.id),
                "name": serie.name,
                "description": serie.description,
                "is_active": serie.is_active,
            },
        ]

        url = "/api/categories/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data, expected_data)
