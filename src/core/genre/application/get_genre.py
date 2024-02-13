# from dataclasses import dataclass
# from uuid import UUID
# from src.core.genre.application.errors import GenreNotFound

# from src.core.genre.gateway.genre_gateway import AbstractGenreRepository


# @dataclass
# class GetGenreInput:
#     id: UUID


# @dataclass
# class GetGenreOutput:
#     id: UUID
#     name: str
#     description: str
#     is_active: bool


# class GetGenre:
#     def __init__(self, repository: AbstractGenreRepository) -> None:
#         self.repository: AbstractGenreRepository = repository

#     def execute(self, input: GetGenreInput) -> GetGenreOutput | None:
#         genre = self.repository.get_by_id(id=input.id)

#         if genre is None:
#             raise GenreNotFound()

#         return GetGenreOutput(
#             id=genre.id,
#             name=genre.name,
#             description=genre.description,
#             is_active=genre.is_active,
#         )
