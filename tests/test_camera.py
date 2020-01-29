"""Define tests for cameras."""
import json

import aiohttp
import pytest

from eufy_security import async_login

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_properties(aresponses, login_success_response):
    """Test authenticating with a bad email."""
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

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        camera = list(api.cameras.values())[0]
        assert camera.hardware_version == "HAIYI-IMX323"
        assert camera.last_camera_image_url == "https://path/to/image.jpg"
        assert camera.mac == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        assert camera.model == "T8111"
        assert camera.name == "Driveway"
        assert camera.serial == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1"
        assert camera.software_version == "1.9.3"
        assert camera.station_serial == "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


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
        camera = list(api.cameras.values())[0]
        stream_url = await camera.async_start_stream()
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
        camera = list(api.cameras.values())[0]
        await camera.async_stop_stream()


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
        camera = list(api.cameras.values())[0]
        await camera.async_update()
