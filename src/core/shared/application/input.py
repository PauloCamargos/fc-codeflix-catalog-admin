from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.core.shared.application.errors import InvalidOrderByRequested


@dataclass(kw_only=True)
class ValidateInputMixin(ABC):
    order_by: str

    def __post_init__(self) -> None:
        self.validate()

    @staticmethod
    @abstractmethod
    def get_valid_order_by_attributes() -> list[str]:
        pass

    def validate(self) -> None:
        if self.order_by not in self.get_valid_order_by_attributes():
            raise InvalidOrderByRequested(
                order_by=self.order_by,
                valid_order_by_attributes=self.get_valid_order_by_attributes(),
            )
