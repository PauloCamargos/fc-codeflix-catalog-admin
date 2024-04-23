from uuid import UUID

from django.core.paginator import Paginator
from django.db.models.query import QuerySet

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.core.shared import settings as core_settings
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.shared.repository.mapper import BaseORMMapper


class CategoryMapper(BaseORMMapper[Category, CategoryModel]):
    @staticmethod
    def to_model(entity: Category, save: bool = False) -> CategoryModel:
        instance = CategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )
        if save:
            instance.save()
        return instance

    @staticmethod
    def to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )

class DjangoORMCategoryRepository(AbstractCategoryRepository):
    def __init__(self, category_model: type[CategoryModel] = CategoryModel):
        self.category_model = category_model
        self._count: int | None = None
    
    def get_queryset(self) -> QuerySet:
        return self.category_model.objects.all()

    def save(self, category: Category) -> None:
        CategoryMapper.to_model(category, save=True)

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            found_category = self.category_model.objects.get(id=id)
        except self.category_model.DoesNotExist:
            return None

        return CategoryMapper.to_entity(found_category)

    def list(
        self,
        order_by: str | None = None,
        page: int | None = None,
    ) -> list[Category]:
        queryset = self.get_queryset()

        if order_by is not None:
            queryset = queryset.order_by(order_by)
        
        if page is not None:
            paginator = Paginator(queryset, core_settings.REPOSITORY["page_size"])
            paginator_page = paginator.page(page)
            categories = paginator_page.object_list
            self._count = paginator.count
        else:
            categories = list(queryset)

        return [
            CategoryMapper.to_entity(category)
            for category in categories
        ]
    
    def count(
        self,
    ) -> int:
        if self._count is None:
            self._count = self.get_queryset().count()
        return self._count

    def delete(self, id: UUID) -> None:
        self.get_queryset().filter(id=id).delete()
        self._count = None

    def update(self, category: Category) -> None:
        (
            self.get_queryset()
            .filter(
                id=category.id,
            ).update(
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        )
