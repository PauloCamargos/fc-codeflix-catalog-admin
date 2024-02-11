from uuid import UUID

from django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category
from src.core.category.gateway.category_gateway import AbstractCategoryRepository


class DjangoORMCategoryRepository(AbstractCategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model

    def save(self, category: Category) -> None:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            found_category = self.category_model.objects.get(id=id)
        except self.category_model.DoesNotExist:
            return None
        else:
            category = Category(
                id=found_category.id,
                name=found_category.name,
                description=found_category.description,
                is_active=found_category.is_active,
            )

        return category

    def list_categories(self) -> list[Category]:
        found_categories = list(self.category_model.objects.all())
        categories = [
            Category(
                id=found_category.id,
                name=found_category.name,
                description=found_category.description,
                is_active=found_category.is_active,
            )
            for found_category in found_categories
        ]

        return categories

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
