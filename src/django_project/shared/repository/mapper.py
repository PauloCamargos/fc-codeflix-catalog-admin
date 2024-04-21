from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db.models import Model

ENTITY = TypeVar("ENTITY")
DJANGO_MODEL = TypeVar("DJANGO_MODEL", bound=Model)


class BaseORMMapper(ABC, Generic[ENTITY, DJANGO_MODEL]):
    @staticmethod
    @abstractmethod
    def to_model(entity: ENTITY, save: bool = False) -> DJANGO_MODEL:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def to_entity(model: DJANGO_MODEL) -> ENTITY:
        raise NotImplementedError()
