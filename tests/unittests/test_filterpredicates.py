"""Tests for the custom pyfes types"""

import logging

import pytest

from pyfes.fes20 import operators

pytestmark = pytest.mark.unit
logger = logging.getLogger(__name__)


def test_filter():
    phony_operator = operators.PropertyIsGreaterThan(
        operators.ValueReference("name"),
        operators.Literal("dummy")
    )
    f1 = operators.Filter(phony_operator)
    assert f1.filter_ == phony_operator


def test_expression():
    raise NotImplementedError


class TestValueReference():

    @pytest.mark.parametrize("value, expected", [
        ("value1", "value1"),
        (1, "1"),
    ])
    def test_value(self, value, expected):
        value_reference = operators.ValueReference(value)
        assert value_reference.value == expected
