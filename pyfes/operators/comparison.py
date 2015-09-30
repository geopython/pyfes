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
            self._name = type_.value
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
                 match_action="any"):
        super(BinaryComparisonOperator, self).__init__(first_expression,
                                                       second_expression)
        self.match_case = match_case
        self.match_action = MatchAction(match_action)
        self.operator_type = operator_type

    @classmethod
    def _from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        operator_type = etree.QName(operator_element).localname
        return cls(
            ExpressionParser.parse(operator_element[0]),
            ExpressionParser.parse(operator_element[1]),
            operator_type=BinaryComparisonName(operator_type),
            match_case=operator_element.get("matchCase") == "true",
            match_action=operator_element.get("matchAction", MatchAction.any_)
        )

    def _to_xml(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.name),
            matchCase="true" if self.match_case else "false",
            matchAction=self.match_action.value, nsmap=namespaces
        )
        first_expression_element = self.first_expression.to_xml(
            as_string=False)
        element.append(first_expression_element)
        second_expression_element = self.second_expression.to_xml(
            as_string=False)
        element.append(second_expression_element)
        return element

    def __repr__(self):
        return ("{0}.{1.__class__.__name__}({1.first_expression}, "
                "{1.second_expression}, {1.operator_type}, {1.match_case}, "
                "{1.match_action})".format(__name__, self))


class LikeOperator(base.BinaryComparisonWithTwoExpressions):
    _name = "PropertyIsLike"
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
    def _from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        return cls(
            ExpressionParser.parse(operator_element[0]),
            ExpressionParser.parse(operator_element[1]),
            wild_card=operator_element.get("wildCard"),
            single_char=operator_element.get("singleChar"),
            escape_char=operator_element.get("escapeChar")
        )

    def _to_xml(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.name),
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
        return self._expression

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

    def to_xml(self, as_string=True):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.type_.value)
        )
        expression_element = self.expression.to_xml(
            as_string=False)
        element.append(expression_element)
        if as_string:
            result = etree.tostring(element, pretty_print=True)
        else:
            result = element
        return result

    # FIXME - Improve validation by using the schema_parser
    @classmethod
    def from_xml(cls, boundary_element):
        """Create a new object from an XML element"""
        instance = None
        qname = etree.QName(boundary_element)
        if qname.namespace == namespaces.get("fes") and \
                qname.localname in [m.value for m in BoundaryType]:
            instance = cls(ExpressionParser.parse(boundary_element[0]),
                           BoundaryType(qname.localname))
        else:
            logger.error("Invalid {}: {}".format(cls.__name__,
                                                 boundary_element))
        return instance


class BetweenComparisonOperator(base.BinaryComparisonWithOneExpression):
    """Tests if the specified property is between a range.

    The lower and upper boundaries are inclusive.
    """

    _name = "PropertyIsBetween"
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
    def _from_xml(cls, operator_element):
        """Create a new object from an XML element"""
        return cls(
            ExpressionParser.parse(operator_element[0]),
            Boundary.from_xml(operator_element[1]),
            Boundary.from_xml(operator_element[2])
        )

    def _to_xml(self):
        element = etree.Element(
            "{{{}}}{}".format(namespaces["fes"], self.name),
            nsmap=namespaces
        )
        expression_element = self.expression.to_xml(as_string=False)
        element.append(expression_element)
        lower_boundary_element = self.lower_boundary.to_xml(as_string=False)
        element.append(lower_boundary_element)
        upper_boundary_element = self.upper_boundary.to_xml(as_string=False)
        element.append(upper_boundary_element)
        return element


class NullOperator(base.BinaryComparisonWithOneExpression):
    """Tests the specified property to see if it exists in the resource."""
    _name = "PropertyIsNull"


class NillOperator(base.BinaryComparisonWithOneExpression):
    """Tests the content of specified property to see if it is nill."""
    _name = "PropertyIsNil"
    nill_reason = ""

    def __init__(self, expression, nill_reason=""):
        super(NillOperator, self).__init__(expression)
        self.nill_reason = nill_reason
