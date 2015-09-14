"""
Assorted utility functions for pyfes.
"""

from . import errors
from .expression import Expression


def check_expression_type(expression, custom_type=Expression):
    if not isinstance(expression, custom_type):
        raise errors.InvalidExpressionError()
    return expression
