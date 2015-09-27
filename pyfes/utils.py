"""
Assorted utility functions for pyfes.
"""

from __future__ import absolute_import
import os
import logging

from . import errors
from .expression import Expression

logger = logging.getLogger(__name__)


def check_expression_type(expression, custom_type=Expression):
    if not isinstance(expression, custom_type):
        raise errors.InvalidExpressionError()
    return expression
