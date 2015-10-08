"""Tests for the custom pyfes types"""

from nose.tools import eq_
from unittest import TestCase
import logging

from lxml import etree

from pyfes import types

logger = logging.getLogger(__name__)


class TestTypes(TestCase):

    @classmethod
    def setup_class(cls):
        cls.value_reference = types.ValueReference("foo")
        cls.literal = types.Literal("baz")
        cls.other_literal = types.Literal("bar")

    def test_should_create_expression_types(self):
        value = "something"
        value_reference = types.ValueReference(value)
        eq_(value_reference.value, value)

        first_literal = types.Literal(value)
        eq_(first_literal.value, value)
        eq_(first_literal.type_, "string")
        type_ = "other"
        second_literal = types.Literal(value, type_)
        eq_(second_literal.type_, type_)

        name = "foo"
        args = ["this", "that"]
        first_func = types.Function(name)
        eq_(first_func.name, name)
        eq_(first_func.arguments, [])
        second_func = types.Function(name, args)
        eq_(second_func.arguments, args)

    def test_should_create_binary_comparison_operators(self):
        for op_type in (types.PropertyIsEqualTo, types.PropertyIsNotEqualTo,
                        types.PropertyIsLessThan, types.PropertyIsGreaterThan,
                        types.PropertyIsLessThanOrEqualTo,
                        types.PropertyIsGreaterThanOrEqualTo):
            op1 = op_type(self.value_reference, self.literal)
            eq_(op1.first_expression, self.value_reference)
            eq_(op1.second_expression, self.literal)
            eq_(op1.match_case, True)
            eq_(op1.match_action, "any")
            op2 = op_type(self.value_reference, self.literal,
                          match_case=False, match_action="other")
            eq_(op2.match_case, False)
            eq_(op2.match_action, "other")

    def test_should_create_PropertyIsLike_operator(self):
        wild_card = "*"
        single_char = "?"
        escape_char = "\\"
        op1 = types.PropertyIsLike(self.value_reference, self.literal,
                                   wild_card, single_char, escape_char)
        eq_(op1.first_expression, self.value_reference)
        eq_(op1.second_expression, self.literal)
        eq_(op1.wild_card, wild_card)
        eq_(op1.single_char, single_char)
        eq_(op1.escape_char, escape_char)

    def test_should_create_Boundary_type(self):
        boundary = types.Boundary(self.literal)
        eq_(boundary.expression, self.literal)

    def test_should_create_PropertyIsBetween_operator(self):
        op1 = types.PropertyIsBetween(self.value_reference,
                                      types.Boundary(self.literal),
                                      types.Boundary(self.other_literal))
        eq_(op1.expression, self.value_reference)
        eq_(op1.lower_boundary.expression, self.literal)
        eq_(op1.upper_boundary.expression, self.other_literal)

    def test_should_create_PropertyIsNull_operator(self):
        op1 = types.PropertyIsNull(self.value_reference)
        eq_(op1.expression, self.value_reference)

    def test_should_create_PropertyIsNil_operator(self):
        nil_reason = "something"
        op1 = types.PropertyIsNil(self.value_reference)
        eq_(op1.expression, self.value_reference)
        eq_(op1.nil_reason, "equals")
        op2 = types.PropertyIsNil(self.value_reference, nil_reason)
        eq_(op2.nil_reason, nil_reason)

    def test_should_create_spatial_distance_operators(self):
        distance = 10
        for op_type in (types.Beyond, types.DWithin):
            op1 = op_type(distance, self.value_reference)
            eq_(op1.distance, distance)
            eq_(op1.first_argument, self.value_reference)
            eq_(op1.second_argument, None)
            op2 = op_type(distance, self.value_reference, self.literal)
            eq_(op2.second_argument, self.literal)

    def test_should_create_spatial_binary_operators(self):
        for op_type in (types.BBOX, types.Equals, types.Disjoint,
                        types.Intersects, types.Touches, types.Crosses,
                        types.Within, types.Contains, types.Overlaps):
            op1 = op_type(self.value_reference)
            eq_(op1.first_argument, self.value_reference)
            eq_(op1.second_argument, None)
            op2 = op_type(self.value_reference, self.literal)
            eq_(op2.second_argument, self.literal)

    def test_should_create_temporal_operators(self):
        raise NotImplementedError

    def test_should_create_logical_operators(self):
        raise NotImplementedError

    def test_should_create_ResourceId_operator(self):
        raise NotImplementedError

    def test_should_create_Filter(self):
        raise NotImplementedError
