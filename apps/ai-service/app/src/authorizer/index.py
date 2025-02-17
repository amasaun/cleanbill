import os
from typing import cast
from uuid import uuid4

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerEventV2,
    APIGatewayAuthorizerResponseV2,
)
from aws_lambda_powertools.utilities.typing import LambdaContext
from jwt.exceptions import PyJWTError

from src.common.handler_setup import (
    create_aws_token_validation_service,
    create_user_service,
)
from src.exceptions.authorizer_exceptions import AuthorizationException
from src.exceptions.central_api_exceptions import CentralApiExceptions
from src.exceptions.idp_exceptions import IDPException
from src.middleware.authorizer_exception import authorizer_exception
from src.middleware.warmer import warmer
from src.services.user_context_service import UserContextService
from src.type_defs.authorizer_responses import APIGatewayAuthorizerResponseV2TypeDef


logger = Logger()
table = boto3.resource("dynamodb").Table(os.environ["IDP_TABLE"])

aws_token_validation_service = create_aws_token_validation_service(
    table=table,
    logger=logger,
)
user_service = create_user_service(
    table=table,
)
user_context_service = UserContextService(
    logger=logger,
    user_service=user_service,
)


@warmer(logger=logger)
@authorizer_exception(
    exceptions=(
        AuthorizationException,
        CentralApiExceptions,
        IDPException,
        PyJWTError,
    ),
    logger=logger,
)
@event_source(data_class=APIGatewayAuthorizerEventV2)
@logger.inject_lambda_context
def handler(
    event: APIGatewayAuthorizerEventV2,
    context: LambdaContext,
) -> APIGatewayAuthorizerResponseV2TypeDef:
    """
    Validates that the AWS Token supplied in a cookie valid, and returns
    context about the user making a request.
    """
    logger.set_correlation_id(str(uuid4()))
    logger.info("Processing Authorization Request")

    if not event.identity_source:
        raise AuthorizationException("No Identity Source")

    tokens = aws_token_validation_service.get_tokens_from_authorizer_event(event)
    verified_tokens = aws_token_validation_service.validate_tokens(tokens)

    user_context = user_context_service.user_context_from_verified_tokens(
        verified_tokens,
        cookie=event.identity_source[0],
    )

    response = cast(
        APIGatewayAuthorizerResponseV2TypeDef,
        APIGatewayAuthorizerResponseV2(
            authorize=True,
            context=user_context,  # type: ignore [arg-type]
        ).asdict(),
    )
    logger.info("Successful")
    logger.debug("Response", extra={"response": response})
    return response
