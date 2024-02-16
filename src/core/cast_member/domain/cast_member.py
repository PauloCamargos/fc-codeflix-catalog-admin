from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

from src.core.cast_member.domain.errors import InvalidCastMemberTypeError

MAX_CAST_MEMBER_NAME_NUM_CHARACTERS = 255


class CastMemberType(str, Enum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

    def __str__(self) -> str:
        return self.value


@dataclass
class CastMember:
    name: str = field(compare=False)
    type: CastMemberType = field(compare=False)
    id: UUID = field(default_factory=uuid4)

    def update_member_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def update_type(self, type: str) -> None:
        self._set_type(type=type)
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_CAST_MEMBER_NAME_NUM_CHARACTERS:
            raise ValueError(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CHARACTERS} characters"
            )

        if self.name == "":
            raise ValueError("'name' must not be empty")

    def __post_init__(self) -> None:
        self._set_type(type=self.type)
        self.validate()

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
