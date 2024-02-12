from dataclasses import dataclass, field
from uuid import UUID
from core.category.gateway.category_gateway import AbstractCategoryRepository
from core.genre.application.errors import InvalidGenreData, RelatedCategoriesNotFound

from core.genre.domain.genre import Genre
from core.genre.gateway.genre_gateway import AbstractGenreRepository


class CreateGenre:
    @dataclass
    class Input:
        name: str
        categories: set[UUID] = field(default_factory=set)
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
            for category in self.category_repository.list_categories()
        }

        if not input.categories.issubset(existing_category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.categories - existing_category_ids}"
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
