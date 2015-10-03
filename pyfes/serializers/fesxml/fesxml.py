"""
XML FES serializer.
"""

from __future__ import absolute_import
import logging

from lxml import etree

from ... import types
from . import expression
from . import comparison

logger = logging.getLogger(__name__)


class FesXmlSerializer(object):
    serializer_map = {
        types.ValueReference.__name__: expression.ValueReferenceSerializer,
        types.Literal.__name__: expression.LiteralSerializer,
        types.Function.__name__: expression.FunctionSerializer,
        types.PropertyIsEqualTo.__name__:
            comparison.PropertyIsEqualToSerializer,
        types.PropertyIsNotEqualTo.__name__:
            comparison.PropertyIsNotEqualToSerializer,
        types.PropertyIsLessThan.__name__:
            comparison.PropertyIsLessThanSerializer,
        types.PropertyIsGreaterThan.__name__:
            comparison.PropertyIsGreaterThanSerializer,
        types.PropertyIsLessThanOrEqualTo.__name__:
            comparison.PropertyIsLessThanOrEqualToSerializer,
        types.PropertyIsGreaterThanOrEqualTo.__name__:
            comparison.PropertyIsGreaterThanOrEqualToSerializer,
        types.PropertyIsLike.__name__: comparison.PropertyIsLikeSerializer,
    }

    @classmethod
    def deserialize(cls, xml_element, validate_schema=True):
        # first get an etree.Element from input xml_element, if necessary
        if isinstance(xml_element, basestring):
            xml_element = etree.fromstring(xml_element)
        # then validate the xml_element with the fes2_0 schema, if needed
        if validate_schema:
            pass
        # then match the xml_element with the appropriate serializer class
        deserializer = cls.serializer_map.get(
            etree.QName(xml_element).localname)
        return deserializer.deserialize(xml_element, validate_schema=False)

    @classmethod
    def serialize(cls, item, as_string=True):
        serializer = cls.serializer_map.get(type(item).__name__)
        return serializer.serialize(item, as_string=as_string)
