from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.shared.domain.entity import Entity

MAX_GENRE_NAME_NUM_CARACTERS = 255
DEFAULT_GENRE_IS_ACTIVE = True


@dataclass(eq=False)
class Genre(Entity):
    name: str
    is_active: bool = field(default=DEFAULT_GENRE_IS_ACTIVE)
    categories: set[UUID] = field(default_factory=set)

    def activate(self) -> None:
        self.is_active = True
        self.validate()

    def deactivate(self) -> None:
        self.is_active = False
        self.validate()

    def update_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def add_category(self, id: UUID) -> None:
        self.categories.add(id)
        self.validate()

    def remove_category(self, id: UUID) -> None:
        if id not in self.categories:
            return
        self.categories.remove(id)
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_GENRE_NAME_NUM_CARACTERS:
            self.notification.add_error(
                "'name' must have less than "
                f"{MAX_GENRE_NAME_NUM_CARACTERS} characters"
            )

        if self.name == "":
            self.notification.add_error("'name' must not be empty")

        super().validate()

    def __str__(self) -> str:
        prefixes: list[str] = []
        if not self.is_active:
            prefixes.append("DEACTIVATED")

        prefixes_str = ", ".join(prefixes)

        return f"<{self.__class__.__qualname__}> ({prefixes_str}) {self.name}"
