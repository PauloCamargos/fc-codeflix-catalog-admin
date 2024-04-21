from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.cast_member.application.create_cast_member import CreateCastMember
from src.core.cast_member.application.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.errors import (
    CastMemberNotFound,
    InvalidCastMemberData,
)
from src.core.cast_member.application.list_cast_member import ListCastMember
from src.core.cast_member.application.update_cast_member import UpdateCastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
    UpdateCastMemberResponseSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        if "order_by" in request.query_params:
            input = ListCastMember.Input(order_by=request.query_params["order_by"])
        else:
            input = ListCastMember.Input()

        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())

        output = use_case.execute(input=input)

        serialized_cast_members = ListCastMemberResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_cast_members.data,
        )

    def create(self, request: Request) -> Response:
        serializer_input = CreateCastMemberRequestSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)

        input = CreateCastMember.Input(**serializer_input.validated_data)
        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output = use_case.execute(input=input)
        except InvalidCastMemberData as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(exc)},
            )

        serialized_output = CreateCastMemberResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized_output.data,
        )

    def update(self, request: Request, pk=None) -> Response:
        serializer_input = UpdateCastMemberRequestSerializer(
            data={
                **request.data,
                "id": pk,
            },
        )
        serializer_input.is_valid(raise_exception=True)

        input = UpdateCastMember.Input(**serializer_input.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output = use_case.execute(input=input)
        except CastMemberNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except InvalidCastMemberData as exc:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(exc)},
            )

        serialized_output = UpdateCastMemberResponseSerializer(instance=output)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data=serialized_output.data,
        )

    def destroy(self, request: Request, pk=None) -> Response:
        serializer_input = DeleteCastMemberRequestSerializer(data={"id": pk})
        serializer_input.is_valid(raise_exception=True)

        input = DeleteCastMember.Input(**serializer_input.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())

        try:
            use_case.execute(input=input)
        except CastMemberNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
