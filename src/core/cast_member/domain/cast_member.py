from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID, uuid4

MAX_CAST_MEMBER_NAME_NUM_CARACTERS = 255


class CastMemberType(str, Enum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember:
    name: str = field(compare=False)
    type: CastMemberType = field(compare=False)
    id: UUID = field(default_factory=uuid4)

    def update_member_name(self, name: str) -> None:
        self.name = name
        self.validate()

    def update_type(self, type: str) -> None:
        self.type = CastMemberType(type)
        self.validate()

    def validate(self) -> None:
        if len(self.name) > MAX_CAST_MEMBER_NAME_NUM_CARACTERS:
            raise ValueError(
                "'name' must have less than "
                f"{MAX_CAST_MEMBER_NAME_NUM_CARACTERS} characters"
            )

        if self.name == "":
            raise ValueError("'name' must not be empty")

    def __post_init__(self) -> None:
        self.type = CastMemberType(self.type)
        self.validate()

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}> ({self.type}) {self.name}"
