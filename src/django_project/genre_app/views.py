from django.http import QueryDict
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.create_genre import CreateGenre
from src.core.genre.application.delete_genre import DeleteGenre
from src.core.genre.application.errors import (
    GenreNotFound,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.list_genres import ListGenres
from src.core.genre.application.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreRequestSerializer,
    CreateGenreResponseSerializer,
    DeleteGenreRequestSerializer,
    ListGenreResponseSerializers,
    UpdateGenreRequestSerializer,
    UpdateGenreResponseSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")

        input = ListGenres.Input(order_by=order_by)
        use_case = ListGenres(repository=DjangoORMGenreRepository())

        output = use_case.execute(input=input)

        serialized_genres = ListGenreResponseSerializers(instance=output)

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_genres.data,
        )

    def create(self, request: Request) -> Response:
        serializer_input = CreateGenreRequestSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer_input.validated_data)
        use_case = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            output = use_case.execute(input=input)
        except (InvalidGenreData, RelatedCategoriesNotFound) as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(exc)},
            )

        serialized_output = CreateGenreResponseSerializer(instance=output)

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

        serializer_input = UpdateGenreRequestSerializer(
            data={
                **data,
                "id": pk,
            },
        )
        serializer_input.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer_input.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            output = use_case.execute(input=input)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (InvalidGenreData, RelatedCategoriesNotFound) as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(exc)},
            )

        serialized_output = UpdateGenreResponseSerializer(instance=output)

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

        serializer_input = UpdateGenreRequestSerializer(
            data={
                **data,
                "id": pk,
            },
            partial=True,
        )
        serializer_input.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer_input.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )

        try:
            output = use_case.execute(input=input)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except (InvalidGenreData, RelatedCategoriesNotFound) as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(exc)},
            )

        serialized_output = UpdateGenreResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=serialized_output.data,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        serializer_input = DeleteGenreRequestSerializer(data={"id": pk})
        serializer_input.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**serializer_input.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())

        try:
            use_case.execute(input=input)
        except GenreNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
