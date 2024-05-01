from unittest.mock import patch
import pytest

from src.core.genre.application.list_genres import GenreOutput, ListGenres
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.shared import settings
from src.core.shared.application.errors import InvalidOrderByRequested


class TestListGenre:
    def test_list_genres_empty_success(
        self,
        genre_repository: InMemoryGenreRepository,
    ) -> None:

        list_genres = ListGenres(repository=genre_repository)

        input = ListGenres.Input()
        output = list_genres.execute(input=input)

        expected_output: ListGenres.Output[GenreOutput] = ListGenres.Output(
            data=[],
            meta=ListGenres.Meta(
                page=1,
                per_page=settings.REPOSITORY["page_size"],
                total=0,
            )
        )

        assert expected_output == output

    def test_list_genre_with_categories_no_order_by_success(
        self,
        romance_genre: Genre,
        drama_genre: Genre,
        genre_repository: InMemoryGenreRepository,
    ) -> None:
        genre_repository.save(romance_genre)
        genre_repository.save(drama_genre)

        list_genre = ListGenres(repository=genre_repository)

        input = ListGenres.Input(order_by=None)

        output = list_genre.execute(input=input)

        expected_genres = sorted(
            [
                drama_genre,
                romance_genre,
            ],
            key=lambda genre: getattr(
                genre,
                ListGenres.default_order_by_field,
            ),
            reverse=ListGenres.default_order_by_field.startswith("-"),
        )

        expected_output = ListGenres.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    categories=genre.categories,
                    is_active=genre.is_active,
                )
                for genre in expected_genres
            ],
            meta=ListGenres.Meta(
                page=1,
                per_page=settings.REPOSITORY["page_size"],
                total=2,
            )
        )

        assert output == expected_output

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
        genre_repository.save(genre=romance_genre)
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
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    categories=genre.categories,
                    is_active=genre.is_active,
                )
                for genre in expected_genres
            ],
            meta=ListGenres.Meta(
                page=1,
                per_page=settings.REPOSITORY["page_size"],
                total=2,
            )
        )

        assert expected_output == output

    def test_list_genre_invalid_order_by_error(
        self,
        genre_repository: InMemoryGenreRepository,
    ):
        order_by = "potato"
        valid_order_by_attrs = ", ".join(
            repr(attr)
            for attr in ListGenres.order_by_fields
        )

        input = ListGenres.Input(order_by=order_by)

        use_case = ListGenres(repository=genre_repository)

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
    def test_list_genres_pagination_success(
        self,
        page: int,
        romance_genre: Genre,
        drama_genre: Genre,
        horror_genre: Genre,
        comedy_genre: Genre,
        action_genre: Genre,
        genre_repository: InMemoryGenreRepository,
    ):
        genre_repository.save(genre=romance_genre)
        genre_repository.save(genre=drama_genre)
        genre_repository.save(genre=horror_genre)
        genre_repository.save(genre=comedy_genre)
        genre_repository.save(genre=action_genre)

        order_by = "-name"

        input = ListGenres.Input(
            order_by=order_by,
            page=page,
        )
        use_case = ListGenres(repository=genre_repository)

        overriden_page_size = 2
        with patch.dict(
            settings.REPOSITORY,
            {"page_size": overriden_page_size},
        ):
            output = use_case.execute(input=input)

        expected_output_by_page = {
            1: [
                romance_genre,
                horror_genre,
            ],
            2: [
                drama_genre,
                comedy_genre,
            ],
            3: [
                action_genre,
            ],
        }

        expected_output = ListGenres.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    categories=genre.categories,
                    is_active=genre.is_active,
                )
                for genre in expected_output_by_page[page]
            ],
            meta=ListGenres.Meta(
                page=page,
                per_page=overriden_page_size,
                total=len(
                    [
                        genre
                        for genres in expected_output_by_page.values()
                        for genre in genres
                    ]
                ),
            )
        )

        assert expected_output == output
