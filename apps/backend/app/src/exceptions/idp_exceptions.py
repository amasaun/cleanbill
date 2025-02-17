from __future__ import annotations


class IDPException(Exception):
    pass


class IDPNotFound(IDPException):
    """
    Exception raised when an IDP is not found.
    """

    message: str
    idp: str | None

    def __init__(
        self,
        idp: str | None = None,
        message: str = "IDP Not Found",
    ) -> None:
        self.idp = idp
        self.message = message

        super().__init__(
            f"{message}{f'| {idp}' if idp else ''}",
        )
