"""
Unit tests for the operators.comparison module.

Run these tests with nose.
"""

import logging
from unittest import TestCase

from nose.tools import eq_
import mock

from pyfes.operators import comparison

logger = logging.getLogger(__name__)


class TestBinaryComparisonOperator(TestCase):

    @classmethod
    def setup_class(cls):
        cls.first_expression = None
        cls.second_expression = None

    def test_should_create_operator(self):
        for item in comparison.BinaryComparisonName:
            operator = comparison.BinaryComparisonOperator(
                self.first_expression, self.second_expression, item)
            eq_(operator.name, item.value)
