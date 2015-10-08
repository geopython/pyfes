"""
XML FES serializer.
"""

from __future__ import absolute_import
import logging

from lxml import etree

from ... import types
from ...utils import lazy_load

logger = logging.getLogger(__name__)


class FesXmlSerializer(object):
    serializer_map = {
        types.ValueReference.__name__: ".expression.ValueReferenceSerializer",
        types.Literal.__name__: ".expression.LiteralSerializer",
        types.Function.__name__: ".expression.FunctionSerializer",
        types.PropertyIsEqualTo.__name__:
            ".comparison.PropertyIsEqualToSerializer",
        types.PropertyIsNotEqualTo.__name__:
            ".comparison.PropertyIsNotEqualToSerializer",
        types.PropertyIsLessThan.__name__:
            ".comparison.PropertyIsLessThanSerializer",
        types.PropertyIsGreaterThan.__name__:
            ".comparison.PropertyIsGreaterThanSerializer",
        types.PropertyIsLessThanOrEqualTo.__name__:
            ".comparison.PropertyIsLessThanOrEqualToSerializer",
        types.PropertyIsGreaterThanOrEqualTo.__name__:
            ".comparison.PropertyIsGreaterThanOrEqualToSerializer",
        types.PropertyIsLike.__name__: ".comparison.PropertyIsLikeSerializer",
        "LowerBoundary": ".comparison.BoundarySerializer",
        "UpperBoundary": ".comparison.BoundarySerializer",
        types.PropertyIsBetween.__name__:
            ".comparison.PropertyIsBetweenSerializer",
        types.PropertyIsNull.__name__: ".comparison.PropertyIsNullSerializer",
        types.PropertyIsNil.__name__: ".comparison.PropertyIsNilSerializer",
        types.And.__name__: ".logical.AndSerializer",
        types.Or.__name__: ".logical.OrSerializer",
        types.Not.__name__: ".logical.NotSerializer",
    }

    @classmethod
    def deserialize(cls, xml_element, validate_schema=True):
        if isinstance(xml_element, basestring):
            xml_element = etree.fromstring(xml_element)
        # validate the xml_element with the fes2_0 schema, if needed
        if validate_schema:
            pass
        # match the xml_element with the appropriate serializer class
        deserializer_class_path = cls.serializer_map[
            etree.QName(xml_element).localname]
        deserializer = lazy_load(deserializer_class_path, package=__package__)
        return deserializer.deserialize(xml_element, validate_schema=False)

    @classmethod
    def serialize(cls, item, as_string=True):
        serializer_class_path = cls.serializer_map[type(item).__name__]
        serializer = lazy_load(serializer_class_path, package=__package__)
        return serializer.serialize(item, as_string=as_string)
