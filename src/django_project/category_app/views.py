from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from core.category.application.errors import CategoryNotFound
from core.category.application.get_category import GetCategory, GetCategoryInput
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

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            category_pk = UUID(pk)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        input = GetCategoryInput(id=category_pk)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_data = {
            "id": str(output.id),
            "name": output.name,
            "description": output.description,
            "is_active": output.is_active,
        }

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_data,
        )
