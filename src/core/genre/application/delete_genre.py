from dataclasses import dataclass
from uuid import UUID
from core.genre.application.errors import GenreNotFound
from core.genre.gateway.genre_gateway import AbstractGenreRepository


class DeleteGenre:
    @dataclass
    class Input:
        id: UUID

    def __init__(self, repository: AbstractGenreRepository):
        self.repository = repository

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(id=input.id)

        if genre is None:
            raise GenreNotFound()

        self.repository.delete(id=genre.id)
