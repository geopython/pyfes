"""
Unit tests for the operators.comparison module.

Run these tests with nose.
"""

from __future__ import absolute_import
from nose.tools import eq_, assert_is_not_none
from unittest import TestCase
import logging
from copy import deepcopy

from lxml import etree

from pyfes import expression
from pyfes.operators import comparison
from pyfes.namespaces import namespaces

logger = logging.getLogger(__name__)


class BaseTestCase(TestCase):

    @classmethod
    def setupClass(cls):
        cls.value_ref_text = "something"
        cls.literal_text = "100"
        cls.property_is_equal_to_operator = comparison.BinaryComparisonOperator(
            expression.ValueReference(cls.value_ref_text),
            expression.Literal(cls.literal_text),
            comparison.BinaryComparisonName.property_is_equal_to,
        )
        cls.property_is_like_operator = comparison.LikeOperator(
            expression.ValueReference(cls.value_ref_text),
            expression.Literal(cls.literal_text),
            wild_card="*", single_char="?", escape_char=r"\\"
        )
        value_ref_el = etree.Element(
            "{{{}}}ValueReference".format(namespaces["fes"])
        )
        value_ref_el.text = cls.value_ref_text
        literal_el = etree.Element(
            "{{{}}}Literal".format(namespaces["fes"])
        )
        literal_el.text = cls.literal_text
        cls.property_is_equal_to_element = etree.Element(
            "{{{}}}PropertyIsEqualTo".format(namespaces["fes"]),
            nsmap=namespaces
        )
        cls.property_is_equal_to_element.append(deepcopy(value_ref_el))
        cls.property_is_equal_to_element.append(deepcopy(literal_el))

        cls.property_is_like_element = etree.Element(
            "{{{}}}PropertyIsLike".format(namespaces["fes"]),
            wildCard="*", singleChar="?", escapeChar=r"\\", nsmap=namespaces)
        cls.property_is_like_element.append(deepcopy(value_ref_el))
        cls.property_is_like_element.append(deepcopy(literal_el))


class TestOperatorParser(BaseTestCase):

    @classmethod
    def setupClass(cls):
        super(TestOperatorParser, cls).setupClass()

    def test_parse_property_is_equal_to_operator(self):
        """OperatorParser parses fes:PropertyIsEqualTo XMl elements"""
        binary_comparison_operator = comparison.OperatorParser.parse(
            self.property_is_equal_to_element)
        eq_(binary_comparison_operator.operator_type, 
            self.property_is_equal_to_operator.operator_type)

    def test_parse_property_is_like_operator(self):
        """OperatorParser parses fes:PropertyIsLike XML elements"""
        like_operator = comparison.OperatorParser.parse(
            self.property_is_like_element)
        eq_(like_operator.__class__, self.property_is_like_operator.__class__)
