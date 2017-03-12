import logging

from lxml import etree

from . import expressions
from . import operators
from .operators import BinaryComparisonName
from .operators import DistanceOperatorName
from .operators import SpatialOperatorName
from . namespaces import NAMESPACES
from ..utils import XML_PARSER

logger = logging.getLogger(__name__)


class BaseFilterParser(object):
    PARSER_TYPE = "FILTER_PARSER"


class FesFilterParser(BaseFilterParser):
    """Parses XML elements encoded following the rules described in OGC FES."""
    VERSION = "2.0.2"

    def __init__(self, etree_parser=None):
        self.etree_parser = etree_parser or XML_PARSER

    def parse(self, data):
        """Parse the input data string.

        Parameters
        ----------
        data: str
            The fes:Filter string to parse

        """

        data_element = etree.fromstring(data, parser=self.etree_parser)
        qualified_name = etree.QName(data_element)
        if not qualified_name == etree.QName(NAMESPACES["fes"], "Filter"):
            raise RuntimeError("Invalid filter element")  # TODO: Replace with a proper exception
        operator_element = data_element[0]
        operator_qname = etree.QName(operator_element)
        if operator_qname.namespace != NAMESPACES["fes"]:
            raise RuntimeError("Invalid operator element")
        operator_name = operator_qname.localname
        # TODO: Add remaining operators
        if operator_name in (m.value for m in BinaryComparisonName):
            result = self.parse_binary_comparison_operator(operator_element)
        elif operator_name in (m.value for m in DistanceOperatorName):
            result = self.parse_distance_operator(operator_element)
        elif operator_name in (m.value for m in SpatialOperatorName):
            result = self.parse_binary_spatial_operator(operator_element)
        else:
            raise RuntimeError("Unrecognized operator")
        return result

    def parse_binary_comparison_operator(self, operator_element):
        return operators.BinaryComparisonOperator(
            operator_type=BinaryComparisonName(
                etree.QName(operator_element).localname),
            first_expression=self.parse_expression(operator_element[0]),
            second_expression=self.parse_expression(operator_element[1]),
            match_case=operator_element.get("matchCase", True),
            match_action=operators.MatchAction(
                operator_element.get("matchAction", operators.MatchAction.ANY)
            )
        )

    def parse_distance_operator(self, operator_element):
        raise NotImplementedError

    def parse_binary_spatial_operator(self, operator_element):
        raise NotImplementedError

    def parse_expression(self, expression_element):
        qname = etree.QName(expression_element)
        if qname.namespace != NAMESPACES["fes"]:
            raise RuntimeError("Invalid expression namespace")
        parser = {
            "ValueReference": self.parse_value_reference_expression,
            "Literal": self.parse_literal_expression,
            "Function": self.parse_function_expression,
        }[qname.localname]
        return parser(expression_element)

    def parse_value_reference_expression(self, value_reference_element):
        return expressions.ValueReference(
            value=value_reference_element.text
        )

    # TODO - Add type casts for primitive types, datetimes and GML geometries
    def parse_literal_expression(self, literal_element):
        declared_type = literal_element.get("type")
        if declared_type == "xs:int":
            value = int(literal_element.text)
        elif declared_type == "xs:float":
            value = float(literal_element.text)
        else:
            value = literal_element.text
        return expressions.Literal(
            value=value
        )

    def parse_function_expression(self, function_element):
        return expressions.Function(
            name=function_element.text
        )


class OgcCqlParser(BaseFilterParser):
    """Parses OGC CQL expressions."""
    VERSION = "0.0.1"
