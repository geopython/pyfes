"""Tests for the custom pyfes types"""

import pytest

from pyfes.fes20 import expressions
from pyfes.fes20 import operators

from pyfes import errors

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("operand", [
    expressions.ValueReference("first"),
    expressions.Literal("second"),
    expressions.Function("third"),
])
def test_validate_operand(operand):
    operators.validate_operand(operand)


@pytest.mark.parametrize("operand, allowed", [
    (
            expressions.ValueReference("first"),
            (expressions.Literal, expressions.Function)
    ),
    (
            expressions.Literal("second"),
            (expressions.ValueReference, expressions.Function)
    ),
    (
            expressions.Function("third"),
            (expressions.ValueReference, expressions.Literal)
    ),
])
def test_validate_operand_invalid(operand, allowed):
    with pytest.raises(errors.InvalidExpressionError):
        operators.validate_operand(operand=operand, allowed_types=allowed)


@pytest.mark.parametrize("first, second", [
    (
        operators.BinaryComparisonOperator(
            operator_type=operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
            first_expression=expressions.ValueReference("this"),
            second_expression=expressions.Literal("that"),
            match_action=operators.MatchAction.ANY,
            match_case=True
        ),
        operators.BinaryComparisonOperator(
            operator_type=operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
            first_expression=expressions.ValueReference("this"),
            second_expression=expressions.Literal("that"),
            match_action=operators.MatchAction.ANY,
            match_case=True
        )
    ),
])
def test_operator_equality(first, second):
    assert first == second


@pytest.mark.parametrize("operator_type", [
    "PropertyIsEqualTo",
    "PropertyIsNotEqualTo",
    "PropertyIsGreaterThan",
    "PropertyIsGreaterThanOrEqualTo",
    "PropertyIsLessThan",
    "PropertyIsLessThanOrEqualTo",
])
def test_binary_comparison_operator_type(operator_type):
    first_expression = expressions.ValueReference("fake")
    second_expression = expressions.ValueReference("phony")
    operator = operators.BinaryComparisonOperator(
        operator_type=operator_type,
        first_expression=first_expression,
        second_expression=second_expression,
    )
    assert operator.operator_type == operators.BinaryComparisonName(
        operator_type)


@pytest.mark.parametrize("type_, first, second, match_action, expected", [
    (
        "fake_type",
        expressions.ValueReference("first"),
        expressions.ValueReference("second"),
        operators.MatchAction.ANY,
        errors.InvalidOperatorError
    ),
    (
            operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
            "first",
            expressions.ValueReference("second"),
            operators.MatchAction.ANY,
            errors.InvalidExpressionError
    ),
    (
            operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
            expressions.ValueReference("first"),
            "second",
            operators.MatchAction.ANY,
            errors.InvalidExpressionError
    ),
    (
            operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
            expressions.ValueReference("first"),
            expressions.ValueReference("second"),
            "fake action",
            ValueError
    ),
])
def test_binary_comparison_operator_invalid(type_, first, second, match_action,
                                            expected):
    with pytest.raises(expected):
        operators.BinaryComparisonOperator(
            operator_type=type_,
            first_expression=first,
            second_expression=second,
            match_action=match_action
        )
