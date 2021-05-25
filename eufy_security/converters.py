"""Define converters."""
import base64
from datetime import datetime, timezone
import json
from typing import Any, Union


class StringConverter:
    """Convert values to and from String."""

    @staticmethod
    def loads(value: str) -> str:
        """Convert the value into a string."""
        return str(value)

    @staticmethod
    def dumps(value: str) -> str:
        """Convert the value into a string."""
        return str(value)


class NumberConverter:
    """Convert values to and from Number."""

    @staticmethod
    def loads(value: str) -> Union[int, float]:
        """Convert the value into a float or an integer."""
        if "." in str(value):
            return float(value)
        else:
            return int(value)

    @staticmethod
    def dumps(value: Union[int, float]) -> str:
        """Convert a float or integer into a string."""
        return str(value)


class BoolConverter:
    """Convert boolean-like values."""

    @staticmethod
    def loads(value: str) -> bool:
        """Convert the value into a boolean."""
        return bool(int(value))

    @staticmethod
    def dumps(value: bool) -> str:
        """Convert the boolean into a string."""
        return str(int(value))


class JsonConverter:
    """Convert values to and from JSON."""

    @staticmethod
    def loads(value: str) -> Any:
        """Parse the value as JSON."""
        if value == "":
            return None
        else:
            return json.loads(value)

    @staticmethod
    def dumps(value: Any) -> str:
        """Serialise the value as JSON."""
        if value is None:
            return ""
        else:
            return json.dumps(value)


class JsonBase64Converter:
    """Wraps and unwraps base64 values then convert to and from JSON."""

    @staticmethod
    def loads(value: str) -> Any:
        """Decode the value from base64 then from JSON."""
        decoded_value = base64.b64decode(value, validate=True).decode()
        return JsonConverter.loads(decoded_value)

    @staticmethod
    def dumps(value: Any) -> str:
        """Encode the value to JSON and then encodes in base64."""
        encoded_value = JsonConverter.dumps(value)
        return base64.b64encode(encoded_value.encode()).decode()


class DatetimeConverter:
    """Convert values to and from datetimes."""

    @staticmethod
    def loads(value: str) -> datetime:
        """Convert a timestamp into a datetime."""
        return datetime.fromtimestamp(int(value), timezone.utc)

    @staticmethod
    def dumps(value: datetime) -> str:
        """Convert datetime into a timestamp."""
        return str(int(value.replace(tzinfo=timezone.utc).timestamp()))
