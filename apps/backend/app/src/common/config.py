from aws_lambda_powertools.utilities.parser.pydantic import BaseSettings


class Config(BaseSettings):
    IDP_TABLE: str
    CENTRAL_API_ENDPOINT: str
