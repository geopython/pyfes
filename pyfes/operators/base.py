"""
Base classes for the operator types defined in the FES standard.
"""

from __future__ import absolute_import
import logging
from lxml import etree

from ..expression import Expression
from .. import errors
from .. import utils

logger = logging.getLogger(__name__)


class Operator(object):

    def serialize(self, as_string=True):
        """Serialize to XML"""
        result = self._serialize()
        if as_string:
            result = etree.tostring(result, pretty_print=True)
        return result

    @classmethod
    def deserialize(cls, xml_element):
        """Return a new instance by parsing the input XML

        The default implementation does nothing so this method must be
        reimplemented in child classes.
        """
        return None


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
