"""Serializer classes for FES:Expression types"""

from __future__ import absolute_import
from __future__ import unicode_literals
import logging

from lxml import etree

from ... import types
from ...namespaces import namespaces
from .base import BaseSerializer

logger = logging.getLogger(__name__)


class ExpressionSerializer(object):

    @classmethod
    def deserialize(cls, xml_element, validate_schema=True):
        # first get an etree.Element from input xml_element, if necessary
        if isinstance(xml_element, basestring):
            xml_element = etree.fromstring(xml_element)
        # then validate the xml_element with the fes2_0 schema, if needed
        if validate_schema:
            pass
        # then match the xml_element with the appropriate serializer class
        deserializer = {
            types.ValueReference.__name__: ValueReferenceSerializer,
            types.Literal.__name__: LiteralSerializer,
            types.Function.__name__: FunctionSerializer,
        }.get(etree.QName(xml_element).localname)
        return deserializer.deserialize(xml_element, validate_schema=False)

    @classmethod
    def serialize(cls, expression, as_string=True):
        serializer = {
            types.ValueReference: ValueReferenceSerializer,
            types.Literal: LiteralSerializer,
            types.Function: FunctionSerializer,
        }.get(type(expression))
        return serializer.serialize(expression, as_string=as_string)


class ValueReferenceSerializer(BaseSerializer):
    TYPE_ = types.ValueReference

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
    TYPE_ = types.Literal

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
    TYPE_ = types.Function

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
