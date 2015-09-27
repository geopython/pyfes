"""
Unit tests for the expression module.

Run these tests with nose.
"""

from __future__ import absolute_import
from nose.tools import eq_
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


class TestValueReference(TestCase):

    @classmethod
    def setupClass(cls):
        cls.value_reference_text = "Dummy"
        xml_expression = (
            "<fes:ValueReference xmlns:fes='{0[fes]}' "
            "xmlns:xsi='{0[xsi]}' xsi:schemaLocation='{0[fes]} "
            "http://schemas.opengis.net/filter/2.0.0/filterAll.xsd'>"
            "{1}</fes:ValueReference>".format(namespaces,
                                              cls.value_reference_text)
        )
        cls.value_reference_element = etree.fromstring(xml_expression)

    def test_from_xml(self):
        """Deserialize ValueReference from XML works correctly"""
        instance = expression.ValueReference.from_xml(
            self.value_reference_element)
        eq_(instance.value, self.value_reference_text)

    def test_to_xml(self):
        """Serialize ValueReference to XML works correctly"""
        instance = expression.ValueReference(self.value_reference_text)
        serialized_xml_el = instance.to_xml(as_string=False)
        eq_(instance.XML_ENTITY_NAME,
            etree.QName(serialized_xml_el.tag).localname)
        eq_(instance.value, serialized_xml_el.text)


class TestLiteral(TestCase):

    @classmethod
    def setupClass(cls):
        cls.literal_value = "30"
        xml_expression = (
            "<fes:Literal xmlns:fes='{0[fes]}' xmlns:xsi='{0[xsi]}' "
            "xsi:schemaLocation='{0[fes]} "
            "http://schemas.opengis.net/filter/2.0.0/filterAll.xsd'>"
            "{1}</fes:Literal>".format(namespaces, cls.literal_value)
        )
        cls.literal_element = etree.fromstring(xml_expression)

    def test_from_xml(self):
        """Deserialize Literal from XML works correctly"""
        instance = expression.Literal.from_xml(self.literal_element)
        eq_(instance.value, self.literal_value)

    def test_to_xml(self):
        """Serialize Literal to XML works correctly"""
        instance = expression.Literal(self.literal_value)
        serialized_xml_el = instance.to_xml(as_string=False)
        eq_(instance.XML_ENTITY_NAME,
            etree.QName(serialized_xml_el.tag).localname)
