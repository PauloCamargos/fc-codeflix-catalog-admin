from django.http import QueryDict
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.category.application.create_category import (
    CreateCategory,
    CreateCategoryInput,
)
from src.core.category.application.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from src.core.category.application.errors import CategoryNotFound, InvalidCategoryData
from src.core.category.application.get_category import GetCategory, GetCategoryInput
from src.core.category.application.list_categories import ListCategories
from src.core.category.application.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
    UpdateCategoryResponseSerializer,
)
from src.django_project.shared.views import mixins


class CategoryViewSet(viewsets.ViewSet, mixins.OrderedPaginatedListMixin):
    repository_class = DjangoORMCategoryRepository

    list_use_case_class = ListCategories
    serializer_class = ListCategoryResponseSerializer

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer_input = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer_input.is_valid(raise_exception=True)

        input = GetCategoryInput(id=serializer_input.validated_data["id"])
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_output = RetrieveCategoryResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_output.data,
        )

    def create(self, request: Request) -> Response:
        serializer_input = CreateCategoryRequestSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)

        input = CreateCategoryInput(**serializer_input.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input=input)
        except InvalidCategoryData:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialized_output = CreateCategoryResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized_output.data,
        )

    def update(self, request: Request, pk=None) -> Response:
        if isinstance(request.data, QueryDict):
            data = request.data.dict()
        elif isinstance(request.data, dict):
            data = request.data
        else:
            data = request.data

        serializer_input = UpdateCategoryRequestSerializer(
            data={
                **data,
                "id": pk,
            },
        )
        serializer_input.is_valid(raise_exception=True)

        input = UpdateCategoryInput(**serializer_input.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_output = UpdateCategoryResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=serialized_output.data,
        )

    def partial_update(self, request: Request, pk=None) -> Response:
        if isinstance(request.data, QueryDict):
            data = request.data.dict()
        elif isinstance(request.data, dict):
            data = request.data
        else:
            data = request.data

        serializer_input = UpdateCategoryRequestSerializer(
            data={
                **data,
                "id": pk,
            },
            partial=True,
        )
        serializer_input.is_valid(raise_exception=True)

        input = UpdateCategoryInput(**serializer_input.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serialized_output = UpdateCategoryResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=serialized_output.data,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        serializer_input = DeleteCategoryRequestSerializer(data={"id": pk})
        serializer_input.is_valid(raise_exception=True)

        input = DeleteCategoryInput(**serializer_input.validated_data)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())

        try:
            use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
