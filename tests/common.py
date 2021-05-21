"""Define common test utilities."""
import json
import os

TEST_ACCESS_TOKEN = "abcde12345"
TEST_EMAIL = "user@host.com"
TEST_PASSWORD = "password12345"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()


def load_json_fixture(filename):
    """Load and parse a JSON encoded fixture."""
    return json.loads(load_fixture(filename))
