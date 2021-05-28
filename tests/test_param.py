"""Define tests for params."""

from datetime import datetime, timezone

import pytest

from eufy_security.param import Param, Params
from eufy_security.types import ParamType


def test_param_init_with_supported_type():
    """Test param init with a supported param type."""
    param = Param({"param_type": ParamType.CHIME_STATE.value, "param_value": "1",})
    assert param.type == ParamType.CHIME_STATE


def test_param_init_with_unsupported_type():
    """Test param init with unsupported param type."""
    with pytest.raises(ValueError):
        Param(
            {"param_type": -1, "param_value": "0",}
        )


def test_param_init_with_param_type():
    """Test param init with a param type."""
    param = Param(ParamType.CHIME_STATE)
    assert param.type == ParamType.CHIME_STATE
    assert param.param_info == {}


def test_param_hash():
    """Test param hash is the param type and id."""
    param = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 1,})
    assert hash(param) == hash((ParamType.CHIME_STATE.value, 1))


def test_param_equals():
    """Test param is equal to other param with the same param type and id."""
    param1 = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 1,})
    param2 = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 1,})
    assert param1 == param2


def test_param_not_equal():
    """Test param is not equal to other param with alternate param type or id."""
    param1 = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 1,})
    param2 = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 2,})
    param3 = Param({"param_type": ParamType.DETECT_EXPOSURE.value, "param_id": 1,})
    assert param1 != param2
    assert param1 != param3


def test_param_id():
    """Returns the param id."""
    param = Param({"param_type": ParamType.CHIME_STATE.value, "param_id": 123,})
    assert param.id == 123


def test_param_status():
    """Returns the param status."""
    param1 = Param({"param_type": ParamType.CHIME_STATE.value, "status": 1,})
    param2 = Param({"param_type": ParamType.CHIME_STATE.value, "status": 0,})
    assert param1.status == True
    assert param2.status == False


def test_param_value():
    """Test the parses param value."""
    param = Param({"param_type": ParamType.CHIME_STATE.value, "param_value": "1234",})
    assert param.value == 1234


def test_param_set_value():
    """Test setting the param value."""
    param = Param({"param_type": ParamType.CHIME_STATE.value, "param_value": "1234",})
    param.set_value(4567)
    assert param.value == 4567
    assert param.param_info["param_value"] == "4567"


def test_param_created():
    """Test the param created date."""
    param = Param(
        {"param_type": ParamType.CHIME_STATE.value, "create_time": 1565008299,}
    )
    assert param.created == datetime(2019, 8, 5, 12, 31, 39, tzinfo=timezone.utc)


def test_param_updated():
    """Test the param updated date."""
    param = Param(
        {"param_type": ParamType.CHIME_STATE.value, "update_time": 1565008299,}
    )
    assert param.updated == datetime(2019, 8, 5, 12, 31, 39, tzinfo=timezone.utc)


def test_params_init():
    """Test params init with a list."""
    params = Params(
        [
            {"param_type": ParamType.CHIME_STATE.value, "param_value": "1"},
            {"param_type": 0, "param_value": "0"},
            {"param_type": ParamType.DETECT_EXPOSURE.value, "param_value": "1"},
        ]
    )
    assert len(params) == 2


def test_params_contains():
    """Test params contains by param or param type."""
    params = Params([{"param_type": ParamType.CHIME_STATE, "param_id": 1},])
    assert ParamType.CHIME_STATE in params
    assert params[ParamType.CHIME_STATE] in params
    assert ParamType.DETECT_EXPOSURE not in params
    assert Param({"param_type": ParamType.DETECT_EXPOSURE.value}) not in params


def test_params_get_existing_item():
    """Test params get an existing item by param type."""
    params = Params(
        [
            {"param_type": ParamType.CHIME_STATE, "param_id": 1},
            {"param_type": ParamType.DETECT_EXPOSURE, "param_id": 2},
        ]
    )
    assert params[ParamType.CHIME_STATE].id == 1
    assert params[ParamType.CHIME_STATE.value].id == 1
    assert params[ParamType.CHIME_STATE.name].id == 1


def test_params_get_non_existing_item():
    """Test params get a non-existing item by param type."""
    params = Params([{"param_type": ParamType.DETECT_EXPOSURE, "param_id": 2},])
    with pytest.raises(KeyError):
        params[ParamType.CHIME_STATE]
    with pytest.raises(KeyError):
        params[ParamType.CHIME_STATE.value]
    with pytest.raises(KeyError):
        params[ParamType.CHIME_STATE.name]
    with pytest.raises(KeyError):
        params[0]


def test_params_set_existing_item():
    """Test params updating the value of an existing param."""
    params = Params(
        [{"param_type": ParamType.DETECT_EXPOSURE, "param_id": 2, "param_value": "1"},]
    )
    params[ParamType.DETECT_EXPOSURE] = 2
    assert params[ParamType.DETECT_EXPOSURE].param_info["param_value"] == "2"
    params[ParamType.DETECT_EXPOSURE.name] = 3
    assert params[ParamType.DETECT_EXPOSURE].param_info["param_value"] == "3"
    params[ParamType.DETECT_EXPOSURE.value] = 4
    assert params[ParamType.DETECT_EXPOSURE].param_info["param_value"] == "4"


def test_params_set_new_item():
    """Test params updating the value of an existing param."""
    params = Params(
        [{"param_type": ParamType.DETECT_EXPOSURE, "param_id": 2, "param_value": "1"},]
    )
    params[ParamType.CHIME_STATE] = 2
    assert params[ParamType.CHIME_STATE].param_info["param_value"] == "2"


def test_params_items():
    """Test params items."""
    params = Params(
        [
            {"param_type": ParamType.CHIME_STATE, "param_id": 1},
            {"param_type": ParamType.DETECT_EXPOSURE, "param_id": 2},
        ]
    )
    items = params.items()
    assert type(items) == dict
    assert len(items) == 2


def test_params_update():
    """Test params updating with a dictionary."""
    params = Params()
    params.update({ParamType.CHIME_STATE: 1})
    assert params[ParamType.CHIME_STATE].value == 1
