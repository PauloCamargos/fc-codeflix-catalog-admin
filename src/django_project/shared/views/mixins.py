
from typing import Any
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.shared.application.list import PaginatedListUseCase
from src.django_project.shared.repository.mapper import ListableRepository
from src.django_project.shared.serializers.serializers import (
    PaginatedListResponseSerializer,
)

CLASS_ATTRIBUTE_NOT_FOUND_ERROR_MESSAGE_TEMPLATE = (
    "Cannot find '{attribute_name}'. "
    "Either implement a '.get_{attribute_name}(self)' method or "
    "add '{attribute_name}' class variable to '{class_name}'"
)


class OrderedPaginatedListMixin:
    order_by_query_pagam = "order_by"
    page_query_param = "page"

    def list(self, request: Request) -> Response:
        input_params = self.get_input_params_dict(request=request)

        use_case_cls = self.get_list_use_case_class()

        output = (
            use_case_cls(
                repository=self.get_repository_class()(),
            )
            .execute(
                input=use_case_cls.Input(**input_params),
            )
        )

        serializer_cls = self.get_list_serializer_cls()
        serialized_categories = serializer_cls(instance=output)

        return Response(
            status=status.HTTP_200_OK,
            data=serialized_categories.data,
        )

    def get_order_by(self, request: Request) -> Any:
        return request.query_params.get(self.order_by_query_pagam, None)

    def get_page_number(self, request: Request) -> Any:
        return request.query_params.get(self.page_query_param, None)

    def get_input_params_dict(self, request: Request) -> dict[str, Any]:
        input_params = {}

        order_by = self.get_order_by(request=request)
        page_number = self.get_page_number(request=request)

        if order_by is not None:
            input_params["order_by"] = order_by

        if page_number is not None:
            input_params["page"] = page_number

        return input_params

    def get_list_use_case_class(self) -> type[PaginatedListUseCase]:
        list_use_case_class = getattr(
            self, "list_use_case_class", None
        )
        assert list_use_case_class is not None, (
            CLASS_ATTRIBUTE_NOT_FOUND_ERROR_MESSAGE_TEMPLATE.format(
                attribute_name="list_use_case_class",
                class_name=self.__class__.__qualname__,
            )
        )
        return list_use_case_class

    def get_repository_class(self) -> type[ListableRepository]:
        repository_class = getattr(self, "repository_class", None)
        assert repository_class is not None, (
            CLASS_ATTRIBUTE_NOT_FOUND_ERROR_MESSAGE_TEMPLATE.format(
                attribute_name="repository_class",
                class_name=self.__class__.__qualname__,
            )
        )
        return repository_class

    def get_list_serializer_cls(self) -> type[PaginatedListResponseSerializer]:
        serializer_class = getattr(self, "serializer_class", None)
        assert serializer_class is not None, (
            CLASS_ATTRIBUTE_NOT_FOUND_ERROR_MESSAGE_TEMPLATE.format(
                attribute_name="serializer_class",
                class_name=self.__class__.__qualname__,
            )
        )
        return serializer_class
