import uuid
from uuid import UUID

import pytest

from core.genre.domain.genre import MAX_GENRE_NAME_NUM_CARACTERS, Genre


class TestCreateGenre:
    def test_create_genre_without_name_error(self):
        with pytest.raises(
            TypeError,
            match="missing 1 required positional argument: 'name'",
        ):
            Genre()

    def test_create_genre_invalid_name_length_error(self):
        with pytest.raises(
            ValueError,
            match=(
                "'name' must have less than "
                f"{MAX_GENRE_NAME_NUM_CARACTERS} characters"
            ),
        ):
            Genre(name="n" * (MAX_GENRE_NAME_NUM_CARACTERS + 1))

    def test_create_genre_invalid_name_content_error(self):
        with pytest.raises(
            ValueError,
            match="'name' must not be empty",
        ):
            Genre(name="")

    def test_create_genre_with_non_default_values_sucess(self):
        genre_id = uuid.uuid4()
        category_id = uuid.uuid4()
        genre_name = "Romance"
        genre_is_active = False

        genre = Genre(
            id=genre_id,
            name=genre_name,
            is_active=genre_is_active,
            categories={category_id},
        )
        assert genre.id == genre_id
        assert genre.name == genre_name
        assert genre.is_active == genre_is_active
        assert genre.categories == {category_id}

    def test_create_genre_with_default_values_success(self):
        genre = Genre(name="Romance")
        assert genre.categories == set()
        assert genre.is_active
        assert isinstance(
            genre.id,
            UUID,
        ), f"genre.id type was {type(genre.id)} instead of {UUID}"


class TestUpdateGenre:
    def test_update_genre_name_success(self):
        genre = Genre(name="Romance")

        new_name = "Drama"
        genre.update_name(name=new_name)

        assert genre.name == new_name, "name was not updated"

    def test_update_genre_invalid_name_lenght_error(self):
        genre = Genre(name="Romance")

        new_name = "n" * (MAX_GENRE_NAME_NUM_CARACTERS + 1)

        with pytest.raises(
            ValueError,
            match=(
                "'name' must have less than "
                f"{MAX_GENRE_NAME_NUM_CARACTERS} characters"
            ),
        ):
            genre.update_name(name=new_name)

    def test_update_genre_invalid_name_content_error(self):
        genre = Genre(name="Romance")

        new_name = ""

        with pytest.raises(
            ValueError,
            match="'name' must not be empty",
        ):
            genre.update_name(name=new_name)


class TestActiveGenre:
    def test_activate_inactive_genre_success(self):
        genre = Genre(name="Romance", is_active=False)

        genre.activate()

        assert genre.is_active, "genre was not activated"

    def test_activate_active_genre_success(self):
        genre = Genre(name="Romance", is_active=True)

        genre.activate()

        assert genre.is_active, "genre was not activated"

    def test_inactivate_active_genre_success(self):
        genre = Genre(name="Romance", is_active=True)

        genre.deactivate()

        assert not genre.is_active, "genre was not deactivated"

    def test_inactivate_inactive_genre_success(self):
        genre = Genre(name="Romance", is_active=False)

        genre.deactivate()

        assert not genre.is_active, "genre was not deactivated"


class TestGenreCategories:
    def test_add_non_existing_category_to_genre(self):
        genre = Genre(name="Romance")
        category_id = uuid.uuid4()
        genre.add_catetory(id=category_id)

        assert genre.categories == {category_id}

    def test_add_existing_category_to_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id})
        genre.add_catetory(id=category_id)

        assert genre.categories == {category_id}

    def test_add_category_to_genre(self):
        category_id_1 = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id_1})
        category_id_2 = uuid.uuid4()
        genre.add_catetory(id=category_id_2)

        assert genre.categories == {category_id_1, category_id_2}

    def test_remove_non_existing_category_from_genre(self):
        category_id_1 = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id_1})
        category_id_2 = uuid.uuid4()
        genre.remove_category(id=category_id_2)

        assert genre.categories == {category_id_1}

    def test_remove_existing_category_from_genre(self):
        category_id_1 = uuid.uuid4()
        genre = Genre(name="Romance", categories={category_id_1})
        genre.remove_category(id=category_id_1)

        assert genre.categories == set()


class TestGenreEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = Genre(id=common_id, name="dummy")
        genre_2 = Genre(id=common_id, name="other name")

        assert genre_1 == genre_2

    def test_when_categories_have_different_id_they_are_not_equal(self):
        id_1 = uuid.uuid4()
        id_2 = uuid.uuid4()
        genre_1 = Genre(id=id_1, name="dummy")
        genre_2 = Genre(id=id_2, name="dummy")

        assert genre_1 != genre_2
