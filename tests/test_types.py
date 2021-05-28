"""Define tests for params."""
import pytest

from eufy_security.types import ParamType


def test_param_type_loads():
    """Test ParamType loads."""
    assert ParamType.CHIME_STATE.loads("123") == 123
    assert ParamType.DETECT_SWITCH.loads('{"a": 1}') == {"a": 1}
    assert ParamType.SNOOZE_MODE.loads("eyJhIjogMX0=") == {"a": 1}


def test_param_type_dumps():
    """Test ParamType dumps."""
    assert ParamType.CHIME_STATE.dumps(123) == "123"
    assert ParamType.DETECT_SWITCH.dumps({"a": 1}) == '{"a": 1}'
    assert ParamType.SNOOZE_MODE.dumps({"a": 1}) == "eyJhIjogMX0="


def test_param_type_lookup():
    """Test ParamType lookup."""
    assert ParamType.lookup(ParamType.CHIME_STATE.value) == ParamType.CHIME_STATE
    assert ParamType.lookup(ParamType.CHIME_STATE.name) == ParamType.CHIME_STATE
    assert ParamType.lookup(ParamType.CHIME_STATE) == ParamType.CHIME_STATE
    with pytest.raises(ValueError):
        ParamType.lookup(0)
