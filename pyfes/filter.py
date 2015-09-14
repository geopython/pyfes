"""
Filter class, as defined in OGC FES/ISO 19143 standard.
"""

from __future__ import absolute_import
import logging

from .operators.base import Operator
from .errors import InvalidOperatorError


logger = logging.getLogger(__name__)


class Filter(object):
    _filter_ = None

    @property
    def filter_(self):
        return self._filter_

    def __init__(self, filter_):
        if isinstance(filter_, Operator):
            self._filter_ = filter_
        else:
            raise InvalidOperatorError()
