from dataclasses import dataclass
from uuid import UUID

from core.category.gateway.category_gateway import AbstractCategoryRepository
from core.genre.application.errors import (
    GenreNotFound,
    InvalidGenreData,
    RelatedCategoriesNotFound,
)
from core.genre.gateway.genre_gateway import AbstractGenreRepository


class UpdateGenre:

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        is_active: bool | None = None
        categories: set[UUID] | None = None

    @dataclass
    class Output:
        id: UUID
        is_active: bool
        name: str
        categories: set[UUID]

    def __init__(
        self,
        repository: AbstractGenreRepository,
        category_repository: AbstractCategoryRepository,
    ):
        self.repository = repository
        self.category_repository = category_repository

    def execute(self, input: Input) -> Output:

        genre = self.repository.get_by_id(id=input.id)

        if genre is None:
            raise GenreNotFound()

        if input.categories is not None:
            existing_category_ids = {
                category.id
                for category in self.category_repository.list_categories()
            }

            if not input.categories.issubset(existing_category_ids):
                raise RelatedCategoriesNotFound(
                    f"Categories not found: {input.categories - existing_category_ids}"
                )

            category_ids_to_remove = genre.categories - input.categories
            category_ids_to_add = input.categories - genre.categories

            for category_id in category_ids_to_remove:
                genre.remove_category(category_id)

            for category_id in category_ids_to_add:
                genre.add_category(category_id)

        if input.name is not None:
            try:
                genre.update_name(name=input.name)
            except ValueError as err:
                raise InvalidGenreData(err)

        if input.is_active is not None:
            if not genre.is_active:
                try:
                    genre.activate()
                except ValueError as err:
                    raise InvalidGenreData(err)
            else:
                try:
                    genre.deactivate()
                except ValueError as err:
                    raise InvalidGenreData(err)

        self.repository.update(genre=genre)

        return UpdateGenre.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )
