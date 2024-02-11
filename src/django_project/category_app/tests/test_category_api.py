from rest_framework.test import APITestCase
from rest_framework import status


class TestCactegoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": "1",
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            },
            {
                "id": "2",
                "name": "Serie",
                "description": "Serie description",
                "is_active": False,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
