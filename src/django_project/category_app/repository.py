from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository
from src.django_project.category_app.models import Category as CategoryModel
from src.django_project.shared.repository.mapper import BaseORMMapper


class CategoryMapper(BaseORMMapper):
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

    def save(self, category: Category) -> None:
        CategoryMapper.to_model(category, save=True)

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            found_category = self.category_model.objects.get(id=id)
        except self.category_model.DoesNotExist:
            return None

        return CategoryMapper.to_entity(found_category)

    def list_categories(self) -> list[Category]:
        return [
            CategoryMapper.to_entity(found_category)
            for found_category in self.category_model.objects.all()
        ]

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        (
            self.category_model.objects.filter(
                id=category.id,
            ).update(
                name=category.name,
                description=category.description,
                is_active=category.is_active,
            )
        )
