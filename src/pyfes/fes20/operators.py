"""FES v2.0 operators

Operators are used in filter parsers.

"""

from collections import namedtuple

from enum import Enum

from . import expressions
from .. import errors
from .. import validators


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


class TemporalOperatorName(Enum):
    AFTER = "After"
    BEFORE = "Before"
    BEGINS = "Begins"
    BEGUN_BY = "BegunBy"
    T_CONTAINS = "TContains"
    T_EQUALS = "TEquals"
    T_OVERLAPS = "TOverlaps"
    DURING = "During"
    MEETS = "Meets"
    OVERLAPPED_BY = "OverlappedBy"
    MET_BY = "MetBy"
    ENDED_BY = "EndedBy"
    ANY_INTERACTS = "AnyInteracts"


class BinaryLogicType(Enum):
    AND = "And"
    OR = "Or"


class UnaryLogicType(Enum):
    NOT = "Not"


def validate_operand(operand, allowed_types=(expressions.Expression,)):
    if not isinstance(operand, allowed_types):
        raise errors.InvalidExpressionError


class NonIdOperator(object):
    _allowed_operand_types = (expressions.Expression,)

    # TODO - It would be nice to implement equality comparisons
    pass


class SingleExpressionOperator(NonIdOperator):
    _expression = None

    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        if isinstance(other, SingleExpressionOperator):
            return self.expression == other.expression
        else:
            return NotImplemented

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, expression):
        validate_operand(expression)
        self._expression = expression


class DoubleExpressionOperator(NonIdOperator):
    _first_expression = None
    _second_expression = None

    def __init__(self, first_expression, second_expression):
        self.first_expression = first_expression
        self.second_expression = second_expression

    def __eq__(self, other):
        if isinstance(other, DoubleExpressionOperator):
            return (self.first_expression == other.first_expression and
                    self.second_expression == other.second_expression)
        else:
            return NotImplemented

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


class BinaryComparisonOperator(DoubleExpressionOperator):
    match_case = True
    _operator_type = None
    _match_action = MatchAction.ANY

    def __init__(self, operator_type, first_expression, second_expression,
                 match_case=True, match_action=MatchAction.ANY):
        super(BinaryComparisonOperator, self).__init__(
            first_expression=first_expression,
            second_expression=second_expression
        )
        self.operator_type = operator_type
        self.match_case = match_case
        self.match_action = match_action

    def __eq__(self, other):
        if isinstance(other, BinaryComparisonOperator):
            return (super(BinaryComparisonOperator, self).__eq__(other) and
                    self.match_action == other.match_action and
                    self.match_case == other.match_case)
        else:
            return NotImplemented

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

    def __init__(self, expression, lower_boundary, upper_boundary):
        super(BetweenComparisonOperator, self).__init__(expression=expression)
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary

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
    _geometry = None
    _operator_type = None

    def __init__(self, expression, operator_type, geometry, distance):
        super(DistanceOperator, self).__init__(expression=expression)
        self.operator_type = operator_type
        self.geometry = geometry
        self.distance = float(distance)

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
    def geometry(self, new_geometry):
        validators.validate_wkt(new_geometry)
        self._geometry = new_geometry


class BinarySpatialOperator(SingleExpressionOperator):
    _second_operand = None
    _operator_type = None

    def __init__(self, first_operand, second_operand, operator_type):
        super(BinarySpatialOperator, self).__init__(expression=first_operand)
        self.operator_type = operator_type
        self.second_operand = second_operand

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
        else:
            try:
                validators.validate_wkt(operand)
                result = operand
            except errors.ValidationError:
                raise errors.InvalidOperatorError
        self._second_operand = result


class TemporalOperator(SingleExpressionOperator):
    _second_operand = None
    _operator_type = None

    def __init__(self, first_operand, second_operand, operator_type):
        super(TemporalOperator, self).__init__(expression=first_operand)
        self.operator_type = operator_type
        self.second_operand = second_operand

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = TemporalOperatorName(type_)
        except ValueError:
            raise errors.InvalidOperatorError

    @property
    def second_operand(self):
        return self._second_operand

    @second_operand.setter
    def second_operand(self, operand):
        if isinstance(operand, expressions.Expression):
            result = operand
        else:
            try:
                validators.validate_gml_temporal_object(operand)
                result = operand
            except errors.ValidationError:
                raise errors.InvalidOperatorError
        self._second_operand = result


class BinaryLogicOperator(DoubleExpressionOperator):
    _operator_type = None
    _allowed_operand_types = (expressions.Expression, NonIdOperator,)

    def __init__(self, first_expression, second_expression, operator_type):
        super(BinaryLogicOperator, self).__init__(
            first_expression=first_expression,
            second_expression=second_expression
        )
        self.operator_type = operator_type

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = BinaryLogicType(type_)
        except ValueError:
            raise errors.InvalidOperatorError


class UnaryLogicOperator(SingleExpressionOperator):
    _operator_type = None
    _allowed_operand_types = (expressions.Expression, NonIdOperator,)

    def __init__(self, operand, operator_type):
        super(UnaryLogicOperator, self).__init__(expression=operand)
        self.operator_type = operator_type

    @property
    def operator_type(self):
        return self._operator_type

    @operator_type.setter
    def operator_type(self, type_):
        try:
            self._operator_type = UnaryLogicType(type_)
        except ValueError:
            raise errors.InvalidOperatorError


class IdentifierOperator(object):
    pass


class ResourceId(IdentifierOperator):
    _rid = ""

    def __init__(self, rid, previous_rid="", version=None,
                 start_time=None, end_time=None):
        self.rid = rid
        self.previous_rid = previous_rid
        # TODO- validate previous rid too
        # TODO- add support for version
        # TODO- add support for start_time
        # TODO- add support for end_time

    @property
    def rid(self):
        return self._rid

    @rid.setter
    def rid(self, rid):
        validators.validate_resource_identifier(rid)
        self._rid = rid
