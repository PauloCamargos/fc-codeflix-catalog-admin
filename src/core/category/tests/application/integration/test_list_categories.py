from unittest.mock import patch

import pytest

from src.core.category.application.list_categories import CategoryOutput, ListCategories
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.shared import settings as core_settings
from src.core.shared.application.errors import InvalidOrderByRequested


class TestListCategoryIntegration:
    def test_list_categories_empty_success(
        self,
        category_repository: InMemoryCategoryRepository,
    ) -> None:

        list_categories = ListCategories(repository=category_repository)

        input = ListCategories.Input()
        output = list_categories.execute(input=input)

        expected_output = ListCategories.Output(
            data=[],
            meta=ListCategories.Meta(
                page=1,
                per_page=core_settings.REPOSITORY["page_size"],
                total=0,
            )
        )

        assert expected_output == output

    def test_list_categories_no_order_by_success(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository: InMemoryCategoryRepository,
    ) -> None:
        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        input = ListCategories.Input(order_by=None)

        use_case = ListCategories(repository=category_repository)

        output = use_case.execute(input=input)

        expected_categories = sorted(
            [
                movie_category,
                documentary_category,
            ],
            key=lambda category: getattr(
                category,
                ListCategories.default_order_by_field,
            ),
            reverse=ListCategories.default_order_by_field.startswith("-"),
        )

        expected_output = ListCategories.Output(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in expected_categories
            ],
            meta=ListCategories.Meta(
                page=1,
                per_page=core_settings.REPOSITORY["page_size"],
                total=2,
            )
        )

        assert output == expected_output


    @pytest.mark.parametrize(
            "order_by",
            ["name", "-name", "description", "-description"]
    )
    def test_list_categories_order_by_success(
        self,
        order_by: str,
        movie_category: Category,
        serie_category: Category,
        category_repository: InMemoryCategoryRepository,
    ):
        category_repository.save(serie_category)
        category_repository.save(movie_category)

        input = ListCategories.Input(order_by=order_by)

        use_case = ListCategories(repository=category_repository)

        output = use_case.execute(input=input)

        expected_categories = sorted(
            [
                movie_category,
                serie_category,
            ],
            key=lambda category: getattr(category, order_by.strip("-")),
            reverse=order_by.startswith("-"),
        )

        expected_output = ListCategories.Output(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in expected_categories
            ],
            meta=ListCategories.Meta(
                page=1,
                per_page=core_settings.REPOSITORY["page_size"],
                total=len(expected_categories),
            )
        )

        assert expected_output == output

    def test_list_categories_invalid_order_by_error(
        self,
        category_repository: InMemoryCategoryRepository,
    ):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListCategories.order_by_fields
        )
        input = ListCategories.Input(order_by=order_by)

        use_case = ListCategories(repository=category_repository)

        with pytest.raises(
            InvalidOrderByRequested,
            match=(
                f"Provided ordering {repr(order_by)} "
                f"is not one of: {valid_order_by_attrs}"
            ),
        ):
            use_case.execute(input=input)

    @pytest.mark.parametrize(
        "page",
        [1, 2, 3],
    )
    def test_list_categories_pagination_success(
        self,
        page: int,
        movie_category: Category,
        serie_category: Category,
        documentary_category: Category,
        music_clip_category: Category,
        lecture_category: Category,
        category_repository: InMemoryCategoryRepository,
    ):
        category_repository.save(category=movie_category)
        category_repository.save(category=serie_category)
        category_repository.save(category=documentary_category)
        category_repository.save(category=music_clip_category)
        category_repository.save(category=lecture_category)

        order_by = "-description"

        input = ListCategories.Input(
            order_by=order_by,
            page=page,
        )
        use_case = ListCategories(repository=category_repository)

        overriden_page_size = 2
        with patch.dict(
            core_settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
            output = use_case.execute(input=input)

        expected_output_by_page = {
            1: [
                serie_category,
                music_clip_category,
            ],
            2: [
                movie_category,
                lecture_category,
            ],
            3: [
                documentary_category,
            ],
        }

        expected_output = ListCategories.Output(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in expected_output_by_page[page]
            ],
            meta=ListCategories.Meta(
                page=page,
                per_page=overriden_page_size,
                total=len(
                    [
                        category
                        for categories in expected_output_by_page.values()
                        for category in categories
                    ]
                ),
            )
        )

        assert expected_output == output
