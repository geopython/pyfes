"""Tests for the custom pyfes types"""

from nose.tools import eq_
from unittest import TestCase
import logging

from lxml import etree

from pyfes import types

logger = logging.getLogger(__name__)


class TestTypes(TestCase):

    @classmethod
    def setup_class(cls):
        cls.value_reference = types.ValueReference("foo")
        cls.literal = types.Literal("baz")

    def test_should_create_expression_types(self):
        value = "something"
        value_reference = types.ValueReference(value)
        eq_(value_reference.value, value)

        first_literal = types.Literal(value)
        eq_(first_literal.value, value)
        eq_(first_literal.type_, "string")
        type_ = "other"
        second_literal = types.Literal(value, type_)
        eq_(second_literal.type_, type_)

        name = "foo"
        args = ["this", "that"]
        first_func = types.Function(name)
        eq_(first_func.name, name)
        eq_(first_func.arguments, [])
        second_func = types.Function(name, args)
        eq_(second_func.arguments, args)

    def test_should_create_comparison_operators(self):
        op1 = types.PropertyIsEqualTo(self.value_reference, self.literal)
