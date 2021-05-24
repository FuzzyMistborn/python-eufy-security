"""Define tests for params."""
import pytest

from eufy_security.params import ParamType


def test_param_type_read_value():
    """Test ParamType read_value."""
    assert ParamType.CHIME_STATE.read_value(None) == None
    assert ParamType.CHIME_STATE.read_value('{"a": 1}') == {"a": 1}
    assert ParamType.SNOOZE_MODE.read_value("eyJhIjogMX0=") == {"a": 1}


def test_param_type_write_value():
    """Test ParamType write_value."""
    assert ParamType.CHIME_STATE.write_value(None) == "null"
    assert ParamType.CHIME_STATE.write_value({"a": 1}) == '{"a": 1}'
    assert ParamType.SNOOZE_MODE.write_value({"a": 1}) == "eyJhIjogMX0="
