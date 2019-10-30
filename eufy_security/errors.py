"""Define package errors."""


class EufySecurityError(Exception):
    """Define a base error."""

    pass


class InvalidCredentialsError(EufySecurityError):
    """Define an error for unauthenticated accounts."""

    pass


class RequestError(EufySecurityError):
    """Define an error related to invalid requests."""

    pass
