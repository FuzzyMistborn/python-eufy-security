"""Define tests for the base API."""
from datetime import datetime, timedelta
import json

import aiohttp
import pytest

from eufy_security import async_login
from eufy_security.errors import InvalidCredentialsError, RequestError

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import (
    devices_list_json,
    empty_response,
    history_json,
    login_invalid_email_json,
    login_invalid_password_json,
    login_success_json,
)


@pytest.mark.asyncio
async def test_401_refresh_failure(
    aresponses, devices_list_json, event_loop, login_success_json
):
    """Test that multiple 401 responses in a row raises the right exception."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=None, status=401),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=None, status=401),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_401_refresh_success(
    aresponses, devices_list_json, event_loop, login_success_json
):
    """Test that a 401 response re-authenticates successfully."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=401),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        assert len(api.cameras) == 2


@pytest.mark.asyncio
async def test_bad_email(aresponses, event_loop, login_invalid_email_json):
    """Test authenticating with a bad email."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_invalid_email_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login("bad_email@host.com", TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_bad_password(aresponses, event_loop, login_invalid_password_json):
    """Test authenticating with a bad pasword."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_invalid_password_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(InvalidCredentialsError):
            await async_login(TEST_EMAIL, "bad_password", websession)


@pytest.mark.asyncio
async def test_empty_response(
    aresponses, empty_response, event_loop, login_success_json
):
    """Test the odd use case that arises when a response is empty."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(RequestError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_expired_access_token(
    aresponses, devices_list_json, event_loop, login_success_json
):
    """Test that an expired access token refreshes automatically and correctly."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        api._token_expiration = datetime.now() - timedelta(seconds=10)
        await api.async_update_device_info()
        assert len(api.cameras) == 2


@pytest.mark.asyncio
async def test_get_history(
    aresponses, devices_list_json, event_loop, history_json, login_success_json
):
    """Test a successful login and API object creation."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/event/app/get_all_history_record",
        "post",
        aresponses.Response(text=json.dumps(history_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        history = await api.async_get_history()
        assert len(history) == 2


@pytest.mark.asyncio
async def test_http_error(aresponses, event_loop, login_success_json):
    """Test the Eufy Security web API returning a non-2xx HTTP error code."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=None, status=500),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(RequestError):
            await async_login(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_login_success(
    aresponses, devices_list_json, event_loop, login_success_json
):
    """Test a successful login and API object creation."""
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/passport/login",
        "post",
        aresponses.Response(text=json.dumps(login_success_json), status=200),
    )
    aresponses.add(
        "mysecurity.eufylife.com",
        "/api/v1/app/get_devs_list",
        "post",
        aresponses.Response(text=json.dumps(devices_list_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        api = await async_login(TEST_EMAIL, TEST_PASSWORD, websession)
        assert api._email == TEST_EMAIL
        assert api._password == TEST_PASSWORD
        assert api._token is not None
        assert api._token_expiration is not None
        assert len(api.cameras) == 2
