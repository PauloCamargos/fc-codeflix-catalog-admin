from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar

from src.core.shared import settings as core_settings
from src.core.shared.application.errors import (
    InvalidOrderByRequested,
    InvalidPageRequested,
)
from src.core.shared.domain.entity import Entity


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


class Repository(Protocol, Generic[ENTITY]):
    def list(
        self,
        order_by: str | None,
        page: int,
    ) -> list[ENTITY]:
        ...

    def count(self) -> int:
        ...


class PaginatedListUseCase(ABC, Generic[ENTITY, ENTITY_OUTPUT_DATA]):
    default_order_by_field = "id"
    order_by_fields = ["id"]

    @dataclass
    class Input:
        order_by: str | None = None
        page: int = field(default=1)

    @dataclass
    class Output(Generic[ENTITY_OUTPUT_DATA2]):
        data: list[ENTITY_OUTPUT_DATA2]
        meta: "PaginatedListUseCase.Meta"

    @dataclass
    class Meta:
        page: int
        per_page: int
        total: int

    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(
        self,
        input: Input,
    ) -> "PaginatedListUseCase.Output[ENTITY_OUTPUT_DATA]":
        self.validate_input(input=input)

        if input.order_by is not None:
            order_by = input.order_by
        else:
            order_by = self.default_order_by_field

        entities = self.repository.list(
            order_by=order_by,
            page=input.page,
        )
        total = self.repository.count()

        data = self.get_output_data_from_entities(entities=entities)

        meta = PaginatedListUseCase.Meta(
            page=input.page,
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

    @classmethod
    def validate_input(cls, input: Input) -> None:
        if input.page < 1:
            raise InvalidPageRequested(page=input.page)

        valid_order_by_fields = getattr(cls, "order_by_fields")

        if (
            input.order_by is not None
            and input.order_by not in valid_order_by_fields
        ):
            raise InvalidOrderByRequested(
                order_by=input.order_by,
                valid_order_by_attributes=valid_order_by_fields,
            )
