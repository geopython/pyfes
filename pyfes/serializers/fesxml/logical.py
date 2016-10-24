"""Serializer classes for fes logical operator types"""

from __future__ import absolute_import
from __future__ import unicode_literals
import logging

from lxml import etree

from ... import festypes
from ...namespaces import namespaces
from .base import BaseSerializer
from .fesxml import FesXmlSerializer

logger = logging.getLogger(__name__)


class BinaryLogicOperatorSerializer(BaseSerializer):

    @classmethod
    def _deserialize(cls, xml_element):
        predicates = [FesXmlSerializer.deserialize(child) for child
                      in xml_element]
        return cls.TYPE_(
            first_predicate=predicates[0], second_predicate=predicates[1],
            extra_predicates=predicates[2:] or None
        )

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            nsmap=namespaces
        )
        predicates_genexp = (p for p in [operator.first_predicate] +
                             [operator.second_predicate] +
                             (operator.extra_predicates or []))
        for predicate in predicates_genexp:
            sub_el = FesXmlSerializer.serialize(predicate, as_string=False)
            xml_element.append(sub_el)
        return xml_element


class AndSerializer(BinaryLogicOperatorSerializer):
    TYPE_ = festypes.And


class OrSerializer(BinaryLogicOperatorSerializer):
    TYPE_ = festypes.Or


class NotSerializer(BaseSerializer):
    TYPE_ = festypes.Not

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(
            filter_predicate=FesXmlSerializer.deserialize(xml_element[0]))

    @classmethod
    def _serialize(cls, operator):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces, operator),
            nsmap=namespaces
        )
        sub_el = FesXmlSerializer.serialize(operator.filter_predicate,
                                            as_string=False)
        xml_element.append(sub_el)
        return xml_element
