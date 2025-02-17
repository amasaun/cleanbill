from typing import Any, Callable, Mapping, Tuple, Type, cast

from aws_lambda_powertools import Logger
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerResponseV2,
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.type_defs.authorizer_responses import APIGatewayAuthorizerResponseV2TypeDef


@lambda_handler_decorator
def authorizer_exception(
    handler: Callable[..., APIGatewayAuthorizerResponseV2TypeDef],
    event: Mapping[str, Any],
    context: LambdaContext,
    exceptions: Tuple[Type[Exception]],
    logger: Logger = Logger(),
) -> APIGatewayAuthorizerResponseV2TypeDef:
    """
    Middleware Decorator meant to capture expected exceptions from an Authorizer
    and return a deny payload.

    If there is an unexpected Exception an error is raised and 500 is returned.
    """

    try:
        return handler(event, context)

    except exceptions as e:
        logger.error(
            "Authorizer Exception",
            exc_info=e,
        )

        return cast(
            APIGatewayAuthorizerResponseV2TypeDef,
            APIGatewayAuthorizerResponseV2(authorize=False).asdict(),
        )
