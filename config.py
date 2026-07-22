"""Runtime configuration.

Every value can be overridden with an environment variable, so the same suite
can be pointed at any deployment of the application under test:

    BASE_URL=https://staging.example.com pytest

The CLI option ``--base-url`` (provided by pytest-base-url) takes precedence
over the environment variable; see ``conftest.py``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BASE_URL = "https://the-internet.herokuapp.com"


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


def get_base_url() -> str:
    """Base URL of the environment under test, without a trailing slash."""
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_credentials() -> Credentials:
    """Valid credentials for the environment under test.

    Defaults are the public demo credentials. On a real project these would
    have no defaults at all and would come from a secret store.
    """
    return Credentials(
        username=os.getenv("APP_USERNAME", "tomsmith"),
        password=os.getenv("APP_PASSWORD", "SuperSecretPassword!"),
    )
