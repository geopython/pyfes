"""
Unit tests for the schemaparser module.

Run these tests with nose.
"""

from __future__ import absolute_import
from nose.tools import eq_
from unittest import TestCase
import logging

from lxml import etree

from pyfes import expression
from pyfes.schemaparsers import SchemaParser

logger = logging.getLogger(__name__)


class TestSchemaParser(TestCase):

    @classmethod
    def setupClass(cls):
        cls.test_filter = """
        <fes:Filter
          xmlns:fes="http://www.opengis.net/fes/2.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.opengis.net/fes/2.0
          http://schemas.opengis.net/filter/2.0.0/filterAll.xsd">
            <fes:PropertyIsEqualTo>
                <fes:ValueReference>SomeProperty</fes:ValueReference>
                <fes:Literal>100</fes:Literal>
            </fes:PropertyIsEqualTo>
        </fes:Filter>
        """
        cls.invalid_schema_path = "/fake/path"
        # find a better way to provide the schema_path
        cls.valid_schema_path = ("/home/ricardo/dev/pycsw/pycsw/pycsw/core/"
            "schemas/ogc/filter/2.0/filterAll.xsd")

    def test_new_parser(self):
        """SchemaParser is able to create a parser for fes 2.0"""
        valid_parser = SchemaParser(self.valid_schema_path)
        valid_parser.validate_xml(etree.fromstring(self.test_filter))

