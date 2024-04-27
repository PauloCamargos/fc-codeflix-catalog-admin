from uuid import UUID

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Prefetch
from django.db.models.query import QuerySet

from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.shared.repository.mapper import BaseORMMapper
from src.core.shared import settings as core_settings


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
                for category in model.categories.all()
            ]
        )


class DjangoORMGenreRepository(AbstractGenreRepository):
    def __init__(self, genre_model: type[GenreModel] = GenreModel):
        self.genre_model = genre_model

    def get_queryset(self) -> QuerySet:
        return self.genre_model.objects.all()

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreMapper.to_model(genre, save=True)
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = (
                self.genre_model.objects
                .filter(id=id)
                .prefetch_related(self._get_categories_prefetch())
                .get()
            )
        except self.genre_model.DoesNotExist:
            return None

        return GenreMapper.to_entity(genre_model)

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[Genre]:
        queryset = self.get_queryset()

        if order_by is not None:
            queryset = queryset.order_by(order_by)

        if page is not None:
            paginator = Paginator(queryset, core_settings.REPOSITORY["page_size"])
            paginator_page = paginator.page(page)
            genres = paginator_page.object_list
            self._count = paginator.count
        else:
            genres = list(queryset)

        return [
            GenreMapper.to_entity(genre)
            for genre in genres
        ]

    def count(
        self,
    ) -> int:
        if self._count is None:
            self._count = self.get_queryset().count()
        return self._count

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

    def _get_categories_prefetch(self, to_attr: str | None = None) -> Prefetch:
        return Prefetch(
            "categories",
            queryset=(
                CategoryModel.objects
                .order_by("name")
                .only("id")
            ),
            to_attr=to_attr,
        )
