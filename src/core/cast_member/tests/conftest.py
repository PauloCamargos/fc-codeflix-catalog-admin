import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def cast_member_repository() -> AbstractCastMemberRepository:
    return InMemoryCastMemberRepository()


@pytest.fixture
def actor_aston_cast_member() -> CastMember:
    cast_member = CastMember(name="Aston", type="ACTOR")
    return cast_member


@pytest.fixture
def actor_john_cast_member() -> CastMember:
    cast_member = CastMember(name="John", type="ACTOR")
    return cast_member


@pytest.fixture
def actor_will_cast_member() -> CastMember:
    cast_member = CastMember(name="Will", type="ACTOR")
    return cast_member


@pytest.fixture
def director_jane_cast_member() -> CastMember:
    cast_member = CastMember(name="Jane", type="DIRECTOR")
    return cast_member


@pytest.fixture
def director_ray_cast_member() -> CastMember:
    cast_member = CastMember(name="Ray", type="DIRECTOR")
    return cast_member
