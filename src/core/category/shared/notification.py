class Notification:
    def __init__(self) -> None:
        self._errors = []

    def add_error(self, message: str) -> None:
        self._errors.append(message)

    @property
    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def messages(self) -> list[str]:
        return ", ".join(self._errors)
