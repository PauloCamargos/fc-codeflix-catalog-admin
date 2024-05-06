from uuid import UUID

from django.core.paginator import EmptyPage, Paginator
from django.db import transaction
from django.db.models import Prefetch
from django.db.models.query import QuerySet

from src.core.genre.domain.genre import Genre
from src.core.genre.gateway.genre_gateway import AbstractGenreRepository
from src.core.shared import settings as core_settings
from src.core.shared.application.errors import (
    InvalidOrderByRequested,
    InvalidPageRequested,
)
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.shared.repository.mapper import BaseORMMapper

DEFAULT_GENRE_LIST_ORDER = "name"
VALID_ORDER_BY_ATTRIBUTES = [
    "name",
    "-name",
]


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
                for category in model.ordered_categories
            ]
        )


class DjangoORMGenreRepository(AbstractGenreRepository):
    def __init__(self, genre_model: type[GenreModel] = GenreModel):
        self.genre_model = genre_model

    def get_queryset(self) -> QuerySet:
        queryset = self.genre_model.objects.all()
        return queryset

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreMapper.to_model(genre, save=True)
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = (
                self.genre_model.objects
                .filter(id=id)
                .prefetch_related(
                    self._get_categories_prefetch(to_attr="ordered_categories")
                )
                .get()
            )
        except self.genre_model.DoesNotExist:
            return None

        return GenreMapper.to_entity(genre_model)

    def list(
        self,
        order_by: str | None = None,
        page: int = 1,
    ) -> list[Genre]:
        if page < 1:
            raise InvalidPageRequested(page=page)

        if order_by is None:
            order_by = DEFAULT_GENRE_LIST_ORDER

        if order_by not in VALID_ORDER_BY_ATTRIBUTES:
            raise InvalidOrderByRequested(
                order_by=order_by,
                valid_order_by_attributes=VALID_ORDER_BY_ATTRIBUTES,
            )

        queryset = (
            self.get_queryset()
            .prefetch_related(
                self._get_categories_prefetch(to_attr="ordered_categories")
            )
            .order_by(order_by)
        )

        paginator = Paginator(queryset, core_settings.REPOSITORY["page_size"])

        try:
            paginator_page = paginator.page(page)
        except EmptyPage:
            raise InvalidPageRequested(
                page=page,
            )

        entities = paginator_page.object_list
        self._count = paginator.count

        return [
            GenreMapper.to_entity(genre)
            for genre in entities
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
