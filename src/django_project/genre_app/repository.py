from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel


class DjangoORMGenreRepository(AbstractGenreRepository):
    def __init__(self, genre_model: type[GenreModel] = GenreModel):
        self.genre_model = genre_model

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreModel.objects.create(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = (
                self.genre_model.objects
                .prefetch_related("categories")
                .get(id=id)
            )
        except self.genre_model.DoesNotExist:
            return None

        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories=set(
                category.id
                for category in genre_model.categories.all()
            )
        )

    def list_genres(self) -> list[Genre]:
        genre_models = self.genre_model.objects.all()

        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories=set(
                    category.id
                    for category in genre_model.categories.only("id")
                )
            )
            for genre_model in genre_models
        ]

    def delete(self, id: UUID) -> None:
        self.genre_model.objects.filter(id=id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_model = self.genre_model.objects.get(id=genre.id)
        except self.genre_model.DoesNotExist:
            return None

        with transaction.atomic():
            self.genre_model.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_model.categories.set(genre.categories)
