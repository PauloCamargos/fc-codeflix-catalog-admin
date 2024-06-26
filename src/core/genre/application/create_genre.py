from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.genre.application.errors import (
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository


class CreateGenre:
    @dataclass
    class Input:
        name: str
        categories: list[UUID] = field(default_factory=list)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def __init__(
        self,
        repository: AbstractGenreRepository,
        category_repository: AbstractCategoryRepository,
    ) -> None:
        self.repository: AbstractGenreRepository = repository
        self.category_repository: AbstractCategoryRepository = category_repository

    def execute(self, input: Input) -> Output:
        existing_category_ids = {
            category.id
            for category in self.category_repository.list()
        }

        input_categories_set = set(input.categories)

        if not input_categories_set.issubset(existing_category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input_categories_set - existing_category_ids}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=input.categories,
            )
        except ValueError as err:
            raise InvalidGenreData(err)
        else:
            self.repository.save(genre=genre)

        return CreateGenre.Output(id=genre.id)
