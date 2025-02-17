from http import HTTPStatus


class CentralApiExceptions(Exception):
    pass


class CentralApiCommunicationFailed(CentralApiExceptions):
    """
    Exception raised when Central-API return something other than 200
    """

    message: str
    status_code: HTTPStatus | int | None

    def __init__(
        self,
        status_code: HTTPStatus | int | None = None,
        message: str = "Central-API Responded with an undesired status_code",
    ) -> None:
        self.status_code = status_code
        self.message = message

        super().__init__(
            f"{message}{f'| {self.status_code}' if self.status_code else ''}",
        )


class BadResponse(CentralApiExceptions):
    def __init__(
        self,
        message: str = "Could not get account_uuid or organization_uuid from payload",
    ) -> None:
        self.message = message

        super().__init__(message)
