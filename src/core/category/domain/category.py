from dataclasses import dataclass, field
from uuid import UUID, uuid4

MAX_CATEGORY_NAME_NUM_CARACTERS = 255
DEFAULT_CATEGORY_DESCRIPTION = ""
DEFAULT_CATEGORY_IS_ACTIVE = False


@dataclass
class Category:
    name: str = field(compare=False)
    description: str = field(default=DEFAULT_CATEGORY_DESCRIPTION, compare=False)
    is_active: bool = field(default=DEFAULT_CATEGORY_IS_ACTIVE, compare=False)
    id: UUID = field(default_factory=uuid4)

    def activate(self) -> None:
        self.is_active = True
        self.validate()

    def deactivate(self) -> None:
        self.is_active = False
        self.validate()

    def update_category(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_CATEGORY_NAME_NUM_CARACTERS:
            raise ValueError(
                "'name' must have less than "
                f"{MAX_CATEGORY_NAME_NUM_CARACTERS} characters"
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
