"""unit tests for pyfes.fes20.expressions"""

import pytest

from pyfes.fes20.expressions import Function
from pyfes.fes20.expressions import Literal
from pyfes.fes20.expressions import ValueReference

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("first, second", [
    (Literal("this"), Literal("this")),
    (ValueReference("this"), ValueReference("this")),
    (Function("do_stuff"), Function("do_stuff")),
    (Function("do_stuff", ["this"]), Function("do_stuff", ["this"])),
])
def test_expression_equality(first, second):
    assert first == second
