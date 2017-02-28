"""Tests for the custom pyfes types"""

import logging

import pytest

from pyfes import filterpredicates

pytestmark = pytest.mark.unit
logger = logging.getLogger(__name__)


def test_filter():
    phony_operator = filterpredicates.PropertyIsGreaterThan(
        filterpredicates.ValueReference("name"),
        filterpredicates.Literal("dummy")
    )
    f1 = filterpredicates.Filter(phony_operator)
    assert f1.filter_ == phony_operator


def test_expression():
    raise NotImplementedError


class TestValueReference():

    @pytest.mark.parametrize("value, expected", [
        ("value1", "value1"),
        (1, "1"),
    ])
    def test_value(self, value, expected):
        value_reference = filterpredicates.ValueReference(value)
        assert value_reference.value == expected
