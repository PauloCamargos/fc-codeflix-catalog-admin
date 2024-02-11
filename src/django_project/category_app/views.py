from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from core.category.application.list_categories import ListCategories, ListCategoryInput
from django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryInput()
        use_case = ListCategories(repository=DjangoORMCategoryRepository())

        output = use_case.execute(input=input)

        serialized_categories = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }
            for category in output.data
        ]

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_categories,
        )
