class InvalidOrderByRequested(Exception):
    message_template = (
        "Provided ordering {order_by} is not one of: {valid_order_by_attributes}"
    )

    def __init__(
        self,
        order_by: str,
        valid_order_by_attributes: list[str],
    ) -> None:
        valid_order_by_elements_str = ", ".join(
            repr(order_by)
            for order_by in valid_order_by_attributes
        )
        message = self.message_template.format(
            order_by=repr(order_by),
            valid_order_by_attributes=valid_order_by_elements_str,
        )
        super().__init__(message)
