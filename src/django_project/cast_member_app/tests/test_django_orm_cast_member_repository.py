
from uuid import uuid4
import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def actor_cast_member() -> CastMember:
    return CastMember(name="John", type="ACTOR")


@pytest.fixture
def director_cast_member() -> CastMember:
    return CastMember(name="Jane", type="DIRECTOR")


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_success(
        self,
        director_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member=director_cast_member)

        created_cast_member = cast_member_repository.get_by_id(
            id=director_cast_member.id,
        )

        assert created_cast_member is not None
        assert created_cast_member.name == director_cast_member.name
        assert created_cast_member.type == director_cast_member.type

    def test_update_cast_member_success(
        self,
        director_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member=director_cast_member)

        director_cast_member.update_name(name="Joane")
        director_cast_member.update_type(type="ACTOR")

        cast_member_repository.update(
            cast_member=director_cast_member,
        )

        updated_cast_member = cast_member_repository.get_by_id(
            id=director_cast_member.id,
        )

        assert updated_cast_member is not None
        assert updated_cast_member.name == director_cast_member.name
        assert updated_cast_member.type == director_cast_member.type

    def test_get_by_id_does_not_exist_cast_member_success(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member = cast_member_repository.get_by_id(
            id=uuid4(),
        )

        assert cast_member is None

    def test_list_cast_member_success(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        director_cast_member: CastMember,
        actor_cast_member: CastMember,
    ):
        cast_member_repository.save(cast_member=director_cast_member)
        cast_member_repository.save(cast_member=actor_cast_member)

        cast_members = cast_member_repository.list()

        assert actor_cast_member in cast_members
        assert director_cast_member in cast_members

    def test_delete_cast_member_success(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        director_cast_member: CastMember,
        actor_cast_member: CastMember,
    ):
        cast_member_repository.save(cast_member=director_cast_member)
        cast_member_repository.save(cast_member=actor_cast_member)

        cast_member_repository.delete(id=actor_cast_member.id)

        cast_members = cast_member_repository.list()

        assert actor_cast_member not in cast_members
        assert director_cast_member in cast_members
