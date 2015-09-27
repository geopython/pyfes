"""
Filter class, as defined in OGC FES/ISO 19143 standard.
"""

from __future__ import absolute_import
import logging

from lxml import etree

from .operators.base import Operator
from .operators.operatorparsers import OperatorParser
from .errors import InvalidOperatorError
from .base import PyfesBase
from .namespaces import namespaces


logger = logging.getLogger(__name__)


class Filter(PyfesBase):
    _filter_ = None

    @property
    def filter_(self):
        return self._filter_

    def __init__(self, filter_):
        if isinstance(filter_, Operator):
            self._filter_ = filter_
        else:
            raise InvalidOperatorError()

    def __repr__(self):
        return ("{0}.{1.__class__.__name__}({1.filter_})".format(
                __name__, self))

    def _to_xml(self):
        element = etree.Element(
            "{{{0[fes]}}}Filter".format(namespaces), nsmap=namespaces)
        element.append(self.filter_._to_xml())
        return element

    @classmethod
    def _from_xml(cls, xml_element):
        return cls(OperatorParser.from_xml(xml_element[0]))
