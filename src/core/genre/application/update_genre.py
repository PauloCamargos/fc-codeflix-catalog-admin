# from dataclasses import dataclass
# from uuid import UUID

# from core.genre.application.errors import InvalidGenreData
# from core.genre.gateway.genre_gateway import AbstractGenreRepository


# @dataclass
# class UpdateGenreInput:
#     id: UUID
#     name: str | None = None
#     description: str | None = None
#     is_active: bool | None = None


# @dataclass
# class UpdateGenreOutput:
#     id: UUID
#     is_active: bool
#     name: str | None = None
#     description: str | None = None


# class UpdateGenre:
#     def __init__(self, repository: AbstractGenreRepository):
#         self.repository = repository

#     def execute(self, input: UpdateGenreInput) -> UpdateGenreOutput:

#         genre = self.repository.get_by_id(id=input.id)

#         if genre is None:
#             raise GenreNotFound()

#         name = genre.name
#         description = genre.description

#         if input.name is not None:
#             name = input.name

#         if input.description is not None:
#             description = input.description

#         try:
#             genre.update_genre(name=name, description=description)
#         except ValueError as err:
#             raise InvalidGenreData(err)

#         if input.is_active is not None:
#             if not genre.is_active:
#                 try:
#                     genre.activate()
#                 except ValueError as err:
#                     raise InvalidGenreData(err)
#             else:
#                 try:
#                     genre.deactivate()
#                 except ValueError as err:
#                     raise InvalidGenreData(err)

#         self.repository.update(genre=genre)

#         return UpdateGenreOutput(
#             id=genre.id,
#             name=genre.name,
#             description=genre.description,
#             is_active=genre.is_active,
#         )
