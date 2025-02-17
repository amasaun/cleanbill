class AuthorizationException(Exception):
    pass


class CookieHeaderMissing(AuthorizationException):
    """
    Exception raised for errors when the Cookie Header is not present on an
    Authorizer Event.

    Attributes:
        message (str): Explanation of the error
    """

    message: str

    def __init__(
        self,
        message: str = "Cookie Header not present, but is required",
    ) -> None:
        self.message = message

        super().__init__(self.message)


class AwsIdTokenMissingFromCookie(AuthorizationException):
    """
    Exception raised when the AWS ID Token cookie is not present on an Authorizer
    Event.
    """

    message: str

    def __init__(
        self,
        message: str = "AWS Id Token missing in Cookie",
    ) -> None:
        self.message = message

        super().__init__(message)


class AwsAccessTokenMissingFromCookie(AuthorizationException):
    """
    Exception raised when the AWS Access Token cookie is not present on an
    Authorizer Event.
    """

    message: str

    def __init__(
        self,
        message: str = "AWS Access Token missing in Cookie",
    ) -> None:
        self.message = message

        super().__init__(message)


class TokenIssuerDifference(AuthorizationException):
    """
    Exception raised when comparing the Issuer (iss) attribute of JWT tokens
    that should match.
    """

    message: str

    def __init__(
        self,
        message: str = "The compared `iss` attributes do not match.",
    ) -> None:
        self.message = message

        super().__init__(message)


class InvalidCognitoUserPool(AuthorizationException):
    """
    Exception raised when a CognitoUserPool is not valid.
    """

    message: str

    def __init__(
        self,
        message: str = "Cognito User Pool is Invalid or Not Found.",
    ) -> None:
        self.message = message

        super().__init__(message)


class UnexpectedJwkResponseFromCognitoUserPool(AuthorizationException):
    """
    Exception raised when a call to a Cognito User Pool's:
    https://cogntio-idp.{region}.amazonaws.com/{user_pool}/
    return a status_code that is not 200
    """

    message: str

    def __init__(
        self,
        message: str = "JWK could not be verified",
    ) -> None:
        self.message = message

        super().__init__(message)


class InvalidAccessToken(AuthorizationException):
    """
    Exception raised when it is determined that an AWS Access Token is invalid.
    """

    message: str

    def __init__(
        self,
        message: str = "Access Token is Invalid",
    ) -> None:
        self.message = message

        super().__init__(message)


class IdentitySourceMissing(AuthorizationException):
    """
    Exception raised when it is determined no identity_source is provided but
    expected in an Authorizer
    """

    message: str

    def __init__(
        self,
        message: str = "IdentitySource is Missing",
    ) -> None:
        self.message = message

        super().__init__(message)
