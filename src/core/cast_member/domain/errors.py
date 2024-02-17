class InvalidCastMemberTypeError(Exception):
    message_template = "Type must be one of: {valid_types_str}"

    def __init__(self, valid_types: list[str]) -> None:
        valid_types_str = ", ".join(
            repr(type)
            for type in valid_types
        )
        message = self.message_template.format(valid_types_str=valid_types_str)
        super().__init__(message)
