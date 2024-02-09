from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.errors import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


@dataclass
class UpdateCategoryInput:
    id: UUID
    name: str | None = None
    description: str | None = None


@dataclass
class UpdateCategoryOutput:
    id: UUID
    is_active: bool
    name: str | None = None
    description: str | None = None


class UpdateCategory:
    def __init__(self, repository: AbstractCategoryRepository):
        self.repository = repository

    def execute(self, input: UpdateCategoryInput) -> Category:

        category = self.repository.get_by_id(id=input.id)

        if category is None:
            raise CategoryNotFound()

        name = category.name
        description = category.description

        if input.name is not None:
            name = input.name

        if input.description is not None:
            description = input.description

        category.update_category(name=name, description=description)

        updated_category = self.repository.update(category=category)

        return UpdateCategoryOutput(
            id=updated_category.id,
            name=updated_category.name,
            description=updated_category.description,
            is_active=updated_category.is_active,
        )
