import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.cast_member_app.models import CastMember as CastMemberModel
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


# ----------------------------- #
# CAST MEMBER MODEL             #
# ----------------------------- #
@pytest.fixture
def actor_cast_member_model() -> CastMemberModel:
    cast_member = CastMemberModel.objects.create(name="John", type="ACTOR")
    return cast_member


@pytest.fixture
def director_cast_member_model() -> CastMemberModel:
    cast_member = CastMemberModel.objects.create(name="Jane", type="DIRECTOR")
    return cast_member


# --------------------------------- #
# CAST MEMBER MODEL (non-persisted) #
# --------------------------------- #
@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(name="Jane", type="DIRECTOR")
