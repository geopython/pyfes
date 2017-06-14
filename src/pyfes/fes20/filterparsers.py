import logging

from lxml import etree

from . import expressions
from . import operators
from . namespaces import NAMESPACES
from .. import errors
from ..utils import XML_PARSER
from ..geometries import parse_gml

logger = logging.getLogger(__name__)


class BaseFilterParser(object):
    PARSER_TYPE = "FILTER_PARSER"


class FesFilterParser(BaseFilterParser):
    """Parses XML elements encoded following the rules described in OGC FES.

    Parameters
    ----------
    etree_parser: lxml.etree.XMLParser, optional
        A parser for XML data.

    """

    VERSION = "2.0.2"

    _OPERATOR_PARSER_HANDLERS = {
        operators.BinaryComparisonName: "parse_binary_comparison_operator",
        operators.BinaryLogicType: "parse_binary_logic_operator",
        operators.DistanceOperatorName: "parse_distance_operator",
        operators.SpatialOperatorName: "parse_binary_spatial_operator",
        operators.UnaryLogicType: "parse_unary_logic_operator",
        operators.TemporalOperatorName: "parse_temporal_operator",
    }

    def __init__(self, etree_parser=None):
        self.etree_parser = etree_parser or XML_PARSER

    def parse_filter(self, data):
        """Parse the input filter.

        Parameters
        ----------
        data: str
            The fes:Filter string to parse

        """
        data_element = etree.fromstring(data, parser=self.etree_parser)
        qualified_name = etree.QName(data_element)
        if not qualified_name == etree.QName(NAMESPACES["fes"], "Filter"):
            raise RuntimeError("Invalid filter element")
        filter_predicate = data_element[0]
        return self._parse_predicate(filter_predicate)

    def _parse_predicate(self, filter_predicate):
        """Parse the input data string.

        Parameters
        ----------
        filter_predicate: etree.Element

        """

        predicate_qname = etree.QName(filter_predicate)
        if predicate_qname.namespace != NAMESPACES["fes"]:
            raise RuntimeError("Invalid operator element")
        predicate_name = predicate_qname.localname
        operator_type = self._get_operator_type(predicate_name)
        handler = getattr(self, self._OPERATOR_PARSER_HANDLERS[operator_type])
        return handler(filter_predicate)

    def parse_binary_comparison_operator(self, operator_element):
        return operators.BinaryComparisonOperator(
            operator_type=operators.BinaryComparisonName(
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
        return operators.BinarySpatialOperator(
            operator_type=operators.SpatialOperatorName(
                etree.QName(operator_element).localname),
            first_operand=self.parse_expression(operator_element[0]),
            second_operand=self.parse_spatial_description(operator_element[1])
        )

    def parse_binary_logic_operator(self, operator_element):
        raise NotImplementedError

    def parse_expression(self, expression_element):
        qname = etree.QName(expression_element)
        if qname.namespace != NAMESPACES["fes"]:
            raise errors.ValidationError("Invalid expression namespace")
        parser = {
            "ValueReference": self.parse_value_reference_expression,
            "Literal": self.parse_literal_expression,
            "Function": self.parse_function_expression,
        }[qname.localname]
        return parser(expression_element)

    def parse_spatial_description(self, element):
        """Parse a spatial description element.

        According to the FES standard, a spatial description can be one of:

        * A fes:Expression type;
        * A geometry type described using GML (any version).

        """
        try:
            result = self.parse_expression(element)
        except (KeyError, errors.ValidationError):
            result = parse_gml(element)
        return result

    def parse_value_reference_expression(self, value_reference_element):
        return expressions.ValueReference(value=value_reference_element.text)

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

    def parse_unary_logic_operator(self, operator_element):
        return operators.UnaryLogicOperator(
            operator_type=operators.UnaryLogicType(
                etree.QName(operator_element).localname),
            operand=self._parse_predicate(operator_element[0])
        )

    def _get_operator_type(self, name):
        for type_ in self._OPERATOR_PARSER_HANDLERS.keys():
            if name in (item.value for item in type_):
                result = type_
                break
        else:
            raise RuntimeError(
                "Unrecognized operator: {!r}".format(name))
        return result


class OgcCqlParser(BaseFilterParser):
    """Parses OGC CQL expressions."""
    VERSION = "0.0.1"
