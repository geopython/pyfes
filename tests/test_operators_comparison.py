"""
Unit tests for the operators.comparison module.

Run these tests with nose.
"""

from __future__ import absolute_import
from nose.tools import eq_, assert_is_not_none
from unittest import TestCase
import logging

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
        cls.property_is_equal_to_text = """
        <fes:PropertyIsEqualTo
          xmlns:fes="{0[fes]}"
          xmlns:xsi="{0[xsi]}"
          xsi:schemaLocation="{0[fes]}
            http://schemas.opengis.net/filter/2.0.0/filterAll.xsd">
          <fes:ValueReference>{1}</fes:ValueReference>
          <fes:Literal>{2}</fes:Literal>
        </fes:PropertyIsEqualTo>
        """.format(namespaces, cls.value_ref_text, cls.literal_text)
        cls.property_is_like_text = """
        <fes:PropertyIsLike
          xmlns:fes="{0[fes]}"
          xmlns:xsi="{0[xsi]}"
          xsi:schemaLocation="{0[fes]}
            http://schemas.opengis.net/filter/2.0.0/filterAll.xsd">
          wildCard="*"
          singlechar="?"
          escapeChar="\\"
          <fes:ValueReference>{1}</fes:ValueReference>
          <fes:Literal>{2}</fes:Literal>
        </fes:PropertyIsLike>
        """.format(namespaces, cls.value_ref_text, cls.literal_text)

        cls.property_is_equal_to = comparison.BinaryComparisonOperator(
            expression.ValueReference(cls.value_ref_text),
            expression.Literal(cls.literal_text),
            comparison.BinaryComparisonName.property_is_equal_to,
        )
        cls.property_is_like = comparison.LikeOperator(
            expression.ValueReference(cls.value_ref_text),
            expression.Literal(cls.literal_text),
            wild_card="*", single_char="?", escape_char=r"\\"
        )
        cls.property_is_equal_to_element = etree.fromstring(
            cls.property_is_equal_to_text)
        cls.property_is_like_element = etree.fromstring(
            cls.property_is_like_text)


class TestOperatorParser(BaseTestCase):

    @classmethod
    def setupClass(cls):
        super(TestOperatorParser, cls).setupClass()

    def test_parse_property_is_equal_to_operator(self):
        """OperatorParser parses fes:PropertyIsEqualTo XMl elements"""
        binary_comparison_operator = comparison.OperatorParser.parse(
            self.property_is_equal_to_element)
        eq_(binary_comparison_operator.operator_type,
            self.property_is_equal_to.operator_type)

    def test_parse_property_is_like_operator(self):
        """OperatorParser parses fes:PropertyIsLike XML elements"""
        like_operator = comparison.OperatorParser.parse(
            self.property_is_like_element)
        eq_(like_operator.__class__, self.property_is_like.__class__)
