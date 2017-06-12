"""Integration tests for pyfes.parsers."""

import pytest

from pyfes import parsers
from pyfes.fes20 import operators
from pyfes.fes20 import expressions

pytestmark = pytest.mark.integration


def test_fes20_examples_212_filter01():
    filter_ = """
        <?xml version="1.0"?>
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
    """.strip()
    expected = operators.BinaryComparisonOperator(
        operators.BinaryComparisonName.PROPERTY_IS_EQUAL_TO,
        first_expression=expressions.ValueReference("SomeProperty"),
        second_expression=expressions.Literal("100")
    )
    result = parsers.parse_filter(filter_)
    assert result == expected


def test_fes20_examples_212_filter02():
    filter_ = """
        <?xml version="1.0"?>
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
    """.strip()
    expected = operators.BinaryComparisonOperator(
        operators.BinaryComparisonName.PROPERTY_IS_LESS_THAN,
        first_expression=expressions.ValueReference("DEPTH"),
        second_expression=expressions.Literal("30")
    )
    result = parsers.parse_filter(filter_)
    assert result == expected


@pytest.mark.skip(reason=NotImplemented)
def test_fes20_examples_212_filter03():
    filter_ = """
        <?xml version="1.0"?>
        <fes:Filter
             xmlns:fes="http://www.opengis.net/fes/2.0"
             xmlns:gml="http://www.opengis.net/gml"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://www.opengis.net/fes/2.0 
                 http://schemas.opengis.net/filter/2.0/filterAll.xsd
                 http://www.opengis.net/gml 
                 http://schemas.opengis.net/gml/2.1.2/geometry.xsd"
        >
            <fes:Not>
                <fes:Disjoint>
                    <fes:ValueReference>Geometry</fes:ValueReference>
                    <gml:Box srsName="urn:fes:def:crs:EPSG::4326">
                        <gml:coordinates>
                            13.0983,31.5899 35.5472 42.8143
                        </gml:coordinates>
                    </gml:Box>
                </fes:Disjoint>
            </fes:Not>
        </fes:Filter>
    """
    pass
