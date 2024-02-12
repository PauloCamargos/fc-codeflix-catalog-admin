from dataclasses import dataclass, field
from uuid import UUID, uuid4

MAX_GENRE_NAME_NUM_CARACTERS = 255
DEFAULT_GENRE_IS_ACTIVE = True


@dataclass
class Genre:
    name: str = field(compare=False)
    id: UUID = field(default_factory=uuid4)
    is_active: bool = field(default=DEFAULT_GENRE_IS_ACTIVE, compare=False)
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

    def add_catetory(self, id: UUID) -> None:
        self.categories.add(id)
        self.validate()

    def remove_category(self, id: UUID) -> None:
        self.categories.pop(id)
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_GENRE_NAME_NUM_CARACTERS:
            raise ValueError(
                "'name' must have less than "
                f"{MAX_GENRE_NAME_NUM_CARACTERS} characters"
            )

        if self.name == "":
            raise ValueError("'name' must not be empty")

    def __post_init__(self):
        self.validate()

    def __str__(self) -> str:
        prefixes: list[str] = []
        if not self.is_active:
            prefixes.append("DEACTIVATED")

        prefixes_str = ", ".join(prefixes)

        return f"<{self.__class__.__qualname__}> ({prefixes_str}) {self.name}"
