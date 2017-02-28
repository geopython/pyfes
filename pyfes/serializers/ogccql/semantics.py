"""Semantic actions for the CQL parser."""

import logging

from .cqlparser import CqlParser
from .cqlparser import CqlSemantics
from ... import filterpredicates

logger = logging.getLogger(__name__)


def from_text(text):
    parser = CqlParser()
    ast = parser.parse(text, rule_name="search_condition",
                       semantics=OgcCqlSemantics())
    return ast


class OgcCqlSemantics(CqlSemantics):
    """Testing out grako's parser for our ebnf."""

    def character_string_literal(self, ast):
        return "".join(ast[1])

    def unsigned_integer(self, ast):
        return int("".join(ast))

    def identifier(self, ast):
        return ast[0] + "".join(ast[1])

    def predicate(self, ast):
        logger.debug("inside predicate rule")
        logger.debug("ast: {}".format(ast))
        return ast

    def comparison_predicate(self, ast):
        """Parse CQL into a fes:BinaryComparisonOperator."""
        logger.debug("inside comparison_predicate rule")
        logger.debug("ast: {}".format(ast))
        first_operand, binary_comparison_operator, second_operand = ast
        operator_map = {
            "=": filterpredicates.PropertyIsEqualTo,
            ">=": filterpredicates.PropertyIsGreaterThanOrEqualTo,
            "<=": filterpredicates.PropertyIsLessThanOrEqualTo,
            ">": filterpredicates.PropertyIsGreaterThan,
            "<": filterpredicates.PropertyIsLessThan,
            "<>": filterpredicates.PropertyIsNotEqualTo,
        }
        return operator_map.get(binary_comparison_operator)(
            first_operand, second_operand)

    def search_condition(self, ast):
        logger.debug("inside search_condition rule")
        logger.debug("ast: {}".format(ast))
        if len(ast) > 1:
            operator = filterpredicates.Or(ast[0], ast[1], extra_predicates=ast[2:])
        else:
            operator = ast[0]
        return operator

    def boolean_term(self, ast):
        logger.debug("inside boolean_term rule")
        logger.debug("ast: {}".format(ast))
        if len(ast) > 1:
            operator = filterpredicates.And(ast[0], ast[1], extra_predicates=ast[2:])
        else:
            operator = ast[0]
        return operator

    def boolean_factor(self, ast):
        logger.debug("inside boolean_factor rule")
        logger.debug("ast: {}".format(ast))
        if isinstance(ast, list):
            operator = filterpredicates.Not(ast[1])
        else:
            operator = ast
        return operator

    def boolean_primary(self, ast):
        logger.debug("inside boolean_primary rule")
        logger.debug("ast: {}".format(ast))
        return ast
