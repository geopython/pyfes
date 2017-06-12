"""Unit tests for pyfes.fes20.filterparsers."""

from lxml import etree
import pytest

from pyfes.fes20.operators import BinaryComparisonOperator
from pyfes.fes20.operators import BinaryComparisonName
from pyfes.fes20 import expressions
from pyfes.fes20 import filterparsers
from pyfes.fes20.namespaces import NAMESPACES

pytestmark = pytest.mark.unit


def test_fes_filter_parser_parse_value_reference_expression():
    value = "something"
    element = etree.Element(
        "{{{fes}}}ValueReference".format(**NAMESPACES), 
        nsmap=NAMESPACES.copy()
    )
    element.text = value
    parser = filterparsers.FesFilterParser()
    result = parser.parse_value_reference_expression(element)
    assert result.value == value


@pytest.mark.parametrize("value, type_, expected_value", [
    ("some string", None, "some string"),
    (10, None, "10"),
    (10, "xs:int", 10),
    (0.2, None, "0.2"),
    (0.2, "xs:float", 0.2),
])
def test_fes_filter_parser_parse_literal_expression(value, type_,
                                                    expected_value):
    element = etree.Element(
        "{{{fes}}}Literal".format(**NAMESPACES),
        nsmap=NAMESPACES.copy()
    )
    element.text = str(value)
    if type_ is not None:
        element.attrib["type"] = type_
    parser = filterparsers.FesFilterParser()
    result = parser.parse_literal_expression(element)
    assert result.value == expected_value
