"""FES v2.0 operators

Operators are used in filter parsers.

"""

from collections import namedtuple

from enum import Enum


class MatchAction(Enum):
    ALL = "All"
    ANY = "Any"
    ONE = "One"


class BinaryComparisonOperator(object):
    match_case = True
    match_action = MatchAction.ANY

    def __init__(self, match_case=True, match_action=MatchAction.ANY):
        self.match_case = match_case
        self.match_action = match_action


class PropertyIsEqualTo(BinaryComparisonOperator):
    first_expression = None
    second_expression = None

    def __init__(self, first_expression, second_expression,
                 match_case=True, match_action=MatchAction.ANY):
        super(PropertyIsEqualTo, self).__init__(
            match_case=match_case, match_action=match_action)
        self.first_expression = first_expression
        self.second_expression = second_expression




PropertyIsNotEqualTo = namedtuple(
    "PropertyIsNotEqualTo",
    "first_expression second_expression match_case match_action"
)
PropertyIsNotEqualTo.__new__.__defaults__ = (True, "any")
PropertyIsLessThan = namedtuple(
    "PropertyIsLessThan",
    "first_expression second_expression match_case match_action"
)
PropertyIsLessThan.__new__.__defaults__ = (True, "any")
PropertyIsGreaterThan = namedtuple(
    "PropertyIsGreaterThan",
    "first_expression second_expression match_case match_action"
)
PropertyIsGreaterThan.__new__.__defaults__ = (True, "any")
PropertyIsLessThanOrEqualTo = namedtuple(
    "PropertyIsLessThanOrEqualTo",
    "first_expression second_expression match_case match_action"
)
PropertyIsLessThanOrEqualTo.__new__.__defaults__ = (True, "any")
PropertyIsGreaterThanOrEqualTo = namedtuple(
    "PropertyIsgreaterThanOrEqualTo",
    "first_expression second_expression match_case match_action"
)
PropertyIsGreaterThanOrEqualTo.__new__.__defaults__ = (True, "any")
PropertyIsLike = namedtuple(
    "PropertyIsLike",
    "first_expression second_expression wild_card single_char escape_char"
)
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
