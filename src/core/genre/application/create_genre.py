from dataclasses import dataclass
from uuid import UUID
from core.genre.application.errors import InvalidGenreData

from core.genre.domain.genre import Genre
from core.genre.gateway.genre_gateway import AbstractGenreRepository


@dataclass
class CreateGenreInput:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateGenreOutput:
    id: UUID


class CreateGenre:
    def __init__(
        self,
        repository: AbstractGenreRepository,
    ) -> None:
        self.repository: AbstractGenreRepository = repository

    def execute(self, input: CreateGenreInput) -> CreateGenreOutput:
        try:
            genre = Genre(
                name=input.name,
                description=input.description,
                is_active=input.is_active,
            )
        except ValueError as err:
            raise InvalidGenreData(err)
        else:
            self.repository.save(genre)

        return CreateGenreOutput(id=genre.id)
