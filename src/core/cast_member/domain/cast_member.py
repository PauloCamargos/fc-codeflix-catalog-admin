from dataclasses import dataclass
from enum import Enum

from src.core.cast_member.domain.errors import InvalidCastMemberTypeError
from src.core.category.shared.domain.entity import Entity

MAX_CAST_MEMBER_NAME_NUM_CHARACTERS = 255


class CastMemberType(str, Enum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

    def __str__(self) -> str:
        return self.value


@dataclass(eq=False)
class CastMember(Entity):
    name: str
    type: CastMemberType | str

    def update_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def update_type(self, type: str) -> None:
        self._set_type(type=type)
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_CAST_MEMBER_NAME_NUM_CHARACTERS:
            self.notification.add_error(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            )

        if self.name == "":
            self.notification.add_error("'name' must not be empty")

        super().validate()

    def __post_init__(self) -> None:
        self._set_type(type=self.type)
        super().__post_init__()

    def _set_type(self, type: str | CastMemberType) -> None:
        try:
            self.type = CastMemberType(type)
        except ValueError:
            raise InvalidCastMemberTypeError(
                valid_types=[
                    str(type)
                    for type in CastMemberType
                ]
            )

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}> ({self.type}) {self.name}"
