from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.shared.application.errors import (
    InvalidOrderByRequested,
    InvalidPageRequested,
)


@dataclass(kw_only=True)
class ListInputMixin(ABC):
    order_by: str
    page: int

    def __post_init__(self) -> None:
        self.validate()

    @staticmethod
    @abstractmethod
    def get_valid_order_by_attributes() -> list[str]:
        pass

    def validate(self) -> None:
        if self.page < 1:
            raise InvalidPageRequested(
                page=self.page,
            )

        if self.order_by not in self.get_valid_order_by_attributes():
            raise InvalidOrderByRequested(
                order_by=self.order_by,
                valid_order_by_attributes=self.get_valid_order_by_attributes(),
            )
