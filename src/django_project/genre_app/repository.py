from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.shared.repository.mapper import BaseORMMapper


class GenreMapper(BaseORMMapper[Genre, GenreModel]):
    @staticmethod
    def to_model(entity: Genre, save: bool = False) -> GenreModel:
        instance = GenreModel(
                id=entity.id,
                name=entity.name,
                is_active=entity.is_active,
            )
        if save:
            instance.save()
        return instance

    @staticmethod
    def to_entity(model: GenreModel) -> Genre:
        return Genre(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            categories=[
                category.id
                for category in model.categories.all().order_by("name")
            ]
        )


class DjangoORMGenreRepository(AbstractGenreRepository):
    def __init__(self, genre_model: type[GenreModel] = GenreModel):
        self.genre_model = genre_model

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreMapper.to_model(genre, save=True)
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

        return GenreMapper.to_entity(genre_model)

    def list(self, order_by: str | None = None) -> list[Genre]:
        genre_models = self.genre_model.objects.all()

        if order_by is not None:
            genre_models = genre_models.order_by(order_by)

        return [
            GenreMapper.to_entity(genre_model)
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
