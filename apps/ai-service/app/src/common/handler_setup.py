from aws_lambda_powertools import Logger
from mypy_boto3_dynamodb.service_resource import Table

from src.repositories.idp_repository import IDPRepository
from src.repositories.user_repository import UserRepository
from src.services.aws_token_validation_service import AwsTokenValidationService
from src.services.idp_service import IDPService
from src.services.user_service import UserService


def create_idp_service(table: Table, logger: Logger) -> IDPService:
    return IDPService(IDPRepository(table), logger=logger)


def create_aws_token_validation_service(
    table: Table,
    logger: Logger = Logger(),
) -> AwsTokenValidationService:
    return AwsTokenValidationService(
        idp_service=create_idp_service(
            table,
            logger=logger,
        ),
        logger=logger,
    )


def create_user_service(
    table: Table,
    logger: Logger = Logger(),
) -> UserService:
    user_repository = UserRepository(
        table=table,
    )
    return UserService(
        repository=user_repository,
        logger=logger,
    )
