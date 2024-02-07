from uuid import UUID
import uuid

import pytest

from entity.category import (
    Category,
    MAX_CATEGORY_NAME_NUM_CARACTERS,
    DEFAULT_CATEGORY_DESCRIPTION,
    DEFAULT_CATEGORY_IS_ACTIVE,
)


class TestCreateCategory:
    def test_create_category_without_name_error(self):
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'name'",
        ):
            Category()

    def test_create_category_invalid_name_length_error(self):
        with pytest.raises(
            ValueError,
            match=(
                "'name' must have less than "
                f"{MAX_CATEGORY_NAME_NUM_CARACTERS} characters"
            ),
        ):
            Category(name="n" * (MAX_CATEGORY_NAME_NUM_CARACTERS + 1))

    def test_create_category_invalid_name_content_error(self):
        with pytest.raises(
            ValueError,
            match="'name' must not be empty",
        ):
            Category(name="")

    def test_create_category_with_uuid_id_sucess(self):
        category = Category(name="dummy")
        assert isinstance(
            category.id,
            UUID,
        ), f"category.id type was {type(category.id)} instead of {UUID}"

    def test_create_category_default_values_success(self):
        category_name = "dummy"
        category = Category(name=category_name)
        assert (
            category.description == DEFAULT_CATEGORY_DESCRIPTION
        ), "unexpected category.description"
        assert (
            category.is_active == DEFAULT_CATEGORY_IS_ACTIVE
        ), "unexpected category.is_active"
        assert category.name == category_name, "unexpected category.name"


class TestUpdateCategory:
    def test_update_category_name_and_description_success(self):
        category = Category(name="dummy name", description="dummy description")

        new_name = "other name"
        new_description = "other description"
        category.update_category(name=new_name, description=new_description)

        assert category.name == new_name, "name was not updated"
        assert category.description == new_description, "description was not updated"

    def test_update_category_invalid_name_lenght_error(self):
        category = Category(name="dummy name", description="dummy description")

        new_name = "n" * (MAX_CATEGORY_NAME_NUM_CARACTERS + 1)
        new_description = "other description"

        with pytest.raises(
            ValueError,
            match=(
                "'name' must have less than "
                f"{MAX_CATEGORY_NAME_NUM_CARACTERS} characters"
            ),
        ):
            category.update_category(name=new_name, description=new_description)

    def test_update_category_invalid_name_content_error(self):
        category = Category(name="dummy name", description="dummy description")

        new_name = ""
        new_description = "other description"

        with pytest.raises(
            ValueError,
            match="'name' must not be empty",
        ):
            category.update_category(name=new_name, description=new_description)


class TestActiveCategory:
    def test_activate_inactive_category_success(self):
        category = Category(name="dummy", is_active=False)

        category.activate()

        assert category.is_active, "category was not activated"

    def test_activate_active_category_success(self):
        category = Category(name="dummy", is_active=True)

        category.activate()

        assert category.is_active, "category was not activated"

    def test_inactivate_active_category_success(self):
        category = Category(name="dummy", is_active=True)

        category.deactivate()

        assert not category.is_active, "category was not deactivated"

    def test_inactivate_inactive_category_success(self):
        category = Category(name="dummy", is_active=False)

        category.deactivate()

        assert not category.is_active, "category was not deactivated"


class TestCategoryEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(id=common_id, name="dummy")
        category_2 = Category(id=common_id, name="other name")

        assert category_1 == category_2

    def test_when_categories_have_different_id_they_are_not_equal(self):
        id_1 = uuid.uuid4()
        id_2 = uuid.uuid4()
        category_1 = Category(id=id_1, name="dummy")
        category_2 = Category(id=id_2, name="dummy")

        assert category_1 != category_2
