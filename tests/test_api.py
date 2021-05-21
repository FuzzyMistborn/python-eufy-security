"""Define tests for the base API."""
from datetime import datetime, timedelta
import json

import aiohttp
import pytest

from eufy_security import async_login
from eufy_security.errors import InvalidCredentialsError, RequestError
from eufy_security.params import ParamType

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_401_refresh_failure(aresponses, login_success_response):
    """Test that multiple 401 responses in a row raises the right exception."""
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
        aresponses.Response(text=None, status=401),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/passport/login",
        "post",
        aresponses.Response(text=None, status=401),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_401_refresh_success(aresponses, login_success_response):
    """Test that a 401 response re-authenticates successfully."""
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
            text=load_fixture("devices_list_response.json"), status=401
        ),
    )
    aresponses.add(
        "security-app.eufylife.com",
        "/v1/passport/login",
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
        assert len(api.devices) == 2


@pytest.mark.asyncio
async def test_bad_email(aresponses):
    """Test authenticating with a bad email."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(
            text=load_fixture("login_failure_invalid_email_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login("bad_email@host.com", TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_bad_password(aresponses):
    """Test authenticating with a bad password."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(
            text=load_fixture("login_failure_invalid_password_response.json"),
            status=200,
        ),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login(TEST_EMAIL, "bad_password", websession)


@pytest.mark.asyncio
async def test_empty_response(aresponses, login_success_response):
    """Test the odd use case that arises when a response is empty."""
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
        aresponses.Response(text=load_fixture("empty_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(RequestError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_expired_access_token(aresponses, login_success_response):
    """Test that an expired access token refreshes automatically and correctly."""
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
        "/v1/passport/login",
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
        api._token_expiration = datetime.now() - timedelta(seconds=10)
        await api.async_update_device_info()
        assert len(api.devices) == 2


@pytest.mark.asyncio
async def test_get_history(aresponses, login_success_response):
    """Test getting the device history."""
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
        "/v1/event/app/get_all_history_record",
        "post",
        aresponses.Response(text=load_fixture("history_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        history = await api.async_get_history()
        assert len(history) == 2


@pytest.mark.asyncio
async def test_http_error(aresponses, login_success_response):
    """Test the Eufy Security web API returning a non-2xx HTTP error code."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=None, status=500),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(RequestError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_login_success(aresponses, login_success_response):
    """Test a successful login and API object creation."""
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
        assert api._email == TEST_EMAIL
        assert api._password == TEST_PASSWORD
        assert api._token is not None
        assert api._token_expiration is not None
        assert len(api.devices) == 2


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
        stream_url = await api.async_start_stream(device)
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
        await api.async_stop_stream(device)

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
        await api.async_set_params(device, {ParamType.SNOOZE_MODE: True})
