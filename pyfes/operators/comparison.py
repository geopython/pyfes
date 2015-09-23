"""
Comparison operator classes

Please refer to page 19, section 7.7 - Comparison Operators for more
details.
"""

from __future__ import absolute_import
import logging
from enum import Enum, unique
from lxml import etree

from .. import utils
from .. import errors
from ..expression import ExpressionParser
from ..namespaces import namespaces
from . import base

logger = logging.getLogger(__name__)


@unique
class BinaryComparisonName(Enum):
    property_is_equal_to = "PropertyIsEqualTo"
    property_is_not_equal_to = "PropertyIsNotEqualTo"
    property_is_less_than = "PropertyIsLessThan"
    property_is_greater_than = "PropertyIsGreaterThan"
    property_is_less_than_or_equal_to = "PropertyIsLessThanOrEqualTo"
    property_is_greater_than_or_equal_to = "PropertyIsGreaterThanOrEqualTo"


@unique
class MatchAction(Enum):
    any_ = "any"
    all_ = "all"
    one = "one"


@unique
class BoundaryType(Enum):
    lower = "LowerBoundary"
    upper = "UpperBoundary"


class OperatorParser(object):
    """A factory for generating Operator objects by deserializing from XML.
    """

    @classmethod
    def parse(cls, operator):
        instance = None
        operator_classes = [BinaryComparisonOperator, LikeOperator,
                            BetweenComparisonOperator, NullOperator,
                            NillOperator]
        current = 0
        while instance is None and current < len(operator_classes):
            instance = operator_classes[current].from_xml(operator)
            current += 1
        return instance


class BinaryComparisonOperator(base.BinaryComparisonWithTwoExpressions):
    _operator_type = None
    _match_action = MatchAction.any_
    match_case = True

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        if type_ in (BinaryComparisonName):
            self._operator_type = type_
        else:
            raise errors.InvalidOperatorError()

    @property
    def match_action(self):
        return self._match_action

    @match_action.setter
    def match_action(self, action):
        if action in (MatchAction):
            self._match_action = action
        else:
            raise errors.InvalidOperatorError()

    def __init__(self, first_expression, second_expression,
                 operator_type, match_case=True,
                 match_action=MatchAction.any_):
        super(BinaryComparisonOperator, self).__init__(first_expression,
                                                       second_expression)
        self.match_case = match_case
        self.match_action = match_action
        self.operator_type = operator_type

    @classmethod
    def from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        instance = None
        qname = etree.QName(operator_element)
        if qname.namespace == namespaces.get("fes") and \
                qname.localname in [m.value for m in BinaryComparisonName]:
            instance = cls(
                ExpressionParser.parse(operator_element[0]),
                ExpressionParser.parse(operator_element[1]),
                operator_type=BinaryComparisonName(qname.localname),
                match_case=operator_element.get("matchCase", True),
                match_action=operator_element.get("matchAction",
                                                  MatchAction.any_)
            )
        else:
            logger.error("Invalid {}: {}".format(cls.__name__,
                                                 operator_element))
        return instance

    def _serialize(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.operator_type.value),
            matchCase="true" if self.match_case else "false",
            matchAction=self.match_action.value, nsmap=namespaces
        )
        first_expression_element = self.first_expression.serialize(
            as_string=False)
        element.append(first_expression_element)
        second_expression_element = self.second_expression.serialize(
            as_string=False)
        element.append(second_expression_element)
        return element


class LikeOperator(base.BinaryComparisonWithTwoExpressions):
    XML_ENTITY_NAME = "PropertyIsLike"
    wild_card = ""
    single_char = ""
    escape_char = ""

    def __init__(self, first_expression, second_expression, wild_card,
                 single_char, escape_char):
        super(LikeOperator, self).__init__(first_expression, second_expression)
        self.wild_card = wild_card
        self.single_char = single_char
        self.escape_char = escape_char

    @classmethod
    def from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        instance = None
        qname = etree.QName(operator_element)
        if qname.namespace == namespaces.get("fes") and \
                qname.localname == cls.XML_ENTITY_NAME:
            instance = cls(
                ExpressionParser.parse(operator_element[0]),
                ExpressionParser.parse(operator_element[1]),
                wild_card=operator_element.get("wildCard"),
                single_char=operator_element.get("singleChar"),
                escape_char=operator_element.get("escapeChar")
            )
        else:
            logger.error("Invalid {}: {}".format(cls.__name__,
                                                 operator_element))
        return instance

    def _serialize(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.XML_ENTITY_NAME),
            wildCard=self.wild_card, singleChar=self.single_char,
            escapeChar=self.escape_char, nsmap=namespaces
        )
        first_expression_element = self.first_expression.serialize(
            as_string=False)
        element.append(first_expression_element)
        second_expression_element = self.second_expression.serialize(
            as_string=False)
        element.append(second_expression_element)
        return element


class Boundary(object):
    """Custom type used by the BetweenComparisonOperator class"""

    _type_ = BoundaryType.lower
    _expression = None

    @property
    def expression(self):
        return self.expression

    @expression.setter
    def expression(self, new_expression):
        utils.check_expression_type(new_expression)  # raises on error
        self._expression = new_expression

    @property
    def type_(self):
        return self._type_

    @type_.setter
    def type_(self, new_type):
        if new_type in BoundaryType:
            self._type_ = new_type
        else:
            raise errors.InvalidBoundaryTypeError()

    def __init__(self, expression, type_):
        self.expression = expression
        self.type_ = type_

    def serialize(self, as_string=True):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.type_.value)
        )
        expression_element = self.expression.serialize(
            as_string=False)
        element.append(first_expression_element)
        if as_string:
            result = etree.tostring(element, pretty_print=True)
        else:
            result = element
        return result

    @classmethod
    def from_xml(cls, boundary_element):
        """Create a new object from an XML element"""
        instance = None
        qname = etree.QName(boundary_element)
        if qname.namespace == namespaces.get("fes") and \
                qname.localname in [m.value for m in BoundaryType]:
            instance = cls(ExpressionParser.parse(operator_element[0]),
                           BoundaryType(qname.localname))
        else:
            logger.error("Invalid {}: {}".format(cls.__name__,
                                                 boundary_element))
        return instance


class BetweenComparisonOperator(base.BinaryComparisonWithOneExpression):
    """Tests if the specified property is between a range.

    The lower and upper boundaries are inclusive.
    """

    XML_ENTITY_NAME = "PropertyIsBetween"
    _lower_boundary = None
    _upper_boundary = None

    @property
    def lower_boundary(self):
        return self._lower_boundary

    @lower_boundary.setter
    def lower_boundary(self, boundary):
        if boundary.type_ != BoundaryType.lower:
            raise errors.InvalidBoundaryTypeError()
        self._lower_boundary = boundary

    @property
    def upper_boundary(self):
        return self._upper_boundary

    @upper_boundary.setter
    def upper_boundary(self, boundary):
        if boundary.type_ != BoundaryType.upper:
            raise errors.InvalidBoundaryTypeError()
        self._upper_boundary = boundary

    def __init__(self, expression, lower_boundary, upper_boundary):
        super(BetweenComparisonOperator, self).__init__(expression)
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary

    @classmethod
    def from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        instance = None
        qname = etree.QName(operator_element)
        if qname.namespace == namespaces.get("fes") and \
                qname.localname == cls.XML_ENTITY_NAME:
            instance = cls(
                ExpressionParser.parse(operator_element[0]),
                Boundary.deserialize(operator_element[1]),
                Boundary.deserialize(operator_element[2])
            )
        else:
            logger.error("Invalid {}: {}".format(cls.__name__,
                                                 operator_element))
        return instance

    def _serialize(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.XML_ENTITY_NAME),
            nsmap=namespaces
        )
        expression_element = self.expression.serialize(as_string=False)
        element.append(expression_element)
        lower_boundary_element = self.lower_boundary.serialize(as_string=False)
        element.append(lower_boundary_element)
        upper_boundary_element = self.upper_boundary.serialize(as_string=False)
        element.append(upper_boundary_element)
        return element


class NullOperator(base.BinaryComparisonWithOneExpression):
    """Tests the specified property to see if it exists in the resource."""
    pass


class NillOperator(base.BinaryComparisonWithOneExpression):
    """Tests the content of specified property to see if it is nill."""
    nill_reason = ""

    def __init__(self, expression, nill_reason=""):
        super(NillOperator, self).__init__(expression)
        self.nill_reason = nill_reason
