"""Define package errors."""
from typing import Dict, Type


class EufySecurityError(Exception):
    """Define a base error."""

    pass


class InvalidCredentialsError(EufySecurityError):
    """Define an error for unauthenticated accounts."""

    pass


class RequestError(EufySecurityError):
    """Define an error related to invalid requests."""

    pass


ERRORS: Dict[int, Type[EufySecurityError]] = {26006: InvalidCredentialsError}


def raise_error(data: dict) -> None:
    """Raise the appropriate error based upon a response code."""
    cls = ERRORS.get(data["code"], EufySecurityError)
    raise cls(data["msg"])
