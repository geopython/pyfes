"""Serializer classes for fes comparison operator types"""

from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from lxml import etree
from pyfes.fes20 import operators

from src.pyfes.fes20.namespaces import namespaces
from .base import BaseSerializer
from .fesxml import FesXmlSerializer

logger = logging.getLogger(__name__)


class BinaryComparisonOperatorSerializer(BaseSerializer):

    @classmethod
    def _deserialize(cls, xml_element):
        match_case = False
        if xml_element.get("matchCase", "true") == "true":
            match_case = True
        return cls.TYPE_(
            first_expression=FesXmlSerializer.deserialize(xml_element[0]),
            second_expression=FesXmlSerializer.deserialize(xml_element[1]),
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
        first = FesXmlSerializer.serialize(operator.first_expression,
                                           as_string=False)
        second = FesXmlSerializer.serialize(operator.second_expression,
                                            as_string=False)
        xml_element.append(first)
        xml_element.append(second)
        return xml_element


class PropertyIsEqualToSerializer(BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsEqualTo


class PropertyIsNotEqualToSerializer(BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsNotEqualTo


class PropertyIsLessThanSerializer(BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsLessThan


class PropertyIsGreaterThanSerializer(BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsGreaterThan


class PropertyIsLessThanOrEqualToSerializer(
        BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsLessThanOrEqualTo


class PropertyIsGreaterThanOrEqualToSerializer(
        BinaryComparisonOperatorSerializer):
    TYPE_ = operators.PropertyIsGreaterThanOrEqualTo


class PropertyIsLikeSerializer(BaseSerializer):
    TYPE_ = operators.PropertyIsLike

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(
            first_expression=FesXmlSerializer.deserialize(xml_element[0]),
            second_expression=FesXmlSerializer.deserialize(xml_element[1]),
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
        first = FesXmlSerializer.serialize(operator.first_expression,
                                           as_string=False)
        second = FesXmlSerializer.serialize(operator.second_expression,
                                            as_string=False)
        xml_element.append(first)
        xml_element.append(second)
        return xml_element


class BoundarySerializer(BaseSerializer):
    TYPE_ = operators.Boundary
    EXTRA_TYPE_NAMES = ["LowerBoundary", "UpperBoundary"]

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(
            expression=FesXmlSerializer.deserialize(xml_element[0]))

    @classmethod
    def _serialize(cls, boundary, tag_name=None):
        tag_name = tag_name or boundary.__class__.__name__
        xml_element = etree.Element(
            "{{{0[fes]}}}{1}".format(namespaces, tag_name),
            nsmap=namespaces
        )
        xml_element.append(FesXmlSerializer.serialize(boundary.expression,
                                                      as_string=False))
        return xml_element


class PropertyIsBetweenSerializer(BaseSerializer):
    TYPE_ = operators.PropertyIsBetween

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(
            expression=FesXmlSerializer.deserialize(xml_element[0]),
            lower_boundary=operators.Boundary(
                FesXmlSerializer.deserialize(xml_element[1])),
            upper_boundary=operators.Boundary(
                FesXmlSerializer.deserialize(xml_element[2])),
        )

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            nsmap=namespaces
        )
        xml_element.append(FesXmlSerializer.serialize(operator.expression,
                                                      as_string=False))
        xml_element.append(
            BoundarySerializer.serialize(operator.lower_boundary,
                                         as_string=False,
                                         tag_name="LowerBoundary"))
        xml_element.append(
            BoundarySerializer.serialize(operator.upper_boundary,
                                         as_string=False,
                                         tag_name="UpperBoundary"))
        return xml_element


class PropertyIsNullSerializer(BaseSerializer):
    TYPE_ = operators.PropertyIsNull

    @classmethod
    def _deserialize(cls, xml_element):
        if len(xml_element) >= 1:
            result = cls.TYPE_(
                expression=FesXmlSerializer.deserialize(xml_element[0]))
        else:
            result = cls.TYPE_()
        return result

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            nsmap=namespaces
        )
        if operator.expression is not None:
            xml_element.append(FesXmlSerializer.serialize(operator.expression,
                                                          as_string=False))
        return xml_element


class PropertyIsNilSerializer(BaseSerializer):
    TYPE_ = operators.PropertyIsNil

    @classmethod
    def _deserialize(cls, xml_element):
        nil_reason = xml_element.get("nilReason", "equals")
        if len(xml_element) >= 1:
            result = cls.TYPE_(
                expression=FesXmlSerializer.deserialize(xml_element[0]),
                nil_reason=nil_reason
            )
        else:
            result = cls.TYPE_(nil_reason=nil_reason)
        return result

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            nilReason=operator.nil_reason, nsmap=namespaces
        )
        if operator.expression is not None:
            xml_element.append(FesXmlSerializer.serialize(operator.expression,
                                                          as_string=False))
        return xml_element
