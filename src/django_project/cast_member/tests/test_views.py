
from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.gateway.cast_member_gateway import (
    AbstractCastMemberRepository,
)
from src.django_project.cast_member.repository import DjangoORMCastMemberRepository

BASE_CAST_MEMBERS_URL = "/api/cast_members/"


@pytest.fixture
def cast_member_repository():
    return DjangoORMCastMemberRepository()


@pytest.fixture
def persisted_actor_cast_member(
    cast_member_repository: AbstractCastMemberRepository,
) -> CastMember:
    cast_member = CastMember(name="John", type="ACTOR")
    cast_member_repository.save(cast_member=cast_member)
    return cast_member


@pytest.fixture
def persisted_director_cast_member(
    cast_member_repository: AbstractCastMemberRepository,
) -> CastMember:
    cast_member = CastMember(name="Jane", type="DIRECTOR")
    cast_member_repository.save(cast_member=cast_member)
    return cast_member


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members_success(
        self,
        persisted_actor_cast_member: CastMember,
        persisted_director_cast_member: CastMember,
    ):

        expected_data = {
            "data": [
                {
                    "id": str(persisted_actor_cast_member.id),
                    "name": persisted_actor_cast_member.name,
                    "type": persisted_actor_cast_member.type,
                },
                {
                    "id": str(persisted_director_cast_member.id),
                    "name": persisted_director_cast_member.name,
                    "type": persisted_director_cast_member.type,
                }
            ]
        }

        response = APIClient().get(path=BASE_CAST_MEMBERS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_list_no_cast_members(
        self,
    ):
        expected_data = {"data": []}

        response = APIClient().get(path=BASE_CAST_MEMBERS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member_invalid_name_content_data_error(
        self,
    ):
        post_data = {
            "name": "",
            "type": "ACTOR",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_cast_member_invalid_type_content_data_error(
        self,
    ):
        post_data = {
            "name": "John",
            "type": "INVALID_TYPE",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"type": ['"INVALID_TYPE" is not a valid choice.']}

    def test_create_cast_member_success(
        self,
        cast_member_repository: AbstractCastMemberRepository,
    ):
        post_data = {
            "name": "John",
            "type": "ACTOR",
        }

        response = APIClient().post(
            path=BASE_CAST_MEMBERS_URL,
            data=post_data,
        )

        assert response.status_code == status.HTTP_201_CREATED

        created_cast_member_id = UUID(response.data["id"])

        created_cast_member = cast_member_repository.get_by_id(
            id=created_cast_member_id,
        )

        assert created_cast_member.name == post_data["name"]
        assert created_cast_member.type == post_data["type"]


@pytest.mark.django_db
class TestUpdateAPI:
    def test_update_cast_member_invalid_payload_error(
        self,
        persisted_actor_cast_member: CastMember,
    ):

        post_data = {
            "name": "",
        }

        url = BASE_CAST_MEMBERS_URL + f"{str(persisted_actor_cast_member.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "type": ['This field is required.'],
        }

    def test_update_cast_member_invalid_id_error(
        self,
        persisted_actor_cast_member: CastMember,
    ):

        post_data = {
            "type": persisted_actor_cast_member.type,
        }

        url = BASE_CAST_MEMBERS_URL + "invalid-id/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ['This field is required.'],
        }

    def test_update_non_existing_cast_member_error(
        self,
    ):
        post_data = {
            "name": "Jonh",
            "type": "ACTOR",
        }

        url = BASE_CAST_MEMBERS_URL + f"/{str(uuid4())}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_cast_member_valid_payload_success(
        self,
        persisted_actor_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):

        post_data = {
            "name": "Jonathan",
            "type": "DIRECTOR",
        }

        url = BASE_CAST_MEMBERS_URL + f"{str(persisted_actor_cast_member.id)}/"
        response = APIClient().put(url, data=post_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["id"] == str(persisted_actor_cast_member.id)

        updated_cast_member = cast_member_repository.get_by_id(
            id=UUID(response.data["id"])
        )

        assert updated_cast_member is not None

        assert updated_cast_member.name == post_data["name"]
        assert updated_cast_member.type == post_data["type"]


@pytest.mark.django_db
class TestDeleteCastMember:
    def test_delete_cast_member_success(
        self,
        persisted_actor_cast_member: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        url = BASE_CAST_MEMBERS_URL + f"{str(persisted_actor_cast_member.id)}/"
        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        found_cast_member = cast_member_repository.get_by_id(
            id=persisted_actor_cast_member.id
        )
        assert found_cast_member is None

    def test_delete_cast_member_non_existing_id_error(
        self,
    ):
        url = f"/api/categories/{str(uuid4())}/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_cast_member_non_invalid_id_error(
        self,
    ):
        url = "/api/cast_members/invalid-id/"

        response = APIClient().delete(path=url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
        }
