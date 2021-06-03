"""Define package errors."""
from typing import Dict, Type


class EufySecurityError(Exception):
    """Define a base error."""

    pass


class ConnectError(EufySecurityError):
    """Connection error."""

    pass


class NeedVerifyCodeError(EufySecurityError):
    """Need verification code error."""

    pass


class NetworkError(EufySecurityError):
    """Network error."""

    pass


class PhoneNoneSupportError(EufySecurityError):
    """Phone none support error."""

    pass


class ServerError(EufySecurityError):
    """Server error."""

    pass


class VerifyCodeError(EufySecurityError):
    """Verify code error."""

    pass


class VerifyCodeExpiredError(EufySecurityError):
    """Verification code has expired."""

    pass


class VerifyCodeMaxError(EufySecurityError):
    """Maximum attempts of verications error."""

    pass


class VerifyCodeNoneMatchError(EufySecurityError):
    """Verify code none match error."""

    pass


class VerifyCodePasswordError(EufySecurityError):
    """Verify code password error."""

    pass


class InvalidCredentialsError(EufySecurityError):
    """Define an error for unauthenticated accounts."""

    pass


class RequestError(EufySecurityError):
    """Define an error related to invalid requests."""

    pass


ERRORS: Dict[int, Type[EufySecurityError]] = {
    997: ConnectError,
    998: NetworkError,
    999: ServerError,
    26006: InvalidCredentialsError,
    26050: VerifyCodeError,
    26051: VerifyCodeExpiredError,
    26052: NeedVerifyCodeError,
    26053: VerifyCodeMaxError,
    26054: VerifyCodeNoneMatchError,
    26055: VerifyCodePasswordError,
    26058: PhoneNoneSupportError,
}


def raise_error(data: dict) -> None:
    """Raise the appropriate error based upon a response code."""
    code = data.get("code", 0)
    if code == 0:
        return
    cls = ERRORS.get(code, EufySecurityError)
    raise cls(data["msg"])
