"""Define tests for devices."""
import json

import aiohttp
import pytest

from eufy_security import async_login
from eufy_security.device import Device
from eufy_security.params import ParamType
from eufy_security.types import DeviceType

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture, load_json_fixture


def test_properties():
    """Test device properties."""
    device_info = load_json_fixture("devices_list_response.json")["data"][0]
    device = Device(None, device_info)
    assert device.type == DeviceType.CAMERA
    assert device.hardware_version == "HAIYI-IMX323"
    assert device.last_camera_image_url == "https://path/to/image.jpg"
    assert device.mac == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    assert device.model == "T8111"
    assert device.name == "Driveway"
    assert device.serial == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1"
    assert device.software_version == "1.9.3"
    assert device.station_serial == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


@pytest.mark.asyncio
async def test_start_stream(aresponses, login_success_response):
    """Test starting the RTSP stream."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_response), status=200),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/get_devs_list",
        "post",
        aresponses.Response(
            text=load_fixture("devices_list_response.json"), status=200
        ),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/web/equipment/start_stream",
        "post",
        aresponses.Response(
            text=load_fixture("start_stream_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        device = next(iter(api.devices.values()))
        stream_url = await device.async_start_stream()
        assert stream_url == "rtmp://p2p-vir-6.eufylife.com/hls/123"


@pytest.mark.asyncio
async def test_stop_stream(aresponses, login_success_response):
    """Test stopping the RTSP stream."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_response), status=200),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/get_devs_list",
        "post",
        aresponses.Response(
            text=load_fixture("devices_list_response.json"), status=200
        ),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/web/equipment/stop_stream",
        "post",
        aresponses.Response(text=load_fixture("stop_stream_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        device = next(iter(api.devices.values()))
        await device.async_stop_stream()


@pytest.mark.asyncio
async def test_update(aresponses, login_success_response):
    """Test stopping the RTSP stream."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_response), status=200),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/get_devs_list",
        "post",
        aresponses.Response(
            text=load_fixture("devices_list_response.json"), status=200
        ),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/get_devs_list",
        "post",
        aresponses.Response(
            text=load_fixture("devices_list_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        device = next(iter(api.devices.values()))
        await device.async_update()


@pytest.mark.asyncio
async def test_set_params(aresponses, login_success_response):
    """Test setting params."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_response), status=200),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/get_devs_list",
        "post",
        aresponses.Response(
            text=load_fixture("devices_list_response.json"), status=200
        ),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/app/upload_devs_params",
        "post",
        aresponses.Response(
            text=load_fixture("upload_devs_params_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        device = next(iter(api.devices.values()))
        await device.async_set_params({ParamType.SNOOZE_MODE: True})
