"""Define common test utilities."""
import os

TEST_ACCESS_TOKEN = "abcde12345"
TEST_EMAIL = "user@host.com"
TEST_PASSWORD = "password12345"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
