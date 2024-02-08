from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.errors import InvalidCategoryData

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


@dataclass
class CreateCategoryInput:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryOutput:
    id: UUID


class CreateCategoryUserCase:
    def __init__(
        self,
        repository: AbstractCategoryRepository,
    ) -> None:
        self.repository: AbstractCategoryRepository = repository

    def execute(self, input: CreateCategoryInput) -> CreateCategoryOutput:
        try:
            category = Category(
                name=input.name,
                description=input.description,
                is_active=input.is_active,
            )
        except ValueError as err:
            raise InvalidCategoryData(err)
        else:
            self.repository.save(category)

        return CreateCategoryOutput(id=category.id)
