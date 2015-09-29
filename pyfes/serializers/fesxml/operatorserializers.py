"""
Serializer classes for pyfes.operator
"""
from __future__ import absolute_import
import logging

from lxml import etree

from ...namespaces import namespaces
from ..expression import ExpressionParser
from ..operators import comparison

logger = logging.getLogger(__name__)


class BinaryComparisonOpSerializer(object):

    @classmethod
    def serialize(cls, operator):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], operator.name),
            matchCase="true" if operator.match_case else "false",
            matchAction=operator.match_action.value, nsmap=namespaces
        )
        first_expression_element = operator.first_expression.to_xml(
            as_string=False)
        element.append(first_expression_element)
        second_expression_element = operator.second_expression.to_xml(
            as_string=False)
        element.append(second_expression_element)
        return element

    @classmethod
    def deserialize(cls, xml_element):
        """Create a new object from an XML element"""
        operator_type = etree.QName(xml_element).localname
        return cls(
            ExpressionParser.parse(xml_element[0]),
            ExpressionParser.parse(xml_element[1]),
            operator_type=comparison.BinaryComparisonName(operator_type),
            match_case=xml_element.get("matchCase") == "true",
            match_action=xml_element.get("matchAction",
                                         comparison.MatchAction.any_)
        )


class LikeOpSerializer(object):

    @classmethod
    def serialize(cls, operator):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, xml_element):
        raise NotImplementedError


class BetweenOpSerializer(object):

    @classmethod
    def serialize(cls, operator):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, xml_element):
        raise NotImplementedError


class NullOpSerializer(object):

    @classmethod
    def serialize(cls, operator):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], operator.name),
            nsmap=namespaces
        )
        serialized_expression = operator.expression.to_xml(as_string=False)
        element.append(serialized_expression)
        return element

    @classmethod
    def deserialize(cls, xml_element):
        raise NotImplementedError


class NilOpSerializer(object):

    @classmethod
    def serialize(cls, operator):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, xml_element):
        raise NotImplementedError
