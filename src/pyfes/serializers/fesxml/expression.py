"""Serializer classes for fes:Expression types"""

from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from lxml import etree
from pyfes.fes20 import operators

from src.pyfes.fes20.namespaces import namespaces
from .base import BaseSerializer

logger = logging.getLogger(__name__)


class ValueReferenceSerializer(BaseSerializer):
    TYPE_ = operators.ValueReference

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(value=xml_element.text)

    @classmethod
    def _serialize(cls, value_reference):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces,
                                                        value_reference),
            nsmap=namespaces
        )
        xml_element.text = value_reference.value
        return xml_element


class LiteralSerializer(BaseSerializer):
    TYPE_ = operators.Literal

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(value=xml_element.text, type_=xml_element.get("type"))

    @classmethod
    def _serialize(cls, literal):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces,
                                                        literal),
            type=literal.type_, nsmap=namespaces
        )
        xml_element.text = literal.value
        return xml_element


class FunctionSerializer(BaseSerializer):
    TYPE_ = operators.Function

    @classmethod
    def _deserialize(cls, xml_element):
        return cls.TYPE_(name=xml_element.get("name"),
                         arguments_=[])  # FIXME: use factory for arguments

    @classmethod
    def _serialize(cls, function_):
        xml_element = etree.Element(
            "{{{0[fes]}}}{1.__class__.__name__}".format(namespaces,
                                                        function_),
            name=function_.name, nsmap=namespaces
        )
        # TODO: add the arguments of the function type
        return xml_element
