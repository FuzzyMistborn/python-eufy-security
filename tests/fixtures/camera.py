"""Define fixtures for cameras."""
import pytest


@pytest.fixture()
def start_stream_json():
    """Define a successful response to POST /api/v1/web/equipment/start_stream."""
    return {
        "code": 0,
        "msg": "Succeed.",
        "data": {"url": "rtmp://p2p-vir-6.eufylife.com/hls/123"},
    }


@pytest.fixture()
def stop_stream_json():
    """Define a successful response to POST /api/v1/web/equipment/stop_stream."""
    return {"code": 0, "msg": "Succeed."}
