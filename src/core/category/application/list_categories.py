from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.shared import settings as core_settings
from src.core.shared.application.list import ListInputMixin

DEFAULT_CATEGORY_LIST_ORDER = "name"

VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
    "description",
    "-description",
]


class ListCategories:
    @dataclass
    class Input(ListInputMixin):
        order_by: str = field(default=DEFAULT_CATEGORY_LIST_ORDER)
        page: int = field(default=1)

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListCategories.CategoryOutput"]
        meta: "ListCategories.OutputMeta"

    @dataclass
    class CategoryOutput:
        id: UUID
        name: str
        description: str
        is_active: bool

    @dataclass
    class OutputMeta:
        page: int
        per_page: int
        total: int

    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        categories = self.repository.list(
            order_by=input.order_by,
            page=input.page,
        )
        total = self.repository.count()

        data = [
            ListCategories.CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
            for category in categories
        ]

        meta = ListCategories.OutputMeta(
            page=input.page,
            per_page=core_settings.REPOSITORY["page_size"],
            total=total,
        )

        return ListCategories.Output(
            data=data,
            meta=meta,
        )
