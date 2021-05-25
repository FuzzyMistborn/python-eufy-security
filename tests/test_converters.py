"""Define tests for converters."""

from datetime import datetime, timezone

import pytest

from eufy_security.converters import *


def test_string_loads():
    """Test loading data as a string."""
    assert StringConverter.loads("foobar") == "foobar"
    assert StringConverter.loads("123") == "123"


def test_string_dumps():
    """Test dumping data as a string."""
    assert StringConverter.dumps("foobar") == "foobar"
    assert StringConverter.dumps(123) == "123"


def test_number_loads():
    """Test loading data as a number."""
    assert NumberConverter.loads("123") == 123
    assert NumberConverter.loads("123.4") == 123.4


def test_number_dumps():
    """Test dumping data as a number."""
    assert NumberConverter.dumps(123) == "123"
    assert NumberConverter.dumps(123.4) == "123.4"


def test_boolean_loads():
    """Test loading data as a boolean."""
    assert BoolConverter.loads("1") == True
    assert BoolConverter.loads("0") == False


def test_boolean_dumps():
    """Test dumping data as a boolean."""
    assert BoolConverter.dumps(True) == "1"
    assert BoolConverter.dumps(False) == "0"


def test_json_loads():
    """Test loading json-encoded data as an object."""
    assert JsonConverter.loads('{"a": 1}') == {"a": 1}
    assert JsonConverter.loads("") == None


def test_json_dumps():
    """Test dumping data as a json-encoded string."""
    assert JsonConverter.dumps({"a": 1}) == '{"a": 1}'
    assert JsonConverter.dumps(None) == ""


def test_json_base64_loads():
    """Test loading base64 json-encoded data as an object."""
    assert JsonBase64Converter.loads("eyJhIjogMX0=") == {"a": 1}


def test_json_base64_dumps():
    """Test dumping data as a base64 json-encoded string."""
    assert JsonBase64Converter.dumps({"a": 1}) == "eyJhIjogMX0="


def test_datetime_loads():
    """Test loading json-encoded data as an object."""
    dt = datetime(2019, 8, 5, 12, 31, 39, tzinfo=timezone.utc)
    assert DatetimeConverter.loads("1565008299") == dt


def test_datetime_dumps():
    """Test dumping data as a json-encoded string."""
    dt = datetime(2019, 8, 5, 12, 31, 39, tzinfo=timezone.utc)
    assert DatetimeConverter.dumps(dt) == "1565008299"
