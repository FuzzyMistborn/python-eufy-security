"""Define package errors."""


class EufySecurityError(Exception):
    """Define a base error."""

    pass


class ExpiredTokenError(EufySecurityError):
    """Define an error to throw upon an expired access token."""

    pass


class InvalidCredentialsError(EufySecurityError):
    """Define an error for unauthenticated accounts."""

    pass


class RequestError(EufySecurityError):
    """Define an error related to invalid requests."""

    pass
