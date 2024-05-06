from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from src.core.shared import settings as core_settings
from src.core.shared.application.errors import (
    InvalidOrderByRequested,
    InvalidPageRequested,
)
from src.core.shared.domain.entity import Entity
from src.django_project.shared.repository.mapper import ListableRepository


@dataclass(kw_only=True)
class ListInputMixin(ABC):
    order_by: str
    page: int

    def __post_init__(self) -> None:
        self.validate()

    @staticmethod
    @abstractmethod
    def get_valid_order_by_attributes() -> list[str]:
        pass

    def validate(self) -> None:
        if self.page < 1:
            raise InvalidPageRequested(
                page=self.page,
            )

        if self.order_by not in self.get_valid_order_by_attributes():
            raise InvalidOrderByRequested(
                order_by=self.order_by,
                valid_order_by_attributes=self.get_valid_order_by_attributes(),
            )


ENTITY_OUTPUT_DATA = TypeVar("ENTITY_OUTPUT_DATA")
ENTITY_OUTPUT_DATA2 = TypeVar("ENTITY_OUTPUT_DATA2")

ENTITY = TypeVar("ENTITY", bound=Entity)


class PaginatedListUseCase(ABC, Generic[ENTITY, ENTITY_OUTPUT_DATA]):
    default_order_by_field = "id"
    order_by_fields = ["id"]

    @dataclass
    class Input:
        order_by: str | None = None
        page: int | str | None = None

    @dataclass
    class Output(Generic[ENTITY_OUTPUT_DATA2]):
        data: list[ENTITY_OUTPUT_DATA2]
        meta: "PaginatedListUseCase.Meta"

    @dataclass
    class Meta:
        page: int
        per_page: int
        total: int

    def __init__(self, repository: ListableRepository):
        self.repository = repository

    def execute(
        self,
        input: Input,
    ) -> "PaginatedListUseCase.Output[ENTITY_OUTPUT_DATA]":
        page = self.get_validated_page(page=input.page)
        order_by = self.get_validated_order_by(order_by=input.order_by)

        entities = self.repository.list(
            order_by=order_by,
            page=page,
        )

        total = self.repository.count()

        data = self.get_output_data_from_entities(entities=entities)

        meta = PaginatedListUseCase.Meta(
            page=page,
            per_page=core_settings.REPOSITORY["page_size"],
            total=total,
        )

        return PaginatedListUseCase.Output(
            data=data,
            meta=meta,
        )

    @staticmethod
    @abstractmethod
    def get_output_data_from_entities(
        entities: list[ENTITY],
    ) -> list[ENTITY_OUTPUT_DATA]:
        pass

    def get_validated_page(self, page: Any) -> int:
        if page is None:
            return 1

        try:
            if isinstance(page, float) and not page.is_integer():
                raise ValueError
            page = int(page)
        except (TypeError, ValueError):
            raise InvalidPageRequested(page=page)
        else:
            if page < 1:
                raise InvalidPageRequested(page=page)

        return page

    def get_validated_order_by(self, order_by: str | None) -> str:
        if order_by is None:
            order_by = self.default_order_by_field

        valid_order_by_fields = getattr(self, "order_by_fields")

        if order_by not in valid_order_by_fields:
            raise InvalidOrderByRequested(
                order_by=order_by,
                valid_order_by_attributes=valid_order_by_fields,
            )

        return order_by
