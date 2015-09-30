"""Operator factory for pyfes"""

from __future__ import absolute_import
import logging

from . import comparison

logger = logging.getLogger(__name__)


class OperatorParser(object):
    """A factory for generating Operator objects by deserializing from XML.
    """

    @classmethod
    def from_xml(cls, operator, schema_path=None):
        instance = None
        operator_classes = [
            comparison.BinaryComparisonOperator, comparison.LikeOperator,
            comparison.BetweenComparisonOperator, comparison.NullOperator,
            comparison.NillOperator
        ]
        current = 0
        while instance is None and current < len(operator_classes):
            try:
                instance = operator_classes[current].from_xml(
                    operator, schema_path=schema_path)
            except Exception as err:  # use a more specific exception
                logger.debug(err)
            current += 1
        return instance
