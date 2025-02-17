from typing import Any, Callable, Mapping

from aws_lambda_powertools import Logger
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.type_defs.authorizer_responses import APIGatewayAuthorizerResponseV2TypeDef


@lambda_handler_decorator
def warmer(
    handler: Callable[..., APIGatewayAuthorizerResponseV2TypeDef],
    event: Mapping[str, Any],
    context: LambdaContext,
    logger: Logger = Logger(),
) -> APIGatewayAuthorizerResponseV2TypeDef | None:
    """
    Middleware Decorator meant to keep a Lambda Warm, without executing the
    handler's core business logic.

    It inspect the initial event and if it's a 'warmer' it exits early.
    """
    if event == {"warmer": True}:
        logger.info("Warmer Event. Exiting Early.")
        return None

    return handler(event, context)
