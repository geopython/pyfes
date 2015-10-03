"""Custom types for pyfes

These types are adapted from the FES standard.
"""

from collections import namedtuple

# expression types
ValueReference = namedtuple("ValueReference", "value")
Literal = namedtuple("Literal", "value type_")
Literal.__new__.__defaults__ = ("string",)
Function = namedtuple("Function", "name arguments")
Function.__new__.__defaults__ = ([],)

# comparison operators
PropertyIsEqualTo = namedtuple(
    "PropertyIsEqualTo",
    "first_expression second_expression match_case match_action"
)
PropertyIsEqualTo.__new__.__defaults__ = (True, "any")
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
Beyond = namedtuple("Beyond", "value_reference geometry distance")
DWithin = namedtuple("DWithin", "value_reference geometry distance")
BBOX = namedtuple("BBOX", "spatial_description value_reference")
BBOX.__new__.__defaults__ = (None,)
Equals = namedtuple("Equals", "spatial_description value_reference")
Equals.__new__.__defaults__ = (None,)
Disjoint = namedtuple("Disjoint", "spatial_description value_reference")
Disjoint.__new__.__defaults__ = (None,)
Intersects = namedtuple("Intersects", "spatial_description value_reference")
Intersects.__new__.__defaults__ = (None,)
Touches = namedtuple("Touches", "spatial_description value_reference")
Touches.__new__.__defaults__ = (None,)
Crosses = namedtuple("Crosses", "spatial_description value_reference")
Crosses.__new__.__defaults__ = (None,)
Within = namedtuple("Within", "spatial_description value_reference")
Within.__new__.__defaults__ = (None,)
Contains = namedtuple("Contains", "spatial_description value_reference")
Contains.__new__.__defaults__ = (None,)
Overlaps = namedtuple("Overlaps", "spatial_description value_reference")
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
And = namedtuple("And", "first_operand second_operand")
Or = namedtuple("Or", "first_operand second_operand")
Not = namedtuple("Not", "operand")

# identifier operators
Version = namedtuple("Version", "version_action_token index timestamp")
ResourceId = namedtuple("ResourceId", "rid version start_time end_time")
ResourceId.__new__.__defaults__ = (None, None, None)

# filter
Filter = namedtuple("Filter", "filter_")
