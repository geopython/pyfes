"""FES v2.0 operators

Operators are used in filter parsers.

"""

from collections import namedtuple

from enum import Enum
from shapely import geometry
from shapely.geos import ReadingError
from shapely import wkt

from . import expressions
from .. import errors


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


class DistanceOperatorName(Enum):
    BEYOND = "Beyond"
    DWITHIN = "DWithin"


class SpatialOperatorName(Enum):
    BBOX = "BBOX"
    EQUALS = "Equals"
    DISJOINT = "Disjoint"
    INTERSECTS = "Intersects"
    TOUCHES = "Touches"
    CROSSES = "Crosses"
    WITHIN = "Within"
    CONTAINS = "Contains"
    OVERLAPS = "Overlaps"


def as_geometry(geom):
    is_shapely_geom = isinstance(
        geom,
        (
            # TODO - add the remaining shapely geometry types
            geometry.Point,
            geometry.LineString,
        )
    )
    if is_shapely_geom:
        result = geom
    else:
        result = wkt.loads(geom)
    return result


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

    def __init__(self, expression):
        self.expression = expression


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


class BetweenComparisonOperator(SingleExpressionOperator):
    """
    According to the FES standard, the PropertyIsBetween operator is defined as
    a compact way of encoding a range check. The lower and upper boundary
    values are inclusive.

    """

    _lower_boundary = None
    _upper_boundary = None

    @property
    def lower_boundary(self):
        return self._lower_boundary

    @lower_boundary.setter
    def lower_boundary(self, expression):
        validate_operand(expression)
        self._lower_boundary = expression

    @property
    def upper_boundary(self):
        return self._upper_boundary

    @upper_boundary.setter
    def lower_boundary(self, expression):
        validate_operand(expression)
        self._upper_boundary = expression

    def __init__(self, expression, lower_boundary, upper_boundary):
        super(BetweenComparisonOperator, self).__init__(expression=expression)
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary


class NullOperator(SingleExpressionOperator):
    """
    The PropertyIsNull operator tests the specified property to see if it
    exists in the resource being evaluated. This corresponds to checking
    whether the property exists in the real-world.
    """

    def __init__(self, expression):
        super(NullOperator, self).__init__(expression=expression)


class NilOperator(SingleExpressionOperator):
    """
    The PropertyIsNil operator tests the content of the specified property and
    evaluates if it is nil. The operator can also evaluate the nil reason using
    the nilReason parameter. The implied operator for evaluating the nil reason
    is "equals".
    """

    nil_reason = ""

    def __init__(self, expression, nil_reason=""):
        super(NilOperator, self).__init__(expression=expression)
        self.nil_reason = nil_reason


class DistanceOperator(SingleExpressionOperator):
    distance = 0.0
    _operator_type = None
    _geometry = None

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = DistanceOperatorName(type_)
        except ValueError:
            raise errors.InvalidOperatorError

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        try:
            self._geometry = as_geometry(geometry)
        except ReadingError:
            raise errors.InvalidOperatorError

    def __init__(self, expression, operator_type, geometry, distance):
        super(DistanceOperator, self).__init__(expression=expression)
        self.operator_type = operator_type
        self.geometry = geometry
        self.distance = float(distance)


class BinarySpatialOperator(SingleExpressionOperator):
    _second_operand = None
    _operator_type = None

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = SpatialOperatorName(type_)
        except ValueError:
            raise errors.InvalidOperatorError

    @property
    def second_operand(self):
        return self._second_operand

    @second_operand.setter
    def second_operand(self, operand):
        if isinstance(operand, expressions.Expression):
            result = operand
        else:  #FIXME - This method is probably not done yet
            try:
                result = as_geometry(operand)
            except ReadingError:
                raise errors.InvalidOperatorError
        self._second_operand = result

    def __init__(self, first_operand, second_operand, operator_type):
        super(DistanceOperator, self).__init__(expression=first_operand)
        self.operator_type = operator_type
        self.second_operand = second_operand

# TODO: Add temporal operators
# TODO: Add logical operators
# TODO: Add identifier operators
