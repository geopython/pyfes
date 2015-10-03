"""Serializer classes for fes comparison operator types"""

from __future__ import absolute_import
from __future__ import unicode_literals
import logging

from lxml import etree

from ... import types
from ...namespaces import namespaces
from .base import BaseSerializer
from .expression import ExpressionSerializer

logger = logging.getLogger(__name__)


class BinaryOperatorSerializer(BaseSerializer):

    @classmethod
    def _deserialize(cls, xml_element):
        match_case = False
        if xml_element.get("matchCase", "true") == "true":
            match_case = True
        return cls.TYPE_(
            first_expression=ExpressionSerializer.deserialize(xml_element[0]),
            second_expression=ExpressionSerializer.deserialize(xml_element[1]),
            match_case=match_case,
            match_action=xml_element.get("matchAction")
        )

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            matchCase="true" if operator.match_case else "false",
            matchAction=operator.match_action, nsmap=namespaces
        )
        first = ExpressionSerializer.serialize(operator.first_expression,
                                               as_string=False)
        second = ExpressionSerializer.serialize(operator.second_expression,
                                                as_string=False)
        xml_element.append(first)
        xml_element.append(second)
        return xml_element


class PropertyIsEqualToSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsEqualTo


class PropertyIsNotEqualToSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsNotEqualTo


class PropertyIsLessThanSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsLessThan


class PropertyIsGreaterThanSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsGreaterThan


class PropertyIsLessThanOrEqualToSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsLessThanOrEqualTo


class PropertyIsGreaterThanOrEqualToSerializer(BinaryOperatorSerializer):
    TYPE_ = types.PropertyIsGreaterThanOrEqualTo


class PropertyIsLikeSerializer(BaseSerializer):
    TYPE_ = types.PropertyIsLike

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(
            first_expression=ExpressionSerializer.deserialize(xml_element[0]),
            second_expression=ExpressionSerializer.deserialize(xml_element[1]),
            wild_card=xml_element.get("wildCard"),
            single_char=xml_element.get("singleChar"),
            escape_char=xml_element.get("escapeChar")
        )

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            wildCard=operator.wild_card, singleChar=operator.single_char,
            escapeChar=operator.escape_char, nsmap=namespaces
        )
        first = ExpressionSerializer.serialize(operator.first_expression,
                                               as_string=False)
        second = ExpressionSerializer.serialize(operator.second_expression,
                                                as_string=False)
        xml_element.append(first)
        xml_element.append(second)
        return xml_element
