"""
Base classes for the operator types defined in the FES standard.

The source code follows the class hierarchy presented in the
standard. Please refer to Section 7 - Filter for more details.
"""

from __future__ import absolute_import
import logging

from lxml import etree

from ..schemaparsers import schema_parser
from .. import utils

logger = logging.getLogger(__name__)


class Operator(object):
    _name = None

    @property
    def name(self):
        return self._name

    def to_xml(self, as_string=True):
        """Serialize to XML"""
        result = self._to_xml()
        if as_string:
            result = etree.tostring(result, pretty_print=True)
        return result

    def _from_xml(self, xml_element):
        """Reimplement this in child classes.

        :arg xml_element: the already validated XML
        :type xml_element: etree.Element
        """

        raise NotImplementedError

    @classmethod
    def from_xml(cls, xml_element, schema_path=None, validate_xml=True):
        """Return a new instance by parsing the input XML

        Child classes should not reimplement this method. They should
        reimplement `_from_xml` instead.

        The default implementation does nothing so this method must be
        reimplemented in child classes.
        """

        if validate_xml:
            if schema_path is not None:
                schema_parser.parse_schema(schema_path)
            try:
                schema_parser.validate_xml(xml_element)
            except etree.DocumentInvalid:
                raise
        return cls._from_xml(xml_element)

    @classmethod
    def from_ogc_common(cls, expression):
        """Return a new instance by parsing the input OGC_Common expression

        The default implementation does nothing so this method must be
        reimplemented in child classes.
        """
        raise NotImplementedError


class IdOperator(Operator):
    pass


class NonIdOperator(Operator):
    pass


class SpatialOperator(NonIdOperator):
    pass


class TemporalOperator(NonIdOperator):
    pass


class ComparisonOperator(NonIdOperator):
    pass


class LogicalOperator(NonIdOperator):
    pass


class ExtensionOperator(NonIdOperator):
    pass


class BinaryComparisonWithOneExpression(ComparisonOperator):
    """Base class for binary operators that accept one expression"""

    _expression = None

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, new_expression):
        utils.check_expression_type(new_expression)  # raises on error
        self._expression = new_expression

    def __init__(self, expression):
        super(BinaryComparisonWithOneExpression, self).__init__()
        self.expression = expression


class BinaryComparisonWithTwoExpressions(ComparisonOperator):
    """Base class for binary operators that accept two expressions"""

    _first_expression = None
    _second_expression = None

    @property
    def first_expression(self):
        return self._first_expression

    @first_expression.setter
    def first_expression(self, expression):
        utils.check_expression_type(expression)  # raises on error
        self._first_expression = expression

    @property
    def second_expression(self):
        return self._second_expression

    @second_expression.setter
    def second_expression(self, expression):
        utils.check_expression_type(expression)  # raises on error
        self._second_expression = expression

    def __init__(self, first_expression, second_expression):
        super(BinaryComparisonWithTwoExpressions, self).__init__()
        self.first_expression = first_expression
        self.second_expression = second_expression
