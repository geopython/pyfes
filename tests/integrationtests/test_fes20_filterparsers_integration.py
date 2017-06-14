"""Integration tests for pyfes.fes20.filterparsers."""

import pytest

from pyfes.fes20.operators import BinaryComparisonOperator
from pyfes.fes20.operators import BinaryComparisonName
from pyfes.fes20 import expressions
from pyfes.fes20 import filterparsers

pytestmark = pytest.mark.integration


@pytest.mark.parametrize("filter_, expected", [
    (
            '''
                <fes:Filter
                  xmlns:fes="http://www.opengis.net/fes/2.0"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="http://www.opengis.net/fes/2.0
                    http://schemas.opengis.net/filter/2.0/filterAll.xsd"
                >
                    <fes:PropertyIsEqualTo>
                        <fes:ValueReference>SomeProperty</fes:ValueReference>
                        <fes:Literal>100</fes:Literal>
                    </fes:PropertyIsEqualTo>
                </fes:Filter>
            ''',
            BinaryComparisonOperator(
                operator_type=BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
                first_expression=expressions.ValueReference("SomeProperty"),
                second_expression=expressions.Literal("100")
            )
    ),
    (
            '''
                <fes:Filter
                  xmlns:fes="http://www.opengis.net/fes/2.0"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="http://www.opengis.net/fes/2.0
                    http://schemas.opengis.net/filter/2.0/filterAll.xsd"
                >
                    <fes:PropertyIsLessThan>
                        <fes:ValueReference>DEPTH</fes:ValueReference>
                        <fes:Literal>30</fes:Literal>
                  </fes:PropertyIsLessThan>
                </fes:Filter>
            ''',
            BinaryComparisonOperator(
                operator_type=BinaryComparisonName.PROPERTY_IS_LESS_THAN,
                first_expression=expressions.ValueReference("DEPTH"),
                second_expression=expressions.Literal("30")
            )
    ),
])
def test_fes_filter_parser_parse(filter_, expected):
    parser = filterparsers.FesFilterParser()
    result = parser.parse_filter(data=filter_)
    assert result == expected
