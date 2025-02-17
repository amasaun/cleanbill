from __future__ import annotations

from http import HTTPStatus

from aws_lambda_powertools.utilities.parser import BaseModel


class HttpResponse(dict):
    def __init__(
        self,
        status_code: HTTPStatus,
        body: BaseModel | str,
    ) -> None:
        """
        Dictionary that accepts and sets to keys on initialization:
            - status_code
            - body: str
        These values are expected by most AWS lambdas associated with API
        Gateway Responses

        Args:
            status_code (HttpStatus): The HttpStatus (int) to return in a
                response

            body (str): The json payload or text as string to return in an the
                response body.
        """
        if isinstance(body, BaseModel):
            formatted_body = body.json()
        elif isinstance(body, str):
            formatted_body = body

        self.update(
            {
                "statusCode": status_code,
                "body": formatted_body,
            }
        )
