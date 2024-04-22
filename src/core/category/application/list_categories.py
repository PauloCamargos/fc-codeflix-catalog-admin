from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.shared.application.input import ValidateInputMixin

DEFAULT_CATEGORY_LIST_ORDER = "name"

VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
    "description",
    "-description",
]


class ListCategories:
    @dataclass
    class Input(ValidateInputMixin):
        order_by: str = field(default=DEFAULT_CATEGORY_LIST_ORDER)

        @staticmethod
        def get_valid_order_by_attributes() -> list[str]:
            return VALID_ORDER_BY_ATTRIBUTES

    @dataclass
    class Output:
        data: list["ListCategories.CategoryOutput"]

    @dataclass
    class CategoryOutput:
        id: UUID
        name: str
        description: str
        is_active: bool

    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: Input) -> Output:
        categories = self.repository.list(order_by=input.order_by)

        return ListCategories.Output(
            data=[
                ListCategories.CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ]
        )
