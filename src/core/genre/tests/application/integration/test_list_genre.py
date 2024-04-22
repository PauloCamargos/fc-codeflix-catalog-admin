import pytest

from src.core.category.domain.category import Category
from src.core.genre.application.list_genres import ListGenres
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.shared.application.errors import InvalidOrderByRequested


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def romance_genre(
    movie_category: Category,
    documentary_category: Category,
) -> Genre:
    return Genre(
        name="Romance",
        categories=[movie_category.id, documentary_category.id],
    )

@pytest.fixture
def drama_genre(
    movie_category: Category,
) -> Genre:
    return Genre(
        name="Drama",
        categories=[movie_category.id],
    )


@pytest.fixture
def genre_repository(
    romance_genre: Genre,
) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[romance_genre])


class TestListGenre:
    def test_list_genre_with_categories_no_order_by_success(
        self,
        romance_genre: Genre,
        genre_repository: InMemoryGenreRepository,
        movie_category: Category,
        documentary_category: Category,
    ) -> None:
        list_genre = ListGenres(repository=genre_repository)

        input = ListGenres.Input()

        output = list_genre.execute(input=input)

        assert len(output.data) == 1

        [genre_data] = output.data

        assert romance_genre.id == genre_data.id
        assert romance_genre.name == genre_data.name
        assert romance_genre.is_active == genre_data.is_active
        expected_categories = [
            movie_category.id,
            documentary_category.id,
        ]
        assert expected_categories == genre_data.categories

    @pytest.mark.parametrize(
            "order_by",
            ["name", "-name"]
    )
    def test_list_genre_with_categories_order_by_success(
        self,
        order_by: str,
        romance_genre: Genre,
        drama_genre: Genre,
        genre_repository: InMemoryGenreRepository,
    ) -> None:
        genre_repository.save(genre=drama_genre)

        input = ListGenres.Input(order_by=order_by)

        use_case = ListGenres(repository=genre_repository)

        output = use_case.execute(input=input)

        expected_genres = sorted(
            [
                romance_genre,
                drama_genre,
            ],
            key=lambda genre: getattr(genre, order_by.strip("-")),
            reverse=order_by.startswith("-"),
        )

        expected_output = ListGenres.Output(
            data=[
                ListGenres.GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    categories=genre.categories,
                    is_active=genre.is_active,
                )
                for genre in expected_genres
            ]
        )

        assert expected_output == output


    def test_list_genre_invalid_order_by_error(
        self,
    ):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListGenres.Input.get_valid_order_by_attributes()
        )

        with pytest.raises(
            InvalidOrderByRequested,
            match=(
                f"Provided ordering {repr(order_by)} "
                f"is not one of: {valid_order_by_attrs}"
            ),
        ):
            ListGenres.Input(order_by=order_by)
