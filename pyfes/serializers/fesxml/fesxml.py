"""
XML FES serializer.
"""

from __future__ import absolute_import
import logging

from lxml import etree

from . import operatorserializers
from ...namespaces import namespaces
from ...types import Filter

logger = logging.getLogger(__name__)


class FilterSerializer(object):

    @classmethod
    def serialize(cls, filter_):
        """Serialize the input filter to XML"""
        element = etree.Element("{{{0[fes]}}}{1}".format(namespaces,
                                type(filter_).__name__, nsmap=namespaces))
        serialized_operator = OperatorSerializer.serialize(filter_.filter_)
        element.append(serialized_operator)
        return element

    @classmethod
    def deserialize(cls, xml_element):
        """Deserialize the input XML to a pyfes.Filter"""
        return Filter(OperatorSerializer.deserialize(xml_element[1]))


class OperatorSerializer(object):
    serialization_map = {
        comparison.BinaryComparisonOperator:
            operatorserializers.BinaryComparisonOpSerializer,
        comparison.LikeOperator: operatorserializers.LikeOpSerializer,
    }

    @classmethod
    def serialize(cls, operator):
        serializer_class = cls.serialization_map.get(operator.__class__)
        return serializer_class.serialize(operator)

    @classmethod
    def deserialize(cls, xml_element):
        op_name = etree.QName(xml_element).localname
        serializer = None
        for op_class, serializer_class in cls.serialization_map.items():
            if op_class.name == op_name:
                serializer = serializer_class
        return serializer.deserialize(xml_element)
