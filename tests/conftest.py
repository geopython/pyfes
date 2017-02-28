"""General pytest configuration file for pyfes' tests."""

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "unit: Run onyl unit tests"
    )
