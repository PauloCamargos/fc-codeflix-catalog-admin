from dataclasses import dataclass
from uuid import UUID
from core.category.application.errors import CategoryNotFound
from core.category.gateway.category_gateway import AbstractCategoryRepository


@dataclass
class DeleteCategoryInput:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: DeleteCategoryInput) -> None:
        category = self.repository.get_by_id(id=input.id)

        if category is None:
            raise CategoryNotFound()

        self.repository.delete(id=input.id)
