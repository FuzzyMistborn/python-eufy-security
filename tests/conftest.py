"""Define fixtures, constants, etc. available for all tests."""
from datetime import datetime, timedelta

import pytest

from .common import TEST_ACCESS_TOKEN, TEST_EMAIL


@pytest.fixture()
def login_success_response():
    """Define a successful response to POST /api/v1/passport/login."""
    return {
        "code": 0,
        "msg": "Succeed.",
        "data": {
            "user_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "email": TEST_EMAIL,
            "nick_name": "",
            "auth_token": TEST_ACCESS_TOKEN,
            "token_expires_at": int((datetime.now() + timedelta(days=1)).timestamp()),
            "avatar": "",
            "invitation_code": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "inviter_code": "",
            "mac_addr": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "domain": "security-app.eufylife.com",
            "ab_code": "US",
            "geo_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "privilege": 0,
            "params": [
                {"param_type": 10000, "param_value": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
            ],
        },
    }
