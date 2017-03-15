"""unit tests for pyfes.fes20.expressions"""

import mock
import pytest

from pyfes import errors
from pyfes.fes20.expressions import Function
from pyfes.fes20.expressions import Literal
from pyfes.fes20.expressions import ValueReference

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("first, second, expected", [
    (Literal("this"), Literal("this"), True),
    (Literal("this"), "this", False),
    (Literal("this"), {"value": "this"}, False),
    (ValueReference("this"), ValueReference("this"), True),
    (ValueReference("this"), "this", False),
    (ValueReference("this"), {"value": "this"}, False),
    (Function("do_stuff"), Function("do_stuff"), True),
    (
        Function("do_stuff", [Literal("this")]),
        Function("do_stuff", [Literal("this")]),
        True
    ),
    (Function("do_stuff"), "do_stuff", False),
    (Function("do_stuff"), {"name":"do_stuff"}, False),
])
def test_expression_equality(first, second, expected):
    result = first == second
    assert result == expected


@pytest.mark.parametrize("expression_cls", [
    Literal,
    ValueReference,
    Function,
])
def test_expression_validators(expression_cls):
    first_validator = mock.MagicMock(return_value=True)
    second_validator = mock.MagicMock(return_value=True)
    value = "fake"
    expression_cls(value, validators=[first_validator, second_validator])
    first_validator.assert_called_with(value)
    second_validator.assert_called_with(value)


@pytest.mark.parametrize("argument", [
    Literal("phony"),
    ValueReference("phony"),
    Function("phony"),
])
def test_function_add_argument(argument):
    function_ = Function("some_name")
    function_.add_argument(argument)
    assert function_.arguments[0] == argument


@pytest.mark.parametrize("argument", [
    "this",
    1,
    None,
    ["things"],
    {"this": "that"},
])
def test_function_add_argument_invalid(argument):
    with pytest.raises(errors.InvalidExpressionError):
        function_ = Function("some_name")
        function_.add_argument(argument)


@pytest.mark.parametrize("arguments", [
    [Literal("this")],
    [Literal("this"), ValueReference("that")],
])
def test_function_create_with_arguments(arguments):
    function_ = Function("some_name", arguments=arguments)
    assert len(function_.arguments) == len(arguments)


def test_function_remove_argument():
    function_ = Function("some_name", arguments=[Literal("stuff")])
    function_.remove_argument(function_.arguments[0])
    assert len(function_.arguments) == 0
