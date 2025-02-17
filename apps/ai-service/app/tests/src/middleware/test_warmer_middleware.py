from typing import Any, Mapping
from unittest.mock import Mock

from aws_lambda_powertools.utilities.typing import LambdaContext

from src.middleware.warmer import warmer


class TestWarmerMiddleware:
    def test_should_exit(
        self,
        mock_context: LambdaContext,
    ) -> None:
        @warmer
        def _handler(event: Mapping[str, Any], context: LambdaContext):
            raise Exception("Should not be called")

        event = {"warmer": True}

        response = _handler(event, mock_context)

        assert response == None

    def test_should_call(
        self,
        mock_context: LambdaContext,
    ) -> None:
        @warmer
        def _handler(event: Mapping[str, Any], context: LambdaContext):
            return event

        event = {"not_warmer": True}
        response = _handler(event, mock_context)
        assert response == event
