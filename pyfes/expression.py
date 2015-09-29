"""
Expression and related classes, as defined in the OGC Filter Encoding Standard/
ISO 19143.
"""

from __future__ import absolute_import
import logging
import datetime

from lxml import etree

from . import validators
from . import errors
from .namespaces import namespaces
from .base import PyfesBase


logger = logging.getLogger(__name__)


class ExpressionParser(object):
    """A factory for generating Expression objects by deserializing from XML.
    """

    @classmethod
    def parse(cls, expression):
        instance = None
        expression_classes = [ValueReference, Literal, Function]
        current = 0
        while instance is None and current < len(expression_classes):
            instance = expression_classes[current].from_xml(expression)
            current += 1
        return instance


class Expression(PyfesBase):
    XML_ENTITY_NAME = ""

    pass


class ValueReference(Expression):
    """A string representing some property of a type.

    Implementation of the fes:ValueReference XML element
    """

    XML_ENTITY_NAME = "ValueReference"
    _value = ""
    validators = [validators.gml_property_name_validator]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            for validator in self.validators:
                validator(new_value)
            self._value = new_value
        except errors.ValidationError:
            raise

    def __init__(self, value):
        self.value = value

    def _to_xml(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.XML_ENTITY_NAME),
            nsmap=namespaces
        )
        element.text = self.value
        return element

    @classmethod
    def _from_xml(cls, expression):
        instance = None
        qname = etree.QName(expression)
        if qname.localname == cls.XML_ENTITY_NAME:
            instance = cls(expression.text)
        else:
            logger.debug("Invalid {}: {}".format(cls.__name__, expression))
        return instance

    def __repr__(self):
        return ("{0}.{1.__class__.__name__}({1.value})".format(__name__, self))


class Literal(Expression):
    XML_ENTITY_NAME = "Literal"
    _value = None
    type_ = None

    @property
    def value(self):
        if self.type_ == "xs:date":
            result = datetime.datetime.strptime(self._value,
                                                "%Y-%m-%dT%H:%M:%S")
        else:
            result = self._value
        return result

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __init__(self, value, type_=None):
        self.value = value
        self.type_ = type_

    def _to_xml(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.XML_ENTITY_NAME),
            nsmap=namespaces
        )
        if self.type_ is not None:
            element.attrib["type"] = self.type_
        element.text = self.value
        return element

    @classmethod
    def _from_xml(cls, expression):
        instance = None
        qname = etree.QName(expression)
        if qname.localname == cls.XML_ENTITY_NAME:
            instance = cls(expression.text, expression.attrib.get("type"))
        else:
            logger.debug("Invalid {}: {}".format(cls.__name__, expression))
        return instance

    def __repr__(self):
        return ("{0}.{1.__class__.__name__}({1.value}, "
                "type_={1.type_})".format(__name__, self))


class Function(Expression):
    XML_ENTITY_NAME = "Function"
    _name = ""
    arguments = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        validators.gml_validator(new_name)  # raises if invalid
        self._name = new_name

    def __init__(self, name, *arguments):
        self.name = name
        for arg in arguments:
            if isinstance(arg, Expression):
                self.arguments.append(arg)
            else:
                logger.warning()
