"""
Unit tests for the expression module.

Run these tests with nose.
"""

from __future__ import absolute_import
from nose.tools import eq_, assert_is_not_none
from unittest import TestCase
import logging

from lxml import etree

from pyfes import expression
from pyfes.namespaces import namespaces

logger = logging.getLogger(__name__)


class BaseTestCase(TestCase):

    @classmethod
    def setupClass(cls):
        cls.value_reference_text = "something"
        cls.value_reference_element = etree.Element(
            "{{{}}}ValueReference".format(namespaces["fes"]), nsmap=namespaces)
        cls.value_reference_element.text = cls.value_reference_text
        cls.value_reference_expression = expression.ValueReference(
            cls.value_reference_text)
        cls.literal_text = "something"
        cls.literal_element = etree.Element(
            "{{{}}}Literal".format(namespaces["fes"]), nsmap=namespaces)
        cls.literal_element.text = cls.literal_text
        cls.literal_expression = expression.Literal(cls.literal_text)


class TestExpressionParser(BaseTestCase):

    @classmethod
    def setupClass(cls):
        super(TestExpressionParser, cls).setupClass()

    def test_parse_value_reference(self):
        """ExpressionParser parses fes:ValueReference XMl elements correctly
        """
        instance = expression.ExpressionParser.parse(
            self.value_reference_element)
        eq_(instance.value, self.value_reference_expression.value)

    def test_parse_literal(self):
        """ExpressionParser parses fes:Literal XML elements correctly"""
        instance = expression.ExpressionParser.parse(
            self.literal_element)
        eq_(instance.value, self.literal_expression.value)


class TestValueReference(BaseTestCase):

    @classmethod
    def setupClass(cls):
        super(TestValueReference, cls).setupClass()

    def test_deserialize(self):
        """Deserialize ValueReference from XML works correctly"""
        instance = expression.ValueReference.deserialize(
            self.value_reference_element)
        eq_(instance.value, self.value_reference_text)

    def test_serialize(self):
        """Serialize ValueReference to XML works correctly"""
        serialized_xml_el = self.value_reference_expression.serialize(
            as_string=False)
        eq_(self.value_reference_element.tag, serialized_xml_el.tag)
        eq_(self.value_reference_element.text, serialized_xml_el.text)


class TestLiteral(BaseTestCase):

    @classmethod
    def setupClass(cls):
        super(TestLiteral, cls).setupClass()

    def test_deserialize(self):
        """Deserialize Literal from XML works correctly"""
        instance = expression.Literal.deserialize(self.literal_element)
        eq_(instance.value, self.literal_text)

    def test_serialize(self):
        """Serialize Literal to XML works correctly"""
        serialized_xml_el = self.literal_expression.serialize(as_string=False)
        eq_(self.literal_element.tag, serialized_xml_el.tag)
