from copy import deepcopy
from uuid import UUID

from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.core.genre.domain.genre import Genre


class InMemoryGenreRepository(AbstractGenreRepository):
    def __init__(self, genres: list[Genre] | None = None):
        if genres is None:
            self.genres = []
        else:
            self.genres = genres

    def save(self, genre: Genre) -> None:
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        return next(
            (
                deepcopy(genre)
                for genre in self.genres
                if genre.id == id
            ),
            None,
        )

    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        if genre:
            self.genres.remove(genre)

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[Genre]:
        genres = (
            deepcopy(genre)
            for genre in self.genres
        )

        if order_by is not None:
            return list(
                sorted(
                    genres,
                    key=lambda genre: getattr(genre, order_by.strip("-")),
                    reverse=order_by.startswith("-"),
                )
            )

        return list(genres)

    def count(self) -> int:
        return len(self.genres)

    def update(self, genre: Genre) -> None:
        old_genre = self.get_by_id(genre.id)
        if old_genre:
            self.genres.remove(old_genre)
            self.genres.append(genre)
