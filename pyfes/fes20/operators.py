"""FES v2.0 operators

Operators are used in filter parsers.

"""

from collections import namedtuple

from enum import Enum

from .. import errors
from . import expressions


class MatchAction(Enum):
    ALL = "All"
    ANY = "Any"
    ONE = "One"


class BinaryComparisonName(Enum):
    PROPERTY_IS_EQUAL_TO = "PropertyIsEqualTo"
    PROPERTY_IS_NOT_EQUAL_TO = "PropertyIsNotEqualTo"
    PROPERTY_IS_LESS_THAN = "PropertyIsLessThan"
    PROPERTY_IS_LESS_THAN_OR_EQUAL_TO = "PropertyIsLessThanOrEqualTo"
    PROPERTY_IS_GREATER_THAN = "PropertyIsGreaterThan"
    PROPERTY_IS_GREATER_THAN_OR_EQUAL_TO = "PropertyIsGreaterThanOrEqualTo"


def validate_operand(operand, allowed_types=(expressions.Expression,)):
    if not isinstance(operand, allowed_types):
        raise errors.InvalidExpressionError


class SingleExpressionOperator(object):
    _expression = None

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, expression):
        validate_operand(expression)
        self._expression = expression


class DoubleExpressionOperator(object):
    _first_expression = None
    _second_expression = None

    @property
    def first_expression(self):
        return self._first_expression

    @first_expression.setter
    def first_expression(self, expression):
        validate_operand(expression)
        self._first_expression = expression

    @property
    def second_expression(self):
        return self._second_expression

    @second_expression.setter
    def second_expression(self, expression):
        validate_operand(expression)
        self._second_expression = expression

    def __init__(self, first_expression, second_expression):
        self.first_expression = first_expression
        self.second_expression = second_expression


class BinaryComparisonOperator(DoubleExpressionOperator):
    match_case = True
    _operator_type = None
    _match_action = MatchAction.ANY

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = BinaryComparisonName(type_)
        except ValueError:
            raise errors.InvalidOperatorError

    @property
    def match_action(self):
        return self._match_action

    @match_action.setter
    def match_action(self, action):
        try:
            self._match_action = MatchAction(action)
        except ValueError:
            raise ValueError("Invalid match_action")

    def __init__(self, operator_type, first_expression, second_expression,
                 match_case=True, match_action=MatchAction.ANY):
        super(BinaryComparisonOperator, self).__init__(
            first_expression=first_expression,
            second_expression=second_expression
        )
        self.operator_type = operator_type
        self.match_case = match_case
        self.match_action = match_action


class LikeOperator(DoubleExpressionOperator):
    wild_card = ""
    single_char = ""
    escape_char = ""

    def __init__(self, first_expression, second_expression,
                 wild_card="", single_char="", escape_char=""):
        super(LikeOperator, self).__init__(
            first_expression=first_expression,
            second_expression=second_expression
        )
        self.wild_card = str(wild_card)
        self.single_char = str(single_char)
        self.escape_char = str(escape_char)


Boundary = namedtuple("Boundary", "expression")
PropertyIsBetween = namedtuple("PropertyIsBetween",
                               "expression lower_boundary upper_boundary")
PropertyIsNull = namedtuple("PropertyIsNull", "expression")
PropertyIsNil = namedtuple("PropertyIsNil", "expression nil_reason")
PropertyIsNil.__new__.__defaults__ = ("equals",)

# spatial operators
Beyond = namedtuple("Beyond", "distance first_argument second_argument")
Beyond.__new__.__defaults__ = (None,)
DWithin = namedtuple("DWithin", "distance first_argument second_argument")
DWithin.__new__.__defaults__ = (None,)
BBOX = namedtuple("BBOX", "first_argument second_argument")
BBOX.__new__.__defaults__ = (None,)
Equals = namedtuple("Equals", "first_argument second_argument")
Equals.__new__.__defaults__ = (None,)
Disjoint = namedtuple("Disjoint", "first_argument second_argument")
Disjoint.__new__.__defaults__ = (None,)
Intersects = namedtuple("Intersects", "first_argument second_argument")
Intersects.__new__.__defaults__ = (None,)
Touches = namedtuple("Touches", "first_argument second_argument")
Touches.__new__.__defaults__ = (None,)
Crosses = namedtuple("Crosses", "first_argument second_argument")
Crosses.__new__.__defaults__ = (None,)
Within = namedtuple("Within", "first_argument second_argument")
Within.__new__.__defaults__ = (None,)
Contains = namedtuple("Contains", "first_argument second_argument")
Contains.__new__.__defaults__ = (None,)
Overlaps = namedtuple("Overlaps", "first_argument second_argument")
Overlaps.__new__.__defaults__ = (None,)
# todo: add the SpatialDescription Union values

# temporal operators
TemporalOperand = namedtuple("TemporalOperand",
                             "temporal_object value_reference")
After = namedtuple("After", "value_reference temporal_operand")
Before = namedtuple("Before", "value_reference temporal_operand")
Begins = namedtuple("Begins", "value_reference temporal_operand")
BegunBy = namedtuple("BegunBy", "value_reference temporal_operand")
TContains = namedtuple("TContains", "value_reference temporal_operand")
During = namedtuple("During", "value_reference temporal_operand")
TEquals = namedtuple("TEquals", "value_reference temporal_operand")
TOverlaps = namedtuple("TOverlaps", "value_reference temporal_operand")
Meets = namedtuple("Meets", "value_reference temporal_operand")
OverlappedBy = namedtuple("OverlappedBy", "value_reference temporal_operand")
MetBy = namedtuple("MetBy", "value_reference temporal_operand")
EndedBy = namedtuple("EndedBy", "value_reference temporal_operand")
AnyInteracts = namedtuple("AnyInteracts", "value_reference temporal_operand")

# logical operators
And = namedtuple("And", "first_predicate second_predicate extra_predicates")
And.__new__.__defaults__ = (None,)
Or = namedtuple("Or", "first_predicate second_predicate extra_predicates")
Or.__new__.__defaults__ = (None,)
Not = namedtuple("Not", "filter_predicate")

# identifier operators
Version = namedtuple("Version", "version_action_token index timestamp")
ResourceId = namedtuple("ResourceId", "rid version start_time end_time")
ResourceId.__new__.__defaults__ = (None, None, None)

# filter
Filter = namedtuple("Filter", "filter_")
